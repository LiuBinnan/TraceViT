"""Per-task synthesis: calibrate the variation space, then oversample ->
validate -> dedup -> collect up to a target count.

Robustness: some generators spin in pathologically long loops for certain
kwargs. A per-attempt wall-clock timeout (SIGALRM) abandons such an attempt and
a per-task wall-clock budget caps total time; offending attempts are counted as
'timeout' discards and hang-inducing params are pruned during calibration.
Normal tasks finish far inside both bounds, so their output stays deterministic;
only tasks that actually hit a bound become time-dependent (flagged in stats)."""

import contextlib
import random
import signal
import time

import task_list
from steps import batch, dimensions, sampler, storage, validate, variations

CALIB_N = 6
CALIB_KEEP = 0.5
ATTEMPT_FACTOR = 20
ATTEMPT_TIMEOUT = 5.0    # seconds, per single generate/trace attempt
TASK_BUDGET = 90.0       # seconds, wall-clock budget for one task's main loop
COLORS_POOLS = ("none", "auto", "always")
FIT_PROBES = 12          # swept values per band-fitted param
FIT_M = 2                # probes per swept value
_PROBE_PALETTES = [
    [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],   # full reversal
    [0, 2, 3, 4, 5, 6, 7, 8, 9, 1],   # rotation
    [0, 5, 1, 6, 2, 7, 3, 8, 4, 9],   # interleave
]


class _Timeout(Exception):
    pass


def _raise_timeout(signum, frame):
    raise _Timeout()


@contextlib.contextmanager
def _time_limit(seconds):
    """Abort the wrapped block after `seconds` of wall clock via SIGALRM.

    Usable only from a process's main thread (true for the serial path and for
    each multiprocessing worker). ARC-GEN generators are pure Python, so the
    alarm lands on a bytecode boundary and unwinds cleanly. `seconds` falsy or
    <= 0 disables the limit."""
    if not seconds or seconds <= 0:
        yield
        return
    previous = signal.signal(signal.SIGALRM, _raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def _generate_only(generate_fn, seed, kwargs):
    random.seed(seed)
    return generate_fn(**kwargs)


def _sweep_values(lo, hi, probes):
    """Sorted unique integers across [lo, hi], always including both endpoints.
    Dense (every integer) when the range is no wider than `probes`."""
    if hi <= lo:
        return [lo]
    if hi - lo + 1 <= probes:
        return list(range(lo, hi + 1))
    step = (hi - lo) / (probes - 1)
    vals = sorted({int(round(lo + i * step)) for i in range(probes)})
    vals[0], vals[-1] = lo, hi
    return vals


def _struct_rate(name, lo, hi, generate_fn, seed_base, rng, n, attempt_timeout):
    """Legacy-style structural success rate over n random values in [lo, hi]."""
    ok = 0
    for j in range(n):
        kwargs = {name: rng.randint(lo, hi)}
        try:
            with _time_limit(attempt_timeout):
                example = _generate_only(generate_fn, seed_base + j, kwargs)
        except Exception:
            continue
        record = {"input": example["input"], "output": example["output"],
                  "steps": []}
        if validate.validate_sample(record, "skip") is None:
            ok += 1
    return ok / n


def _usable_span(name, lo, hi, generate_fn, seed_base, attempt_timeout,
                 probes=FIT_PROBES, m=FIT_M):
    """(min, max) swept value in [lo, hi] that is usable (>=1 of m probes a
    legal grid <=30x30), or (None, None) if nothing is usable."""
    usable = []
    seed = seed_base
    for value in _sweep_values(lo, hi, probes):
        ok = False
        for _ in range(m):
            try:
                with _time_limit(attempt_timeout):
                    example = _generate_only(generate_fn, seed, {name: value})
            except Exception:
                seed += 1
                continue
            seed += 1
            record = {"input": example["input"],
                      "output": example["output"], "steps": []}
            if validate.validate_sample(record, "skip") is None:
                ok = True
        if ok:
            usable.append(value)
    if not usable:
        return (None, None)
    return (min(usable), max(usable))


def _fit_param(name, samp, generate_fn, seed_base, rng, n, keep,
               attempt_timeout):
    """Fit an IntSampler size param to the widest safe band, floored at the
    legacy default band so fit never yields less diversity than legacy:

    - if legacy keep/drop would KEEP the param at its default band, keep
      [def_lo, max(def_hi, widest_usable)] -- extend up, never shrink;
    - else if a usable RANGE (more than one value) exists, recover the param as
      [min_usable, max_usable] (legacy would have dropped it entirely);
    - else prune -- including when only a single value is usable: forcing one
      value adds no diversity and could override a better generator default
      (e.g. a param with a valid non-None default), regressing below legacy.

    Heuristic (name-class) params widen up to FIT_BANDS; an override-supplied
    range is respected as-is (no widening past the override)."""
    def_lo, def_hi = samp.lo, samp.hi
    cls = dimensions._class_of(name)
    if cls is not None and (def_lo, def_hi) == dimensions.DEFAULT_BANDS.get(cls):
        fit_cap = dimensions.FIT_BANDS[cls][1]
    else:
        fit_cap = def_hi
    legacy_kept = _struct_rate(name, def_lo, def_hi, generate_fn, seed_base,
                               rng, n, attempt_timeout) >= keep
    lo_u, hi_u = _usable_span(name, def_lo, fit_cap, generate_fn, seed_base,
                              attempt_timeout)
    if legacy_kept:
        hi = def_hi if hi_u is None else max(def_hi, hi_u)
        return dimensions.IntSampler(def_lo, hi)
    if lo_u is not None and hi_u > lo_u:
        return dimensions.IntSampler(lo_u, hi_u)
    return None


def calibrate(task_id, generate_fn, space, seed_base, n=CALIB_N,
              keep=CALIB_KEEP, attempt_timeout=ATTEMPT_TIMEOUT,
              size_mode="legacy"):
    """Probe each inferred param; keep the usable ones, prune the rest.

    size_mode="legacy" (default): drop-or-keep — keep a param whose structural
    success rate over `n` probes is >= `keep`, else prune. Byte-identical to the
    historical behavior.

    size_mode="fit": band-fit IntSampler params — keep each with a shrunk
    [min_usable, max_usable] range (prune only if nothing is usable). Choice/bool
    samplers still use the legacy keep/drop path."""
    rng = random.Random(sampler.task_seed(seed_base, task_id, "calib"))
    kept, pruned = {}, []
    for name, samp in space.items():
        if size_mode == "fit" and isinstance(samp, dimensions.IntSampler):
            fitted = _fit_param(name, samp, generate_fn, seed_base, rng, n, keep,
                                attempt_timeout)
            if fitted is None:
                pruned.append(name)
            else:
                kept[name] = fitted
            continue
        ok = 0
        for j in range(n):
            kwargs = {name: samp.sample(rng)}
            try:
                with _time_limit(attempt_timeout):
                    example = _generate_only(generate_fn, seed_base + j, kwargs)
            except Exception:
                continue
            record = {"input": example["input"], "output": example["output"],
                      "steps": []}
            if validate.validate_sample(record, "skip") is None:
                ok += 1
        if ok / n >= keep:
            kept[name] = samp
        else:
            pruned.append(name)
    return kept, pruned


def _dedup_key(record):
    return (tuple(map(tuple, record["input"])),
            tuple(map(tuple, record["output"])))


def _recolor_safe(generate_fn, palette, seed=2025,
                  attempt_timeout=ATTEMPT_TIMEOUT):
    """True iff regenerating under `palette` yields exactly the palette-mapped
    identity grids.

    Catches generators that compare colors against literal ints: recoloring
    would silently change their behavior (a different transformation), not
    just their palette."""
    try:
        with _time_limit(attempt_timeout):
            base = _generate_only(generate_fn, seed, {})
        previous = variations.push_colors(palette)
        try:
            with _time_limit(attempt_timeout):
                colored = _generate_only(generate_fn, seed, {})
        finally:
            variations.pop_colors(previous)

        def mapped(grid):
            return [[palette[value] if 0 <= value <= 9 else value
                     for value in row] for row in grid]

        return (colored["input"] == mapped(base["input"]) and
                colored["output"] == mapped(base["output"]))
    except Exception:
        return False


def _recolor_safe_multi(generate_fn, seed_base=2025,
                        attempt_timeout=ATTEMPT_TIMEOUT):
    """Stronger recolor-safety gate: require consistency across several
    palettes and seeds before we recolor an entire task. Catches generators
    that are color-consistent under one palette but branch on a literal under
    another."""
    for offset, palette in enumerate(_PROBE_PALETTES):
        if not _recolor_safe(generate_fn, palette, seed=seed_base + offset,
                             attempt_timeout=attempt_timeout):
            return False
    return True


def synthesize_task(task_id, target, seed_base=2025,
                    directory=storage.DEFAULT_DIR, attempt_factor=ATTEMPT_FACTOR,
                    attempt_timeout=ATTEMPT_TIMEOUT, task_budget=TASK_BUDGET,
                    colors_pool="none", size_mode="legacy"):
    """Synthesize up to `target` distinct valid records for one task.

    colors_pool: "none" identity only; "auto" identity then top up the shortfall
    with random palettes; "always" recolor every record from the start (recolor-
    unsafe / colors:"off" tasks stay identity, flagged). size_mode: "legacy"
    drop-or-keep calibration; "fit" band-fits size params over widened bands."""
    if colors_pool not in COLORS_POOLS:
        raise ValueError("unknown colors_pool: %r" % colors_pool)
    generate_fn = task_list.task_list()[task_id][0]
    annotation = storage.load_annotation(task_id, directory=directory)
    category = annotation["category"] if annotation else "selectable"

    space = dimensions.variation_space(task_id, generate_fn)
    kept, pruned = calibrate(task_id, generate_fn, space, seed_base,
                             attempt_timeout=attempt_timeout, size_mode=size_mode)
    stream = sampler.candidates(kept, seed_base, task_id)

    seen, records, discards = set(), [], {}

    def attempt(kwargs, gen_seed, palette=None):
        try:
            with _time_limit(attempt_timeout):
                if category == "skip":
                    previous = variations.push_colors(palette)
                    try:
                        example = _generate_only(generate_fn, gen_seed, kwargs)
                    finally:
                        variations.pop_colors(previous)
                    candidate = {"input": example["input"],
                                 "output": example["output"], "steps": []}
                else:
                    candidate = batch.example_with_steps(
                        task_id, gen_seed, annotation,
                        generator_kwargs=kwargs, colors=palette)
        except _Timeout:
            discards["timeout"] = discards.get("timeout", 0) + 1
            return
        except Exception:
            discards["crash"] = discards.get("crash", 0) + 1
            return
        reason = validate.validate_sample(candidate, category)
        if reason is not None:
            discards[reason] = discards.get(reason, 0) + 1
            return
        key = _dedup_key(candidate)
        if key in seen:
            discards["dup"] = discards.get("dup", 0) + 1
            return
        seen.add(key)
        records.append({
            "task_id": task_id,
            "category": category,
            "input": candidate["input"],
            "output": candidate["output"],
            "steps": candidate["steps"],
            "variation": {"seed": gen_seed, "kwargs": kwargs,
                          "colors": palette},
        })

    def fill(palettes=None):
        attempts = 0
        max_attempts = max((target - len(records)) * attempt_factor,
                           attempt_factor)
        start = time.time()
        while (len(records) < target and attempts < max_attempts and
               (not task_budget or time.time() - start < task_budget)):
            attempts += 1
            kwargs, gen_seed = next(stream)
            attempt(kwargs, gen_seed,
                    palette=next(palettes) if palettes else None)

    start = time.time()
    colors_flag = None
    override = dimensions.load_override(task_id) or {}

    if colors_pool == "always":
        if override.get("colors") == "off":
            colors_flag = "colors_off"
            fill()
        elif _recolor_safe_multi(generate_fn, seed_base,
                                 attempt_timeout=attempt_timeout):
            fill(sampler.palette_stream(seed_base, task_id))
        else:
            colors_flag = "recolor_unsafe"
            fill()
    else:
        fill()
        if colors_pool == "auto" and len(records) < target:
            if override.get("colors") == "off":
                colors_flag = "colors_off"
            elif _recolor_safe_multi(generate_fn, seed_base,
                                     attempt_timeout=attempt_timeout):
                fill(sampler.palette_stream(seed_base, task_id))
            else:
                colors_flag = "recolor_unsafe"

    stats = {
        "task_id": task_id, "category": category, "target": target,
        "produced": len(records), "distinct": len(records),
        "discards": discards, "hit_ceiling": len(records) < target,
        "calibrated_params": sorted(kept), "pruned_params": pruned,
        "colored": sum(1 for r in records
                       if r["variation"]["colors"] is not None),
        "elapsed_sec": round(time.time() - start, 2),
    }
    if size_mode == "fit":
        stats["fitted_bands"] = {
            name: [samp.lo, samp.hi] for name, samp in kept.items()
            if isinstance(samp, dimensions.IntSampler)}
    if colors_flag:
        stats[colors_flag] = True
    return records, stats
