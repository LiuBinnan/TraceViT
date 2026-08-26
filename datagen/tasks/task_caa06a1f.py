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


def generate(size=None, border=None, colors=None, b=None, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    border: the thickness of the border
    colors: a list of digits representing the colors to be used
    b: the integer used for all background cells
    height: the number of rows (decoupled extent; falls back to size)
    width: the number of columns (decoupled extent; falls back to size)
  """
  if size is None:
    if height is None:
      height = common.randint(10, 30)
    if width is None:
      width = common.randint(10, 30)
    border = common.randint(1, min(height, width) // 2)
    b = common.random_color()
    colors = common.random_colors(2 + max(height, width) // 12, exclude=[b])
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid, output = common.grids(width, height, b)
  for r in range(height):
    for c in range(width):
      if r + border < height and c + border < width:
        grid[r][c] = colors[(r % 2 + c) % len(colors)]
      output[r][c] = colors[(r % 2 + c + 1) % len(colors)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=11, border=4, colors=[6, 7], b=3),
      generate(size=8, border=1, colors=[6, 3], b=1),
      generate(size=6, border=1, colors=[5, 4], b=6),
  ]
  test = [
      generate(size=18, border=6, colors=[8, 5, 7], b=3),
  ]
  return {"train": train, "test": test}
