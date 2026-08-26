"""Trace ARC-GEN generate() and extract per-top-level-block grid checkpoints."""

import ast
import copy
import inspect
import random
import sys

import task_list
from steps import variations


def _is_grid(value):
    """True for a non-empty list-of-lists (an ARC grid)."""
    return (isinstance(value, list) and len(value) > 0 and
            all(isinstance(row, list) for row in value))


def top_level_blocks(generate_fn):
    """Return [(block_index, abs_lineno, code_summary), ...] for each top-level
    statement in the body of `generate_fn`."""
    src_lines, start = inspect.getsourcelines(generate_fn)
    source = "".join(src_lines)
    func = ast.parse(source).body[0]
    blocks = []
    for index, stmt in enumerate(func.body):
        abs_lineno = start + stmt.lineno - 1
        segment = ast.get_source_segment(source, stmt) or ""
        summary = segment.splitlines()[0].strip() if segment else ""
        blocks.append((index, abs_lineno, summary))
    return blocks


class Checkpoint:
    """One top-level block's completed state."""

    def __init__(self, block_index, lineno, code, snapshots, changed):
        self.block_index = block_index
        self.lineno = lineno
        self.code = code
        self.snapshots = snapshots      # {var_name: grid}
        self.changed = changed          # output differs from previous checkpoint

    def __repr__(self):
        return (f"Checkpoint(block={self.block_index}, "
                f"code={self.code!r}, changed={self.changed})")


class TraceResult:
    def __init__(self, result, checkpoints):
        self.result = result            # generate() return value
        self.checkpoints = checkpoints  # list[Checkpoint]


def _block_of(lineno, starts):
    """Index of the top-level block whose range contains `lineno`."""
    index = -1
    for i, start in enumerate(starts):
        if start <= lineno:
            index = i
        else:
            break
    return index


def _snapshot(frame_locals, save_vars):
    out = {}
    for name, value in frame_locals.items():
        if _is_grid(value) and (save_vars is None or name in save_vars):
            out[name] = copy.deepcopy(value)
    return out


def trace_checkpoints(task_id, seed=2025, save_vars=None, generator_kwargs=None,
                      colors=None):
    """Trace a random `generate()` run and return a TraceResult whose
    `checkpoints` hold the grid snapshots at each top-level block boundary.

    `save_vars=None` auto-detects every grid-typed local; otherwise only the
    named variables are captured. Always reseeds `random` with `seed` first so
    the trace matches the example produced by the same seed.
    `generator_kwargs` are passed to the task generator, and `colors` optionally
    applies a temporary `common.set_colors(...)` palette override.

    Note: tracing fires a line-event callback for every executed line, so a
    single trace costs on the order of 100+ ms; batch generation scales linearly.
    """
    generator_kwargs = variations.normalize_kwargs(generator_kwargs)
    generate_fn = task_list.task_list()[task_id][0]
    blocks = top_level_blocks(generate_fn)
    starts = [b[1] for b in blocks]
    code_filename = generate_fn.__code__.co_filename

    completed = {}                      # block_index -> snapshot dict
    state = {"last_block": None, "last_locals": None}

    def tracer(frame, event, arg):
        if (frame.f_code.co_name != "generate" or
                frame.f_code.co_filename != code_filename):
            # Only the generate frame's line events drive checkpoint detection;
            # returning None disables line tracing for callee frames (e.g. the
            # common.py helpers called in tight loops), which is the dominant
            # tracing cost and produces identical checkpoints either way.
            return None
        if event == "line":
            block = _block_of(frame.f_lineno, starts)
            if state["last_block"] is not None and block != state["last_block"]:
                # Entering a new block: current locals == previous block done.
                completed[state["last_block"]] = _snapshot(frame.f_locals, save_vars)
            state["last_block"] = block
            state["last_locals"] = frame.f_locals
        return tracer

    previous_colors = variations.push_colors(colors)
    previous_trace = sys.gettrace()
    try:
        random.seed(seed)
        sys.settrace(tracer)
        result = generate_fn(**generator_kwargs)
    finally:
        sys.settrace(previous_trace)
        variations.pop_colors(previous_colors)

    # The final block never sees a "next block"; snapshot the last-seen locals so
    # the returned grids are captured under their real variable names and honour
    # save_vars (rather than a hardcoded "output" key).
    if state["last_block"] is not None and state["last_block"] not in completed:
        completed[state["last_block"]] = _snapshot(state["last_locals"] or {}, save_vars)

    key = save_vars[0] if save_vars else "output"
    checkpoints = []
    previous = None
    for index, lineno, code in blocks:
        if index not in completed:
            continue
        snaps = completed[index]
        current = snaps.get(key)
        changed = current is not None and current != previous
        checkpoints.append(Checkpoint(index, lineno, code, snaps, changed))
        if current is not None:
            previous = current
    return TraceResult(result, checkpoints)
