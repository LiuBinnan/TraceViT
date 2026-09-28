"""rearc_steps.py - extract intermediate solving steps from RE-ARC verifiers.

Post-processes an existing RE-ARC dataset (tasks/<id>.json + metadata.json) into a
dataset dir in the ARC-GEN layout (by_task/<id>.jsonl + manifest.json + shards/) where each
record carries `steps`: the grid-typed intermediate states of the task's verifier
(a straight-line DSL program) traced statement by statement on the example's input.
Samples are copied verbatim; a record whose traced return value does not equal the
stored output degrades to steps=[] and is counted, never silently kept.

Usage: python3 rearc_steps.py --data <re_arc_dir> --out <dir> [--tasks a,b]
           [--procs N] [--shard-size 10000] [--max-steps N]
"""
import argparse
import ast
import hashlib
import json
import multiprocessing
import os
import random
import sys
import time

SHUFFLE_SEED = 2025  # same shard shuffle seed as the ARC-GEN pipeline


def is_grid(g):
    """re-arc utils.is_grid semantics: tuple grid, 1-30 rows/cols, ints 0-9."""
    if not isinstance(g, tuple) or not 0 < len(g) <= 30:
        return False
    if not all(isinstance(r, tuple) and 0 < len(r) <= 30 for r in g):
        return False
    if len({len(r) for r in g}) != 1:
        return False
    return all(isinstance(x, int) and 0 <= x <= 9 for r in g for x in r)


def parse_verifiers(path):
    """Map task_id -> FunctionDef for every verify_* in `path`.

    Rejects anything that is not a straight-line program (single-Name
    assignments and one return), so upstream structure changes fail loudly."""
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    out = {}
    for node in tree.body:
        if not (isinstance(node, ast.FunctionDef)
                and node.name.startswith("verify_")):
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                if len(stmt.targets) != 1 or not isinstance(stmt.targets[0],
                                                            ast.Name):
                    raise ValueError(
                        f"{node.name}: unsupported assignment target")
            elif not isinstance(stmt, ast.Return):
                raise ValueError(
                    f"{node.name}: non-straight-line statement "
                    f"{type(stmt).__name__}")
        out[node.name[len("verify_"):]] = node
    return out


def load_verifier_trees(repo_dir):
    """Verifier trees for extraction: upstream verifiers.py, overlaid with any
    step-friendly rewrites in verifiers_steps.py (same names, same outputs,
    restructured into semantic same-dim stages). Returns (trees, overridden)."""
    trees = parse_verifiers(os.path.join(repo_dir, "verifiers.py"))
    overridden = []
    override_path = os.path.join(repo_dir, "verifiers_steps.py")
    if os.path.exists(override_path):
        for tid, tree in parse_verifiers(override_path).items():
            trees[tid] = tree
            overridden.append(tid)
    return trees, sorted(overridden)


def load_offdim_tasks(repo_dir):
    """Task ids whose rewrites deliberately emit off-dimension reference
    frames (stages like a denoised input or a bordered window whose dims
    differ from the output). Declared as a
    module-level literal `OFFDIM_TASKS = {"id", ...}` in verifiers_steps.py;
    missing file or assignment -> empty."""
    path = os.path.join(repo_dir, "verifiers_steps.py")
    if not os.path.exists(path):
        return frozenset()
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "OFFDIM_TASKS"):
            return frozenset(ast.literal_eval(node.value))
    return frozenset()


def _plan(fn_tree):
    """Compile the function's statements once; cached on the tree node."""
    plan = getattr(fn_tree, "_rearc_plan", None)
    if plan is None:
        plan = []
        for stmt in fn_tree.body:
            expr = ast.Expression(stmt.value)
            ast.fix_missing_locations(expr)
            code = compile(expr, "<rearc_steps>", "eval")
            if isinstance(stmt, ast.Assign):
                plan.append(("assign", stmt.targets[0].id, code))
            else:
                plan.append(("return", None, code))
        fn_tree._rearc_plan = plan
    return plan


def trace_verifier(fn_tree, I, ns):
    """Run a straight-line verifier on input grid I (tuple form).

    Returns (grid_candidates, return_value): every assigned value that is a
    grid, in statement order, plus the function's return value."""
    env = dict(ns)
    env["I"] = I
    candidates = []
    ret = None
    for kind, name, code in _plan(fn_tree):
        val = eval(code, env)
        if kind == "assign":
            env[name] = val
            if is_grid(val):
                candidates.append(val)
        else:
            ret = val
    return candidates, ret


def build_steps(candidates, inp, out, keep_offdim=False):
    """The ARC-GEN step post-processing, tightened: consecutive dedup, drop
    leading frames equal to the input, drop frames equal to the output wherever
    they appear (an early answer frame that later regresses is harmful
    supervision); no intermediates -> [], else intermediates + [output].

    Frames whose dimensions differ from the output's are solver working grids
    (crops, sub-canvases) rather than partial outputs - dropped unless
    keep_offdim (off-dimension frames read as working state rather than
    partial answers, while same-dimension frames converge to the output)."""
    if not keep_offdim:
        dims = (len(out), len(out[0]))
        candidates = [f for f in candidates
                      if (len(f), len(f[0])) == dims]
    frames = []
    for f in candidates:
        if f == out:  # answer frames only ever appear once, at the end
            continue
        if not frames or frames[-1] != f:
            frames.append(f)
    while frames and frames[0] == inp:
        frames.pop(0)
    if not frames:
        return []
    return frames + [out]


def downsample(steps, max_steps):
    """Uniformly subsample overlong sequences, always keeping the last frame."""
    if not max_steps or len(steps) <= max_steps:
        return steps
    if max_steps == 1:
        return [steps[-1]]
    n = len(steps)
    idxs = sorted({round(i * (n - 1) / (max_steps - 1))
                   for i in range(max_steps)})
    return [steps[i] for i in idxs]


def _tuplize(grid):
    return tuple(tuple(row) for row in grid)


def _listify(grid):
    return [list(row) for row in grid]


def process_task(task_id, examples, fn_tree, ns, difficulty=None,
                 max_steps=None, keep_offdim=False, emit_steps=True):
    """Trace one task's examples. Returns (records, stats).

    Consistency gate: traced return value must equal the stored output,
    otherwise the record keeps steps=[] and the mismatch is counted.
    emit_steps=False (whitelist mode: task not rewritten against the
    human-reviewed ARC-GEN semantics) still runs the gate but emits no
    steps."""
    rng_list, pso_list = difficulty if difficulty else (None, None)
    aligned = (rng_list is not None and pso_list is not None
               and len(rng_list) == len(examples) == len(pso_list))
    records = []
    stats = {"n_examples": len(examples), "n_with_steps": 0,
             "n_mismatch": 0, "n_error": 0, "frame_hist": {}}
    for i, ex in enumerate(examples):
        inp = _tuplize(ex["input"])
        out = _tuplize(ex["output"])
        steps = []
        try:
            candidates, ret = trace_verifier(fn_tree, inp, ns)
        except Exception:
            stats["n_error"] += 1
        else:
            if ret != out:
                stats["n_mismatch"] += 1
            elif emit_steps:
                steps = downsample(
                    build_steps(candidates, inp, out,
                                keep_offdim=keep_offdim), max_steps)
        if steps:
            stats["n_with_steps"] += 1
        key = str(len(steps))
        stats["frame_hist"][key] = stats["frame_hist"].get(key, 0) + 1
        records.append({
            "task_id": task_id,
            "category": None,  # set below once the task's category is known
            "input": ex["input"],
            "output": ex["output"],
            "steps": [_listify(f) for f in steps],
            "source": "rearc",
            "variation": None,
            "difficulty": ({"rng": rng_list[i], "pso": pso_list[i]}
                           if aligned else None),
        })
    category = "selectable" if stats["n_with_steps"] else "skip"
    stats["category"] = category
    for r in records:
        r["category"] = category
    return records, stats


# ---------------------------------------------------------------------------
# dataset run


def _repo_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _dsl_ns():
    repo = _repo_dir()
    if repo not in sys.path:
        sys.path.insert(0, repo)
    import dsl
    return vars(dsl)


def _load_examples(data_dir, task_id):
    with open(os.path.join(data_dir, "tasks", f"{task_id}.json")) as f:
        return json.load(f)


def _load_difficulty(metadata, task_id):
    m = (metadata or {}).get(task_id)
    if not m:
        return None
    return (m.get("rng_difficulties"), m.get("pso_difficulties"))


def _atomic_write_jsonl(path, records):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
    os.replace(tmp, path)


_WORKER = {}


def _init_worker(repo_dir):
    _WORKER["trees"], _WORKER["overridden"] = load_verifier_trees(repo_dir)
    _WORKER["offdim"] = load_offdim_tasks(repo_dir)
    _WORKER["ns"] = _dsl_ns()


def _run_one(task_id, data_dir, out_dir, difficulty, max_steps,
             keep_offdim=False, steps_from="rewritten"):
    examples = _load_examples(data_dir, task_id)
    started = time.time()
    rewritten = task_id in _WORKER.get("overridden", [])
    keep_offdim = keep_offdim or task_id in _WORKER.get("offdim", ())
    records, stats = process_task(task_id, examples,
                                  _WORKER["trees"][task_id], _WORKER["ns"],
                                  difficulty=difficulty, max_steps=max_steps,
                                  keep_offdim=keep_offdim,
                                  emit_steps=(steps_from == "all"
                                              or rewritten))
    stats["rewritten"] = rewritten
    stats["elapsed_sec"] = round(time.time() - started, 3)
    _atomic_write_jsonl(os.path.join(out_dir, "by_task", f"{task_id}.jsonl"),
                        records)
    return task_id, stats


def _check_invariants(data_dir, out_dir, task_ids, max_failures=20):
    """Spec invariants over the produced dataset; also returns file-derived
    totals so resume runs report accurate counts."""
    failures = []
    n_records = 0
    n_with_steps = 0

    def fail(msg):
        if len(failures) < max_failures:
            failures.append(msg)

    for tid in task_ids:
        src = _load_examples(data_dir, tid)
        path = os.path.join(out_dir, "by_task", f"{tid}.jsonl")
        try:
            with open(path) as f:
                recs = [json.loads(line) for line in f]
        except (OSError, json.JSONDecodeError) as e:
            fail(f"{tid}: unreadable output ({e})")
            continue
        n_records += len(recs)
        if len(recs) != len(src):
            fail(f"{tid}: {len(recs)} records != {len(src)} source examples")
            continue
        for i, (rec, ex) in enumerate(zip(recs, src)):
            try:
                if rec["input"] != ex["input"] or rec["output"] != ex["output"]:
                    fail(f"{tid}[{i}]: input/output differ from source")
                steps = rec["steps"]
            except (KeyError, TypeError):
                fail(f"{tid}[{i}]: record missing required keys")
                continue
            if not steps:
                continue
            n_with_steps += 1
            if any(not is_grid(_tuplize(fr)) for fr in steps):
                fail(f"{tid}[{i}]: illegal grid frame")
            if steps[-1] != rec["output"]:
                fail(f"{tid}[{i}]: last step != output")
            if steps[0] == rec["input"]:
                fail(f"{tid}[{i}]: leading step equals input")
            if any(a == b for a, b in zip(steps, steps[1:])):
                fail(f"{tid}[{i}]: consecutive duplicate frames")
    return ({"passed": not failures, "failures": failures},
            {"n_records": n_records, "n_with_steps": n_with_steps})


def _export_shards(out_dir, task_ids, shard_size):
    lines = []
    for tid in sorted(task_ids):
        with open(os.path.join(out_dir, "by_task", f"{tid}.jsonl")) as f:
            lines.extend(f.readlines())
    random.Random(SHUFFLE_SEED).shuffle(lines)
    shard_dir = os.path.join(out_dir, "shards")
    os.makedirs(shard_dir, exist_ok=True)
    for old in os.listdir(shard_dir):
        if old.startswith("shard-") and old.endswith(".jsonl"):
            os.unlink(os.path.join(shard_dir, old))
    num = 0
    for start in range(0, len(lines), shard_size):
        with open(os.path.join(shard_dir, "shard-%05d.jsonl" % num),
                  "w") as f:
            f.writelines(lines[start:start + shard_size])
        num += 1
    return len(lines), num


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--data", required=True,
                   help="re-arc dataset dir (tasks/<id>.json [+ metadata.json])")
    p.add_argument("--out", required=True, help="output dataset dir")
    p.add_argument("--tasks", default=None,
                   help="comma-separated task ids (default: all in --data)")
    p.add_argument("--procs", type=int, default=1)
    p.add_argument("--shard-size", type=int, default=10000)
    p.add_argument("--max-steps", type=int, default=None,
                   help="uniformly subsample longer step sequences")
    p.add_argument("--keep-offdim", action="store_true",
                   help="keep working-grid frames whose dims differ from "
                        "the output (dropped by default)")
    p.add_argument("--steps-from", choices=["rewritten", "all"],
                   default="rewritten",
                   help="'rewritten' (default): only tasks rewritten in "
                        "verifiers_steps.py emit steps (human-reviewed "
                        "ARC-GEN semantics); 'all': also auto-extracted")
    args = p.parse_args(argv)

    trees, overridden = load_verifier_trees(_repo_dir())
    available = sorted(f[:-5]
                       for f in os.listdir(os.path.join(args.data, "tasks"))
                       if f.endswith(".json"))
    if args.tasks:
        wanted = sorted({t.strip() for t in args.tasks.split(",") if t.strip()})
        missing = [t for t in wanted if t not in set(available)]
        if missing:
            p.error(f"tasks not in --data: {','.join(missing)}")
        task_ids = wanted
    else:
        task_ids = available
    unknown = [t for t in task_ids if t not in trees]
    if unknown:
        p.error(f"no verifier for tasks: {','.join(unknown)}")

    metadata = None
    meta_path = os.path.join(args.data, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            metadata = json.load(f)

    os.makedirs(os.path.join(args.out, "by_task"), exist_ok=True)
    done = {t for t in task_ids
            if os.path.exists(os.path.join(args.out, "by_task",
                                           f"{t}.jsonl"))}
    pending = [t for t in task_ids if t not in done]
    for t in sorted(done):
        print(f"[resume] {t}: by_task file exists, skipping")

    jobs = [(t, args.data, args.out, _load_difficulty(metadata, t),
             args.max_steps, args.keep_offdim, args.steps_from)
            for t in pending]
    stats = {t: {"resumed": True} for t in done}
    if jobs:
        if args.procs > 1:
            with multiprocessing.Pool(args.procs, initializer=_init_worker,
                                      initargs=(_repo_dir(),)) as pool:
                results = pool.starmap(_run_one, jobs)
        else:
            _init_worker(_repo_dir())
            results = [_run_one(*job) for job in jobs]
        for tid, st in results:
            stats[tid] = st
            print(f"[done] {tid}: {st['category']:>10} "
                  f"with_steps {st['n_with_steps']}/{st['n_examples']} "
                  f"mismatch {st['n_mismatch']} error {st['n_error']} "
                  f"({st['elapsed_sec']}s)")

    invariants, file_totals = _check_invariants(args.data, args.out, task_ids)
    n_lines, n_shards = _export_shards(args.out, task_ids, args.shard_size)

    with open(os.path.join(_repo_dir(), "verifiers.py"), "rb") as f:
        verifiers_sha = hashlib.sha256(f.read()).hexdigest()
    override_path = os.path.join(_repo_dir(), "verifiers_steps.py")
    override_sha = None
    if os.path.exists(override_path):
        with open(override_path, "rb") as f:
            override_sha = hashlib.sha256(f.read()).hexdigest()
    totals = {
        "n_tasks": len(task_ids),
        "n_records": file_totals["n_records"],
        "n_with_steps": file_totals["n_with_steps"],
        "n_mismatch": sum(s.get("n_mismatch", 0) for s in stats.values()),
        "n_error": sum(s.get("n_error", 0) for s in stats.values()),
        "n_selectable_tasks": sum(
            1 for s in stats.values() if s.get("category") == "selectable"),
        "n_shards": n_shards,
    }
    manifest = {
        "config": {"data": os.path.abspath(args.data),
                   "out": os.path.abspath(args.out),
                   "tasks": task_ids, "procs": args.procs,
                   "shard_size": args.shard_size,
                   "max_steps": args.max_steps,
                   "keep_offdim": args.keep_offdim,
                   "offdim_tasks": sorted(load_offdim_tasks(_repo_dir())),
                   "steps_from": args.steps_from,
                   "override_tasks": overridden,
                   "verifiers_sha256": verifiers_sha,
                   "verifiers_steps_sha256": override_sha},
        "stats": stats,
        "totals": totals,
        "invariants": invariants,
    }
    with open(os.path.join(args.out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    print(f"[totals] records {totals['n_records']} "
          f"with_steps {totals['n_with_steps']} "
          f"mismatch {totals['n_mismatch']} error {totals['n_error']} "
          f"shards {n_shards} ({n_lines} lines)")
    if invariants["passed"]:
        print("[invariants] all passed")
        return 0
    print("[invariants] FAILED:")
    for msg in invariants["failures"]:
        print(f"  - {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
