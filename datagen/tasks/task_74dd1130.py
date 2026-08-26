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


def generate(colors=None, size=3, height=None, width=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    num_colors: how many distinct colors appear in generated grids
    density: optional percentage of cells to paint with non-background colors
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    area = height * width
    if num_colors is None:
      num_colors = common.randint(1, min(10, area))
    num_colors = max(1, min(num_colors, 10, area))
    palette = common.sample(list(range(10)), num_colors)
    colors = [palette[0]] * area
    foreground = palette[1:]
    if foreground:
      remaining = common.all_pixels(width, height)
      if density is None:
        for color in foreground:
          count = common.randint(1, max(1, len(remaining) // len(foreground)))
          cells = common.sample(remaining, count)
          for r, c in cells:
            colors[r * width + c] = color
          remaining = [cell for cell in remaining if cell not in cells]
      else:
        count = round(area * max(0, min(100, density)) / 100)
        count = max(len(foreground), min(area, count))
        cells = common.sample(common.all_pixels(width, height), count)
        for idx, (r, c) in enumerate(cells):
          colors[r * width + c] = foreground[idx % len(foreground)]

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c] = colors[r * width + c]
  output = common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 1, 1, 5, 1, 5, 2, 2]),
      generate(colors=[2, 2, 5, 6, 2, 2, 5, 5, 5]),
      generate(colors=[9, 9, 5, 5, 5, 8, 5, 8, 9]),
      generate(colors=[2, 6, 6, 2, 1, 1, 2, 6, 2]),
  ]
  test = [
      generate(colors=[9, 3, 4, 9, 4, 4, 9, 3, 4]),
  ]
  return {"train": train, "test": test}
