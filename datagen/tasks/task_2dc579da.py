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


def generate(size=None, row=None, col=None, linecolor=None, dotcolor=None,
             b=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the "mini" grid (square fallback)
    row: a vertical coordinate where the odd pixel is placed
    col: a horizontal coordinate where the odd pixel is placed
    linecolor: a digit representing a color to be used for the lines
    dotcolor: a digit representing a color to be used for the dot
    b: the integer used for all background cells
    height: the number of rows of the "mini" grid (defaults to size)
    width: the number of columns of the "mini" grid (defaults to size)
  """
  if size is None:
    if height is None:
      height = common.randint(1, 14)
    if width is None:
      width = common.randint(1, 14)
    row = common.randint(0, height - 1)
    col = common.randint(0, width - 1)
    row += 0 if common.randint(0, 1) == 0 else height + 1
    col += 0 if common.randint(0, 1) == 0 else width + 1
    colors = common.sample(range(10), k=3)
    linecolor, dotcolor, b = colors[0], colors[1], colors[2]
  else:
    height = width = size

  grid = common.grid(2 * width + 1, 2 * height + 1, b)
  output = common.grid(width, height, b)
  for i in range(2 * width + 1):
    grid[height][i] = linecolor
  for i in range(2 * height + 1):
    grid[i][width] = linecolor
  grid[row][col] = dotcolor
  row -= 0 if row < height else height + 1
  col -= 0 if col < width else width + 1
  output[row][col] = dotcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, row=4, col=0, linecolor=3, dotcolor=4, b=8),
      generate(size=3, row=1, col=5, linecolor=2, dotcolor=1, b=4),
      generate(size=5, row=2, col=1, linecolor=1, dotcolor=8, b=3),
  ]
  test = [
      generate(size=6, row=3, col=8, linecolor=0, dotcolor=2, b=1),
  ]
  return {"train": train, "test": test}
