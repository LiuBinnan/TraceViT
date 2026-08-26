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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             size=10, grid_height=None, grid_width=None, count=None,
             num_colors=None, row_anchor=3, col_anchor=6,
             background_color=0, square_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the pool
    height: the height of the pool
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    grid_height: the number of rows in the grid (defaults to size)
    grid_width: the number of columns in the grid (defaults to size)
    count: the number of colored border pixels
    num_colors: the number of colors used for the border pixels
    row_anchor: the top row of the pool
    col_anchor: the column just to the right of the pool
    background_color: the color of the background
    square_color: the color of the pool
  """
  if grid_height is None: grid_height = size
  if grid_width is None: grid_width = size
  if square_color is None: square_color = common.cyan()
  if width is None:
    max_height = max(2, min(grid_height - 4, 2 * (grid_height // 3)))
    max_width = max(2, min(grid_width - 4, 2 * (grid_width // 3)))
    width, height = common.randint(2, max_width), common.randint(2, max_height)
    row_anchor = common.randint(2, grid_height - height - 2)
    col_anchor = common.randint(2, grid_width - width - 2) + width
    background_color, square_color = common.sample(range(10), 2)
    exclude = [background_color, square_color]
    max_colors = min(8, 10 - len(exclude))
    if num_colors is None:
      num_colors = common.randint(1, max_colors)
    num_colors = max(1, min(num_colors, max_colors))
    palette = common.sample([c for c in range(10) if c not in exclude],
                            num_colors)
    top_left = common.randint(0, 1)
    bottom_left = common.randint(0, 1)
    top_right = common.randint(0, 1)
    bottom_right = common.randint(0, 1)
    candidates = []
    left = col_anchor - width
    right = col_anchor - 1
    top = row_anchor
    bottom = row_anchor + height - 1
    for r in range(top + (not top_left), bottom + 1 - (not bottom_left)):
      candidates.append((r, 0))
    for r in range(top + (not top_right), bottom + 1 - (not bottom_right)):
      candidates.append((r, grid_width - 1))
    for c in range(left + top_left, right + 1 - top_right):
      candidates.append((0, c))
    for c in range(left + bottom_left, right + 1 - bottom_right):
      candidates.append((grid_height - 1, c))
    if count is None:
      count = common.randint(1, len(candidates))
    count = max(1, min(count, len(candidates)))
    candidates = common.sample(candidates, count)
    rows = [r for r, c in candidates]
    cols = [c for r, c in candidates]
    colors = [common.choice(palette) for _ in range(count)]

  grid, output = common.grids(grid_width, grid_height, background_color)
  for r in range(row_anchor, row_anchor + height):
    for c in range(col_anchor - width, col_anchor):
      output[r][c] = grid[r][c] = square_color

  def project_side(side_idx):
    if side_idx >= 4:
      return
    for r, c, color in zip(rows, cols, colors):
      side = 0 if r == 0 else 1 if c == 0 else 2 if c == grid_width - 1 else 3
      if side != side_idx:
        continue
      output[r][c] = grid[r][c] = color
      r = r if r >= row_anchor else row_anchor
      r = r if r <= row_anchor + height - 1 else row_anchor + height - 1
      c = c if c >= col_anchor - width else col_anchor - width
      c = c if c <= col_anchor - 1 else col_anchor - 1
      output[r][c] = color

  project_side(0)
  project_side(1)
  project_side(2)
  project_side(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=4, rows=[0, 6, 9], cols=[4, 0, 5],
               colors=[9, 6, 4]),
      generate(width=3, height=5, rows=[0, 3, 5, 7, 9], cols=[4, 0, 9, 0, 5],
               colors=[7, 6, 2, 3, 1]),
      generate(width=3, height=5, rows=[0, 3, 4, 6, 7, 9],
               cols=[3, 9, 0, 0, 9, 3], colors=[4, 6, 3, 2, 2, 7]),
  ]
  test = [
      generate(width=4, height=4, rows=[0, 0, 3, 4, 5, 6, 9],
               cols=[3, 5, 0, 9, 0, 0, 4], colors=[6, 2, 9, 7, 3, 4, 6]),
  ]
  return {"train": train, "test": test}
