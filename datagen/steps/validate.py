"""Structural invariants for synthesized samples."""

MAX_DIM = 30


def is_grid(value):
    """True for a non-empty rectangular list-of-lists of ints 0-9."""
    if not isinstance(value, list) or len(value) == 0:
        return False
    if not all(isinstance(row, list) and len(row) > 0 for row in value):
        return False
    width = len(value[0])
    return all(
        len(row) == width and
        all(isinstance(c, int) and 0 <= c <= 9 for c in row)
        for row in value)


def within_cap(grid):
    """True if the grid is within the ARC 30x30 cap (assumes is_grid)."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return 1 <= rows <= MAX_DIM and 1 <= cols <= MAX_DIM


def validate_sample(record, category):
    """Return None if the record is valid, else a short reason string.

    `record` is {input, output, steps}. `category` is 'selectable' or 'skip'.
    skip: input/output well-formed & capped, steps must be empty.
    selectable: additionally steps non-empty, every step a well-formed grid
    within the 30x30 cap, and the last step equals output. Intermediate steps
    MAY differ in size from output -- crop/resize/tile tasks have differently
    sized intermediate states; only the last step must equal output (which also
    catches non-representative annotation seeds)."""
    inp, out, steps = record["input"], record["output"], record["steps"]
    if not is_grid(inp) or not is_grid(out):
        return "malformed"
    if not within_cap(inp) or not within_cap(out):
        return "oversize"
    if category == "skip":
        return "skip_with_steps" if steps else None
    if not steps:
        return "empty_steps"
    for step in steps:
        if not is_grid(step):
            return "malformed_step"
        if not within_cap(step):
            return "step_oversize"
    if steps[-1] != out:
        return "laststep_mismatch"
    return None
