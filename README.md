# TraceViT

**TraceViT: Grounded Trace Supervision for Visual Abstract Reasoning**

[![arXiv](https://img.shields.io/badge/arXiv-2607.29586-b31b1b.svg)](https://arxiv.org/abs/2607.29586)
[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-arc--steps-blue)](https://huggingface.co/datasets/lbn32/arc-steps)

## The `arc-steps` dataset

| config | tasks | records | traced | implementation |
|---|---:|---:|---:|---|
| `arcgen_v1` | 400 | 399,990 | 305,616 | ARC-GEN generators, ARC-AGI-1 training tasks |
| `arcgen_v2` | 500 | 487,091 | 486,091 | ARC-GEN generators, ARC-AGI-2 training tasks |
| `rearc` | 400 | 399,871 | 270,854 | RE-ARC generators + step-decomposed solver programs, ARC-AGI-1 training tasks |

- Grids are `int[][]` with values 0-9, at most 30×30.
- A record is traced if its `steps` list is non-empty. **The last step equals
  `output`**; intermediate grids can differ in size from the output.
- `arcgen_v2` records also carry a `rule` text that summarizes the task's
  transformation. Claude Opus 4.8 wrote these summaries without human review,
  so some may be wrong.
- All records are synthetic; no official ARC grids are included.

### Browsing the chains

`visualize_steps.py` renders one config as a static site: a searchable task
index and one page per task, with each record drawn as an
input → steps → output filmstrip.

```bash
# grab one config's raw jsonl (~1 GB each)
hf download lbn32/arc-steps --repo-type dataset --include "data/rearc/*" --local-dir .

python visualize_steps.py data/rearc/train.jsonl
# then open steps_viz_rearc/index.html in a browser
```

`--tasks` renders only the listed tasks, `--records-per-task` sets how many
records each task page shows (default 10), and `--out-dir` changes the output
directory.

## Regenerating the data

[`datagen/`](datagen/) holds the pipeline behind the `arcgen_v1` and
`arcgen_v2` configs: the ARC-GEN generators for 400 ARC-AGI-1 and 500
ARC-AGI-2 tasks, rewritten into single-action steps; the per-task checkpoint
annotations; and the tracing and synthesis code that turns them into
`{input, steps, output}` records. See [`datagen/README.md`](datagen/README.md)
for usage.

[`rearc/`](rearc/) holds the pipeline behind the `rearc` config: the RE-ARC
solver programs, rewritten into semantic stages, and a script that replays them
on the RE-ARC examples to extract `steps`. See
[`rearc/README.md`](rearc/README.md).

## Acknowledgements

We thank the authors of the following projects:

- [RE-ARC](https://github.com/michaelhodel/re-arc): procedural generators and
  solver programs behind the `rearc` config (`rearc/` is derived from it).
- [ARC-GEN](https://github.com/google/ARC-GEN): procedural generators behind the
  `arcgen_v1` / `arcgen_v2` configs (`datagen/` is derived from it).
- [VARC](https://github.com/lillian039/VARC) (*ARC Is a Vision Problem!*): the
  training and test-time-training (TTT) framework that TraceViT builds on.
- [LoopViT](https://github.com/WenjieShu/LoopViT) (*Scaling Visual ARC with Looped
  Transformers*): the looped-transformer backbone that TraceViT extends.
