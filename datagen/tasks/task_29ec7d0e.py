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


def generate(mod=None, rows=None, cols=None, wides=None, talls=None, size=18,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    mod: how much to mod the row * col products
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    wides: a list of cutout widths
    talls: a list of cutout heights
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if mod is None:
    mod = common.randint(4, 9)
    wides = [common.randint(2, 4) for _ in range(5)]
    talls = [common.randint(2, 4) for _ in range(5)]
    rows = [common.randint(0, height - tall) for tall in talls]
    cols = [common.randint(0, width - wide) for wide in wides]

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      grid[r][c] = output[r][c] = (r * c) % mod + 1
  pattern = [row[:] for row in output]
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.black()
  output = [row[:] for row in grid]
  def fill_hole(idx):
    for r in range(rows[idx], rows[idx] + talls[idx]):
      for c in range(cols[idx], cols[idx] + wides[idx]):
        output[r][c] = pattern[r][c]

  fill_hole(0)
  fill_hole(1)
  fill_hole(2)
  fill_hole(3)
  fill_hole(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(mod=5, rows=[0, 2, 4, 5, 10], cols=[3, 10, 6, 11, 0],
               wides=[2, 2, 2, 3, 4], talls=[3, 2, 2, 2, 3]),
      generate(mod=6, rows=[0, 4, 5, 11, 11], cols=[7, 11, 3, 7, 12],
               wides=[3, 3, 4, 3, 4], talls=[4, 2, 3, 3, 3]),
      generate(mod=7, rows=[2, 3, 3, 5, 6], cols=[12, 6, 10, 1, 13],
               wides=[4, 4, 2, 2, 3], talls=[4, 4, 2, 4, 2]),
      generate(mod=8, rows=[3, 8, 8, 13, 15], cols=[14, 3, 4, 6, 4],
               wides=[2, 2, 4, 2, 2], talls=[3, 2, 3, 2, 2]),
  ]
  test = [
      generate(mod=9, rows=[0, 5, 5, 6, 13], cols=[13, 3, 13, 9, 1],
               wides=[3, 3, 3, 4, 3], talls=[3, 4, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
