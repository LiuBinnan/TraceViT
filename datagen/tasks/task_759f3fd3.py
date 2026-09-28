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


def generate(size=None, row=None, col=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    row: The row of the T.
    col: The column of the T.
    height: The height of the grid. Defaults to size.
    width: The width of the grid. Defaults to size.
  """

  if size is None or height is None or width is None or row is None or col is None:
    if size is None:
      size = common.randint(10, 26)
    height = size if height is None else height
    width = size if width is None else width
    row = common.randint(2, height - 3) if row is None else row
    col = common.randint(2, width - 3) if col is None else col

  grid, output = common.grids(width, height)
  for i in range(max(height, width)):
    if i < width:
      grid[row][i] = 3
    if i < height:
      grid[i][col] = 3

  for r in range(height):
    for c in range(width):
      if max(abs(row - r), abs(col - c)) % 2 == 0:
        output[r][c] = 4

  for i in range(max(height, width)):
    if i < width:
      output[row][i] = 3
    if i < height:
      output[i][col] = 3
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, row=4, col=6),
      generate(size=20, row=5, col=7),
  ]
  test = [
      generate(size=12, row=8, col=6),
  ]
  return {"train": train, "test": test}
