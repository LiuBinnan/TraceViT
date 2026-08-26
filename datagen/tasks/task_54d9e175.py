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


def generate(colors=None, cell_height=None, cell_width=None,
             cell_rows=None, cell_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    cell_height: pixel height of every cell (default 3)
    cell_width: pixel width of every cell (default 3)
    cell_rows: number of stacked cell rows
    cell_cols: number of cell columns (default 3)
  """
  if colors is None:
    if cell_height is None:
      cell_height = common.randint(2, 5)
    if cell_width is None:
      cell_width = common.randint(2, 5)
    if cell_rows is None:
      cell_rows = common.randint(1, 31 // (cell_height + 1))
    if cell_cols is None:
      cell_cols = common.randint(1 if cell_rows > 1 else 2, 31 // (cell_width + 1))
    cell_rows = min(cell_rows, 31 // (cell_height + 1))
    cell_cols = min(cell_cols, 31 // (cell_width + 1))
    pool = common.sample([1, 2, 3, 4], common.randint(1, 4))
    colors = [common.choice(pool) for _ in range(cell_rows * cell_cols)]
  else:
    cell_height = 3 if cell_height is None else cell_height
    cell_width = 3 if cell_width is None else cell_width
    cell_cols = 3 if cell_cols is None else cell_cols
    cell_rows = -(-len(colors) // cell_cols)

  width, height = (cell_width + 1) * cell_cols - 1, (cell_height + 1) * cell_rows - 1
  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(cell_width, width, cell_width + 1):
      output[r][c] = grid[r][c] = common.gray()
  for r in range(cell_height, height, cell_height + 1):
    for c in range(width):
      output[r][c] = grid[r][c] = common.gray()
  for idx, color in enumerate(colors):
    r, c = idx // cell_cols, idx % cell_cols
    pr, pc = (cell_height + 1) * r + cell_height // 2, (cell_width + 1) * c + cell_width // 2
    output[pr][pc] = grid[pr][pc] = color
  for idx, color in enumerate(colors):
    r, c = idx // cell_cols, idx % cell_cols
    pr, pc = (cell_height + 1) * r + cell_height // 2, (cell_width + 1) * c + cell_width // 2
    output[pr][pc] = color + 5
  for idx, color in enumerate(colors):
    r, c = idx // cell_cols, idx % cell_cols
    for dr in range(cell_height):
      for dc in range(cell_width):
        output[(cell_height + 1) * r + dr][(cell_width + 1) * c + dc] = color + 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 2, 1]),
      generate(colors=[2, 3, 1]),
      generate(colors=[3, 1, 4]),
      generate(colors=[4, 1, 2, 2, 3, 4]),
  ]
  test = [
      generate(colors=[2, 3, 4, 1, 1, 3]),
  ]
  return {"train": train, "test": test}
