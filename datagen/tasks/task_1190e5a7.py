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

"""Generator."""

import common


def generate(rows=None, cols=None, colors=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of row thicknesses
    cols: a list of column thicknesses
    colors: background followed by separator colors
    num_colors: the number of colors to use in random grids
  """
  if rows is None:
    row_count = common.randint(2, 11)
    col_count = common.randint(2, 11)
    remaining = 30 - row_count + 1
    rows = []
    for idx in range(row_count):
      left = row_count - idx - 1
      row = common.randint(1, remaining - left)
      rows.append(row)
      remaining -= row
    remaining = 30 - col_count + 1
    cols = []
    for idx in range(col_count):
      left = col_count - idx - 1
      col = common.randint(1, remaining - left)
      cols.append(col)
      remaining -= col
    max_colors = min(10, len(rows) + len(cols) - 1)
    if num_colors is None:
      num_colors = common.randint(2, max_colors)
    num_colors = min(num_colors, max_colors)
    colors = common.sample(list(range(10)), num_colors)

  separator_colors = colors[1:]
  if not separator_colors:
    separator_colors = [common.random_color(exclude=[colors[0]])]

  width = sum(cols) + len(cols) - 1
  height = sum(rows) + len(rows) - 1
  grid = common.grid(width, height, colors[0])
  output = common.grid(width, height, colors[0])
  r = -1
  color_idx = 0
  for row in rows:
    r += row + 1
    if r >= height: break
    color = separator_colors[color_idx % len(separator_colors)]
    color_idx += 1
    for c in range(width):
      output[r][c] = grid[r][c] = color
  c = -1
  for col in cols:
    c += col + 1
    if c >= width: break
    color = separator_colors[color_idx % len(separator_colors)]
    color_idx += 1
    for r in range(height):
      output[r][c] = grid[r][c] = color
  output = common.grid(2 * len(cols) - 1, 2 * len(rows) - 1, colors[0])
  for r in range(1, 2 * len(rows) - 1, 2):
    for c in range(2 * len(cols) - 1):
      output[r][c] = separator_colors[0]
  for c in range(1, 2 * len(cols) - 1, 2):
    for r in range(2 * len(rows) - 1):
      output[r][c] = separator_colors[0]
  output = common.grid(len(cols), len(rows), colors[0])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 12], cols=[1, 8, 2, 1], colors=[3, 7]),
      generate(rows=[3, 5, 1], cols=[4, 6], colors=[1, 8]),
      generate(rows=[2, 4, 8, 4, 1, 3], cols=[6, 14, 1, 1, 1], colors=[3, 1]),
  ]
  test = [
      generate(rows=[2, 4, 4, 4, 4], cols=[15, 4, 1], colors=[1, 5]),
  ]
  return {"train": train, "test": test}
