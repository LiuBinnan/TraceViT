"""Add each task's ORIGINAL examples (with steps) to an existing dataset, tag
the existing synthetic records with source='synthetic', refresh the manifest,
and re-export shards. Idempotent: re-running replaces the originals rather than
duplicating them.

Usage (from the ARC-GEN repo root):
    python3 add_originals.py <dataset_dir> [--tasks-file ids.txt]

Default scope is the 400 V1 tasks (backward compatible); pass --tasks-file
(one task id per line, e.g. the 500 V2 ids) to change the scope."""

import json
import os
import sys

import task_list
from steps import dataset, originals


def main(out_dir, task_ids=None):
    ids = task_ids if task_ids is not None else list(task_list.task_list())[:400]
    manifest_path = os.path.join(out_dir, "manifest.json")
    manifest = json.load(open(manifest_path))

    total_originals = 0
    total_without_steps = 0
    for task_id in ids:
        path = dataset.task_path(out_dir, task_id)
        synthetic = []
        if os.path.exists(path):
            for line in open(path):
                record = json.loads(line)
                if record.get("source") == "original":
                    continue                   # drop prior originals (idempotent)
                record.setdefault("source", "synthetic")
                record.setdefault("split", None)
                synthetic.append(record)
        orig_records, stats = originals.original_records(task_id)
        total_originals += stats["originals"]
        total_without_steps += stats["without_steps"]
        dataset.write_task_records(out_dir, task_id, orig_records + synthetic)
        if task_id in manifest["tasks"]:
            manifest["tasks"][task_id]["originals"] = stats["originals"]
            manifest["tasks"][task_id]["original_without_steps"] = \
                stats["without_steps"]

    by_task_dir = os.path.join(out_dir, "by_task")
    grand_total = 0
    for fn in sorted(os.listdir(by_task_dir)):
        if fn.endswith(".jsonl"):
            grand_total += sum(1 for _ in open(os.path.join(by_task_dir, fn)))
    manifest["totals"]["produced"] = grand_total
    manifest["totals"]["originals"] = total_originals
    manifest["totals"]["original_without_steps"] = total_without_steps
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    total, num = dataset.export_shards(out_dir)
    print("added %d originals (%d without steps); dataset now %d samples in %d "
          "shards" % (total_originals, total_without_steps, total, num))


def _tasks_from_file(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    out_arg = sys.argv[1]
    ids_arg = None
    if "--tasks-file" in sys.argv:
        ids_arg = _tasks_from_file(sys.argv[sys.argv.index("--tasks-file") + 1])
    main(out_arg, task_ids=ids_arg)
