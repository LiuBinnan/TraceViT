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


def generate(rows=None, cols=None, minirows=None, minicols=None, color=None,
             minisize=3, block_rows=None, block_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    color: the color of the pixels
    minisize: the width and height of the mini grids
    block_rows: the number of mini-grid rows in the block layout
    block_cols: the number of mini-grid cols in the block layout
  """
  if block_rows is None: block_rows = minisize
  if block_cols is None: block_cols = minisize
  if rows is None:
    max_pixels = common.randint(2, 5)
    rows, cols, minirows, minicols = [], [], [], []
    for r in range(block_rows):
      for c in range(block_cols):
        count = common.randint(0, max_pixels)
        pixels = common.sample(common.all_pixels(minisize, minisize), count)
        rows.extend([r] * count)
        cols.extend([c] * count)
        minirows.extend([p[0] for p in pixels])
        minicols.extend([p[1] for p in pixels])
    color = common.random_color(exclude=[common.gray()])

  grid = common.hollywood_squares(minisize, common.black(), common.gray(),
                                  block_rows=block_rows, block_cols=block_cols,
                                  row_content=minisize, col_content=minisize)
  counts = {}
  max_pixels = 0
  for r, c, mr, mc in zip(rows, cols, minirows, minicols):
    grid[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = color
    counts[(r, c)] = 1 if (r, c) not in counts else counts[(r, c)] + 1
    max_pixels = max(max_pixels, counts[(r, c)])
  selected = {cell for cell, count in counts.items() if count == max_pixels}
  output = common.hollywood_squares(minisize, common.black(), common.gray(),
                                    block_rows=block_rows, block_cols=block_cols,
                                    row_content=minisize, col_content=minisize)
  for r, c, mr, mc in zip(rows, cols, minirows, minicols):
    if (r, c) not in selected: continue
    output[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = color
  output = common.hollywood_squares(minisize, common.black(), common.gray(),
                                    block_rows=block_rows, block_cols=block_cols,
                                    row_content=minisize, col_content=minisize)
  for (r, c), num_pixels in counts.items():
    if num_pixels < max_pixels: continue
    for dr in range(minisize):
      for dc in range(minisize):
        output[r * (minisize + 1) + dr][c * (minisize + 1) + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 1, 2, 0, 2, 2],
               minirows=[1, 2, 1, 0, 1, 1, 0, 1],
               minicols=[0, 2, 1, 2, 1, 1, 0, 2], color=1),
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 2, 0, 0, 1, 2, 0, 1, 2],
               minirows=[1, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1],
               minicols=[0, 1, 0, 2, 0, 0, 2, 1, 0, 2, 2],
               color=2),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2],
               cols=[0, 0, 2, 0, 1, 1, 0, 1, 2, 2, 2],
               minirows=[0, 0, 1, 1, 1, 2, 1, 1, 1, 1, 2],
               minicols=[0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 2],
               color=3),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2],
               cols=[0, 0, 0, 0, 1, 2, 2, 2, 0, 1, 2, 2, 2, 0, 1, 1, 1, 1, 2,
                     2],
               minirows=[0, 0, 1, 2, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 2, 2,
                         0, 1],
               minicols=[0, 1, 1, 0, 2, 0, 1, 1, 0, 1, 1, 0, 2, 0, 1, 2, 0, 1,
                         2, 1],
               color=4),
  ]
  return {"train": train, "test": test}
