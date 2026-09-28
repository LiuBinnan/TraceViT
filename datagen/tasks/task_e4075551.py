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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  if width is None:
    width, height = common.randint(12, 28), common.randint(12, 28)
    wide, tall = (common.randint(7, min(width, height) - 3),
                  common.randint(7, min(width, height) - 3))
    row = common.randint(1, height - tall - 1)
    col = common.randint(1, width - wide - 1)
    rows = [row,
            row + common.randint(3, tall - 4),
            row + common.randint(3, tall - 4),
            row + common.randint(3, tall - 4),
            row + tall - 1]
    cols = [col + common.randint(3, wide - 4),
            col,
            col + common.randint(3, wide - 4),
            col + wide - 1,
            col + common.randint(3, wide - 4)]
    colors = common.random_colors(5, exclude=[2, 5])
    colors[2] = 2

  # The input shows five dots. The red dot in the middle projects a grey cross
  # (its horizontal and vertical axes); each of the four boundary dots extends
  # into one wall of a rectangle, in its own color. Rebuild the figure from a
  # blank canvas, one dot's projection per frame - the two side walls first,
  # then the top and bottom walls closing the corners over them.
  grid, output = common.grids(width, height)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color

  def project_grey_cross():
    """The red center dot shoots grey axes across the figure and marks itself."""
    for row in range(rows[0], rows[4] + 1):
      output[row][cols[2]] = common.gray()
    for col in range(cols[1], cols[3] + 1):
      output[rows[2]][col] = common.gray()
    output[rows[2]][cols[2]] = colors[2]

  def grow_left_wall():
    """The left dot extends up and down into the left wall."""
    for row in range(rows[0], rows[4] + 1):
      output[row][cols[1]] = colors[1]

  def grow_right_wall():
    """The right dot extends up and down into the right wall."""
    for row in range(rows[0], rows[4] + 1):
      output[row][cols[3]] = colors[3]

  def grow_top_wall():
    """The top dot spans across into the top wall, closing the corners."""
    for col in range(cols[1], cols[3] + 1):
      output[rows[0]][col] = colors[0]

  def grow_bottom_wall():
    """The bottom dot spans across into the bottom wall, closing the corners."""
    for col in range(cols[1], cols[3] + 1):
      output[rows[4]][col] = colors[4]

  project_grey_cross()
  grow_left_wall()
  grow_right_wall()
  grow_top_wall()
  grow_bottom_wall()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=15, rows=[2, 8, 8, 5, 12],
               cols=[6, 3, 7, 10, 6], colors=[4, 8, 2, 7, 6]),
      generate(width=15, height=14, rows=[1, 4, 7, 5, 11],
               cols=[5, 2, 5, 9, 3], colors=[8, 4, 2, 3, 6]),
      generate(width=15, height=15, rows=[3, 9, 6, 7, 13],
               cols=[4, 2, 6, 12, 5], colors=[3, 1, 2, 6, 9]),
  ]
  test = [
      generate(width=15, height=16, rows=[1, 9, 7, 7, 13],
               cols=[7, 2, 4, 11, 6], colors=[1, 7, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
