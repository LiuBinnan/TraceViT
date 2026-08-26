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


def generate(rows=None, cols=None, thick=None, color=None, flip=None,
             xpose=None, size=14, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    thick: the thickness of the horizon
    color: the color of the pixels
    flip: whether to flip the grid vertically
    xpose: whether to transpose the grid
    size: the size of the grid
    height: the number of rows in the (display) grid
    width: the number of columns in the (display) grid
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    # Logical (pre-transpose) dimensions: lh is the falling axis, lw the
    # horizontal axis.  After an optional transpose the display grid is always
    # height x width.
    lh = width if xpose else height
    lw = height if xpose else width
    # The horizon sits at logical row 5 and is `thick` rows tall; keep it (and
    # at least one landing row below it) inside the falling axis.
    thick = common.randint(2, min(5, lh - 6))
    while True:
      pixels = common.random_pixels(lw, lh, 0.05)
      pixels = [p for p in pixels if p[0] < 5 or p[0] >= 5 + thick]
      if pixels: break
    rows, cols = zip(*pixels)
    color = common.random_color(exclude=[common.gray()])
  else:
    lh = lw = size

  def coords(r, c):
    if flip: r = lh - 1 - r
    if xpose: r, c = c, r
    return r, c

  grid, output = common.grids(width, height)
  for r in range(thick):
    for c in range(lw):
      rr, cc = coords(5 + r, c)
      output[rr][cc] = grid[rr][cc] = common.gray()
  logical = common.grid(lw, lh)
  for r in range(thick):
    for c in range(lw):
      logical[5 + r][c] = common.gray()
  landings = []
  for r, c in zip(rows, cols):
    rr, cc = coords(r, c)
    grid[rr][cc] = color
    dr = 1 if r < 5 else -1
    landing = 0 if r < 5 else lh - 1
    while logical[landing + dr][c] == common.black():
      landing += dr
    logical[landing][c] = common.gray()
    rr, cc = coords(landing, c)
    output[rr][cc] = color
    landings.append((rr, cc))
  for r, c in landings:
    output[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2, 3, 9, 10, 11, 12], cols=[8, 2, 10, 9, 1, 4, 11],
               thick=4, color=2, flip=0, xpose=0),
      generate(rows=[1, 1, 1, 2, 3, 3, 4, 10, 11, 12, 13],
               cols=[0, 6, 9, 2, 6, 12, 1, 2, 9, 7, 4],
               thick=5, color=3, flip=1, xpose=1),
      generate(rows=[2, 2, 3, 4, 8, 10, 10, 10, 12],
               cols=[3, 8, 11, 1, 8, 3, 7, 12, 7],
               thick=2, color=1, flip=1, xpose=0),
  ]
  test = [
      generate(rows=[1, 1, 2, 3, 3, 7, 9, 10, 11, 12],
               cols=[4, 11, 1, 3, 11, 6, 1, 11, 6, 13],
               thick=2, color=4, flip=0, xpose=1),
  ]
  return {"train": train, "test": test}
