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


def generate(colors=None, rows=None, cols=None, xpose=None, size=10,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a pair of digits representing two different colors
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    xpose: xpose: an integer indicating whether to transpose the grid
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    colors, pixels = common.random_colors(2, exclude=[common.green()]), []
    for r in range(height):
      for c in range(1, width - 1):
        pixels.append((r, c))
    pixels = common.sample(pixels, common.randint(2, 10))
    rows, cols = zip(*pixels)
    xpose = common.randint(0, 1)

  raw_grid, raw_output = common.grids(width, height)
  output = common.transpose(raw_output) if xpose else raw_output
  for r in range(height):
    raw_output[r][0] = raw_grid[r][0] = colors[0]
  output = common.transpose(raw_output) if xpose else raw_output
  for r in range(height):
    raw_output[r][-1] = raw_grid[r][-1] = colors[1]
  output = common.transpose(raw_output) if xpose else raw_output
  for r, c in zip(rows, cols):
    raw_grid[r][c] = common.green()
  for r, c in zip(rows, cols):
    if c >= width // 2:
      continue
    raw_output[r][c] = colors[0]
  output = common.transpose(raw_output) if xpose else raw_output
  for r, c in zip(rows, cols):
    if c < width // 2:
      continue
    raw_output[r][c] = colors[1]
  output = common.transpose(raw_output) if xpose else raw_output
  grid = common.transpose(raw_grid) if xpose else raw_grid
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 2], rows=[1, 4, 6], cols=[6, 4, 2], xpose=0),
      generate(colors=[4, 7], rows=[1, 3, 4, 7, 8], cols=[2, 3, 6, 2, 7],
               xpose=1),
      generate(colors=[8, 9], rows=[1, 1, 3, 4, 6, 7], cols=[3, 6, 7, 2, 6, 3],
               xpose=1),
  ]
  test = [
      generate(colors=[5, 4], rows=[0, 1, 1, 3, 4, 5, 7, 8, 8],
               cols=[1, 5, 8, 3, 6, 3, 4, 2, 6], xpose=0),
  ]
  return {"train": train, "test": test}
