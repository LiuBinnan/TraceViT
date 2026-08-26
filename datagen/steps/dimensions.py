"""Infer a per-task kwargs variation space from the generator signature.

Only scalar numeric/bool params are auto-varied (by name class); color-like and
opaque/list-like params are left None so the generator randomizes them. The
validation layer (steps.validate) and calibration (steps.synthesize) backstop
over-generous bands, so ranges here are heuristics, not per-task ground truth.
A per-task overrides/<id>.json can replace/exclude/restrict the space."""

import inspect
import json
import os

OVERRIDES_DIR = os.path.join(os.path.dirname(__file__), "overrides")

OUTER_SIZE = {"size", "width", "height", "rows", "cols", "row", "col",
              "wide", "tall", "radius"}
BLOCK_SIZE = {"minisize", "minirows", "minicols", "brow", "bcol",
              "megarows", "megacols", "zoom_width", "zoom_height"}
COUNT = {"boxes", "count", "num", "n", "k"}
BOOL = {"xpose", "flip"}
OFFSET = {"offset"}

DEFAULT_BANDS = {
    "outer_size": (4, 22),
    "block_size": (2, 5),
    "count": (1, 8),
    "offset": (0, 4),
}

# Widened sweep bands used only by size_mode="fit" calibration. Only the genuine
# grid-size classes are widened; count/offset keep DEFAULT_BANDS (more objects can
# drift task semantics, which the structural <=30x30 check would not catch).
FIT_BANDS = {
    "outer_size": (4, 30),
    "block_size": (2, 10),
    "count": DEFAULT_BANDS["count"],
    "offset": DEFAULT_BANDS["offset"],
}


class IntSampler:
    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi

    def sample(self, rng):
        return rng.randint(self.lo, self.hi)


class ChoiceSampler:
    def __init__(self, choices):
        self.choices = list(choices)

    def sample(self, rng):
        return rng.choice(self.choices)


def _class_of(name):
    if name in OUTER_SIZE:
        return "outer_size"
    if name in BLOCK_SIZE:
        return "block_size"
    if name in COUNT:
        return "count"
    if name in OFFSET:
        return "offset"
    if name in BOOL:
        return "bool"
    return None


def infer_space(generate_fn, bands=DEFAULT_BANDS):
    """Return {param_name: sampler} for the auto-varied params of a generator."""
    space = {}
    for name in inspect.signature(generate_fn).parameters:
        cls = _class_of(name)
        if cls is None:
            continue
        if cls == "bool":
            space[name] = ChoiceSampler([True, False])
        else:
            lo, hi = bands[cls]
            space[name] = IntSampler(lo, hi)
    return space


def load_override(task_id, directory=OVERRIDES_DIR):
    path = os.path.join(directory, task_id + ".json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def _sampler_from_spec(spec):
    if spec["type"] == "int":
        lo, hi = spec["range"]
        return IntSampler(lo, hi)
    if spec["type"] == "choice":
        return ChoiceSampler(spec["choices"])
    raise ValueError("unknown sampler spec type: %r" % spec.get("type"))


def variation_space(task_id, generate_fn, directory=OVERRIDES_DIR,
                    bands=DEFAULT_BANDS):
    """Inferred space adjusted by an optional overrides/<id>.json:
    `kwargs` replaces per-param samplers, `exclude` drops params, and a non-null
    `include_only` restricts the space to the listed params."""
    space = infer_space(generate_fn, bands=bands)
    override = load_override(task_id, directory)
    if override:
        for name, spec in (override.get("kwargs") or {}).items():
            space[name] = _sampler_from_spec(spec)
        for name in (override.get("exclude") or []):
            space.pop(name, None)
        include_only = override.get("include_only")
        if include_only is not None:
            space = {k: v for k, v in space.items() if k in include_only}
    return space
