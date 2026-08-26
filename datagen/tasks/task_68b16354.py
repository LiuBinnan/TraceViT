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


def generate(size=None, colors=None, color_list=(1, 2, 3, 4, 7, 8),
             height=None, width=None, num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: digits representing the colors to be used
    height: number of rows (defaults to size for a square grid)
    width: number of columns (defaults to size for a square grid)
  """
  if size is None:
    if height is None:
      height = common.randint(4, 8)
    if width is None:
      width = common.randint(4, 8)
    area = height * width
    if num_colors is None:
      num_colors = common.randint(0, min(9, area))
    num_colors = min(num_colors, 9, area)
    colors = [0 for _ in range(area)]
    if num_colors:
      palette = common.random_colors(num_colors, exclude=[0])
      cells = list(range(area))
      if density is None:
        for color in palette:
          if not cells:
            break
          count = min(len(cells),
                      common.randint(1, max(1, len(cells) // num_colors)))
          selected = common.sample(cells, count)
          for idx in selected:
            colors[idx] = color
          cells = [idx for idx in cells if idx not in selected]
      else:
        total = min(area, max(num_colors, area * density // 100))
        selected = common.sample(cells, total)
        for idx, cell in enumerate(selected):
          if idx < num_colors:
            colors[cell] = palette[idx]
          else:
            colors[cell] = palette[common.randint(0, num_colors - 1)]
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid, output = common.grids(width, height, 0)
  for r in range(height):
    for c in range(width):
      output[height - r - 1][c] = grid[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, colors=[8, 1, 2, 1, 4,
                               4, 4, 2, 4, 8,
                               3, 7, 2, 4, 8,
                               2, 7, 7, 8, 7,
                               8, 7, 7, 4, 8]),
      generate(size=5, colors=[7, 3, 3, 1, 2,
                               1, 8, 2, 4, 1,
                               2, 7, 8, 7, 2,
                               7, 7, 4, 1, 8,
                               8, 1, 7, 7, 1]),
      generate(size=7, colors=[2, 7, 4, 3, 4, 8, 3,
                               2, 3, 7, 1, 2, 3, 3,
                               8, 7, 4, 3, 2, 2, 4,
                               1, 1, 2, 1, 4, 4, 7,
                               2, 4, 3, 1, 1, 4, 1,
                               4, 8, 7, 4, 4, 8, 2,
                               7, 3, 8, 4, 3, 2, 8]),
  ]
  test = [
      generate(size=7, colors=[2, 8, 1, 3, 2, 4, 1,
                               4, 4, 1, 1, 4, 3, 4,
                               1, 1, 1, 1, 4, 7, 3,
                               1, 1, 2, 3, 8, 1, 3,
                               4, 1, 1, 1, 7, 8, 4,
                               3, 2, 8, 4, 1, 8, 4,
                               1, 4, 7, 1, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
