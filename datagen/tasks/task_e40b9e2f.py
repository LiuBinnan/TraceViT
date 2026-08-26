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


def generate(row=None, col=None, rows=None, cols=None, idxs=None, colors=None,
             bump=None, size=10, height=None, width=None, length=None,
             count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical offset for the pinwheel
    col: a horizontal offset for the pinwheel
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the quadrant list (-1 for all quadrants)
    colors: a list of colors to be used
    bump: whether to bump the pinwheel
    size: the width and height of the (square) input grid
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
    length: the radius of the sampled pinwheel quadrant
    count: the number of non-core tail cells sampled
    num_colors: the number of foreground colors to use
  """
  if height is None: height = size
  if width is None: width = size
  if row is None:
    max_length = max(2, min(height, width) // 2)
    if length is None:
      length = common.randint(2, max_length)
    length = min(length, max_length)
    bump = length == 2
    row = common.randint(length + bump, height - length - bump)
    col = common.randint(length + bump, width - length - bump)
    all_cells, core_cells = [], []
    for c in range(length):
      for r in range(c + 1):
        all_cells.append((r, c))
        if (length == 2 and r < 1 and c < 1) or (
            length > 2 and r < 2 and c < 2):
          core_cells.append((r, c))
    tail_cells = [cell for cell in all_cells if cell not in core_cells]
    if count is None:
      count = common.randint(1, len(tail_cells))
    count = min(count, len(tail_cells))
    cells = core_cells + common.sample(tail_cells, count)
    rows, cols, idxs = [], [], []
    for r, c in cells:
      rows.append(r)
      cols.append(c)
      idxs.append(-1 if (r, c) in core_cells else common.randint(0, 3))
    if num_colors is None:
      num_colors = common.randint(1, 9)
    color_list = common.random_colors(num_colors)
    colors = common.shuffle(
        [color_list[idx % num_colors] for idx in range(len(idxs))])

  def coords(r, c, quadrant):
    if quadrant == 0:
      return row + r + bump, col + c
    if quadrant == 1:
      return row - c, col + r
    if quadrant == 2:
      return row + c + bump, col - r - bump
    return row - r, col - c - bump

  def rotate(r, c, turns):
    for _ in range(turns):
      r, c = row + col - c, r - row + col - bump
    return r, c

  grid = common.grid(width, height)
  for r, c, idx, color in zip(rows, cols, idxs, colors):
    for quadrant in range(4):
      if idx not in [-1, quadrant]: continue
      rr, cc = coords(r, c, quadrant)
      grid[rr][cc] = color
  output = [list(row) for row in grid]
  base_pixels = [
      (r, c, grid[r][c])
      for r in range(height) for c in range(width) if grid[r][c]
  ]
  for r, c, color in base_pixels:
    rr, cc = rotate(r, c, 1)
    output[rr][cc] = color
  for r, c, color in base_pixels:
    rr, cc = rotate(r, c, 2)
    output[rr][cc] = color
  for r, c, color in base_pixels:
    rr, cc = rotate(r, c, 3)
    output[rr][cc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=4, rows=[0, 0, 0, 1, 2], cols=[0, 1, 2, 1, 2],
               idxs=[-1, -1, 1, -1, 0], colors=[4, 7, 7, 4, 4], bump=0),
      generate(row=4, col=3, rows=[0, 1, 1], cols=[0, 0, 1],
               idxs=[-1, 0, 3], colors=[6, 6, 3], bump=1),
      generate(row=4, col=4, rows=[0, 0, 1, 2], cols=[0, 1, 1, 2],
               idxs=[-1, -1, -1, 1], colors=[8, 8, 8, 9], bump=0),
  ]
  test = [
      generate(row=4, col=4,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 3],
               cols=[0, 1, 0, 1, 2, 3, 0, 1, 1],
               idxs=[-1, -1, -1, -1, 3, 3, 3, 2, 2],
               colors=[3, 2, 2, 3, 3, 3, 2, 3, 3], bump=0),
  ]
  return {"train": train, "test": test}
