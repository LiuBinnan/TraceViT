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


def generate(size=None, rows=None, cols=None, rowoff=None, coloff=None,
             color=None, legcolor=None, flip_horiz=None, flip_vert=None,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    rowoff: a vertical offset for the body
    coloff: a horizontal offset for the body
    color: a digit representing a color to be used for the body
    legcolor: a digit representing a color to be used for the legs
    flip_horiz: whether to flip the body horizontally
    flip_vert: whether to flip the body vertically
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if height is None:
      height = common.randint(12, 15)
    if width is None:
      width = common.randint(12, 15)
    # Cap sprite dims at their original max (5, from size<=15) so conway_sprite's
    # cell count stays solvable; the min(h,w)//2-2 bound preserves range validity.
    spritew = common.randint(4, min(5, min(height, width) // 2 - 2))
    spriteh = common.randint(4, min(5, min(height, width) // 2 - 2))
    while True:
      rows, cols = common.conway_sprite(spritew, spriteh, spritew * spriteh)
      if common.diagonally_connected(list(zip(rows, cols))): break
    rowoff = common.randint(spriteh, height - spriteh - 4)
    coloff = common.randint(spritew, width - spritew - 4)
    color = common.random_color()
    legcolor = common.random_color(exclude=[color])
    flip_horiz, flip_vert = common.randint(0, 1), common.randint(0, 1)

  body = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
  body_pixels = {(rowoff + dr, coloff + dc) for dr, dc in body}
  base_grid = common.grid(width, height)
  base_output = common.grid(width, height)

  def orient(ingrid):
    outgrid = common.deepcopy(ingrid)
    if flip_horiz:
      outgrid = common.flip_horiz(outgrid)
    if flip_vert:
      outgrid = outgrid[::-1]
    return outgrid

  def paint_body(ingrid):
    for dr, dc in body:
      ingrid[rowoff + dr][coloff + dc] = color

  def paint_leg(ingrid, row_sign, col_sign):
    for r, c in zip(rows, cols):
      rr = rowoff - r if row_sign < 0 else rowoff + 2 + r
      cc = coloff - c if col_sign < 0 else coloff + 2 + c
      if (rr, cc) in body_pixels: continue
      ingrid[rr][cc] = legcolor

  paint_body(base_grid)
  paint_body(base_output)
  output = orient(base_output)
  paint_leg(base_grid, -1, -1)
  paint_leg(base_output, -1, -1)
  output = orient(base_output)
  paint_leg(base_output, -1, 1)
  output = orient(base_output)
  paint_leg(base_output, 1, -1)
  output = orient(base_output)
  paint_leg(base_output, 1, 1)
  output = orient(base_output)
  grid = orient(base_grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=14, rows=[0, 1, 1, 2, 2, 3, 3, 3, 4, 4],
               cols=[3, 1, 2, 0, 1, 0, 2, 3, 0, 3], rowoff=7, coloff=6, color=4,
               legcolor=2, flip_horiz=0, flip_vert=0),
      generate(size=14, rows=[1, 1, 1, 2, 2, 2, 3],
               cols=[0, 1, 2, 1, 2, 3, 2], rowoff=6, coloff=7, color=3,
               legcolor=8, flip_horiz=1, flip_vert=0),
      generate(size=12, rows=[1, 1, 2, 2, 3], cols=[1, 2, 1, 3, 2], rowoff=3,
               coloff=4, color=8, legcolor=1, flip_horiz=0, flip_vert=1),
  ]
  test = [
      generate(size=15, rows=[0, 1, 1, 1, 2, 3, 3, 4, 5],
               cols=[2, 0, 1, 3, 1, 1, 2, 0, 0], rowoff=6, coloff=7, color=7,
               legcolor=4, flip_horiz=1, flip_vert=1),
  ]
  return {"train": train, "test": test}
