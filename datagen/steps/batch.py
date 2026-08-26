"""Batch-generate examples enriched with intermediate `steps`."""

from steps import checkpoints, storage

BASE_SEED = 2025


def _flip_h(grid):
    return [row[::-1] for row in grid]


def _flip_v(grid):
    return grid[::-1]


def _transpose(grid):
    return [list(col) for col in zip(*grid)]


# The eight square-symmetry (dihedral) operations, built from the primitives
# above; used to re-express steps in the output's orientation.
_SYMMETRIES = [
    lambda g: g,
    _flip_h,
    _flip_v,
    lambda g: _flip_h(_flip_v(g)),
    _transpose,
    lambda g: _flip_h(_transpose(g)),
    lambda g: _flip_v(_transpose(g)),
    lambda g: _flip_h(_flip_v(_transpose(g))),
]


def _orient_to_output(steps, output):
    """Re-express every step in the output's orientation.

    Some generators build the grids in a canonical orientation and apply a
    final transpose/flip to BOTH input and output, so the traced intermediate
    snapshots sit in the pre-reorientation frame and the last one differs from
    the output by that symmetry. Detect the symmetry mapping the last step onto
    the output and apply it to every step, so the whole sequence shares the
    input/output frame (no orientation jump). Act only when the symmetry is
    unambiguous; otherwise leave the steps untouched."""
    if not steps or steps[-1] == output:
        return steps
    variants = [[op(s) for s in steps]
                for op in _SYMMETRIES if op(steps[-1]) == output]
    if variants and all(v == variants[0] for v in variants):
        return variants[0]
    return steps


def steps_from_trace(trace, save_vars, selected):
    """Pick the selected blocks' snapshots (under save_vars[0]) as steps,
    dropping any frame identical to the one before it and any leading frame
    identical to the input (a no-op "solving step" carries no signal), then
    re-expressing the sequence in the output's orientation (see
    _orient_to_output)."""
    key = save_vars[0]
    steps = []
    for cp in trace.checkpoints:
        if cp.block_index in selected and key in cp.snapshots:
            snap = cp.snapshots[key]
            if not steps or steps[-1] != snap:
                steps.append(snap)
    raw_input = trace.result.get("input")
    while steps and steps[0] == raw_input:
        steps.pop(0)
    return _orient_to_output(steps, trace.result["output"])


def example_with_steps(task_id, seed, annotation, generator_kwargs=None,
                       colors=None):
    """One {input, output, steps} example for `seed` using a loaded annotation."""
    save_vars = annotation["save_vars"]
    selected = set(annotation["checkpoints"])
    trace = checkpoints.trace_checkpoints(
        task_id, seed=seed, save_vars=save_vars,
        generator_kwargs=generator_kwargs, colors=colors)
    return {
        "input": trace.result["input"],
        "output": trace.result["output"],
        "steps": steps_from_trace(trace, save_vars, selected),
    }


def generate_with_steps(task_id, num, base_seed=BASE_SEED,
                        directory=storage.DEFAULT_DIR, generator_kwargs=None,
                        colors=None):
    """Return `num` examples {input, output, steps} using the saved annotation.

    Seeds match arc_gen.py's convention (`base_seed + i`), so example `i`'s
    input/output match `arc_gen.py generate`'s example `i` for the same kwargs
    and color override."""
    annotation = storage.load_annotation(task_id, directory=directory)
    if annotation is None:
        raise FileNotFoundError(
            f"No annotation for task {task_id}; run 'annotate' first.")
    return [example_with_steps(task_id, base_seed + i, annotation,
                               generator_kwargs=generator_kwargs, colors=colors)
            for i in range(num)]
