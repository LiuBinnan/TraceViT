"""Read/write checkpoint annotations as JSON keyed by task id."""

import json
import os

SCHEMA_VERSION = 3
DEFAULT_DIR = "annotations"

CATEGORY_SELECTABLE = "selectable"   # type 2: pick + save intermediate steps
CATEGORY_REWRITE = "rewrite"         # type 3: generator must be rewritten
CATEGORY_SKIP = "skip"               # type 1: no intermediate steps needed
CATEGORIES = (CATEGORY_SELECTABLE, CATEGORY_REWRITE, CATEGORY_SKIP)
DEFAULT_CATEGORY = CATEGORY_SELECTABLE


def _path(task_id, directory):
    return os.path.join(directory, task_id + ".json")


def save_annotation(task_id, trace_seed, save_vars, checkpoints,
                    category=DEFAULT_CATEGORY, group=None, directory=DEFAULT_DIR):
    """Persist one task's category, class (group) and selected block indices."""
    if category not in CATEGORIES:
        raise ValueError("unknown category: %r" % category)
    if group is not None:
        if not isinstance(group, str):
            raise ValueError("group must be a string or None: %r" % group)
        group = group.strip() or None
    os.makedirs(directory, exist_ok=True)
    payload = {
        "task_id": task_id,
        "trace_seed": trace_seed,
        "save_vars": save_vars,
        "checkpoints": checkpoints,
        "category": category,
        "group": group,
        "schema_version": SCHEMA_VERSION,
    }
    with open(_path(task_id, directory), "w") as f:
        json.dump(payload, f, indent=2)


def load_annotation(task_id, directory=DEFAULT_DIR):
    """Return the annotation dict, or None if it does not exist.

    Legacy files may lack `category` (defaulted to selectable) or `group`
    (defaulted to None); both are filled in so callers always see them."""
    path = _path(task_id, directory)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    data.setdefault("category", DEFAULT_CATEGORY)
    data.setdefault("group", None)
    return data
