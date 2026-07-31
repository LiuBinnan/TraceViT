# TraceViT

<!-- TODO(paper): fill in the arXiv badge link once the paper is public. -->

**TraceViT: Grounded Trace Supervision for Visual Abstract Reasoning**

[![arXiv](https://img.shields.io/badge/arXiv-TODO-b31b1b.svg)](https://arxiv.org/abs/TODO)
[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-arc--steps-blue)](https://huggingface.co/datasets/lbn32/arc-steps)

## The `arc-steps` dataset

| config | tasks | records | traced | implementation |
|---|---:|---:|---:|---|
| `arcgen_v1` | 400 | 399,990 | 305,616 | ARC-GEN generators, ARC-AGI-1 training tasks |
| `arcgen_v2` | 500 | 487,091 | 486,091 | ARC-GEN generators, ARC-AGI-2 training tasks |
| `rearc` | 400 | 399,871 | 270,854 | RE-ARC generators + step-decomposed solver programs, ARC-AGI-1 training tasks |

- grids are `int[][]` with values 0–9, at most 30×30;
- a record is traced iff `steps` is non-empty; **the last step equals `output`**,
  and intermediate grids may differ in size from the output;
- `arcgen_v2` records additionally carry a `rule` text describing the task's
  transformation, summarized by Claude Opus 4.8 without human review — not
  guaranteed to be correct;
- all records are synthetic — no official ARC grids are included.

### Browsing the chains

`visualize_steps.py` renders one config as a
static site — an index page with a task search box, one page per task, records
drawn as input → steps → output filmstrips:

```bash
# grab one config's raw jsonl (~1 GB each)
hf download lbn32/arc-steps --repo-type dataset --include "data/rearc/*" --local-dir .

python visualize_steps.py data/rearc/train.jsonl
# then open steps_viz_rearc/index.html in a browser
```

`--tasks` renders a subset, `--records-per-task` sets how many records each task
page shows (default 10), `--out-dir` overrides the output directory.

## Acknowledgements

TraceViT builds on, and is grateful to, the following projects:

- [RE-ARC](https://github.com/michaelhodel/re-arc) — procedural generators and
  solver programs behind the `rearc` config;
- [ARC-GEN](https://github.com/google/ARC-GEN) — procedural generators behind the
  `arcgen_v1` / `arcgen_v2` configs;
- [VARC](https://github.com/lillian039/VARC) (*ARC Is a Vision Problem!*) — the
  training and test-time-training (TTT) framework that TraceViT builds on;
- [LoopViT](https://github.com/WenjieShu/LoopViT) (*Scaling Visual ARC with Looped
  Transformers*) — the looped-transformer backbone that TraceViT extends.
