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


def generate(rows=None, cols=None, size=15, height=None, width=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: number of 5x5 boxes to attempt to place
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    if count is None:
      count = common.randint(1, max(1, (height * width) // 16))
    rows, cols = [], []
    blocked = set()
    tries = 0
    max_tries = 20 * count
    while len(rows) < count and tries < max_tries:
      tries += 1
      if height < 5 or width < 5:
        break
      row = common.randint(2, height - 3)
      col = common.randint(2, width - 3)
      frame = set()
      for i in range(5):
        frame.add((row - 2, col - 2 + i))
        frame.add((row + 2, col - 2 + i))
        frame.add((row - 2 + i, col - 2))
        frame.add((row - 2 + i, col + 2))
      if frame & blocked:
        continue
      rows.append(row)
      cols.append(col)
      for r in range(row - 2, row + 3):
        for c in range(col - 2, col + 3):
          blocked.add((r, c))

  grid, output = common.grids(width, height, common.cyan())
  for r, c in zip(rows, cols):
    for i in range(width):
      output[r][i] = common.pink()
    for i in range(height):
      output[i][c] = common.pink()
  for r, c in zip(rows, cols):
    for i in range(5):
      output[r - 2][c - 2 + i] = grid[r - 2][c - 2 + i] = common.blue()
      output[r + 2][c - 2 + i] = grid[r + 2][c - 2 + i] = common.blue()
      output[r - 2 + i][c - 2] = grid[r - 2 + i][c - 2] = common.blue()
      output[r - 2 + i][c + 2] = grid[r - 2 + i][c + 2] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3], cols=[5]),
      generate(rows=[5, 11], cols=[5, 10]),
  ]
  test = [
      generate(rows=[3, 11], cols=[8, 5]),
  ]
  return {"train": train, "test": test}
