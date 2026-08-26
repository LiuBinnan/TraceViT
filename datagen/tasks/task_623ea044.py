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


def generate(size=None, row=None, col=None, color=None, height=None, width=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    row: an integer with the pixel's row
    col: an integer with the pixel's column
    color: a digit representing the color of the pixel
    height: the number of rows (defaults to size when omitted)
    width: the number of columns (defaults to size when omitted)
    count: the number of source pixels
  """
  if size is None:
    if height is None:
      height = common.randint(3, 30)
    if width is None:
      width = common.randint(3, 30)
    if count is None:
      count = common.randint(1, max(1, (height * width) // 10))
  if height is None:
    height = size
  if width is None:
    width = size
  if count is None:
    count = 1
  count = max(1, min(count, max(1, (height * width) // 10), height * width))
  if color is None:
    color = common.random_color()

  pixels = []
  if row is not None and col is not None:
    pixels.append((row, col))
  if len(pixels) < count:
    candidates = [
        (r, c) for r in range(height) for c in range(width)
        if (r, c) not in pixels
    ]
    pixels.extend(common.shuffle(candidates)[:count - len(pixels)])

  grid, output = common.grids(width, height)
  for r, c in pixels:
    output[r][c] = grid[r][c] = color

  def draw_descending():
    for row, col in pixels:
      for c in range(width):
        r = row + col - c
        if r >= 0 and r < height:
          output[r][c] = color

  def draw_ascending():
    for row, col in pixels:
      for c in range(width):
        r = row - col + c
        if r >= 0 and r < height:
          output[r][c] = color

  draw_descending()
  draw_ascending()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, row=3, col=3, color=2),
      generate(size=15, row=5, col=11, color=7),
      generate(size=7, row=3, col=2, color=8),
  ]
  test = [
      generate(size=17, row=7, col=12, color=6),
  ]
  return {"train": train, "test": test}
