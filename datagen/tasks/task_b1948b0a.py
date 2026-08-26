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


def generate(width=None, height=None, rows=None, cols=None,
             count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  The rule recolors the pink(6) background to red(2) and leaves every other
  cell untouched (oracle: replace(input, 6, 2)). Any foreground color except
  pink(6) and the reserved output red(2) is therefore legal and passes through.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    count: number of foreground (non-background) pixels; area-scaled when None
    num_colors: number of distinct foreground colors to use; random when None
  """
  pixel_colors = None
  if width is None:
    # Independent height/width draws widen the output-size tail, mirroring
    # re_arc's h, w in [2, 30]; every grid stays <= 30x30.
    width = common.randint(2, 30)
    height = common.randint(2, 30)
    area = width * height
    # Area-scaled foreground count (re_arc: unifint(0, h*w//2)); >= 1 so there
    # is always at least one placed pixel, and <= area//2 so the pink
    # background stays the majority color.
    if count is None:
      count = common.randint(1, max(1, area // 2))
    count = max(1, min(count, area))
    all_cells = [(r, c) for r in range(height) for c in range(width)]
    pixels = common.sample(all_cells, count)
    rows, cols = zip(*pixels)
    # Sample how many distinct foreground colors appear. Foreground may be any
    # color except pink(6) (the recolored background) and red(2) (the reserved
    # output color); mirrors re_arc's cols = remove(6, ...).
    palette = [c for c in range(10)
               if c not in (common.pink(), common.red())]
    if num_colors is None:
      num_colors = common.randint(1, min(len(palette), count))
    num_colors = max(1, min(num_colors, len(palette), count))
    chosen = common.sample(palette, num_colors)
    pixel_colors = list(chosen)  # guarantee every chosen color is used
    while len(pixel_colors) < count:
      pixel_colors.append(chosen[common.randint(0, num_colors - 1)])

  if pixel_colors is None:
    pixel_colors = [common.orange()] * len(rows)

  grid = common.grid(width, height, common.pink())
  output = common.grid(width, height, common.red())
  for r, c, color in zip(rows, cols, pixel_colors):
    output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, rows=[0, 1, 1, 2, 2, 2],
               cols=[2, 2, 3, 0, 1, 3]),
      generate(width=4, height=6,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5],
               cols=[0, 1, 2, 2, 0, 1, 3, 0, 2, 3, 0, 2, 3]),
      generate(width=6, height=3,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 1, 3, 4, 5, 0, 2, 3, 5]),
  ]
  test = [
      generate(width=4, height=4,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 3],
               cols=[1, 2, 1, 3, 0, 1, 2, 0, 2]),
  ]
  return {"train": train, "test": test}
