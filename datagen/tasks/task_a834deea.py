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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the box pixels.
  """

  if size is None:
    size = common.randint(6, 28)
    # Box-count ladder: one more 5x5 box roughly every +2 grid cells. The formula
    # reproduces the original mapping exactly for size 6-16 (1,1,1,1,1,2,2,3,3,4,4)
    # and extends it upward. Capped at 7 so the non-overlap rejection loop below
    # stays feasible at the widest sizes (empirically < ~1s worst-case placement).
    num_boxes = min(7, max(1, (size - 7) // 2))
    while True:
      rows = [common.randint(0, size - 5) for _ in range(num_boxes)]
      cols = [common.randint(0, size - 5) for _ in range(num_boxes)]
      lengths = [5 for _ in range(num_boxes)]
      if not common.overlaps(rows, cols, lengths, lengths, 1): break
    colors = []
    for _ in range(num_boxes):
      while True:
        vals = [common.randint(0, 1) for _ in range(9)]
        if sum(vals) not in [0, 9]: break  # need at least one dot, but not all.
      colors.extend(vals)

  grid = common.grid(size, size, 8)
  for row, col in zip(rows, cols):
    common.rect(grid, 5, 5, row, col, 0)
  for group in range(len(rows)):
    for r in range(3):
      for c in range(3):
        row = rows[group] + r + 1
        col = cols[group] + c + 1
        grid[row][col] = 8 * colors[group * 9 + r * 3 + c]

  order = [1, 7, 6, 4, 0, 5, 2, 9, 3]
  output = common.deepcopy(grid)

  def fill_key_row(kr):
    """Stamps key-row kr of the fixed 3x3 positional key into every box hole."""
    nonlocal output
    for group in range(len(rows)):
      for c in range(3):
        if colors[group * 9 + kr * 3 + c] == 0:
          row = rows[group] + kr + 1
          col = cols[group] + c + 1
          output[row][col] = order[kr * 3 + c]

  fill_key_row(0)
  fill_key_row(1)
  fill_key_row(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, rows=[1, 7], cols=[1, 4],
               colors=[1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
      generate(size=9, rows=[2], cols=[2], colors=[1, 0, 1, 0, 0, 0, 1, 0, 1]),
      generate(size=13, rows=[0, 6, 7], cols=[8, 7, 0],
               colors=[0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1]),
  ]
  test = [
      generate(size=16, rows=[0, 5, 7, 11], cols=[11, 5, 11, 1],
               colors=[1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
