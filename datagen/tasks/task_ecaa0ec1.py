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


def generate(width=None, height=None, brow=None, bcol=None, angle=None,
             flip=None, flop=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brow: The row of the brow of the input grid.
    bcol: The column of the brow of the input grid.
    angle: The angle of rotation of the input grid.
    flip: Whether to flip the input grid horizontally.
    flop: Whether to flop the input grid vertically.
    colors: The colors to use for the input and output grids.
  """

  if width is None:
    width, height = common.randint(10, 18), common.randint(10, 18)
    marker_bound = min(height, width) - 4
    brow, bcol = common.randint(2, marker_bound), common.randint(2, marker_bound)
    angle = common.randint(1, 3)
    flip, flop = common.randint(0, 1), common.randint(0, 1)
    while True:
      colors = [1 if common.randint(0, 1) else 8 for _ in range(9)]
      if colors.count(1) >= 3 and colors.count(1) <= 6: break

  # Input: the 3x3 color block plus the yellow orientation markers whose layout
  # encodes how far the block should be turned. Build it first, logic unchanged.
  grid, output = common.grids(width, height)
  grid[brow - 2][bcol - 2] = grid[brow - 2][bcol] = grid[brow][bcol - 2] = 4
  if angle == 1: grid[brow - 1][bcol + 3] = 4
  if angle == 2: grid[brow + 3][bcol + 3] = 4
  if angle == 3: grid[brow + 3][bcol - 1] = 4
  for i, color in enumerate(colors):
    grid[brow + i // 3][bcol + i % 3] = color
  if flip: grid = common.flip(grid)
  if flop: grid = common.flop(grid)

  # Bookkeeping (no randomness, no frames): the block after each quarter turn.
  def rotate_once(cells):
    turned = []
    for col in range(2, -1, -1):
      for row in range(3):
        turned.append(cells[3 * row + col])
    return turned

  orientations = [colors]
  for _ in range(3):
    orientations.append(rotate_once(orientations[-1]))

  # Every output write goes through put(), which places the cell directly in the
  # final (flipped/flopped) orientation so each frame is built in output space.
  def put(row, col, value):
    if flip: row = height - 1 - row
    if flop: col = width - 1 - col
    output[row][col] = value

  def place_block(cells):
    for i, color in enumerate(cells):
      put(brow + i // 3, bcol + i % 3, color)

  # Stage 0: copy the block onto the answer canvas in its starting orientation.
  def show_block():
    place_block(orientations[0])

  # Stage k: turn the block another quarter; on the last turn stamp the corner.
  def rotate_block(turns):
    if turns > angle: return
    place_block(orientations[turns])
    if turns == angle:
      put(brow - 1, bcol - 1, common.yellow())

  show_block()
  rotate_block(1)
  rotate_block(2)
  rotate_block(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=11, brow=5, bcol=3, angle=3, flip=1, flop=0,
               colors=[1, 1, 1, 1, 8, 8, 8, 1, 8]),
      generate(width=10, height=10, brow=3, bcol=3, angle=1, flip=0, flop=0,
               colors=[1, 1, 1, 8, 1, 8, 8, 1, 1]),
      generate(width=11, height=11, brow=4, bcol=4, angle=3, flip=1, flop=1,
               colors=[1, 8, 1, 8, 8, 8, 1, 1, 1]),
      generate(width=10, height=12, brow=5, bcol=4, angle=2, flip=0, flop=0,
               colors=[8, 1, 8, 8, 1, 8, 1, 1, 8]),
  ]
  test = [
      generate(width=11, height=11, brow=4, bcol=4, angle=2, flip=0, flop=1,
               colors=[1, 1, 1, 8, 8, 1, 1, 8, 1]),
  ]
  return {"train": train, "test": test}
