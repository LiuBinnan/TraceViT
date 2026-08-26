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


_SIZE_INDEX = 0


def generate(rows=None, cols=None, color=None, width=4, height=3,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the folded grid
    height: the width of the folded grid
    num_colors: number of non-background colors to place in the folded grid
    density: number of folded-grid cells to color when explicitly varied
  """
  if rows is None:
    global _SIZE_INDEX
    if width == 4 and height == 3:
      size_index = _SIZE_INDEX % 225
      _SIZE_INDEX += 1
      height = size_index // 15 + 1
      width = size_index % 15 + 1
    area = width * height
    max_colors = min(9, area)
    rows, cols, colors = [], [], []
    cells = [(r, c) for r in range(height) for c in range(width)]
    if density is None:
      if num_colors is None:
        num_colors = common.randint(0, max_colors)
      num_colors = max(0, min(num_colors, max_colors))
      for pixel_color in common.random_colors(num_colors):
        count = common.randint(1, max(1, len(cells) // num_colors))
        pixels = common.sample(cells, count)
        for r, c in pixels:
          rows.append(r)
          cols.append(c)
          colors.append(pixel_color)
        cells = [cell for cell in cells if cell not in pixels]
    else:
      density = max(0, min(density, area))
      if num_colors is None:
        num_colors = common.randint(0 if density == 0 else 1,
                                    min(max_colors, density))
      num_colors = max(0, min(num_colors, max_colors, density))
      pixels = common.sample(cells, density if num_colors else 0)
      color_list = common.random_colors(num_colors)
      for idx, (r, c) in enumerate(pixels):
        rows.append(r)
        cols.append(c)
        colors.append(color_list[idx % num_colors])
  else:
    colors = [color] * len(rows)

  grid = common.grid(width, height)
  output = common.grid(2 * width, 2 * height)
  for r, c, pixel_color in zip(rows, cols, colors):
    grid[r][c] = pixel_color
  for r, c, pixel_color in zip(rows, cols, colors):
    output[r][c] = pixel_color
  for r, c, pixel_color in zip(rows, cols, colors):
    output[2 * height - r - 1][c] = pixel_color
  for r, c, pixel_color in zip(rows, cols, colors):
    output[r][2 * width - c - 1] = pixel_color
  for r, c, pixel_color in zip(rows, cols, colors):
    output[2 * height - r - 1][2 * width - c - 1] = pixel_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2], cols=[2, 1, 3, 2], color=8),
      generate(rows=[0, 0, 1, 1, 2, 2, 2], cols=[2, 3, 1, 3, 0, 1, 2], color=3),
      generate(rows=[0, 0, 0, 0, 1, 2], cols=[0, 1, 2, 3, 0, 0], color=3),
  ]
  test = [
      generate(rows=[0, 1, 2, 2], cols=[0, 3, 0, 1], color=4),
  ]
  return {"train": train, "test": test}
