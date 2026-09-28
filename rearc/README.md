# rearc: step-decomposed RE-ARC solver programs

This is the extraction pipeline behind the `rearc` config of
[arc-steps](https://huggingface.co/datasets/lbn32/arc-steps).
[RE-ARC](https://github.com/michaelhodel/re-arc) pairs every ARC-AGI-1
training task with a procedural example generator and a solver program (a
*verifier*) written in a small grid DSL. `verifiers_steps.py` rewrites 291 of
these verifiers so that the intermediate grids they assign are the task's
semantic solving stages, each with the output's dimensions. The rewrites keep
the exact input → output mapping of the upstream programs. `rearc_steps.py`
replays a verifier statement by statement on each RE-ARC example and records
those intermediate grids as the example's `steps`.

- `dsl.py`, `verifiers.py`: the upstream DSL and the 400 original verifiers,
  unchanged.
- `verifiers_steps.py`: the 291 rewritten verifiers, which replace the
  same-named verifiers in `verifiers.py`. `OFFDIM_TASKS` lists the tasks whose
  stages deliberately use dimensions other than the output's.
- `no_stages.txt`: 16 reviewed tasks whose solution is a single action. They
  keep the upstream verifier and emit no steps.
- `rearc_steps.py`: the extraction script.

## Usage

```bash
# the RE-ARC dataset: 1000 verified examples per task (re_arc/tasks/<id>.json)
curl -LO https://github.com/michaelhodel/re-arc/raw/main/re_arc.zip && unzip re_arc.zip

python3 rearc_steps.py --data re_arc --out out/rearc --procs 8
```

The output uses the same layout as the `datagen/` corpora: `by_task/<id>.jsonl`
with one `{task_id, input, output, steps, ...}` record per RE-ARC example,
`shards/`, and a `manifest.json` with per-task counts. Each example's input and
output are copied unchanged from RE-ARC. A record gets steps only when the
traced verifier reproduces the stored output exactly; `n_mismatch` in the
manifest counts the records where it does not (0 on the released data). Tasks
without a rewrite emit `steps: []`. Pass `--steps-from all` to trace the
upstream verifiers for those tasks as well.

On the full RE-ARC dataset this gives 400,000 records, 270,854 of them with
steps (all from the 291 rewritten tasks). The `rearc` config of arc-steps also
drops the 129 records that contain a grid larger than 30x30.
