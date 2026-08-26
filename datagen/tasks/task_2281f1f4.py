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


def generate(rows=None, cols=None, size=10, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: number of rows (defaults to size, keeping square behavior)
    width: number of columns (defaults to size, keeping square behavior)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    rows = [item for item in range(1, height) if common.randint(0, 1) == 0]
    cols = [item for item in range(0, width - 1) if common.randint(0, 1) == 0]
    # Secondary-count guard: only 9 mark_column handlers are unrolled below, so
    # never expose more than 9 marked columns (a wide grid could overrun).
    cols = cols[:9]

  grid, output = common.grids(width, height)
  for c in cols:
    output[0][c] = grid[0][c] = common.gray()
  for r in rows:
    output[r][width - 1] = grid[r][width - 1] = common.gray()
  def mark_column(col_idx):
    if col_idx >= len(cols):
      return
    c = cols[col_idx]
    for r in rows:
      output[r][c] = common.red()

  mark_column(0)
  mark_column(1)
  mark_column(2)
  mark_column(3)
  mark_column(4)
  mark_column(5)
  mark_column(6)
  mark_column(7)
  mark_column(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 7], cols=[0, 3, 7]),
      generate(rows=[2, 4, 7], cols=[1, 3, 4, 7]),
      generate(rows=[2, 3, 6, 8], cols=[2, 3, 5, 7, 8]),
  ]
  test = [
      generate(rows=[2, 3, 5, 7, 9], cols=[0, 2, 3, 6, 8]),
  ]
  return {"train": train, "test": test}
