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


def generate(row=None, col=None, boxcolor=None, colors=None, size=5,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a list of vertical coordinates where the box should be placed
    col: a list of horizontal coordinates where the box should be placed
    boxcolor: a digit representing a color to be used for the box
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if row is None:
    row, col = common.choice([(0, 1), (1, 0), (1, 1)])
    boxcolor = common.random_color(exclude=[common.red()])
    colors = [common.random_color(exclude=[common.red(), boxcolor])]
    # The output is the input upscaled by factor = distinct(colors) + 1, so the
    # number of distinct colors (driven by the widened dimension) must be capped
    # to keep every output dimension <= 30 (re_arc keeps factor*max(h,w) <= 30).
    max_distinct = max(1, min(9, 30 // max(height, width) - 1))
    for _ in range(max(height, width) - 1):
      if len(set(colors)) >= max_distinct:
        colors.append(colors[-1])
        continue
      color = common.random_color(
          exclude=[common.red(), boxcolor] + list(set(colors))
      )
      colors.append(color if common.randint(0, 1) else colors[-1])

  factor = len(set(colors)) + 1
  grid = common.grid(width, height)
  output = common.grid(width * factor, height * factor)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    grid[row + dr][col + dc] = boxcolor
    for ddr in range(factor):
      for ddc in range(factor):
        output[(row + dr) * factor + ddr][(col + dc) * factor + ddc] = boxcolor
  for idx, color in enumerate(colors):
    if idx < height:
      r, c = height - idx - 1, width - 1
      grid[r][c] = color
      for ddr in range(factor):
        for ddc in range(factor):
          output[r * factor + ddr][c * factor + ddc] = color
    if idx < width:
      r, c = height - 1, width - idx - 1
      grid[r][c] = color
      for ddr in range(factor):
        for ddc in range(factor):
          output[r * factor + ddr][c * factor + ddc] = color
  # Each red diagonal ray emanates outward from a corner of the (upscaled) box
  # region and extends until it leaves the grid or meets a non-background cell
  # (the box itself or a color block). This makes every ray reach the grid
  # border in open directions instead of stopping after a fixed `factor` cells.
  for sr, sc, dr, dc in [
      (row * factor - 1, col * factor - 1, -1, -1),       # toward NW corner
      (row * factor - 1, (col + 2) * factor, -1, +1),     # toward NE corner
      ((row + 2) * factor, col * factor - 1, +1, -1),     # toward SW corner
      ((row + 2) * factor, (col + 2) * factor, +1, +1),   # toward SE corner
  ]:
    r, c = sr, sc
    while (0 <= r < height * factor and 0 <= c < width * factor and
           output[r][c] == common.black()):
      output[r][c] = common.red()
      r, c = r + dr, c + dc
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, col=1, boxcolor=8, colors=[3, 3, 3, 3, 3]),
      generate(row=1, col=0, boxcolor=4, colors=[6, 6, 6, 7, 7]),
      generate(row=1, col=1, boxcolor=1, colors=[4, 3, 3, 9, 9]),
  ]
  test = [
      generate(row=0, col=1, boxcolor=6, colors=[9, 7, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
