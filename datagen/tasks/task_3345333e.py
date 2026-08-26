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


def generate(rows=None, cols=None, srow=None, scol=None, brow=None, bcol=None,
             wide=None, tall=None, colors=None, off=None, flip=None, size=16,
             height=None, width=None, count=None, shape_height=None,
             shape_width=None, box_height=None, box_width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    srow: the row where the sprite is placed
    scol: the column where the sprite is placed
    brow: the row where the box is placed
    bcol: the column where the box is placed
    wide: the width of the box
    tall: the height of the box
    colors: a list of two colors, one for the sprite and one for the box
    off: an offset to make the sprite length odd or even
    flip: whether to flip the sprite horizontally
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: the number of cells in the half-creature before mirroring
    shape_height: the sampling height of the half-creature
    shape_width: the sampling width of the half-creature
    box_height: the occluding box height
    box_width: the occluding box width
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    max_shape_height = max(4, height - 2)
    max_shape_width = max(4, (width - 2) // 2)
    if shape_height is None:
      shape_height = common.randint(4, max_shape_height)
    if shape_width is None:
      shape_width = common.randint(4, max_shape_width)
    shape_height = min(max(4, shape_height), max_shape_height)
    shape_width = min(max(4, shape_width), max_shape_width)
    max_count = max(1, (shape_height * shape_width * 2) // 3)
    min_count = max(5, min(shape_height, shape_width))
    if count is None:
      count = common.randint(min_count, max_count)
    count = min(max(min_count, count), max_count)
    while True:
      pixels = common.continuous_creature(count, shape_width, shape_height)
      if max(r for r, _ in pixels) >= 2 and max(c for _, c in pixels) >= 2:
        break
    rows, cols = zip(*pixels)
    off, flip = common.randint(0, 2), common.randint(0, 1)
    shape_tall = max(rows) + 1
    shape_wide = max(cols) + 1
    if box_height is None:
      box_height = common.randint(2, max(2, shape_tall - 1))
    if box_width is None:
      box_width = common.randint(2, max(2, shape_wide))
    tall = min(max(2, box_height), max(2, shape_tall - 1))
    wide = min(max(2, box_width), max(2, shape_wide))
    srow = common.randint(1, height - shape_tall - 1)
    min_scol = shape_wide - 1 + off
    max_scol = min(width - shape_wide, width - wide - 1 + off)
    scol = common.randint(min_scol, max_scol)
    min_brow = max(0, srow - 1)
    max_brow = min(height - tall, srow + shape_tall - tall + 1)
    brow = common.randint(min_brow, max_brow)
    min_bcol = scol + 1 - off
    max_bcol = min(width - wide, scol + shape_wide)
    bcol = common.randint(min_bcol, max_bcol)
    colors = common.random_colors(2)

  def final_col(c):
    return width - 1 - c if flip else c

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[srow + r][final_col(scol - c - off)] = colors[0]
    grid[srow + r][final_col(scol + c)] = colors[0]
  for r in range(brow, brow + tall):
    for c in range(bcol, bcol + wide):
      grid[r][final_col(c)] = colors[1]
  output = common.deepcopy(grid)
  for r in range(brow, brow + tall):
    for c in range(bcol, bcol + wide):
      output[r][final_col(c)] = common.black()
  for r, c in zip(rows, cols):
    output[srow + r][final_col(scol - c - off)] = colors[0]
    output[srow + r][final_col(scol + c)] = colors[0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8],
               cols=[1, 2, 1, 2, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
               srow=2, scol=6, brow=3, bcol=6, wide=4, tall=3, colors=[6, 1],
               off=1, flip=0),
      generate(rows=[0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5, 5, 5, 6, 6, 6, 7, 7],
               cols=[1, 0, 1, 2, 0, 1, 2, 3, 0, 2, 2, 0, 1, 2, 0, 2, 3, 2, 3],
               srow=3, scol=11, brow=4, bcol=12, wide=4, tall=4, colors=[2, 3],
               off=1, flip=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 6, 6, 6,
                     7],
               cols=[2, 0, 1, 3, 3, 4, 0, 1, 2, 3, 4, 0, 0, 1, 2, 3, 4, 0, 2, 3,
                     2],
               srow=5, scol=6, brow=6, bcol=8, wide=4, tall=5, colors=[5, 8],
               off=0, flip=1),
  ]
  return {"train": train, "test": test}
