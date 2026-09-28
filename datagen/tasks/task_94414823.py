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


def generate(colors=None, flip=None, xpose=None, quadrant_size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
    quadrant_size: The side length of each box-interior quadrant.
  """

  if colors is None:
    colors = common.random_colors(2, exclude=[5])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    if quadrant_size is None:
      quadrant_size = common.randint(1, 3)
  quadrant_size = 2 if quadrant_size is None else quadrant_size

  # Input: a centered gray box with two corner markers above it, the left
  # marker in colors[0] and the right marker in colors[1]. The box interior is
  # empty and consists of four equal square quadrants for the solver to fill.
  grid = common.grid(10, 10)
  for i in range(4 - quadrant_size, 6 + quadrant_size):
    grid[4 - quadrant_size][i] = 5
    grid[5 + quadrant_size][i] = 5
    grid[i][4 - quadrant_size] = 5
    grid[i][5 + quadrant_size] = 5
  grid[3 - quadrant_size][3 - quadrant_size] = colors[0]
  grid[3 - quadrant_size][6 + quadrant_size] = colors[1]
  output = common.deepcopy(grid)

  def fill_diagonal_quadrants(color, cells):
    """Paints the two interior quadrants lying on one marker's diagonal."""
    for r, c in cells:
      output[r][c] = color

  # Each corner marker's color spreads into the two box-interior quadrants on
  # its diagonal: the left marker (colors[0]) fills the top-left and
  # bottom-right quadrants, the right marker (colors[1]) fills the other two.
  fill_diagonal_quadrants(
      colors[0],
      [(r, c) for r in range(5 - quadrant_size, 5)
       for c in range(5 - quadrant_size, 5)] +
      [(r, c) for r in range(5, 5 + quadrant_size)
       for c in range(5, 5 + quadrant_size)])
  fill_diagonal_quadrants(
      colors[1],
      [(r, c) for r in range(5 - quadrant_size, 5)
       for c in range(5, 5 + quadrant_size)] +
      [(r, c) for r in range(5, 5 + quadrant_size)
       for c in range(5 - quadrant_size, 5)])
  if flip:
    grid, output = common.flip(grid), common.flip(output)
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 7], flip=True, xpose=True),
      generate(colors=[4, 8], flip=False, xpose=False),
      generate(colors=[3, 2], flip=False, xpose=True),
  ]
  test = [
      generate(colors=[9, 1], flip=True, xpose=False),
  ]
  return {"train": train, "test": test}
