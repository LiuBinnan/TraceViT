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


def generate(rows=None, cols=None, wides=None, talls=None, xpose=None, size=10,
             height=None, width=None, count=None, colors=None, background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of widths of the pixels to be placed
    talls: a list of heights of the pixels to be placed
    xpose: a list of x-positions of the pixels to be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: how many rectangles to try to place
    colors: a list of input rectangle colors
    background: the background color
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if count is None:
      count = common.randint(1, 9)
    count = min(count, 9)
    if background is None:
      background = common.choice([
          common.black(), common.green(), common.gray(), common.pink(),
          common.orange(), common.cyan(), common.maroon()])
    color_pool = [
        common.green(), common.gray(), common.pink(), common.orange(),
        common.cyan(), common.maroon()]
    if background in color_pool:
      color_pool.remove(background)
    count = min(count, len(color_pool))
    if colors is None:
      colors = common.sample(color_pool, count)
    available = [(r, c) for r in range(height) for c in range(width)]
    rows, cols, wides, talls = [], [], [], []
    for color in colors:
      if len(rows) >= count: break
      for _ in range(4):
        tall = common.randint(3, 7)
        wide = common.randint(3, 7)
        candidates = [(r, c) for r, c in available
                      if r < height - tall and c < width - wide]
        if not candidates: continue
        row, col = common.choice(candidates)
        pixels = [(r, c) for r in range(row, row + tall)
                  for c in range(col, col + wide)]
        if all(pixel in available for pixel in pixels):
          rows.append(row)
          cols.append(col)
          wides.append(wide)
          talls.append(tall)
          available = [pixel for pixel in available if pixel not in pixels]
          break
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height, common.black() if background is None else background)
  for row, col, wide, tall, color in zip(
      rows, cols, wides, talls, colors if colors is not None else [common.gray()] * len(rows)):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        output[r][c] = common.red()
        grid[r][c] = color
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        if r in [row, row + tall - 1] or c in [col, col + wide - 1]:
          output[r][c] = common.yellow()
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in [row, row + tall - 1]:
      for c in [col, col + wide - 1]:
        output[r][c] = common.blue()
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 5], cols=[1, 6], wides=[4, 4], talls=[4, 5], xpose=0),
      generate(rows=[0, 4], cols=[0, 6], wides=[5, 4], talls=[6, 6], xpose=1),
  ]
  test = [
      generate(rows=[1, 4], cols=[0, 7], wides=[6, 3], talls=[4, 6], xpose=1),
  ]
  return {"train": train, "test": test}
