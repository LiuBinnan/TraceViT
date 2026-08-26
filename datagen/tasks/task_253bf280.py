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


def generate(width=None, height=None, rows=None, cols=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    count: the number of foreground pixels to sample
  """
  if width is None:
    width = common.randint(3, 30)
  if height is None:
    height = common.randint(3, 30)
  if not isinstance(rows, list) or not isinstance(cols, list):
    max_count = max(1, (width * height) // 4)
    if count is None:
      count = common.randint(1, max_count)
    count = min(max(1, count), max_count)
    pixels = common.sample(common.all_pixels(width, height), count)
    rows = [r for r, _ in pixels]
    cols = [c for _, c in pixels]

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.cyan()
  horizontal_pairs, vertical_pairs = [], []
  for j in range(len(rows)):
    for i in range(j):
      if rows[i] == rows[j]:
        horizontal_pairs.append((i, j))
  for j in range(len(rows)):
    for i in range(j):
      if cols[i] == cols[j]:
        vertical_pairs.append((i, j))

  for i, j in horizontal_pairs:
    min_col, max_col = min(cols[i], cols[j]), max(cols[i], cols[j])
    for c in range(min_col + 1, max_col):
      output[rows[i]][c] = common.green()

  for i, j in vertical_pairs:
    min_row, max_row = min(rows[i], rows[j]), max(rows[i], rows[j])
    for r in range(min_row + 1, max_row):
      output[r][cols[i]] = common.green()

  for r, c in zip(rows, cols):
    output[r][c] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=7, rows=[3, 3], cols=[2, 9]),
      generate(width=11, height=10, rows=[1, 2, 6, 7], cols=[4, 8, 8, 4]),
      generate(width=11, height=12, rows=[1, 1, 8, 8], cols=[1, 9, 2, 7]),
      generate(width=6, height=9, rows=[1, 7], cols=[2, 2]),
      generate(width=3, height=3, rows=[1], cols=[1]),
      generate(width=6, height=5, rows=[1, 3], cols=[1, 4]),
      generate(width=6, height=7, rows=[1, 3, 6], cols=[3, 1, 3]),
      generate(width=11, height=12,
               rows=[1, 4, 4, 5, 9], cols=[3, 6, 10, 1, 3]),
  ]
  test = [
      generate(width=13, height=12, rows=[1, 1, 5, 5, 7, 9, 10],
               cols=[2, 10, 6, 12, 1, 8, 1]),
  ]
  return {"train": train, "test": test}
