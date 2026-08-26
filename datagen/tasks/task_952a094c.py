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


def generate(brow=None, bcol=None, wide=None, tall=None, colors=None,
             bcolor=None, size=10, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brow: a list of vertical coordinates where the box should be placed
    bcol: a list of horizontal coordinates where the box should be placed
    wide: a width of the box
    tall: a height of the box
    colors: a list of colors to be used for the pixels
    bcolor: the color of the box
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if brow is None:
    wide, tall = common.randint(4, 6), common.randint(4, 6)
    brow = common.randint(1, height - tall - 1)
    bcol = common.randint(1, width - wide - 1)
    bcolor = common.random_color()
    colors = common.random_colors(4, exclude=[bcolor])

  grid, output = common.grids(width, height)
  for r in range(brow, brow + tall):
    for c in range(bcol, bcol + wide):
      output[r][c] = grid[r][c] = bcolor
  for r in range(brow + 1, brow + tall - 1):
    for c in range(bcol + 1, bcol + wide - 1):
      output[r][c] = grid[r][c] = common.black()
  grid[brow + 1][bcol + 1] = colors[0]
  grid[brow + 1][bcol + wide - 2] = colors[1]
  grid[brow + tall - 2][bcol + 1] = colors[2]
  grid[brow + tall - 2][bcol + wide - 2] = colors[3]
  output = [row[:] for row in grid]
  moves = [
      (brow + 1, bcol + 1, brow + tall, bcol + wide, colors[0]),
      (brow + 1, bcol + wide - 2, brow + tall, bcol - 1, colors[1]),
      (brow + tall - 2, bcol + 1, brow - 1, bcol + wide, colors[2]),
      (brow + tall - 2, bcol + wide - 2, brow - 1, bcol - 1, colors[3]),
  ]

  def move_corner(corner_idx):
    if corner_idx >= len(moves):
      return
    sr, sc, tr, tc, color = moves[corner_idx]
    output[sr][sc] = common.black()
    output[tr][tc] = color

  move_corner(0)
  move_corner(1)
  move_corner(2)
  move_corner(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brow=2, bcol=3, wide=4, tall=5, colors=[4, 3, 2, 6], bcolor=8),
      generate(brow=2, bcol=2, wide=6, tall=6, colors=[2, 8, 9, 3], bcolor=7),
      generate(brow=1, bcol=1, wide=6, tall=5, colors=[2, 5, 6, 3], bcolor=1),
  ]
  test = [
      generate(brow=3, bcol=2, wide=6, tall=5, colors=[6, 4, 8, 2], bcolor=3),
  ]
  return {"train": train, "test": test}
