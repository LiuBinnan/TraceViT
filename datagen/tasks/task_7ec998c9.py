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


def generate(size=None, row=None, col=None, bgcolor=None, fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    row: The row of the pixel.
    col: The column of the pixel.
    bgcolor: The background color of the grid.
    fgcolor: The foreground color of the grid.
  """

  if size is None:
    size = common.randint(5, 16)
    bgcolor = common.random_color(exclude=[1])
    fgcolor = common.random_color(exclude=[1, bgcolor])
    while True:
      row, col = common.randint(1, size - 2), common.randint(1, size - 2)
      if row == col: continue
      if size % 2 == 1 and col * 2 + 1 == size:
        row = col
      break

  # Input: a plain background field with a single foreground marker pixel.
  grid = common.grid(size, size, bgcolor)
  grid[row][col] = fgcolor

  # Output is solved forward on top of the marked input.
  output = common.deepcopy(grid)

  def draw_column():
    """Shoots a blue axis line up and down through the marker's column."""
    for r in range(size):
      if r != row:
        output[r][col] = common.blue()

  def draw_top_arm():
    """Draws the blue arm that runs along the top edge to the axis."""
    for c in range(size):
      r = 0 if c < col else size - 1
      if row == col: r = size - 1 - r
      if r == 0:
        output[0][c] = common.blue()

  def draw_bottom_arm():
    """Draws the blue arm that runs along the bottom edge from the axis."""
    for c in range(size):
      r = 0 if c < col else size - 1
      if row == col: r = size - 1 - r
      if r == size - 1:
        output[size - 1][c] = common.blue()

  draw_column()
  draw_top_arm()
  draw_bottom_arm()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, row=3, col=2, bgcolor=4, fgcolor=9),
      generate(size=5, row=2, col=2, bgcolor=7, fgcolor=8),
      generate(size=7, row=3, col=4, bgcolor=2, fgcolor=4),
  ]
  test = [
      generate(size=7, row=3, col=3, bgcolor=5, fgcolor=6),
  ]
  return {"train": train, "test": test}
