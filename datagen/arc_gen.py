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

"""A command-line interface for ARC-GEN."""

import json
import os
import random
import sys
import task_list
from steps import batch, dataset, variations

# Reference JSON for validate: ARC-AGI-1 training tasks first, then ARC-AGI-2.
ARC_AGI_DATA_DIRS = ["external/ARC-AGI/data/training/",
                     "external/ARC-AGI-2/data/training/"]
BASE_SEED = 2025


def _flag_value(argv, flag):
  if flag not in argv:
    return None
  index = argv.index(flag)
  if index + 1 >= len(argv):
    raise ValueError(flag + " requires a value")
  return argv[index + 1]


def _json_flag(argv, flag, default):
  value = _flag_value(argv, flag)
  if value is None:
    return default
  return json.loads(value)


def _int_flag(argv, flag, default):
  value = _flag_value(argv, flag)
  return default if value is None else int(value)


def _float_flag(argv, flag, default):
  value = _flag_value(argv, flag)
  return default if value is None else float(value)


def _tasks_from_file(path):
  """Read newline-separated task ids from a file (blank lines ignored)."""
  with open(path) as f:
    return [line.strip() for line in f if line.strip()]


def synthesize_dataset_cmd(argv):
  """Drive the full dataset synthesis from CLI flags."""
  out = _flag_value(argv, "--out")
  if out is None:
    raise ValueError("synthesize requires --out <dir>")
  tasks_file = _flag_value(argv, "--tasks-file")
  task_ids = _tasks_from_file(tasks_file) if tasks_file else None
  dataset.synthesize_dataset(
      out,
      total=_int_flag(argv, "--total", 200000),
      seed_base=_int_flag(argv, "--seed-base", BASE_SEED),
      steps_weight=_float_flag(argv, "--steps-weight", 2.16),
      procs=_int_flag(argv, "--procs", None),
      attempt_timeout=_float_flag(argv, "--attempt-timeout", 5.0),
      task_budget=_float_flag(argv, "--task-budget", 90.0),
      colors_pool=_flag_value(argv, "--colors-pool") or "none",
      size_mode=_flag_value(argv, "--size-mode") or "legacy",
      task_ids=task_ids,
      redistribute_shortfall=("--no-redistribute" not in argv))
  if "--no-shards" not in argv:
    dataset.export_shards(
        out, shard_size=_int_flag(argv, "--shard-size", 10000))


def _variation_args(argv):
  generator_kwargs = variations.normalize_kwargs(_json_flag(argv, "--kwargs", {}))
  colors = variations.normalize_colors(_json_flag(argv, "--colors", None))
  return generator_kwargs, colors


def reference_path(task_id):
  """The task's reference JSON, searched in ARC_AGI_DATA_DIRS order."""
  for directory in ARC_AGI_DATA_DIRS:
    path = directory + task_id + ".json"
    if os.path.exists(path): return path
  return None


def validate_generators():
  """Validates all generators against their expected outputs."""
  passing, failing, missing = 0, [], []
  for task_id, task_info in task_list.task_list().items():
    _, validator = task_info
    path = reference_path(task_id)
    if path is None:
      missing.append(task_id)
      continue
    actual_result = validator()
    with open(path, "r") as f:
      expected_result = json.load(f)
      if "name" in expected_result: del expected_result["name"]
      if actual_result == expected_result:
        passing += 1
      else:
        failing.append(task_id)
  print("A total of " + str(passing) + " generators passed.")
  print("A total of " + str(len(failing)) + " generators failed.")
  if failing: print("Failing generators: " + str(failing))
  if missing:
    print("No reference JSON for " + str(len(missing)) + " generators (run "
          "`git submodule update --init`): " + str(missing))


def generate_benchmarks(task_id, num_examples, base_seed=BASE_SEED,
                        generator_kwargs=None, colors=None):
  """Creates a benchmark suite for a given task."""
  generator_kwargs = variations.normalize_kwargs(generator_kwargs)
  task_info = task_list.task_list()[task_id]
  generator, _ = task_info
  examples = []
  previous_colors = variations.push_colors(colors)
  try:
    for example_id in range(num_examples):
      random.seed(base_seed + example_id)
      examples.append(generator(**generator_kwargs))
  finally:
    variations.pop_colors(previous_colors)
  print(examples)


def generate_steps(task_id, num_examples, base_seed=BASE_SEED,
                   generator_kwargs=None, colors=None):
  """Print examples enriched with intermediate steps as JSON."""
  print(json.dumps(batch.generate_with_steps(
      task_id, num_examples, base_seed=base_seed,
      generator_kwargs=generator_kwargs, colors=colors)))


def main(argv) -> None:
  if argv[1] == "generate":
    kwargs, colors = _variation_args(argv)
    generate_benchmarks(argv[2], int(argv[3]),
                        base_seed=_int_flag(argv, "--base-seed", BASE_SEED),
                        generator_kwargs=kwargs, colors=colors)
  if argv[1] == "validate": validate_generators()
  if argv[1] == "steps":
    kwargs, colors = _variation_args(argv)
    generate_steps(argv[2], int(argv[3]),
                   base_seed=_int_flag(argv, "--base-seed", BASE_SEED),
                   generator_kwargs=kwargs, colors=colors)
  if argv[1] == "synthesize": synthesize_dataset_cmd(argv)


if __name__ == "__main__":
  main(sys.argv)
