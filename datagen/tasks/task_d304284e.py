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


def generate(tall=None, colors=None, brow=None, bcol=None, wide=3, width=28,
             height=23):
  """Returns input and output grids according to the given parameters.

  Args:
    tall: The height of the box.
    colors: The colors of the box.
    brow: The row of the box.
    bcol: The column of the box.
    wide: The width of the box.
    width: The width of the grid.
    height: The height of the grid.
  """

  if tall is None:
    tall = common.randint(3, 5)
    brow, bcol = common.randint(2, 8), common.randint(2, 8)
    width = common.randint(20, 30)
    height = common.randint(15, 26)
    while True:
      rows, cols = common.conway_sprite(wide, tall, common.randint(1, 8))
      if common.diagonally_connected(list(zip(rows, cols))): break
    colors = [0] * (wide * tall)
    for row, col in zip(rows, cols):
      colors[row * wide + col] = 1

  grid, output = common.grids(width, height)

  # Draw the single source sprite into the input grid (input logic unchanged).
  for j, color in enumerate(colors):
    if color:
      common.draw(grid, brow + j // 3, bcol + j % 3, common.orange())

  # Bookkeeping (no randomness, no output writes -> produces no frame):
  # enumerate the rightward copies and flag every third one, which is
  # recolored and later cascades downward.
  copies = []
  i = 0
  while True:
    col = bcol + (wide + 1) * i
    if col >= width: break
    hue = common.pink() if i % 3 == 2 else common.orange()
    copies.append((col, hue, i % 3 == 2))
    i += 1
  cascades = [(col, hue) for col, hue, grows in copies if grows]

  def tile_horizontally():
    """Replicates the sprite rightward across the top band (7,7,6 cycle)."""
    for col, hue, _ in copies:
      for j, color in enumerate(colors):
        if color:
          common.draw(output, brow + j // 3, col + j % 3, hue)

  def cascade_column(idx):
    """Rains the idx-th recolored copy straight down to the bottom edge."""
    if idx >= len(cascades): return
    col, hue = cascades[idx]
    row = brow
    while True:
      if row > height: break
      for j, color in enumerate(colors):
        if color:
          common.draw(output, row + j // 3, col + j % 3, hue)
      row += tall + 1

  tile_horizontally()
  cascade_column(0)
  cascade_column(1)
  for i in range(2, len(cascades)):
    cascade_column(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tall=3, colors=[1, 1, 1, 1, 0, 1, 1, 1, 1], brow=5, bcol=3),
      generate(tall=5, colors=[1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
               brow=4, bcol=5),
  ]
  test = [
      generate(tall=5, colors=[0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
               brow=7, bcol=2),
  ]
  return {"train": train, "test": test}
