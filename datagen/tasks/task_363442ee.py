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


def generate(rows=None, cols=None, colors=None, size=3, cell_h=None,
             cell_w=None, grid_rows=None, grid_cols=None, num_colors=None,
             num_dots=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
    cell_h: the height (rows) of the template / cell block
    cell_w: the width (cols) of the template / cell block
    grid_rows: the number of cell rows in the pattern region
    grid_cols: the number of cell columns in the pattern region
    num_colors: the number of distinct colors used to paint the template
    num_dots: the number of marked cells (capped at the number of handlers)
  """
  if rows is None:
    if cell_h is None:
      cell_h = common.randint(1, 3) * 2 + 1
    if cell_w is None:
      cell_w = common.randint(1, 3) * 2 + 1
    if grid_rows is None:
      grid_rows = common.randint(2, 30 // cell_h)
    if grid_cols is None:
      grid_cols = common.randint(2, (30 - cell_w - 1) // cell_w)
    if num_colors is None:
      num_colors = common.randint(1, min(7, cell_h * cell_w))
    colors_list = common.random_colors(num_colors, exclude=[common.blue(),
                                                            common.gray()])
    idxs = [common.randint(0, num_colors - 1) for _ in range(cell_h * cell_w)]
    colors = [colors_list[idx] for idx in idxs]
    cells = grid_rows * grid_cols
    if num_dots is None:
      num_dots = common.randint(2, min(20, cells))
    num_dots = min(20, cells, num_dots)
    pixels = common.sample(common.all_pixels(grid_cols, grid_rows), num_dots)
    rows, cols = zip(*pixels)
  else:
    if cell_h is None:
      cell_h = size
    if cell_w is None:
      cell_w = size
    if grid_rows is None:
      grid_rows = 3
    if grid_cols is None:
      grid_cols = 3

  grid, output = common.grids(cell_w * (grid_cols + 1) + 1, grid_rows * cell_h)
  for r in range(grid_rows * cell_h):
    output[r][cell_w] = grid[r][cell_w] = common.gray()
  for mr in range(cell_h):
    for mc in range(cell_w):
      output[mr][mc] = grid[mr][mc] = colors[mr * cell_w + mc]
  for r, c in zip(rows, cols):
    output[cell_h * r + cell_h // 2][cell_w * (c + 1) + 1 + cell_w // 2] = grid[cell_h * r + cell_h // 2][cell_w * (c + 1) + 1 + cell_w // 2] = common.blue()

  def place_pattern(idx):
    if idx >= len(rows):
      return
    r, c = rows[idx], cols[idx]
    for mr in range(cell_h):
      for mc in range(cell_w):
        output[cell_h * r + mr][cell_w * (c + 1) + 1 + mc] = colors[mr * cell_w + mc]

  place_pattern(0)
  place_pattern(1)
  place_pattern(2)
  place_pattern(3)
  place_pattern(4)
  place_pattern(5)
  place_pattern(6)
  place_pattern(7)
  place_pattern(8)
  place_pattern(9)
  place_pattern(10)
  place_pattern(11)
  place_pattern(12)
  place_pattern(13)
  place_pattern(14)
  place_pattern(15)
  place_pattern(16)
  place_pattern(17)
  place_pattern(18)
  place_pattern(19)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2], cols=[0, 1, 1],
               colors=[4, 2, 2, 2, 6, 2, 6, 4, 4]),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 1],
               colors=[2, 7, 3, 2, 3, 3, 3, 7, 7]),
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 1, 2],
               colors=[3, 8, 6, 9, 8, 2, 9, 9, 9]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[1, 2, 0, 2, 0, 1],
               colors=[3, 3, 9, 8, 4, 4, 8, 9, 8]),
  ]
  return {"train": train, "test": test}
