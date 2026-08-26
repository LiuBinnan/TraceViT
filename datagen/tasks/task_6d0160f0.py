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


def generate(rows=None, cols=None, minirows=None, minicols=None, colors=None,
             minisize=3, block_rows=None, block_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    colors: a digit representing a color to be used
    minisize: the width and height of each mini-rid
    block_rows: number of block rows; also the inner-grid height (defaults to
      minisize, giving the original square layout)
    block_cols: number of block cols; also the inner-grid width (defaults to
      minisize, giving the original square layout)
  """
  if block_rows is None: block_rows = minisize
  if block_cols is None: block_cols = minisize
  if rows is None:
    rows, cols, minirows, minicols, colors = [], [], [], [], []
    for r in range(block_rows):
      for c in range(block_cols):
        count = common.randint(2, 4)
        pixels = common.sample(common.all_pixels(block_cols, block_rows), count)
        rows.extend([r] * count)
        cols.extend([c] * count)
        minirows.extend([p[0] for p in pixels])
        minicols.extend([p[1] for p in pixels])
        colors.extend(common.random_colors(count, exclude=[common.gray(),
                                                           common.yellow()]))
    colors[common.randint(0, len(colors) - 1)] = common.yellow()

  grid = common.hollywood_squares(minisize, common.black(), common.gray(),
                                  block_rows=block_rows, block_cols=block_cols,
                                  row_content=block_rows, col_content=block_cols)
  yellowrow, yellowcol, minirow, minicol = None, None, None, None
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    grid[r * (block_rows + 1) + mr][c * (block_cols + 1) + mc] = color
    if color != common.yellow(): continue
    yellowrow, yellowcol, minirow, minicol = r, c, mr, mc
  output = common.deepcopy(grid)

  def erase_other_grids():
    # Clears every mini-grid except the one holding the yellow pixel.
    for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
      if r == yellowrow and c == yellowcol: continue
      output[r * (block_rows + 1) + mr][c * (block_cols + 1) + mc] = common.black()

  def move_yellow():
    # The yellow pixel moves to the mini-grid addressed by its own position.
    src_row = yellowrow * (block_rows + 1) + minirow
    src_col = yellowcol * (block_cols + 1) + minicol
    dst_row = minirow * (block_rows + 1) + minirow
    dst_col = minicol * (block_cols + 1) + minicol
    output[src_row][src_col] = common.black()
    output[dst_row][dst_col] = common.yellow()

  def move_neighbor(idx):
    # The rest of the yellow pixel's mini-grid moves along, one pixel each.
    neighbors = [(mr, mc, color) for r, c, mr, mc, color
                 in zip(rows, cols, minirows, minicols, colors)
                 if r == yellowrow and c == yellowcol
                 and color != common.yellow()]
    if idx >= len(neighbors): return
    mr, mc, color = neighbors[idx]
    output[yellowrow * (block_rows + 1) + mr][yellowcol * (block_cols + 1) + mc] = (
        common.black())
    output[minirow * (block_rows + 1) + mr][minicol * (block_cols + 1) + mc] = color

  erase_other_grids()
  move_yellow()
  move_neighbor(0)
  move_neighbor(1)
  move_neighbor(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 1,
                     2, 0, 1, 2, 0, 0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0,
                         1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               minicols=[0, 0, 2, 0, 2, 2, 1, 1, 0, 1, 2, 1, 0, 2, 0, 1, 1, 2,
                         2, 2, 2, 0, 0, 1, 1, 2, 1, 0, 2, 0, 0, 2, 2, 2, 1, 1],
               colors=[3, 7, 6, 8, 7, 9, 3, 6, 7, 2, 2, 3, 7, 2, 8, 7, 2, 3, 6,
                       3, 7, 3, 2, 6, 3, 4, 2, 2, 7, 7, 7, 3, 1, 2, 6, 3]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2],
               cols=[0, 1, 2, 0, 2, 0, 1, 0, 0, 0, 1, 2, 2, 0, 1, 2, 0, 1, 2,
                     1],
               minirows=[0, 0, 0, 1, 1, 2, 2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,
                         1, 2],
               minicols=[0, 1, 1, 2, 2, 1, 1, 1, 0, 2, 2, 1, 2, 0, 1, 1, 1, 2,
                         2, 0],
               colors=[3, 2, 6, 7, 9, 6, 1, 3, 1, 9, 6, 7, 3, 9, 9, 9, 6, 4, 1,
                       7]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                     2, 2, 2, 2, 2, 2, 2],
               cols=[0, 1, 2, 0, 0, 0, 2, 1, 0, 0, 1, 2, 1, 2, 2, 0, 2, 0, 1, 0,
                     1, 2, 2, 0, 1, 2, 2],
               minirows=[0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0,
                         0, 1, 1, 1, 1, 2, 2, 2, 2],
               minicols=[1, 1, 0, 0, 1, 2, 1, 1, 1, 2, 1, 2, 0, 1, 2, 2, 0, 1,
                         1, 0, 0, 0, 2, 1, 1, 1, 2],
               colors=[7, 6, 7, 8, 3, 6, 8, 3, 8, 7, 3, 7, 8, 8, 6, 6, 3, 6, 8,
                       8, 3, 4, 8, 7, 6, 6, 7]),
      generate(rows=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 2, 0, 0, 1, 1, 2, 2, 0, 1, 2, 1, 2, 0,
                     1, 2],
               minirows=[0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1,
                         1, 2, 2, 2],
               minicols=[0, 1, 2, 1, 1, 1, 1, 1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1,
                         0, 1, 1, 2],
               colors=[3, 1, 2, 2, 3, 6, 1, 3, 7, 6, 2, 7, 7, 6, 7, 4, 3, 7, 2,
                       3, 3, 6]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               cols=[0, 0, 1, 2, 0, 0, 1, 2, 2, 1, 1, 2, 0, 2, 2, 0, 1, 1, 2, 0,
                     0, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1, 1,
                         1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2],
               minicols=[0, 2, 0, 1, 0, 1, 1, 0, 1, 0, 2, 2, 0, 0, 2, 1, 1, 2,
                         1, 0, 2, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2],
               colors=[2, 3, 2, 3, 7, 6, 7, 6, 7, 6, 3, 2, 7, 6, 4, 6, 2, 7, 2,
                       6, 2, 3, 7, 7, 6, 2, 3, 6, 2, 2, 7, 6, 7]),
  ]
  return {"train": train, "test": test}
