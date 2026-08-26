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


def generate(size=None, rows=None, cols=None, color=None, height=None,
             width=None, num_pixels=None, num_colors=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_pixels: the number of colored pixels to place
    num_colors: the number of foreground colors to draw from
    colors: a list of foreground colors to use
  """
  if size is None:
    if height is None:
      height = common.randint(2, 15)
    if width is None:
      width = common.randint(2, 15)
    max_pixels = max(1, height * width // 2 - 1)
    if num_pixels is None:
      num_pixels = common.randint(1, max_pixels)
    num_pixels = min(num_pixels, max_pixels)
    pixels = common.sample(common.all_pixels(width, height), num_pixels)
    rows, cols = zip(*pixels)
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = max(1, min(num_colors, 8))
    if colors is None:
      colors = common.random_colors(num_colors, exclude=[common.cyan()])
    else:
      colors = colors[:num_colors]
    point_colors = [colors[common.randint(0, len(colors) - 1)]
                    for _ in pixels]
  else:
    height = width = size
    if colors is None:
      point_colors = [color for _ in rows]
    elif len(colors) == len(rows):
      point_colors = colors
    else:
      point_colors = [colors[idx % len(colors)] for idx in range(len(rows))]

  grid, output = common.grid(width, height), common.grid(2 * width, 2 * height)
  for c in cols:
    for r in range(2 * height):
      output[r][c] = output[r][c + width] = common.cyan()
  for r, c, point_color in zip(rows, cols, point_colors):
    grid[r][c] = point_color
    for dr, dc in [(0, 0), (0, width), (height, 0), (height, width)]:
      output[r + dr][c + dc] = point_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[0, 2], cols=[0, 2], color=2),
      generate(size=6, rows=[0, 4, 4], cols=[1, 0, 5], color=5),
      generate(size=2, rows=[0], cols=[1], color=4),
  ]
  test = [
      generate(size=4, rows=[0, 2, 3], cols=[2, 3, 0], color=3),
  ]
  return {"train": train, "test": test}
