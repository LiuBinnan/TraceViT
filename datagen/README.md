# datagen: step-instrumented generators (ARC-AGI-1 and ARC-AGI-2)

This is the generation pipeline behind the `arcgen_v1` and `arcgen_v2` configs
of [arc-steps](https://huggingface.co/datasets/lbn32/arc-steps). It contains
[ARC-GEN](https://github.com/google/ARC-GEN) generators for 400 ARC-AGI-1 and
500 ARC-AGI-2 training tasks, rewritten so that each top-level statement of
`generate()` performs one semantic action. A tracing layer replays a generator
and snapshots the grid at annotated checkpoints, which turns each example into
an `{input, steps, output}` transformation chain.

## Layout

- `tasks/task_<id>.py`: one generator per task (`generate()` and `validate()`),
  registered in `task_list.py`. The 400 ARC-AGI-1 tasks come first, then the
  500 ARC-AGI-2 tasks; `task_ids_v2.txt` lists the latter.
- `annotations/<id>.json`: for each task, the checkpoints in `generate()` that
  mark meaningful solving stages.
- `steps/overrides/<id>.json`: per-task sampling constraints, namely parameter
  ranges, excluded parameters, and which colors stay fixed under recoloring
  (`foreground_freeze`, `background_recolor`, `foreground_recolor`). Tasks
  without a file use the inferred defaults.
- `steps/`: tracing (`checkpoints.py`, `batch.py`), variation-space inference
  (`dimensions.py`, `sampler.py`), synthesis (`synthesize.py`, `dataset.py`),
  and the recoloring layers (`background.py`, `foreground.py`).
- `external/`: the official ARC-AGI-1 and ARC-AGI-2 task JSON (git
  submodules), used only by `validate` and `add_originals`.

## Quick start

```bash
python3 arc_gen.py generate 007bbfb7 3    # plain input/output pairs
python3 arc_gen.py steps e5790162 3       # pairs with transformation chains

git submodule update --init               # one-time, needed only by validate / add_originals
python3 arc_gen.py validate               # reproduce all 900 official tasks byte-for-byte
```

`generate` and `steps` reseed for every example (`BASE_SEED = 2025`), so the
output for a single task is exactly reproducible.

## Synthesizing a corpus

```bash
# arcgen_v1: the 400 ARC-AGI-1 tasks (the default task set)
python3 arc_gen.py synthesize --out out/v1 --total 200000
python3 add_originals.py out/v1
python3 add_backgrounds.py out/v1
python3 add_foregrounds.py out/v1

# arcgen_v2: the 500 ARC-AGI-2 tasks
python3 arc_gen.py synthesize --out out/v2 --tasks-file task_ids_v2.txt \
    --total 500000 --steps-weight 1.0 --colors-pool none --no-redistribute
python3 add_originals.py out/v2 --tasks-file task_ids_v2.txt
python3 add_backgrounds.py out/v2
python3 add_foregrounds.py out/v2
```

`--procs N` runs synthesis over tasks in parallel. Sampling is capped by
per-attempt and per-task time budgets, so a rerun produces a corpus with the
same distribution, not a byte-identical one; the frozen
[arc-steps](https://huggingface.co/datasets/lbn32/arc-steps) release is the
canonical version.

`add_originals` appends replays of the official ARC examples. The public
release leaves these replays out.
