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


def generate(rows=None, cols=None, colors=None, pixelrows=None, pixelcols=None,
             size=3, height=None, width=None, num=None, num_colors=None,
             noise_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    pixelrows: a list of vertical coordinates where pixels should be placed
    pixelcols: a list of horizontal coordinates where pixels should be placed
    size: the size of the grid
    height: optional number of output rows
    width: optional number of output columns
    num: optional number of colored output cells
    num_colors: optional number of foreground colors to draw from
    noise_count: optional number of gray distractor pixels per input block
  """
  height_defaulted = height is None
  width_defaulted = width is None
  if height_defaulted: height = size
  if width_defaulted: width = size
  if rows is None:
    height = common.randint(2, 10) if height_defaulted else height
    width = common.randint(2, 10) if width_defaulted else width
    area = height * width
    if num is None: num = common.randint(1, area)
    num = min(num, area)
    if num_colors is None: num_colors = common.randint(1, 8)
    boxes = common.sample(common.all_pixels(width, height), num)
    rows, cols = zip(*boxes)
    colset = common.random_colors(num_colors, exclude=[common.gray()])
    colors = [common.choice(colset) for _ in boxes]
    pixelrows, pixelcols = [], []
    for r in range(height):
      for c in range(width):
        num_pixels = (common.randint(0, 8)
                      if noise_count is None else noise_count)
        pixels = common.sample(common.all_pixels(3, 3), num_pixels)
        for p in pixels:
          pixelrows.append(r * 3 + p[0])
          pixelcols.append(c * 3 + p[1])

  grid, output = common.grids(width * 3, height * 3)
  for r, c, color in zip(rows, cols, colors):
    for dr in range(3):
      for dc in range(3):
        grid[r * 3 + dr][c * 3 + dc] = color
        output[r * 3 + dr][c * 3 + dc] = color
  for r, c in zip(pixelrows, pixelcols):
    grid[r][c] = common.gray()
  output = common.grid(width, height)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               colors=[3, 8, 7, 6, 9], pixelrows=[1, 3, 6, 8, 8, 8],
               pixelcols=[7, 4, 5, 1, 4, 8]),
      generate(rows=[0, 2], cols=[1, 1], colors=[2, 7],
               pixelrows=[1, 3, 4, 4, 6, 7], pixelcols=[1, 0, 3, 7, 1, 5]),
  ]
  test = [
      generate(rows=[0, 1, 2], cols=[0, 1, 1], colors=[4, 3, 9],
               pixelrows=[0, 1, 2, 3, 6, 7], pixelcols=[7, 0, 4, 7, 2, 4]),
  ]
  return {"train": train, "test": test}
