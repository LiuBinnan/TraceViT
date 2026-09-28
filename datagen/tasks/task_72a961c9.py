# Copyright 2026 Google LLC
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

"""Generator."""

import common


def generate(height=None, row=None, vals=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: The height of the grid.
    row: The row of the line.
    vals: The values of the line.
  """

  if height is None:
    height = common.randint(9, 16)
    vals = []
    group_count = common.randint(2, 6)
    for group_index in range(group_count):
      if vals:
        vals.append(common.choice([2, 8]))
      groups_left = group_count - group_index - 1
      max_run = min(4, 28 - len(vals) - 2 * groups_left)
      for _ in range(common.randint(1, max_run)):
        vals.append(1)
    min_row = 4 if 2 in vals else 3
    row = common.randint(min_row, height - 2)

  grid, output = common.grids(len(vals), height)
  for i, val in enumerate(vals):
    output[row][i] = grid[row][i] = val

  def draw_stems():
    for i, val in enumerate(vals):
      if val == 8:
        output[row - 1][i] = 1
        output[row - 2][i] = 1
      if val == 2:
        output[row - 1][i] = 1
        output[row - 2][i] = 1
        output[row - 3][i] = 1

  def cap_eights():
    for i, val in enumerate(vals):
      if val == 8:
        output[row - 3][i] = 8

  def cap_twos():
    for i, val in enumerate(vals):
      if val == 2:
        output[row - 4][i] = 2

  draw_stems()
  cap_eights()
  cap_twos()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=9, row=3, vals=[1, 8, 1, 1, 1, 1]),
      generate(height=10, row=5, vals=[1, 1, 1, 2, 1, 1, 1]),
      generate(height=9, row=7, vals=[1, 8, 1, 1, 1, 8, 1, 2, 1]),
      generate(height=13, row=9, vals=[1, 1, 2, 1, 1, 1, 8, 1, 1, 1]),
  ]
  test = [
      generate(height=9, row=6, vals=[1, 2, 1, 8, 1, 1, 1, 8, 1, 2, 1]),
  ]
  return {"train": train, "test": test}
