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


def generate(depth=None, mid=None, shown=None, flip=None, gravity=None,
             size=12, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    depth: how many cells deep the wall is
    mid: the horizontal placement of the rebounding point
    shown: how many cells in the diagonal are shown
    flip: whether we should flip the grid so the diagonal starts from the right
    gravity: which side of the grid the wall adheres to (0: top, 1: left, ...)
    size: the width and height of the (square) grid (square fallback)
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  gh, gw = height, width
  if depth is None:
    gravity = common.randint(0, 3)
    # gravity %2 transposes the logical frame, so the logical row/col extents
    # depend on whether the frame is swapped onto the physical grid.
    lr = gw if gravity % 2 else gh
    lc = gh if gravity % 2 else gw
    depth = common.randint(1, min(lr // 2 - 1, (lc - 2) // 2))
    mid = common.randint(depth, lc - depth - 2)
    shown = common.randint(2, 3)
    flip = common.randint(0, 1)

  # Logical row/col extents in the (possibly transposed) construction frame.
  lr = gw if gravity % 2 else gh
  lc = gh if gravity % 2 else gw

  def coords(r, c):
    if flip: c = lc - 1 - c
    if gravity >= 2: r = lr - 1 - r
    if gravity % 2: r, c = c, r
    return r, c

  grid = common.grid(gw, gh)
  for r in range(lr):
    for c in range(lc):
      rr, cc = coords(r, c)
      grid[rr][cc] = common.red() if r < depth else common.black()
  incident, reflected = [], []
  for c in range(lc):
    r = depth + (mid - c if c < mid else c - mid)
    if r >= lr: continue  # bounced ray has left the (rectangular) grid
    rr, cc = coords(r, c)
    if c < shown:
      grid[rr][cc] = common.cyan()
    elif c <= mid:
      incident.append((rr, cc))
    else:
      reflected.append((rr, cc))
  output = [row[:] for row in grid]
  for r, c in incident:
    output[r][c] = common.green()
  for r, c in reflected:
    output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(depth=2, mid=7, shown=2, flip=1, gravity=3),
      generate(depth=3, mid=6, shown=3, flip=0, gravity=2),
      generate(depth=2, mid=6, shown=3, flip=1, gravity=1),
  ]
  test = [
      generate(depth=4, mid=4, shown=2, flip=0, gravity=3),
  ]
  return {"train": train, "test": test}
