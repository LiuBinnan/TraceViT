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

import common


def generate(vals=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: A list of integers.
    gsize: The width and height of the square canvas.
  """

  if vals is None:
    if gsize is None:
      gsize = common.randint(9, 16)
    while True:
      vals = [common.randint(0, 1)
              for _ in range(common.randint(7, gsize))]
      num_up_steps = vals.count(0)
      if (num_up_steps <= gsize - 1 and
          (num_up_steps < gsize - 1 or vals[-1] == 0)):
        break
  elif gsize is None:
    gsize = 10

  grid, output = common.grids(gsize, gsize)
  row, col = gsize - 1, gsize - len(vals)
  grid[row][col] = 2
  block_row, block_col = row, col
  for val in vals:
    if val == 0:
      block_row -= 1
    else:
      grid[block_row - 1][block_col] = 1
    block_col += 1

  def draw_segment(row, col, segment):
    for val in segment:
      output[row][col] = 2
      if val == 0:
        row -= 1
        output[row][col] = 2
      else:
        output[row - 1][col] = 1
      col += 1
    return row, col

  midpoint = len(vals) // 2
  row, col = draw_segment(row, col, vals[:midpoint])
  row, col = draw_segment(row, col, vals[midpoint:])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[0, 0, 1, 0, 0, 0, 0, 0, 0]),
      generate(vals=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(vals=[0, 1, 0, 0, 1, 1, 0, 0, 0, 0]),
      generate(vals=[0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(vals=[0, 0, 1, 1, 0, 0, 1, 0, 0]),
  ]
  return {"train": train, "test": test}
