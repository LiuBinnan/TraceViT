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


def generate(colors=None, size=3, height=None, width=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: number of rows in the input grid (structural variation)
    width: number of columns in the input grid (structural variation)
    num_colors: number of distinct non-background colors to scatter
  """
  if colors is None:
    if height is None:
      height = common.randint(1, 15)
    if width is None:
      width = common.randint(1, 30)
    cells = height * width
    if num_colors is None:
      num_colors = common.randint(0, min(9, cells))
    num_colors = min(num_colors, 9, cells)
    palette = [common.black(), common.blue(), common.red(), common.green(),
               common.yellow(), common.gray(), common.pink(), common.orange(),
               common.cyan(), common.maroon()]
    background = palette[common.randint(0, len(palette) - 1)]
    foreground = [color for color in palette if color != background]
    colors = [background for _ in range(cells)]
    available = list(range(cells))
    for color in common.sample(foreground, num_colors):
      if not available:
        break
      num = common.randint(1, max(1, len(available) // num_colors))
      num = min(num, len(available))
      chosen = set(common.sample(available, num))
      for idx in chosen:
        colors[idx] = color
      available = [idx for idx in available if idx not in chosen]
    height_size, width_size = height, width
  else:
    height_size = width_size = size

  grid = common.grid(width_size, height_size)
  output = common.grid(width_size, 2 * height_size)
  for r in range(height_size):
    for c in range(width_size):
      color = colors[r * width_size + c]
      output[2 * height_size - r - 1][c] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 1, 4, 9, 1, 4, 2, 1, 1]),
      generate(colors=[4, 8, 4, 7, 6, 7, 8, 7, 8]),
      generate(colors=[7, 7, 7, 9, 5, 5, 5, 1, 7]),
      generate(colors=[2, 6, 9, 2, 6, 9, 2, 9, 2]),
  ]
  test = [
      generate(colors=[2, 9, 2, 8, 5, 2, 2, 2, 8]),
  ]
  return {"train": train, "test": test}
