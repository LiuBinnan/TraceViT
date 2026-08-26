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


def generate(width=None, height=None, megarows=None, megacols=None,
             megacolor=None, rows=None, cols=None, colors=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    megarows: a list of vertical coordinates where lasers should be placed
    megacols: a list of horizontal coordinates where lasers should be placed
    megacolor: the color to be used for laser pixels
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    num_colors: how many distinct noise (distractor) colors to scatter
    density: the fraction of grid cells to fill with noise
  """
  if rows is None:
    width, height = common.randint(15, 25), common.randint(10, 20)
    area = width * height
    # noise colors: re_arc samples 1..7 distinct distractor colors
    if num_colors is None:
      num_colors = common.randint(1, 7)
    palette = common.random_colors(num_colors + 1)
    noise_palette, megacolor = palette[:num_colors], palette[num_colors]
    # noise density: re_arc scatters up to a third of the grid with noise
    if density is None:
      density = common.randint(1, max(1, area // 3)) / area
    num_noise = min(area, max(1, int(round(density * area))))
    scatter = common.sample(
        [(r, c) for r in range(height) for c in range(width)], num_noise)
    placed = {}
    for r, c in scatter:
      placed[(r, c)] = noise_palette[common.randint(0, num_colors - 1)]
    # seed one interior cell per noise color: guarantees every noise color is
    # present (pins the color count) and can never be mistaken for the laser
    # color, which the rule reads off as the color living only on the border
    interior = [(r, c) for r in range(1, height - 1)
                for c in range(1, width - 1)]
    for (r, c), color in zip(common.sample(interior, num_colors),
                             noise_palette):
      placed[(r, c)] = color
    items = list(placed.items())
    rows = [rc[0] for rc, _ in items]
    cols = [rc[1] for rc, _ in items]
    colors = [color for _, color in items]
    # lasers: re_arc places up to (h-2)//2 horizontal and (w-2)//2 vertical
    num_h = common.randint(0, (height - 2) // 2)
    num_v = common.randint(0, (width - 2) // 2)
    if num_h + num_v < 2:  # the rule's instances always show at least two
      num_v = min((width - 2) // 2, 2 - num_h)
    megarows = common.sample(list(range(1, height - 1)), num_h)
    megacols = common.sample(list(range(1, width - 1)), num_v)

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  for r in megarows:
    grid[r][0] = grid[r][width - 1] = megacolor
    for c in range(width):
      output[r][c] = megacolor
  for c in megacols:
    grid[0][c] = grid[height - 1][c] = megacolor
    for r in range(height):
      output[r][c] = megacolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=11, megarows=[8], megacols=[11], megacolor=3,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                     5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 8, 8, 8, 8, 8, 9, 9,
                     9, 9, 9, 10, 10, 10, 10],
               cols=[5, 6, 17, 0, 6, 13, 6, 7, 9, 10, 12, 18, 4, 5, 14, 20, 0,
                     3, 5, 14, 3, 7, 10, 18, 20, 2, 9, 10, 13, 19, 20, 13, 18,
                     3, 4, 6, 7, 20, 9, 11, 12, 14, 18, 2, 8, 17, 19],
               colors=[2, 2, 2, 2, 2, 2, 5, 2, 5, 2, 5, 2, 5, 5, 2, 2, 5, 2, 2,
                       2, 2, 2, 2, 2, 5, 2, 5, 5, 5, 2, 5, 2, 2, 5, 5, 2, 5, 2,
                       2, 2, 5, 5, 2, 2, 5, 5, 5]),
      generate(width=20, height=13, megarows=[3, 11], megacols=[], megacolor=2,
               rows=[0, 1, 1, 2, 2, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8, 9, 9, 11, 11,
                     12, 12],
               cols=[5, 10, 12, 8, 12, 17, 18, 5, 8, 11, 13, 1, 4, 13, 14, 14,
                     19, 8, 11, 0, 17],
               colors=[8, 8, 1, 1, 1, 8, 1, 1, 1, 1, 8, 8, 8, 8, 1, 8, 1, 8, 1,
                       8, 8]),
      generate(width=17, height=15, megarows=[10], megacols=[13], megacolor=8,
               rows=[0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7,
                     7, 8, 9, 9, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 14,
                     14],
               cols=[1, 2, 7, 15, 2, 4, 14, 16, 0, 3, 4, 8, 7, 8, 16, 1, 5, 10,
                     14, 15, 16, 12, 6, 11, 0, 14, 1, 12, 15, 6, 8, 15, 0, 2, 4,
                     8, 9],
               colors=[4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 5, 4, 5, 4, 4,
                       5, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5]),
  ]
  test = [
      generate(width=19, height=16, megarows=[5], megacols=[3], megacolor=6,
               rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 4, 5, 5, 5, 6, 6, 6, 6, 7,
                     7, 7, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 14, 14, 15,
                     15, 15, 15],
               cols=[12, 16, 17, 0, 6, 9, 15, 1, 6, 15, 16, 11, 10, 16, 17, 1,
                     8, 10, 12, 3, 6, 8, 10, 12, 14, 18, 4, 10, 15, 18, 9, 17,
                     18, 12, 13, 0, 4, 6, 7],
               colors=[7, 7, 8, 7, 8, 8, 7, 7, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 8,
                       8, 7, 7, 7, 8, 8, 7, 7, 7, 7, 7, 7, 8, 7, 7, 8, 7, 7, 8,
                       7]),
  ]
  return {"train": train, "test": test}
