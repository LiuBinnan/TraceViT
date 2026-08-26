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


def generate(rows=None, cols=None, corners=None, size=7, height=None, width=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    corners: a list of digits specifying which corners are missing
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    count: the target number of three-cell corner shapes to place
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    bitmap = common.grid(width, height)
    def has_neighbor(r, c):
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if r + dr < 0 or r + dr >= height or c + dc < 0 or c + dc >= width:
            continue
          if bitmap[r + dr][c + dc] > 0: return True
      return False
    rows, cols, corners = [], [], []
    if count is None:
      count = common.randint(1, max(1, (height * width) // 6))
    placed, trials, max_trials = 0, 0, count * 2
    while placed < count and trials < max_trials:
      trials += 1
      row, col = common.randint(0, height - 2), common.randint(0, width - 2)
      corner = common.randint(0, 3)
      if corner != 0 and has_neighbor(row, col):
        continue
      if corner != 1 and has_neighbor(row, col + 1):
        continue
      if corner != 2 and has_neighbor(row + 1, col):
        continue
      if corner != 3 and has_neighbor(row + 1, col + 1):
        continue
      rows.append(row)
      cols.append(col)
      corners.append(corner)
      bitmap[row][col] = 0 if corner == 0 else 1
      bitmap[row][col + 1] = 0 if corner == 1 else 1
      bitmap[row + 1][col] = 0 if corner == 2 else 1
      bitmap[row + 1][col + 1] = 0 if corner == 3 else 1
      placed += 1

  grid, output = common.grids(width, height)
  for r, c, corner in zip(rows, cols, corners):
    grid[r][c] = 0 if corner == 0 else common.cyan()
    grid[r][c + 1] = 0 if corner == 1 else common.cyan()
    grid[r + 1][c] = 0 if corner == 2 else common.cyan()
    grid[r + 1][c + 1] = 0 if corner == 3 else common.cyan()
  output = [row[:] for row in grid]

  def fill_corners(pair_idx):
    base = len(rows) // 5
    extra = len(rows) % 5
    start = pair_idx * base + min(pair_idx, extra)
    stop = start + base + (1 if pair_idx < extra else 0)
    if start >= stop:
      return
    for idx in range(start, stop):
      r, c, corner = rows[idx], cols[idx], corners[idx]
      if corner == 0: output[r][c] = common.blue()
      if corner == 1: output[r][c + 1] = common.blue()
      if corner == 2: output[r + 1][c] = common.blue()
      if corner == 3: output[r + 1][c + 1] = common.blue()

  fill_corners(0)
  fill_corners(1)
  fill_corners(2)
  fill_corners(3)
  fill_corners(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3], cols=[1, 4], corners=[1, 2]),
      generate(rows=[0, 2, 5], cols=[4, 2, 3], corners=[2, 1, 0]),
  ]
  test = [
      generate(rows=[0, 1, 3, 5], cols=[5, 0, 3, 0], corners=[2, 3, 1, 0]),
  ]
  return {"train": train, "test": test}
