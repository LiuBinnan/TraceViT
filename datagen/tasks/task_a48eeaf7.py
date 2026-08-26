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


def generate(rows=None, cols=None, boxrow=None, boxcol=None, size=10,
             height=None, width=None, boxheight=None, boxwidth=None,
             count=None, corner_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxrow: the row of the box
    boxcol: the column of the box
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    boxheight: the height of the box
    boxwidth: the width of the box
    count: the number of side pixels to place
    corner_count: the number of diagonal corner pixels to place
  """
  if height is None: height = size
  if width is None: width = size
  if boxheight is None: boxheight = 2
  if boxwidth is None: boxwidth = 2
  if rows is None:
    boxheight = min(max(2, boxheight), max(2, height // 2))
    boxwidth = min(max(2, boxwidth), max(2, width // 2))
    boxrow = common.randint(2, height - boxheight - 2)
    boxcol = common.randint(2, width - boxwidth - 2)

    sources = []
    for r in range(boxrow, boxrow + boxheight):
      sources.append((r, common.randint(0, boxcol - 2)))
      sources.append((r, common.randint(boxcol + boxwidth + 1, width - 1)))
    for c in range(boxcol, boxcol + boxwidth):
      sources.append((common.randint(0, boxrow - 2), c))
      sources.append((common.randint(boxrow + boxheight + 1, height - 1), c))
    if count is None: count = common.randint(1, len(sources))
    count = min(max(1, count), len(sources))
    rows, cols = [], []
    for idx in common.sample(range(len(sources)), count):
      rows.append(sources[idx][0])
      cols.append(sources[idx][1])

    corners = [
        (boxrow - 1, boxcol - 1, -1, -1),
        (boxrow - 1, boxcol + boxwidth, -1, 1),
        (boxrow + boxheight, boxcol - 1, 1, -1),
        (boxrow + boxheight, boxcol + boxwidth, 1, 1),
    ]
    if corner_count is None: corner_count = common.randint(0, len(corners))
    corner_count = min(max(0, corner_count), len(corners))
    for r, c, dr, dc in common.sample(corners, corner_count):
      max_len = max(height, width)
      if dr < 0: max_len = min(max_len, r)
      if dr > 0: max_len = min(max_len, height - r - 1)
      if dc < 0: max_len = min(max_len, c)
      if dc > 0: max_len = min(max_len, width - c - 1)
      length = common.randint(1, max_len)
      rows.append(r + dr * length)
      cols.append(c + dc * length)

  grid, output = common.grids(width, height)
  for dr in range(boxheight):
    for dc in range(boxwidth):
      grid[boxrow + dr][boxcol + dc] = common.red()
      output[boxrow + dr][boxcol + dc] = common.red()
  for r, c in zip(rows, cols):
    grid[r][c] = common.gray()
    out_r = r
    out_r = out_r if out_r >= boxrow else boxrow - 1
    out_r = out_r if out_r < boxrow + boxheight else boxrow + boxheight
    out_c = c
    out_c = out_c if out_c >= boxcol else boxcol - 1
    out_c = out_c if out_c < boxcol + boxwidth else boxcol + boxwidth
    output[out_r][out_c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 3, 7], cols=[3, 8, 7], boxrow=3, boxcol=3),
      generate(rows=[0, 3, 6, 8], cols=[8, 1, 9, 5], boxrow=2, boxcol=5),
  ]
  test = [
      generate(rows=[0, 1, 6, 9], cols=[2, 8, 7, 2], boxrow=6, boxcol=2),
  ]
  return {"train": train, "test": test}
