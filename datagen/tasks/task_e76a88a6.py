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


def generate(width=None, height=None, colors=None, rows=None, cols=None,
             size=10, grid_height=None, grid_width=None, num_sprites=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the *sprite*
    height: the height of the *sprite*
    colors: a list of digits representing colors to be used
    rows: a list of vertical coordinates where the sprites should live
    cols: a list of horizontal coordinates where the sprites should live
    size: the size of the grid
    grid_height: the number of rows of the grid (defaults to size)
    grid_width: the number of columns of the grid (defaults to size)
    num_sprites: the total number of source/copy sprites to place
    num_colors: the number of distinct source colors
  """
  if grid_height is None: grid_height = size
  if grid_width is None: grid_width = size
  if width is None:
    while True:
      width, height = common.randint(3, 4), common.randint(3, 4)
      if width < 4 or height < 4: break
    num_pixels = width * height
    if num_sprites is None:
      count_cap = max(1, (grid_width * grid_height) // num_pixels // 2)
      num_sprites = common.randint(3, count_cap + 1)
    if num_colors is None:
      num_colors = common.randint(2, min(8, num_pixels))
    num_colors = max(2, min(8, num_colors, num_pixels))
    color_list = common.random_colors(num_colors, exclude=[common.gray()])
    colors = color_list[:]
    while len(colors) < num_pixels:
      colors.append(color_list[common.randint(0, num_colors - 1)])
    colors = common.shuffle(colors)
    locs = [(r, c) for r in range(grid_height - height + 1)
            for c in range(grid_width - width + 1)]
    rows, cols = [], []
    for row, col in common.shuffle(locs):
      if common.overlaps(rows + [row], cols + [col],
                         [width] * (len(rows) + 1),
                         [height] * (len(rows) + 1), spacing=1):
        continue
      rows.append(row)
      cols.append(col)
      if len(rows) >= num_sprites: break

  grid = common.grid(grid_width, grid_height)
  for idx in range(len(rows)):
    for r in range(height):
      for c in range(width):
        color = colors[r * width + c]
        grid[rows[idx] + r][cols[idx] + c] = common.gray() if idx > 0 else color
  output = [row[:] for row in grid]

  def recolor_copies(i):
    palette = sorted(set(colors))
    if i >= len(palette): return
    targets = palette[i:] if i == 1 else [palette[i]]
    for idx in range(1, len(rows)):
      for r in range(height):
        for c in range(width):
          if colors[r * width + c] not in targets: continue
          output[rows[idx] + r][cols[idx] + c] = colors[r * width + c]

  recolor_copies(0)
  recolor_copies(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, colors=[2, 2, 2, 2, 4, 4, 4, 4, 4],
               rows=[1, 4, 7], cols=[1, 6, 2]),
      generate(width=4, height=3, colors=[6, 6, 6, 6, 8, 8, 6, 8, 6, 8, 8, 8],
               rows=[1, 0, 5], cols=[1, 6, 4]),
  ]
  test = [
      generate(width=3, height=4, colors=[4, 4, 4, 1, 4, 4, 1, 4, 1, 1, 1, 1],
               rows=[0, 1, 5, 6], cols=[1, 6, 2, 7]),
  ]
  return {"train": train, "test": test}
