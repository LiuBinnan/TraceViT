# datagen: step-instrumented generators (ARC-AGI-1)

The generation pipeline behind the `arcgen_v1` config of
[arc-steps](https://huggingface.co/datasets/lbn32/arc-steps): the 400
[ARC-GEN](https://github.com/google/ARC-GEN) generators for the ARC-AGI-1
training tasks, rewritten so that each top-level statement of `generate()`
performs one semantic action. A tracing layer replays a generator and snapshots
the grid at annotated checkpoints, turning every example into an
`{input, steps, output}` transformation chain.

## Quick start

```bash
python3 arc_gen.py generate 007bbfb7 3    # plain input/output pairs
python3 arc_gen.py steps 007bbfb7 3       # pairs with transformation chains

git submodule update --init               # one-time, needed only by validate
python3 arc_gen.py validate               # reproduce all 400 official tasks byte-for-byte
```

`generate` and `steps` reseed per example (`BASE_SEED = 2025`), so single-task
outputs reproduce exactly.

## Synthesizing a corpus

```bash
python3 arc_gen.py synthesize --out out/v1 --total 200000
python3 add_backgrounds.py out/v1
python3 add_foregrounds.py out/v1
python3 add_originals.py out/v1
```

Synthesis samples under per-attempt and per-task time budgets, so a rerun gives
a same-distribution corpus rather than a byte-identical one. The frozen
[arc-steps](https://huggingface.co/datasets/lbn32/arc-steps) release is
canonical. `add_originals` appends replays of the official ARC examples. The
public release ships without those replays.
