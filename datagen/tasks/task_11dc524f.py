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


def generate(wide=None, tall=None, brow=None, bcol=None, angle=None,
             colors=None, size=13):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the box.
    tall: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
    angle: The angle of the box.
    colors: The colors of the box.
    size: The height and width of the grids.
  """

  if size is None:
    size = common.randint(11, 22)

  mirror_row, mirror_col = size // 2, size // 3
  if wide is None:
    angle = common.randint(0, 3)
    if angle == 0:
      wide = common.randint(2, 4)
      tall = common.randint(2, min(3, size - mirror_row - 4))
    if angle == 1:
      wide = common.randint(2, min(3, mirror_col - 1))
      tall = common.randint(2, 4)
    if angle == 2:
      wide = common.randint(2, 4)
      tall = common.randint(2, min(4, mirror_row - 2))
    if angle == 3:
      wide = common.randint(2, min(5, size - mirror_col - 4))
      tall = common.randint(2, 4)
    pixels = common.diagonally_connected_sprite(
        wide, tall, common.randint(1, wide * tall))
    colors = []
    for r in range(tall):
      for c in range(wide):
        colors.append(1 if (r, c) in pixels else 0)
    brow = common.randint(mirror_row + 2 - tall, mirror_row)
    bcol = common.randint(mirror_col + 2 - wide, mirror_col)
    if angle == 0: brow = common.randint(mirror_row + 4, size - tall)
    if angle == 1: bcol = common.randint(0, mirror_col - 1 - wide)
    if angle == 2: brow = common.randint(0, mirror_row - 2 - tall)
    if angle == 3: bcol = common.randint(mirror_col + 4, size - wide)

  grid = common.grid(size, size, common.orange())
  common.rect(grid, 2, 2, mirror_row, mirror_col, common.gray())
  for r in range(tall):
    for c in range(wide):
      if not colors[r * wide + c]: continue
      grid[brow + r][bcol + c] = common.red()
  if angle == 0: brow = mirror_row + 2
  if angle == 1: bcol = mirror_col - wide
  if angle == 2: brow = mirror_row - tall
  if angle == 3: bcol = mirror_col + 2
  output = common.grid(size, size, common.orange())

  def place_shifted_shape():
    """Moves the red shape next to the gray square."""
    for r in range(tall):
      for c in range(wide):
        if not colors[r * wide + c]: continue
        output[brow + r][bcol + c] = common.red()

  place_shifted_shape()

  def add_reflected_shape():
    """Adds the gray reflection through the square."""
    for r in range(tall):
      for c in range(wide):
        if not colors[r * wide + c]: continue
        row, col = brow + r, bcol + c
        if angle == 0: row = mirror_row + 1 - r
        if angle == 1: col = mirror_col - 1 + wide - c
        if angle == 2: row = mirror_row - 1 + tall - r
        if angle == 3: col = mirror_col + 1 - c
        output[row][col] = common.gray()

  add_reflected_shape()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=2, tall=3, brow=5, bcol=0, angle=1,
               colors=[1, 0, 0, 1, 1, 1]),
      generate(wide=2, tall=3, brow=1, bcol=4, angle=2,
               colors=[1, 0, 1, 0, 1, 1]),
      generate(wide=3, tall=3, brow=10, bcol=3, angle=0,
               colors=[0, 1, 1, 0, 1, 0, 1, 0, 0]),
  ]
  test = [
      generate(wide=2, tall=3, brow=5, bcol=9, angle=3,
               colors=[0, 1, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
