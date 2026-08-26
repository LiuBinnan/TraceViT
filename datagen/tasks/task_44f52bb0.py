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


def generate(rows=None, cols=None, size=3, width=None, height=None, count=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    width: the randomized grid width; sampled 3..30 when omitted
    height: the randomized grid height; sampled 3..30 when omitted
    count: target number of painted cells before area clamping
    num_colors: number of foreground colors to draw from
    density: optional percent fill target, used with count when provided
  """
  if rows is None:
    if width is None:
      width = common.randint(3, 30)
    if height is None:
      height = common.randint(3, 30)
    width, height = max(3, min(30, width)), max(3, min(30, height))
    area = width * height
    if count is None:
      count = common.randint(1, area - 1)
    if density is not None:
      density_count = round(area * max(1, min(100, density)) / 100)
      count = max(count, density_count)
    count = max(1, min(area - 1, count))
    if num_colors is None:
      num_colors = common.randint(2, 9)
    num_colors = max(1, min(9, num_colors, count))
    colors = common.random_colors(num_colors)

    cells = common.sample(common.all_pixels(width, height), count)
    grid = common.grid(width, height)
    force_symmetric = common.randint(0, 1)
    mirror_vertical = common.randint(0, 1)
    for idx, (r, c) in enumerate(cells):
      color = colors[idx % num_colors]
      grid[r][c] = color
      if force_symmetric and mirror_vertical:
        grid[r][width - c - 1] = color
      if force_symmetric and not mirror_vertical:
        grid[height - r - 1][c] = color
  else:
    width = height = size
    grid = common.grid(width, height)
    for r, c in zip(rows, cols):
      grid[r][c] = common.red()

  vert, horiz = True, True
  for r in range(height):
    for c in range(width):
      vert = vert and grid[r][c] == grid[r][width - c - 1]
      horiz = horiz and grid[r][c] == grid[height - r - 1][c]
  output = common.grid(1, 1)
  symmetric = vert or horiz
  output[0][0] = common.blue() if symmetric else common.orange()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2]),
      generate(rows=[0, 1, 2], cols=[0, 0, 1]),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 2, 0, 2, 0, 2]),
      generate(rows=[1, 1], cols=[0, 2]),
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2]),
      generate(rows=[0, 0, 1], cols=[0, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[0, 2, 0, 1, 2, 0, 2]),
      generate(rows=[1, 2], cols=[0, 0]),
  ]
  return {"train": train, "test": test}
