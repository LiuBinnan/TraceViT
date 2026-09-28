"""Records for a task's ORIGINAL ARC-AGI examples, each enriched with steps --
the canonical counterpart of the synthetic records.

input/output come from the reference JSON (the true ARC-AGI-1 examples). For
steps, validate() reproduces every original via an explicit generate() call, so
we capture those kwargs and trace the same call once (seed 2025). The few
generators that retain residual randomness (or whose selected blocks don't fire
for the canonical params) won't reproduce/yield valid steps -- those originals
are still emitted with steps == [] and counted in `without_steps`."""

import copy
import importlib
import json
import os

import task_list
from steps import batch, checkpoints, storage

SEED = 2025
# Resolution order: ARC-AGI-1 training, then ARC-AGI-2 training, then ARC-AGI-1
# evaluation. Training first so the V1 tasks that also appear in ARC-AGI-2
# replay against the V1 JSON (validate()'s call order is the V1 example
# order). ARC-AGI-2 before evaluation because the ARC-AGI-2 registry tasks
# reproduce the ARC-AGI-2 examples, and some of them also appear in the V1
# evaluation set with different content.
ARC_DIRS = ["external/ARC-AGI/data/training",
            "external/ARC-AGI-2/data/training",
            "external/ARC-AGI/data/evaluation"]


def _reference(task_id):
    """[(split, {input, output}), ...] from the reference JSON, or None."""
    for directory in ARC_DIRS:
        path = os.path.join(directory, task_id + ".json")
        if os.path.exists(path):
            data = json.load(open(path))
            return ([("train", ex) for ex in data.get("train", [])] +
                    [("test", ex) for ex in data.get("test", [])])
    return None


def _validate_kwargs(task_id):
    """The kwargs of each generate() call validate() makes, in order."""
    module = importlib.import_module("tasks.task_" + task_id)
    captured = []
    original = module.generate

    def wrapper(**kwargs):
        captured.append(copy.deepcopy(kwargs))
        return original(**kwargs)

    module.generate = wrapper
    try:
        module.validate()
    finally:
        module.generate = original
    return captured


def original_records(task_id, directory=storage.DEFAULT_DIR):
    """Return (records, stats) for one task's original examples (train + test),
    each tagged source="original" and split="train"/"test". selectable records
    carry steps where reproducible (skip / un-reproducible -> steps == [])."""
    annotation = storage.load_annotation(task_id, directory=directory)
    category = annotation["category"] if annotation else "selectable"
    references = _reference(task_id) or []
    kwargs_list = _validate_kwargs(task_id)

    records, without_steps = [], 0
    for (split, example), kwargs in zip(references, kwargs_list):
        steps = []
        if annotation is not None and category != "skip":
            trace = checkpoints.trace_checkpoints(
                task_id, seed=SEED, save_vars=annotation["save_vars"],
                generator_kwargs=kwargs)
            if (trace.result["input"] == example["input"] and
                    trace.result["output"] == example["output"]):
                candidate = batch.steps_from_trace(
                    trace, annotation["save_vars"],
                    set(annotation["checkpoints"]))
                if candidate and candidate[-1] == example["output"]:
                    steps = candidate
            if not steps:
                without_steps += 1
        elif annotation is None:
            # No annotation -> no meaningful checkpoints to trace; the original
            # is still emitted with steps == [] and counted as without_steps.
            without_steps += 1
        records.append({
            "task_id": task_id,
            "category": category,
            "source": "original",
            "split": split,
            "input": example["input"],
            "output": example["output"],
            "steps": steps,
            "variation": {"seed": None, "kwargs": kwargs, "colors": None},
        })
    stats = {"task_id": task_id, "category": category,
             "originals": len(records), "without_steps": without_steps}
    return records, stats
