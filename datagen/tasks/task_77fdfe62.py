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


def _reveal_quadrant(output, rows, cols, color, r_lo, r_hi, c_lo, c_hi):
  """Colors the pixels of one interior quadrant with that quadrant's corner color.

  A pixel (r, c) belongs to this quadrant when r_lo <= r < r_hi and
  c_lo <= c < c_hi; the four quadrants partition the interior, so each pixel is
  colored exactly once across the four calls.
  """
  for r, c in zip(rows, cols):
    if r_lo <= r < r_hi and c_lo <= c < c_hi:
      output[r][c] = color
  return output


def generate(size=None, rows=None, cols=None, colors=None, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of four digits representing the colors to be used
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if rows is None:
    if height is None:
      height = 2 * common.randint(1, 3)
    if width is None:
      width = 2 * common.randint(1, 3)
    while True:
      pixels = common.random_pixels(width, height)
      if pixels: break
    rows, cols = zip(*pixels)
    colors = common.random_colors(4, exclude=[common.blue(), common.cyan()])
  if height is None:
    height = size
  if width is None:
    width = size

  grid, output = common.grid(width + 4, height + 4), common.grid(width, height)
  for i in range(4 + width):
    for r, c in [(1, i), (height + 2, i)]:
      grid[r][c] = common.blue()
  for i in range(4 + height):
    for r, c in [(i, 1), (i, width + 2)]:
      grid[r][c] = common.blue()
  grid[0][0] = colors[0]
  grid[0][width + 3] = colors[1]
  grid[height + 3][0] = colors[2]
  grid[height + 3][width + 3] = colors[3]
  for r, c in zip(rows, cols):
    grid[r + 2][c + 2] = common.cyan()
  r_mid, c_mid = height // 2, width // 2
  output = _reveal_quadrant(output, rows, cols, colors[0], 0, r_mid, 0, c_mid)
  output = _reveal_quadrant(output, rows, cols, colors[1], 0, r_mid, c_mid, width)
  output = _reveal_quadrant(output, rows, cols, colors[2], r_mid, height, 0, c_mid)
  output = _reveal_quadrant(output, rows, cols, colors[3], r_mid, height, c_mid, width)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, rows=[0, 1, 1, 1, 2, 3, 3, 3],
               cols=[1, 0, 1, 3, 2, 0, 2, 3], colors=[2, 3, 4, 6]),
      generate(size=2, rows=[0, 0, 1], cols=[0, 1, 0], colors=[9, 4, 2, 3]),
      generate(size=4, rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
               cols=[1, 3, 0, 1, 2, 0, 2, 3, 0, 1, 2], colors=[6, 2, 7, 4]),
  ]
  test = [
      generate(size=6,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5],
               cols=[1, 2, 0, 1, 2, 4, 2, 4, 1, 3, 4, 0, 1, 3, 5, 1, 4],
               colors=[3, 4, 7, 5]),
  ]
  return {"train": train, "test": test}
