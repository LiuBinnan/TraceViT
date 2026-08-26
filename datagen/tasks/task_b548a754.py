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


def generate(width=None, height=None, row=None, col=None, wide=None, tall=None,
             dotrow=None, dotcol=None, inner=None, outer=None, xpose=None,
             flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    row: a vertical coordinate where the box starts
    col: a horizontal coordinate where the box starts
    wide: the width of the box
    tall: the height of the box
    dotrow: the vertical coordinate of the dot
    dotcol: the horizontal coordinate of the dot
    inner: the color of the inner box
    outer: the color of the outer box
    xpose: whether to transpose the grid
    flip: whether to flip the grid
  """
  if any(value is None for value in [
      width, height, row, col, wide, tall, dotrow, dotcol, inner, outer,
      xpose, flip]):
    if width is None:
      width = common.randint(4, 30)
    if height is None:
      height = common.randint(5, 30)
    full_tall = None if dotrow is None or row is None else dotrow - row + 1
    if wide is None:
      wide = common.randint(3, width - 1)
    if full_tall is None:
      full_tall = common.randint(4, height - 1)
    if row is None:
      row = common.randint(0, height - full_tall)
    else:
      full_tall = min(full_tall, height - row)
    if col is None:
      col = common.randint(0, width - wide)
    if tall is None:
      tall = common.randint(3, full_tall - 1)
    if dotrow is None:
      dotrow = row + full_tall - 1
    if dotcol is None:
      dotcol = col + common.randint(0, wide - 1)
    if inner is None or outer is None:
      colors = common.random_colors(2, exclude=[common.cyan()])
      inner = colors[0] if inner is None else inner
      outer = colors[1] if outer is None else outer
    if xpose is None:
      xpose = common.randint(0, 1)
    if flip is None:
      flip = common.randint(0, 1)

  final_width, final_height = (height, width) if xpose else (width, height)
  grid, output = common.grids(final_width, final_height)

  def coords(r, c):
    if xpose:
      r, c = c, r
    if flip:
      r = final_height - 1 - r
    return r, c

  def set_cell(bitmap, r, c, color):
    r, c = coords(r, c)
    bitmap[r][c] = color

  for r in range(row, row + tall):
    for c in range(col, col + wide):
      set_cell(grid, r, c, outer)
  for r in range(row + 1, row + tall - 1):
    for c in range(col + 1, col + wide - 1):
      set_cell(grid, r, c, inner)
  set_cell(grid, dotrow, dotcol, common.cyan())

  def extend_outer():
    for r in range(row, dotrow + 1):
      for c in range(col, col + wide):
        set_cell(output, r, c, outer)

  def extend_inner():
    for r in range(row + 1, dotrow):
      for c in range(col + 1, col + wide - 1):
        set_cell(output, r, c, inner)

  extend_outer()
  extend_inner()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11, row=1, col=1, wide=4, tall=4, dotrow=8,
               dotcol=3, inner=1, outer=2, xpose=0, flip=0),
      generate(width=11, height=11, row=1, col=1, wide=4, tall=5, dotrow=10,
               dotcol=2, inner=2, outer=3, xpose=1, flip=0),
      generate(width=13, height=12, row=2, col=1, wide=5, tall=3, dotrow=10,
               dotcol=5, inner=6, outer=1, xpose=1, flip=0),
  ]
  test = [
      generate(width=13, height=13, row=0, col=3, wide=5, tall=4, dotrow=11,
               dotcol=4, inner=4, outer=6, xpose=0, flip=1),
  ]
  return {"train": train, "test": test}
