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


def generate(width=None, height=None, rows=None, cols=None, color=None,
             num_cells=None, num_colors=None, background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    num_cells: how many foreground pixels to place
    num_colors: how many foreground colors to use
    background: the background color
  """
  if width is None:
    width, height = common.randint(2, 15), common.randint(2, 15)
    if background is None:
      background = common.randint(0, 9)
      while background == common.cyan():
        background = common.randint(0, 9)
    max_cells = max(1, (width * height) // 6)
    if num_cells is None:
      num_cells = common.randint(1, max_cells)
    num_cells = max(1, min(max_cells, num_cells))
    if num_colors is None:
      num_colors = common.randint(1, 8)
    max_colors = 8 if background == 0 else 7
    num_colors = max(1, min(max_colors, num_colors))
    colors = common.random_colors(num_colors,
                                  exclude=[background, common.cyan()])
    cells = [(r, c) for r in range(height) for c in range(width)]
    cells = common.sample(cells, num_cells)
    rows = [r for r, c in cells]
    cols = [c for r, c in cells]
    cell_colors = [
        colors[common.randint(0, len(colors) - 1)] for _ in cells
    ]
  else:
    if background is None:
      background = 0
    cell_colors = [color for _ in rows]

  def put(thegrid, r, c, color):
    if r >= 0 and r < 2 * height and c >= 0 and c < 2 * width:
      thegrid[r][c] = color
  grid = common.grid(width, height, background)
  for r, c, cell_color in zip(rows, cols, cell_colors):
    grid[r][c] = cell_color
  output = common.grid(2 * width, 2 * height, background)

  def draw_grid_on_original():
    # Draws the sky blue grid around the pixels at their original position.
    for r, c in zip(rows, cols):
      for dr, dc in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        put(output, r + dr, c + dc, common.cyan())
    for r, c, cell_color in zip(rows, cols, cell_colors):
      output[r][c] = cell_color

  def place_copy(idx):
    # Places one more copy of the image along with its sky blue grid.
    dr, dc = [(0, width), (height, 0), (height, width)][idx]
    for r, c in zip(rows, cols):
      for ddr, ddc in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        rr, cc = r + dr + ddr, c + dc + ddc
        if rr < 0 or rr >= 2 * height or cc < 0 or cc >= 2 * width: continue
        if output[rr][cc] != background: continue
        output[rr][cc] = common.cyan()
    for r, c, cell_color in zip(rows, cols, cell_colors):
      output[r + dr][c + dc] = cell_color

  draw_grid_on_original()
  place_copy(0)
  place_copy(1)
  place_copy(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=2, rows=[1], cols=[1], color=5),
      generate(width=4, height=3, rows=[0, 2], cols=[2, 1], color=6),
      generate(width=3, height=5, rows=[1, 4], cols=[1, 0], color=4),
      generate(width=4, height=4, rows=[1], cols=[1], color=2),
  ]
  test = [
      generate(width=5, height=6, rows=[0, 3, 5], cols=[1, 3, 1], color=3),
  ]
  return {"train": train, "test": test}
