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


def generate(rows=None, cols=None, color=None, size=3, height=None, width=None,
             count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: number of rows of the input grid (defaults to size)
    width: number of columns of the input grid (defaults to size)
    count: number of foreground pixels to place
    num_colors: number of foreground colors to use
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    max_count = width * height
    if count is None:
      count = common.randint(1, max_count)
    count = max(1, min(count, max_count))
    if num_colors is None:
      num_colors = common.randint(1, min(9, count))
    num_colors = max(1, min(num_colors, 9, count))
    pixels = common.sample(common.all_pixels(width, height), count)
    rows, cols = zip(*pixels)
    palette = common.random_colors(num_colors)
    cell_colors = palette + [
        palette[common.randint(0, len(palette) - 1)]
        for _ in range(count - num_colors)
    ]
    cell_colors = common.sample(cell_colors, len(cell_colors))
  else:
    cell_colors = [color for _ in rows]

  grid = common.grid(width, height)
  output = common.grid(height, width)
  for r, c, cell_color in zip(rows, cols, cell_colors):
    output[width - 1 - c][r] = grid[r][c] = cell_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2, 2, 2], cols=[0, 0, 1, 2, 0, 1, 2], color=9),
      generate(rows=[0, 0, 0, 2, 2], cols=[0, 1, 2, 0, 1], color=6),
      generate(rows=[0, 1, 2, 2, 2], cols=[2, 2, 0, 1, 2], color=9),
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 2, 1, 2], color=2),
  ]
  test = [
      generate(rows=[1, 2, 2], cols=[0, 1, 2], color=5),
  ]
  return {"train": train, "test": test}
