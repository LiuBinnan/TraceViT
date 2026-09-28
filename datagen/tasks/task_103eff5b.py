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


def generate(width=None, height=None, size=None, scale=None, brow=None,
             bcol=None, srow=None, scol=None, rotate=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    size: The size of the sprite.
    scale: The scale of the sprite.
    brow: The row of the box.
    bcol: The column of the box.
    srow: The row of the sprite.
    scol: The column of the sprite.
    rotate: Whether to rotate the grids.
    colors: The colors of the sprite.
  """

  if width is None:
    if size is None:
      size = common.randint(2, 4)
    if scale is None:
      scale = common.randint(2, min(4, 12 // size))
    length = size * scale
    width = length + common.randint(3, 5)
    height = 12 + length + common.randint(0, 4)
    brow, bcol = common.randint(1, 3), common.randint(1, width - size - 2)
    srow = common.randint(10, height - 1 - length)
    scol = common.randint(1, width - 1 - length)
    pixels = common.diagonally_connected_sprite(size, size)
    colors = []
    for r in range(size):
      for c in range(size):
        colors.append(common.choice([1, 2, 3, 4]) if (r, c) in pixels else 0)
    rotate = common.randint(0, 3)

  grid = common.grid(width, height)
  for row in range(size):
    for col in range(size):
      color = colors[row * size + col]
      if not color: continue
      grid[brow + row][bcol + col] = color
      for r in range(scale):
        for c in range(scale):
          rr, cc = srow + col * scale + r, scol + (size - 1 - row) * scale + c
          grid[rr][cc] = common.cyan()
  for _ in range(rotate):
    grid = common.flip(grid)
    grid = common.transpose(grid)
  output = common.deepcopy(grid)

  def rotated_cell(row, col):
    """Maps an unrotated cell into the displayed input orientation."""
    h, w = height, width
    for _ in range(rotate):
      row, col, h, w = col, h - 1 - row, w, h
    return row, col

  def fill_sprite_row(row):
    """Colors the enlarged gray blocks that correspond to one sprite row."""
    if row >= size: return
    for col in range(size):
      color = colors[row * size + col]
      if not color: continue
      for r in range(scale):
        for c in range(scale):
          rr = srow + col * scale + r
          cc = scol + (size - 1 - row) * scale + c
          rr, cc = rotated_cell(rr, cc)
          output[rr][cc] = color

  fill_sprite_row(0)
  fill_sprite_row(1)
  fill_sprite_row(2)
  fill_sprite_row(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=22, size=3, scale=3, brow=3, bcol=3, srow=10,
               scol=1, rotate=0, colors=[0, 3, 1, 4, 3, 0, 2, 0, 4]),
      generate(width=13, height=24, size=4, scale=2, brow=1, bcol=2, srow=12,
               scol=2, rotate=0,
               colors=[0, 0, 3, 0, 2, 0, 3, 4, 2, 1, 1, 0, 2, 0, 0, 4]),
  ]
  test = [
      generate(width=16, height=26, size=3, scale=4, brow=2, bcol=6, srow=12,
               scol=3, rotate=1, colors=[0, 2, 2, 4, 4, 0, 0, 0, 3]),
  ]
  return {"train": train, "test": test}
