# Copyright 2026 Google LLC
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


def generate(heights=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    heights: The heights of the lines.
    colors: The colors of the lines.
    gsize: The side length of the (square) canvas. When omitted it is sampled;
      when explicit heights are given it is derived from them so validate()
      stays byte-identical.
  """

  if heights is None:
    if gsize is None:
      gsize = common.randint(8, 16)
    heights, colors = [], []
    while len(heights) <= gsize:
      wide = common.choice([1, 1, 1, 1, 1, 2, 3, 3, 3, 6])
      wide = min(wide, gsize - len(heights))
      tall = 1
      if wide <= 3: tall = common.randint(1, 2)
      if wide <= 1: tall = common.randint(1, 3)
      # A wider canvas can fit more bar groups than there are bar colors
      # (random_color draws from {1..9}\{7,8} = 7 colors). Stop opening new
      # groups once the palette is exhausted, otherwise random_color would draw
      # from an empty pool and crash. Never fires on the 8-wide canvas.
      if len(set(colors) - {7, 8}) >= 7:
        break
      color = common.random_color(exclude=colors + [7, 8])
      talls = [tall] * wide
      if wide >= 2 and tall >= 2:  # Trim one or both corners.
        cols = common.sample([0, -1], common.randint(1, 2))
        for col in cols:
          talls[col] -= 1
      heights.extend(talls)
      colors.extend([color] * wide)
      #  Add some space between us and the next shape.
      for _ in range(common.randint(1, 2)):
        heights.append(0)
        colors.append(8)
    # Hack to trim values or extend them.
    while len(heights) < gsize:
      heights.append(0)
      colors.append(8)
    while len(heights) > gsize:
      heights.pop()
      colors.pop()

  gsize = len(heights)

  grid, output = common.grids(gsize, gsize, 7)
  for c in range(gsize):
    output[gsize - 1][c] = grid[gsize - 1][c] = 8
  color_to_count = {}
  for col, height in enumerate(heights):
    color = colors[col]
    for r in range(gsize - 1 - height, gsize - 1):
      grid[r][col] = color
    if color not in color_to_count: color_to_count[color] = 0
    color_to_count[color] += height
  # Build the output forward: start from the input, then float each color's
  # bars straight up by that color's total cell count, one color at a time.
  # (Random generation yields at most 4 distinct bar colors on the original
  # 8-wide canvas; a widened canvas can fit up to 7, so a catch-all loop after
  # the unrolled calls lifts any remaining groups.)
  output = common.deepcopy(grid)

  order = []
  for col in range(gsize):
    if colors[col] != 8 and colors[col] not in order:
      order.append(colors[col])

  def lift_color(k):
    """Floats color-group k's bars straight up by its total cell count."""
    nonlocal output
    if k >= len(order): return
    color = order[k]
    count = color_to_count[color]
    for col in range(gsize):
      if colors[col] != color: continue
      for r in range(gsize - 1 - heights[col], gsize - 1):
        output[r][col] = 7
    for col in range(gsize):
      if colors[col] != color: continue
      for r in range(gsize - 1 - heights[col], gsize - 1):
        output[r - count][col] = color

  lift_color(0)
  lift_color(1)
  lift_color(2)
  lift_color(3)
  for k in range(4, len(order)):
    lift_color(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(heights=[1, 2, 1, 0, 0, 1, 1, 1], colors=[9, 9, 9, 8, 8, 2, 2, 2]),
      generate(heights=[0, 2, 0, 3, 0, 1, 0, 2], colors=[8, 2, 8, 9, 8, 1, 8, 3]),
      generate(heights=[2, 2, 1, 0, 1, 2, 0, 3], colors=[1, 1, 1, 8, 3, 3, 8, 4]),
  ]
  test = [
      generate(heights=[1, 1, 1, 1, 1, 1, 0, 1], colors=[5, 5, 5, 5, 5, 5, 8, 6]),
  ]
  return {"train": train, "test": test}
