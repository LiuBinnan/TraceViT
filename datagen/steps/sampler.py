"""Deterministic, parallelism-independent variation-tuple stream per task."""

import hashlib
import random


def task_seed(seed_base, task_id, salt):
    """A stable integer seed from (seed_base, task_id, salt).

    Uses hashlib (NOT Python's built-in hash(), which is PYTHONHASHSEED-
    randomized for strings) so the stream is identical across processes/runs."""
    digest = hashlib.sha256(
        ("%d:%s:%s" % (seed_base, task_id, salt)).encode()).digest()
    return int.from_bytes(digest[:8], "big")


def kwargs_stream(space, seed_base, task_id):
    """Yield kwargs dicts forever, deterministically, from a per-task PRNG."""
    rng = random.Random(task_seed(seed_base, task_id, "kwargs"))
    names = sorted(space)
    while True:
        yield {name: space[name].sample(rng) for name in names}


def candidates(space, seed_base, task_id):
    """Yield (kwargs, gen_seed) candidates; gen_seed = seed_base + index."""
    stream = kwargs_stream(space, seed_base, task_id)
    index = 0
    while True:
        yield (next(stream), seed_base + index)
        index += 1


def palette_stream(seed_base, task_id):
    """Yield color palettes forever, deterministically, from a per-task PRNG.

    Each palette keeps the background (0) fixed and permutes colors 1-9 --
    the same palette shape arc_gen_variations.py uses for recolored
    variations."""
    rng = random.Random(task_seed(seed_base, task_id, "colors"))
    while True:
        tail = list(range(1, 10))
        rng.shuffle(tail)
        yield [0] + tail
