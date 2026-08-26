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


def generate(rows=None, cols=None, colors=None, size=10, height=None,
             width=None, count=None, bg_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) input grid
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
    count: the number of latent half-grid pixels to place
    bg_color: the background color
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if bg_color is None:
    bg_color = common.randint(0, 9) if rows is None else 0
  if rows is None:
    half_rows, half_cols = height // 2, width // 2
    if count is None:
      count = common.randint(0, max(0, half_rows * half_cols // 2 - 1))
    count = min(count, half_rows * half_cols)
    pixels = common.sample(
        common.all_pixels(half_cols, half_rows), count)
    rows = [r for r, _ in pixels]
    cols = [c for _, c in pixels]
    color_choices = list(range(10))
    color_choices.remove(bg_color)
    colors = [common.choice(color_choices) for _ in range(len(pixels))]

  grid, output = (common.grid(width, height, bg_color),
                  common.grid(2 * width, 2 * height, bg_color))
  for r, c, color in zip(rows, cols, colors):
    grid[2 * r + 1][2 * c + 1] = color

  def expand_pixel(idx):
    if idx >= len(rows):
      return
    r, c, color = rows[idx], cols[idx], colors[idx]
    for dr in range(4):
      for dc in range(4):
        output[4 * r + dr][4 * c + dc] = color

  for idx in range(len(rows)):
    expand_pixel(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 3, 4], cols=[0, 0, 1, 2, 3, 4],
               colors=[2, 4, 1, 3, 4, 3]),
      generate(rows=[0, 0, 1, 3, 4, 4], cols=[0, 1, 1, 4, 3, 4],
               colors=[1, 3, 4, 8, 2, 2]),
      generate(rows=[0, 0, 4, 4, 4], cols=[0, 1, 0, 1, 4],
               colors=[3, 2, 1, 1, 4]),
  ]
  test = [
      generate(rows=[1, 2, 3, 3, 4], cols=[1, 2, 1, 3, 0],
               colors=[6, 1, 3, 4, 2]),
  ]
  return {"train": train, "test": test}
