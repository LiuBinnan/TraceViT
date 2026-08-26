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


def generate(rows=None, cols=None, row=None, col=None, color=None, flip=None,
             xpose=None, size=10, minisize=3, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: the row where the grid should be placed
    col: the column where the grid should be placed
    color: a digit representing a color to be used
    flip: whether the grid should be flipped horizontally
    xpose: whether the grid should be flipped vertically
    size: the width and height of the (square) grid
    minisize: the width and height of the sprite
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    rows, cols = [], []
    while True:
      bitmap, unshown = common.grid(minisize, minisize, 0), 0
      queue = [(common.randint(0, 2), 0)]  # Start with some random row
      while queue:
        r, c = queue.pop()
        if r < 0 or r >= minisize or c < 0 or c >= minisize: continue
        if bitmap[r][c] == 1: continue
        bitmap[r][c] = 1
        if c > 0: unshown += 1
        for dr, dc in [(-1, 0), (0, 1), (1, 0)]:
          if common.randint(0, 1) == 0: continue
          queue.append((r + dr, c + dc))
      if unshown == 0: continue
      for r in range(minisize):
        for c in range(minisize):
          if bitmap[r][c] == 0: continue
          rows.append(r)
          cols.append(c)
      break
    row, col = common.randint(1, 6), common.randint(4, 6)
    color = common.random_color(exclude=[common.red(), common.green()])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    # A non-square grid has no symmetric diagonal, so a transpose would fuse the
    # two independent extents; keep the sprite placement orientation-stable there.
    if height != width: xpose = 0
    # Clamp the sprite anchor so the whole sprite fits the (possibly rectangular)
    # grid in whichever orientation it is drawn (row-extent uses minisize rows,
    # col-extent spans minisize columns on each side of col).
    maxrow, maxcol = (width, height) if xpose else (height, width)
    row = min(row, max(1, maxrow - minisize))
    lo, hi = minisize, maxcol - minisize
    col = lo if hi < lo else min(max(col, lo), hi)

  def coords(r, c):
    if flip: c = width - 1 - c
    if xpose: r, c = c, r
    return r, c

  def inb(rr, cc):
    return 0 <= rr < height and 0 <= cc < width

  grid = common.grid(width, height)
  output = common.grid(width, height)
  pattern = set()
  for r, c in zip(rows, cols):
    rr, cc = coords(row + r, col + c)
    if inb(rr, cc): grid[rr][cc] = color
    rr, cc = coords(row + r, col - c - 1)
    if inb(rr, cc): grid[rr][cc] = common.red() if c == 0 else common.black()
    for cc in [col + c, col - c - 1]:
      rr, cc = coords(row + r, cc)
      if inb(rr, cc):
        output[rr][cc] = color
        pattern.add((rr, cc))
  for r in range(height):
    for c in range(width):
      if (r, c) not in pattern:
        output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2], cols=[0, 0, 1, 2, 0], row=3, col=5,
               color=4, flip=1, xpose=0),
      generate(rows=[0, 1, 1, 1, 2], cols=[0, 0, 1, 2, 2], row=3, col=4,
               color=6, flip=0, xpose=1),
      generate(rows=[0, 1, 1], cols=[0, 0, 1], row=4, col=4,
               color=7, flip=0, xpose=0),
      generate(rows=[0, 1, 2, 2], cols=[1, 1, 0, 1], row=3, col=4,
               color=8, flip=1, xpose=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 0], row=3, col=4,
               color=1, flip=1, xpose=0),
  ]
  return {"train": train, "test": test}
