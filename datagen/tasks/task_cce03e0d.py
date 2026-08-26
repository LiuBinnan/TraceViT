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


def generate(rows=None, cols=None, colors=None, size=3, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    pixels = common.all_pixels(width, height)
    pixels = common.sample(pixels, common.randint(2, min(8, width * height)))
    rows, cols = zip(*pixels)
    colors = [common.randint(1, 2) for _ in pixels]

  grid = common.grid(width, height)
  output = common.grid(width, height)
  red_cells = []
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    if color != common.red(): continue
    red_cells.append((r, c))

  def identify_red_nodes():
    for r, c in red_cells:
      output[r][c] = common.red()

  identify_red_nodes()
  output = common.grid(width * width, height * height)

  def reveal_red_block(block_idx):
    if block_idx >= len(red_cells):
      return
    r, c = red_cells[block_idx]
    for rr, cc, colorcolor in zip(rows, cols, colors):
      output[r * height + rr][c * width + cc] = colorcolor

  reveal_red_block(0)
  reveal_red_block(1)
  reveal_red_block(2)
  reveal_red_block(3)
  reveal_red_block(4)
  reveal_red_block(5)
  reveal_red_block(6)
  reveal_red_block(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2], cols=[0, 0, 1, 2], colors=[1, 2, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 1, 0],
               colors=[1, 2, 1, 1, 2]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 2, 0, 1],
               colors=[2, 1, 2, 2, 1, 2, 1]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1],
               colors=[1, 2, 2, 2, 1, 1, 2]),
  ]
  return {"train": train, "test": test}
