# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Post-process a synthesized dataset dir in place: recolor the FOREGROUND of
synthetic records (skip originals) with a per-record consistent color bijection,
then re-export shards. Idempotent (marks done records with a `foreground` field),
deterministic, and color-sensitive tasks are skipped via overrides. Stacks on
add_originals + add_backgrounds.

Each record's rng is seeded from its ABSOLUTE line index within the task file,
so reproducibility depends on running this pass LAST (after add_originals +
add_backgrounds) and on no upstream pass reordering records.

Usage (from repo root):  python3 add_foregrounds.py <dataset_dir>"""
import json
import os
import random
import sys

from steps import dataset, dimensions, foreground

SEED_BASE = 2025


def _recolor_from_override(override):
    """Whether to recolor this task at all (whole-task block via overrides)."""
    return (override.get("foreground_recolor") != "off" and
            override.get("colors") != "off")


def _frozen_from_override(override):
    """Per-color FREEZE set: colors held fixed (neither source nor target of the
    bijection) while OTHER foreground colors still recolor."""
    return set(override.get("foreground_freeze", []))


def _should_recolor(task_id):
    return _recolor_from_override(dimensions.load_override(task_id) or {})


def _frozen_colors(task_id):
    return _frozen_from_override(dimensions.load_override(task_id) or {})


def add_foregrounds(out_dir, seed_base=SEED_BASE):
    by_task = os.path.join(out_dir, "by_task")
    n_recolored = 0
    for fn in sorted(os.listdir(by_task)):
        if not fn.endswith(".jsonl"):
            continue
        task_id = fn[:-len(".jsonl")]
        override = dimensions.load_override(task_id) or {}  # load once per task
        recolor = _recolor_from_override(override)
        frozen = _frozen_from_override(override) | {0}  # CLASS-1: black(0) is background, never foreground-recolor
        path = os.path.join(by_task, fn)
        with open(path) as f:
            records = [json.loads(line) for line in f if line.strip()]
        changed = False
        for idx, rec in enumerate(records):
            if rec.get("source") == "original" or "foreground" in rec:
                continue                                   # faithful / already done
            if not recolor:
                continue
            rng = random.Random("%d-%s-%d" % (seed_base, task_id, idx))
            ni, no, ns, applied = foreground.recolor_foreground(
                rec["input"], rec["output"], rec["steps"], rng, freeze=frozen)
            rec["input"], rec["output"], rec["steps"] = ni, no, ns
            rec["foreground"] = applied                    # {} if identity draw
            changed = True
            if applied:
                n_recolored += 1
        if changed:
            dataset.write_task_records(out_dir, task_id, records)
    total, num = dataset.export_shards(out_dir)
    return n_recolored, total, num


if __name__ == "__main__":
    out = sys.argv[1]
    recolored, total, shards = add_foregrounds(out)
    print("foreground-recolored %d records; re-exported %d shards (%d lines)"
          % (recolored, shards, total))
