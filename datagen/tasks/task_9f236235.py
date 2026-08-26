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


def create_rect_linegrid(bitmap, cell_height, cell_width, linecolor):
  """Creates a line grid whose cells can be rectangular."""
  actual_height = len(bitmap) * (cell_height + 1) - 1
  actual_width = len(bitmap[0]) * (cell_width + 1) - 1
  ingrid = common.grid(actual_width, actual_height)
  for r in range(actual_height):
    for c in range(actual_width):
      if ((r + 1) % (cell_height + 1) == 0 or
          (c + 1) % (cell_width + 1) == 0):
        ingrid[r][c] = linecolor
  for r, row in enumerate(bitmap):
    for c, color in enumerate(row):
      for dr in range(cell_height):
        for dc in range(cell_width):
          ingrid[r * (cell_height + 1) + dr][
              c * (cell_width + 1) + dc] = color
  return ingrid


def generate(size=None, rows=None, cols=None, colors=None, magnifier=None,
             linecolor=None, height=None, width=None, num_colors=None,
             num_cells=None, cell_height=None, cell_width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    magnifier: the zoom ratio in the input grid
    linecolor: the color of the gridlines
    height: the number of rows of the bitmap grid (defaults to size)
    width: the number of columns of the bitmap grid (defaults to size)
    num_colors: the number of foreground colors sampled for random records
    num_cells: the number of bitmap cells sampled for random records
    cell_height: the height of each magnified bitmap cell
    cell_width: the width of each magnified bitmap cell
  """
  if rows is None:
    if height is None: height = common.randint(2, 14)
    if width is None: width = common.randint(2, 14)
    max_cell_height = max(1, 31 // height - 1)
    max_cell_width = max(1, 31 // width - 1)
    if cell_height is None:
      cell_height = common.randint(1, max_cell_height)
    else:
      cell_height = min(cell_height, max_cell_height)
    if cell_width is None:
      cell_width = common.randint(1, max_cell_width)
    else:
      cell_width = min(cell_width, max_cell_width)
    if magnifier is None and cell_height == cell_width:
      magnifier = cell_height
    linecolor = common.random_color() if linecolor is None else linecolor
    if num_colors is None:
      num_colors = common.randint(1, min(8, height * width))
    else:
      num_colors = min(num_colors, 8)
    color_list = common.random_colors(num_colors, exclude=[linecolor])
    if num_cells is None:
      num_cells = common.randint(1, height * width)
    else:
      num_cells = min(num_cells, height * width)
    pixels = common.sample(common.all_pixels(width, height), num_cells)
    rows, cols = zip(*pixels)
    colors = [common.choice(color_list) for _ in pixels]
  if height is None: height = size
  if width is None: width = size
  if cell_height is None: cell_height = magnifier
  if cell_width is None: cell_width = magnifier

  bitmap, _ = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    bitmap[r][width - c - 1] = color
  if cell_height == cell_width:
    grid = common.create_linegrid(bitmap, cell_height, linecolor)
  else:
    grid = create_rect_linegrid(bitmap, cell_height, cell_width, linecolor)
  # The magnified input is criss-crossed with `linecolor` gridlines; those lines
  # are distractors, so step 1 of the solve erases them (linecolor -> background).
  # Then collapse the magnified blocks back to the bitmap and flip to the answer.
  output = [[common.black() if v == linecolor else v for v in row] for row in grid]
  output = bitmap
  output = common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, rows=[0, 1, 2, 3, 3, 3], cols=[3, 2, 1, 1, 2, 3],
               colors=[3, 3, 3, 3, 3, 3], magnifier=4, linecolor=2),
      generate(size=4, rows=[0, 1, 1, 2, 3], cols=[2, 2, 3, 1, 0],
               colors=[2, 1, 2, 1, 3], magnifier=4, linecolor=8),
      generate(size=3, rows=[0, 1, 1, 2], cols=[1, 1, 2, 0],
               colors=[8, 8, 8, 4], magnifier=3, linecolor=2),
  ]
  test = [
      generate(size=4, rows=[0, 0, 0, 0, 1, 2, 2, 2, 3],
               cols=[0, 1, 2, 3, 2, 0, 2, 3, 2],
               colors=[1, 1, 3, 1, 3, 2, 3, 2, 3], magnifier=5, linecolor=8),
  ]
  return {"train": train, "test": test}
