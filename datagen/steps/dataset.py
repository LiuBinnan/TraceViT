"""Dataset orchestration: budget allocation, parallel synthesis, JSONL output,
manifest, resume, and shard export."""

import json
import multiprocessing as mp
import os
import random
import subprocess

import task_list
from steps import storage, synthesize

V1_COUNT = 400


def v1_task_ids():
    """The 400 ARC-AGI-1 task ids (registry is V1-first; see CLAUDE.md)."""
    return list(task_list.task_list())[:V1_COUNT]


def categorize(task_ids, directory):
    """Group task ids by annotation category ('selectable' / 'skip')."""
    by_cat = {storage.CATEGORY_SELECTABLE: [], storage.CATEGORY_SKIP: []}
    for task_id in task_ids:
        annotation = storage.load_annotation(task_id, directory=directory)
        category = annotation["category"] if annotation \
            else storage.CATEGORY_SELECTABLE
        by_cat.setdefault(category, []).append(task_id)
    return by_cat


def allocate(by_cat, total, steps_weight):
    """selectable density = steps_weight x skip density; sums to ~total."""
    unknown = set(by_cat) - {storage.CATEGORY_SELECTABLE, storage.CATEGORY_SKIP}
    if unknown:
        raise ValueError(
            "allocate cannot budget unhandled task categories: %s"
            % sorted(unknown))
    selectable = by_cat.get(storage.CATEGORY_SELECTABLE, [])
    skip = by_cat.get(storage.CATEGORY_SKIP, [])
    denom = len(selectable) * steps_weight + len(skip)
    base = total / denom if denom else 0
    t_skip = round(base)
    t_sel = round(steps_weight * base)
    targets = {tid: t_sel for tid in selectable}
    targets.update({tid: t_skip for tid in skip})
    return targets


def redistribute(targets, stats, total):
    """Raise targets of open (non-ceiling) tasks to absorb the ceiling tasks'
    shortfall. `skip` tasks are NOT backfilled, so skip stays at its base
    allocation and the dataset does not become skip-heavy when many selectable
    tasks hit their diversity ceiling.

    Returns {task_id: new_target} for the eligible open tasks, or {} when there
    is no shortfall or no eligible open task."""
    shortfall = sum(max(0, targets[t] - s["produced"])
                    for t, s in stats.items() if s["hit_ceiling"])
    open_tasks = [t for t, s in stats.items()
                  if not s["hit_ceiling"] and s.get("category") != "skip"]
    if shortfall <= 0 or not open_tasks:
        return {}
    add = shortfall // len(open_tasks)
    if add == 0:
        return {}
    return {t: targets[t] + add for t in open_tasks}


def task_path(out_dir, task_id):
    return os.path.join(out_dir, "by_task", task_id + ".jsonl")


def write_task_records(out_dir, task_id, records):
    """Atomically write one task's records as JSONL (write .tmp then rename)."""
    path = task_path(out_dir, task_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    os.replace(tmp, path)


def is_complete(out_dir, task_id, target):
    """True if the task's file already holds at least `target` records."""
    path = task_path(out_dir, task_id)
    if not os.path.exists(path):
        return False
    with open(path) as f:
        return sum(1 for _ in f) >= target


def _git_sha():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root,
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None


def write_manifest(out_dir, config, all_stats):
    """Write manifest.json: run config + per-task stats + global totals."""
    produced = sum(s.get("produced", 0) for s in all_stats.values())
    ceilings = sum(1 for s in all_stats.values() if s.get("hit_ceiling"))
    manifest = {
        "config": dict(config),
        "totals": {"tasks": len(all_stats), "produced": produced,
                   "hit_ceiling_tasks": ceilings},
        "tasks": all_stats,
    }
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


def _worker(args):
    (task_id, target, seed_base, directory, attempt_timeout, task_budget,
     colors_pool, size_mode) = args
    records, stats = synthesize.synthesize_task(
        task_id, target, seed_base=seed_base, directory=directory,
        attempt_timeout=attempt_timeout, task_budget=task_budget,
        colors_pool=colors_pool, size_mode=size_mode)
    return task_id, records, stats


def _run_pass(out_dir, targets, seed_base, directory, procs,
              attempt_timeout, task_budget, colors_pool, size_mode):
    """Synthesize every not-yet-complete task; write its file; return stats.

    Determinism is independent of `procs`: each task is seeded from
    (seed_base, task_id) and writes its own file, so pool ordering is irrelevant.
    """
    jobs = [(tid, tgt, seed_base, directory, attempt_timeout, task_budget,
             colors_pool, size_mode)
            for tid, tgt in targets.items()
            if not is_complete(out_dir, tid, tgt)]
    results = {}
    if procs and procs > 1 and jobs:
        with mp.Pool(procs) as pool:
            for task_id, records, stats in pool.imap_unordered(_worker, jobs):
                write_task_records(out_dir, task_id, records)
                results[task_id] = stats
    else:
        for job in jobs:
            task_id, records, stats = _worker(job)
            write_task_records(out_dir, task_id, records)
            results[task_id] = stats
    return results


def synthesize_dataset(out_dir, total=200000, seed_base=2025,
                       steps_weight=2.16, procs=None,
                       directory=storage.DEFAULT_DIR, task_ids=None,
                       attempt_timeout=synthesize.ATTEMPT_TIMEOUT,
                       task_budget=synthesize.TASK_BUDGET,
                       colors_pool="none", size_mode="legacy",
                       redistribute_shortfall=True):
    """Allocate a budget over the V1 tasks, synthesize (two passes:
    initial + shortfall redistribution), and write per-task files + manifest."""
    os.makedirs(os.path.join(out_dir, "by_task"), exist_ok=True)
    ids = task_ids if task_ids is not None else v1_task_ids()
    by_cat = categorize(ids, directory)
    targets = allocate(by_cat, total, steps_weight)

    stats = _run_pass(out_dir, targets, seed_base, directory, procs,
                      attempt_timeout, task_budget, colors_pool, size_mode)
    if redistribute_shortfall:
        raised = redistribute(targets, stats, total)
        if raised:
            stats.update(_run_pass(out_dir, raised, seed_base, directory, procs,
                                   attempt_timeout, task_budget, colors_pool,
                                   size_mode))

    config = {"total": total, "seed_base": seed_base,
              "steps_weight": steps_weight, "colors_pool": colors_pool,
              "size_mode": size_mode,
              "redistribute": redistribute_shortfall, "procs": procs,
              "attempt_timeout": attempt_timeout,
              "task_budget": task_budget, "git_sha": _git_sha()}
    write_manifest(out_dir, config, stats)
    return stats


def export_shards(out_dir, shard_size=10000, shuffle_seed=2025):
    """Concat all by_task/*.jsonl, deterministically shuffle, write fixed-size
    shards under shards/. Returns (total_lines, num_shards)."""
    by_task = os.path.join(out_dir, "by_task")
    lines = []
    for fn in sorted(os.listdir(by_task)):
        if not fn.endswith(".jsonl"):
            continue
        with open(os.path.join(by_task, fn)) as f:
            lines.extend(line for line in f.read().splitlines() if line)
    random.Random(shuffle_seed).shuffle(lines)

    shard_dir = os.path.join(out_dir, "shards")
    os.makedirs(shard_dir, exist_ok=True)
    num = 0
    for start in range(0, len(lines), shard_size):
        chunk = lines[start:start + shard_size]
        with open(os.path.join(shard_dir,
                               "shard-%05d.jsonl" % num), "w") as f:
            f.write("\n".join(chunk) + "\n")
        num += 1
    return len(lines), num
