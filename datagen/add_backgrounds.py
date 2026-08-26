"""Post-process: vary the (black) background color of an existing dataset's
synthetic records via steps.background.recolor_background -- a pure background
relabel (0 -> a random unused color, consistent across input/output/steps), so
the foreground and the input->output transformation are untouched. Mirrors
re_arc's varied backgrounds.

Originals are left as-is (ground truth). Idempotent: records already carrying a
`background` field are skipped, so reruns are no-ops. Re-exports shards.

Usage (from the ARC-GEN repo root): python3 add_backgrounds.py <dataset_dir>
"""

import json
import os
import random
import sys

from steps import background, dataset, dimensions, sampler, validate

BASE_SEED = 2025


def _should_recolor(task_id):
    """Whether to vary this task's background at all. A per-task override of
    `"background_recolor": "off"` keeps the whole task black (mirrors
    add_foregrounds._should_recolor); used for black-canvas tasks."""
    override = dimensions.load_override(task_id) or {}
    return override.get("background_recolor") != "off"


def _any_background(task_id):
    """Whether to relabel a NON-zero background too (opt-in). A per-task override
    of `"background_recolor": "any"` lets a task whose canvas is a non-black
    color (e.g. an orange 8x8 board) vary that background; default keeps the
    always-safe black(0)-only behavior."""
    override = dimensions.load_override(task_id) or {}
    return override.get("background_recolor") == "any"


def augment_backgrounds(out_dir, seed_base=BASE_SEED):
    """Apply recolor_background to every not-yet-processed synthetic record in
    `out_dir`, in place. Returns a stats dict. Each record gains a `background`
    field (the chosen color, 0 when left black). Deterministic per record."""
    with open(os.path.join(out_dir, "manifest.json")) as f:
        manifest = json.load(f)
    stats = {"recolored": 0, "kept_black": 0, "skipped_original": 0,
             "already_done": 0, "failures": 0}
    for task_id in manifest["tasks"]:
        path = dataset.task_path(out_dir, task_id)
        if not os.path.exists(path):
            continue
        if not _should_recolor(task_id):
            continue                                   # keep black (override)
        any_bg = _any_background(task_id)
        category = manifest["tasks"][task_id].get("category", "selectable")
        with open(path) as f:
            records = [json.loads(line) for line in f]
        changed = False
        for index, record in enumerate(records):
            if record.get("source") == "original":
                stats["skipped_original"] += 1
                continue
            if "background" in record:
                stats["already_done"] += 1
                continue
            rng = random.Random(
                sampler.task_seed(seed_base, task_id, "bg:%d" % index))
            inp, out, steps, color = background.recolor_background(
                record["input"], record["output"],
                record.get("steps") or [], rng, any_background=any_bg)
            record["input"], record["output"], record["steps"] = inp, out, steps
            record["background"] = color
            changed = True
            stats["recolored" if color else "kept_black"] += 1
            if validate.validate_sample(record, category) is not None:
                stats["failures"] += 1
        if changed:
            dataset.write_task_records(out_dir, task_id, records)
    return stats


if __name__ == "__main__":
    out = sys.argv[1]
    s = augment_backgrounds(out)
    print("backgrounds: recolored %d, kept black %d, originals skipped %d, "
          "already-done %d; validate failures=%d"
          % (s["recolored"], s["kept_black"], s["skipped_original"],
             s["already_done"], s["failures"]))
    total, num = dataset.export_shards(out)
    print("re-exported %d shards (%d lines)" % (num, total))
