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


def generate(width=None, height=None, rows=None, cols=None, bgcolor=None,
             color=None, rdiff=None, cdiff=None, brow=None, bcol=None,
             prow=None, pcol=None, flip=None, xpose=None, length=None,
             cell_count=None, step=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    bgcolor: a digit representing the background color
    color: a digit representing the foreground color
    rdiff: the row delta to add for each iteration of the sprite
    cdiff: the column delta to add for each iteration of the sprite
    brow: the vertical coordinate of the origin sprite
    bcol: the horizontal coordinate of the origin sprite
    prow: the vertical coordinate of the pixel hint
    pcol: the horizontal coordinate of the pixel hint
    flip: whether to flip the sprite
    xpose: whether to transpose the sprite
  """
  if width is None:
    width = common.randint(9, 30)
  if height is None:
    height = common.randint(9, 30)
  max_length = max(3, min(width, height) // 2 - 1)
  if length is None:
    length = common.randint(3, max_length)
  length = min(length, max_length)
  if rows is None or cols is None:
    cells = []
    for row in range(length // 2, length):
      for col in range(length // 2, length):
        cells.append((row, col))
    max_count = max(2, len(cells) - 1)
    if cell_count is None:
      half = max(1, len(cells) // 2)
      ncd = common.randint(1, half)
      cell_count = common.choice([ncd, len(cells) - ncd])
    cell_count = min(max(2, cell_count), max_count)
    cells = common.sample(cells, cell_count)
    cells.append((0, 0))
    pixels = set()
    for row, col in cells:
      pixels.add((row, col))
      pixels.add((row, length - col - 1))
      pixels.add((length - row - 1, col))
      pixels.add((length - row - 1, length - col - 1))
    rows, cols = [], []
    for row, col in sorted(pixels):
      rows.append(row)
      cols.append(col)
  if brow is None:
    brow = common.randint(length, height // 2)
  if bcol is None:
    bcol = common.randint(length, width // 2)
  if step is None:
    step = length
  if rdiff is None:
    rdiff = step
  if cdiff is None:
    cdiff = step
  if prow is None:
    prow = brow + rdiff
  if pcol is None:
    pcol = bcol + cdiff
  if color is None:
    color = common.random_color()
  if bgcolor is None:
    bgcolor = common.random_color(exclude=[color])
  if flip is None:
    flip = common.randint(0, 1)
  if xpose is None:
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height, bgcolor)
  for row, col in zip(rows, cols):
    grid[brow + row][bcol + col] = common.black()
    output[brow + row][bcol + col] = common.black()
  grid[prow][pcol] = color
  for _ in range(width + height):
    brow, bcol = brow + rdiff, bcol + cdiff
    for row, col in zip(rows, cols):
      common.draw(output, brow + row, bcol + col, color)
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, rows=[0, 1, 1, 2], cols=[1, 0, 2, 1],
               bgcolor=8, color=2, rdiff=2, cdiff=2, brow=3, bcol=3, prow=5,
               pcol=6, flip=0, xpose=0),
      generate(width=15, height=13, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1],
               bgcolor=1, color=3, rdiff=2, cdiff=-2, brow=5, bcol=5, prow=7,
               pcol=4, flip=0, xpose=0),
      generate(width=16, height=12,
               rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 4],
               cols=[0, 1, 3, 4, 0, 1, 3, 4, 2, 0, 1, 3, 4, 0, 1, 3, 4],
               bgcolor=4, color=8, rdiff=-5, cdiff=5, brow=5, bcol=6, prow=4,
               pcol=11, flip=0, xpose=0),
  ]
  test = [
      generate(width=16, height=18, rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               bgcolor=3, color=6, rdiff=-3, cdiff=-3, brow=6, bcol=4, prow=5,
               pcol=3, flip=0, xpose=0),
  ]
  return {"train": train, "test": test}
