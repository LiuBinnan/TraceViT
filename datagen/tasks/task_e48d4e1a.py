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


def generate(row=None, col=None, color=None, offset=None, size=10,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the axis center
    col: a horizontal coordinate for the axis center
    color: a digit representing a color to be used
    offset: the amount to shift the axis
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if row is None:
    row, col = common.randint(1, height - 2), common.randint(1, width - 2)
    color = common.random_color(exclude=[common.gray()])
    offset = common.randint(1, 3)
    offset = min(offset, height - row - 1)
    offset = min(offset, row)
    offset = min(offset, col)

  grid, output = common.grids(width, height)
  for c in range(width):
    grid[row][c] = color
    output[row + offset][c] = color
  for r in range(height):
    grid[r][col] = color
    output[r][col - offset] = color
  for r in range(offset):
    grid[r][width - 1] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=6, col=3, color=2, offset=2),
      generate(row=3, col=3, color=4, offset=3),
      generate(row=4, col=6, color=6, offset=3),
      generate(row=2, col=4, color=3, offset=1),
  ]
  test = [
      generate(row=3, col=5, color=8, offset=2),
  ]
  return {"train": train, "test": test}
