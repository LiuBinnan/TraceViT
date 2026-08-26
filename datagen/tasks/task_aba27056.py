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


def generate(size=None, wide=None, tall=None, col=None, row=None, color=None,
             flip=None, xpose=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    wide: the width of the colorful box
    tall: the height of the colorful box
    col: the leftmost column of the colorful box
    row: the lower offset of the colorful box
    color: a digit representing a color to be used
    flip: whether to flip the grids
    xpose: whether to transpose the grids
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if size is None:
    size = common.randint(5, 10)
    height = common.randint(5, 10) if height is None else height
    width = common.randint(5, 10) if width is None else width
    wide, tall = common.randint(5, width), common.randint(3, height - 2)
    row, col = common.randint(0, 1), common.randint(0, width - wide)
    color = common.random_color()
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
  if height is None: height = size
  if width is None: width = size
  # Logical grid extent: gh = row-axis (height), gw = col-axis (width).
  gh, gw = height, width

  def coords(r, c):
    if flip: r = gh - 1 - r
    if xpose: r, c = c, r
    return r, c

  def draw_pixel(target, r, c, value):
    r, c = coords(r, c)
    common.draw(target, r, c, value)

  # When transposed, the physical grid's axes swap: logical rows (gh) become
  # physical columns and logical cols (gw) become physical rows.
  phys_w, phys_h = (gh, gw) if xpose else (gw, gh)
  grid, output = common.grids(phys_w, phys_h)
  # Draw the colorful box.
  for r in range(gh - tall, gh):
    for c in range(col, col + wide):
      draw_pixel(output, r - row, c, color)
      draw_pixel(grid, r - row, c, color)
  for r in range(gh - tall + 1, gh - 1):
    for c in range(col + 1, col + wide - 1):
      draw_pixel(output, r - row, c, common.black())
      draw_pixel(grid, r - row, c, common.black())
  for c in range(col + 2, col + wide - 2):
    draw_pixel(output, gh - tall - row, c, common.black())
    draw_pixel(grid, gh - tall - row, c, common.black())
  # Draw the yellow fountain.
  for r in range(gh - tall + 1, gh - 1):
    for c in range(col + 1, col + wide - 1):
      draw_pixel(output, r - row, c, common.yellow())
  for r in range(0, gh - 1 - row):
    for c in range(col + 2, col + wide - 2):
      draw_pixel(output, r, c, common.yellow())
  for r in range(0, gh - tall):
    diff = gh - tall - r
    draw_pixel(output, r - row, col + 2 - diff, common.yellow())
    draw_pixel(output, r - row, col - 3 + diff + wide, common.yellow())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, wide=5, tall=3, col=1, row=0, color=6, flip=0, xpose=0),
      generate(size=9, wide=7, tall=5, col=2, row=0, color=7, flip=0, xpose=1),
      generate(size=6, wide=6, tall=4, col=0, row=0, color=3, flip=1, xpose=0),
  ]
  test = [
      generate(size=10, wide=9, tall=4, col=0, row=1, color=2, flip=1, xpose=1),
  ]
  return {"train": train, "test": test}
