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


def generate(colors=None, values=None, size=3, height=None, width=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    values: a list of color indices for all cells in the grid
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    num_colors: how many distinct colors appear in generated grids
    density: how many non-background cells to scatter in generated grids
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    area = height * width
    if num_colors is None:
      num_colors = common.randint(2, min(10, area))
    num_colors = max(1, min(num_colors, 10, area))
    colors = common.sample(list(range(10)), num_colors)
    values = [0] * area
    foreground = num_colors - 1
    if foreground:
      if density is None:
        remaining = common.all_pixels(width, height)
        for idx in range(1, num_colors):
          count = common.randint(1, max(1, len(remaining) // foreground))
          cells = common.sample(remaining, count)
          for r, c in cells:
            values[r * width + c] = idx
          remaining = [cell for cell in remaining if cell not in cells]
      else:
        total = max(foreground, min(area, density))
        cells = common.sample(common.all_pixels(width, height), total)
        for idx, (r, c) in enumerate(cells):
          values[r * width + c] = 1 + (idx % foreground)
      if all(values[idx] == values[area - idx - 1] for idx in range(area)):
        values[0] = 1 if values[-1] != 1 else 0

  grid = common.grid(width, height)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[values[r * width + c]]
  output = common.grid(width, height)

  def rotate_row(out_row):
    for r in range(out_row * height // 3, (out_row + 1) * height // 3):
      for c in range(width):
        output[r][c] = grid[height - r - 1][width - c - 1]

  rotate_row(0)
  rotate_row(1)
  rotate_row(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 1, 8], values=[0, 0, 1, 0, 1, 0, 0, 2, 1]),
      generate(colors=[9, 2, 4], values=[0, 1, 2, 1, 2, 2, 1, 0, 1]),
      generate(colors=[8, 5, 7], values=[0, 0, 0, 1, 1, 0, 0, 1, 1]),
      generate(colors=[3, 2, 9], values=[0, 1, 2, 2, 2, 2, 1, 0, 0]),
  ]
  test = [
      generate(colors=[6, 4, 7], values=[0, 1, 1, 0, 0, 1, 1, 0, 2]),
  ]
  return {"train": train, "test": test}
