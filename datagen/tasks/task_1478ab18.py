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


def generate(length=None, brow=None, bcol=None, dogear=None, size=8):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the box.
    brow: The row of the box.
    bcol: The column of the box.
    dogear: The dogear of the box.
    size: The height and width of the square grid.
  """

  if length is None:
    length = common.randint(4, size)
    brow, bcol = (common.randint(0, size - length),
                  common.randint(0, size - length))
    dogear = common.randint(0, 3)

  grid, output = common.grids(size, size, 7)
  points = [[brow, bcol],
            [brow, bcol + length - 1],
            [brow + length - 1, bcol],
            [brow + length - 1, bcol + length - 1]]
  dr = 1 if dogear in [0, 1] else -1
  dc = 1 if dogear in [0, 2] else -1
  points[dogear][0] += dr
  points[dogear][1] += dc
  srow = brow if dogear in [0, 1] else (brow + length - 1)
  scol = bcol if dogear in [0, 2] else (bcol + length - 1)

  def is_corner_point(row, col):
    return [row, col] in points

  def mark_corner_points():
    """Copies the four given corner points into both grids."""
    for point in points:
      output[point[0]][point[1]] = grid[point[0]][point[1]] = 5

  def draw_vertical_side():
    """Draws the side column that touches the dog-eared corner."""
    for row in range(brow, brow + length):
      if not is_corner_point(row, scol):
        output[row][scol] = 8

  def draw_horizontal_side():
    """Draws the side row that touches the dog-eared corner."""
    for col in range(bcol, bcol + length):
      if not is_corner_point(srow, col):
        output[srow][col] = 8

  def draw_diagonal_side():
    """Draws the diagonal connecting the two opposite corners."""
    for i in range(length):
      r = brow + i
      c = (bcol + i) if dogear in [1, 2] else (bcol + length - 1 - i)
      if not is_corner_point(r, c):
        output[r][c] = 8

  mark_corner_points()
  draw_vertical_side()
  draw_horizontal_side()
  draw_diagonal_side()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=4, brow=0, bcol=0, dogear=2),
      generate(length=6, brow=1, bcol=1, dogear=3),
      generate(length=8, brow=0, bcol=0, dogear=0),
  ]
  test = [
      generate(length=7, brow=0, bcol=1, dogear=1),
  ]
  return {"train": train, "test": test}
