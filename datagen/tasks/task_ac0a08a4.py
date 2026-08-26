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


def generate(rows=None, cols=None, colors=None, size=3, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digits representing the colors to be used
    size: the width and height of the (square) input grid
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    pixels = common.all_pixels(width, height)
    # enhance = number of placed pixels is also the magnification factor, so the
    # output is (height*enhance) x (width*enhance). Cap the count so the output
    # stays <= 30 on its longest axis, never exceeds the 9 unrolled reveal
    # handlers, and never exceeds the number of available cells (sample).
    cap = min(9, width * height, 30 // max(width, height))
    cap = max(1, cap)
    # Use at least 2 pixels when feasible so enhance >= 2 and the reveal stages
    # produce non-trivial (non-collapsing) intermediate steps.
    lo = 2 if cap >= 2 else 1
    pixels = common.sample(pixels, common.randint(lo, cap))
    rows, cols = zip(*pixels)
    colors = common.random_colors(len(pixels))

  enhance = len(colors)
  grid = common.grid(width, height)
  output = common.grid(width * enhance, height * enhance)
  pixels = list(zip(rows, cols, colors))
  for row, col, color in pixels:
    grid[row][col] = color

  def reveal_pixel(pixel_idx):
    if pixel_idx >= len(pixels):
      return
    row, col, color = pixels[pixel_idx]
    for dr in range(enhance):
      for dc in range(enhance):
        output[row * enhance + dr][col * enhance + dc] = color

  reveal_pixel(0)
  reveal_pixel(1)
  reveal_pixel(2)
  reveal_pixel(3)
  reveal_pixel(4)
  reveal_pixel(5)
  reveal_pixel(6)
  reveal_pixel(7)
  reveal_pixel(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1], cols=[0, 2], colors=[2, 7]),
      generate(rows=[0, 1, 2], cols=[1, 2, 0], colors=[4, 8, 6]),
      generate(rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 2, 1],
               colors=[6, 9, 3, 2, 7]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[0, 1, 2, 0], colors=[1, 9, 6, 8]),
  ]
  return {"train": train, "test": test}
