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


def generate(rows=None, cols=None, heights=None, colors=None, size=10,
             height=None, width=None, count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    heights: a list of heights for the different boxes
    colors: digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: number of boxes to attempt to place
    num_colors: number of non-blue foreground colors to sample
  """
  gh = size if height is None else height
  gw = size if width is None else width
  if rows is None:
    if count is None:
      count = common.randint(1, max(1, (gh * gw) // 25))
    if num_colors is None:
      num_colors = common.randint(2, 8)
    palette = common.random_colors(num_colors, exclude=[common.blue()])
    rows, cols, heights, colors = [], [], [], []
    blocked = set()
    tries = 0
    max_tries = 5 * count
    while len(rows) < count and tries < max_tries:
      tries += 1
      box_height = common.randint(4, 6)
      if gh < box_height or gw < 5:
        break
      row = common.randint(0, gh - box_height)
      col = common.randint(0, gw - 5)
      footprint = set()
      for r in range(row, row + box_height):
        for c in range(col, col + 5):
          footprint.add((r, c))
      if footprint & blocked:
        continue
      rows.append(row)
      cols.append(col)
      heights.append(box_height)
      colors.append(palette[len(colors) % len(palette)])
      for r in range(row - 1, row + box_height + 1):
        for c in range(col - 1, col + 6):
          if 0 <= r < gh and 0 <= c < gw:
            blocked.add((r, c))

  grid, output = common.grids(gw, gh)
  for row, col, height, color in zip(rows, cols, heights, colors):
    grid[row + height // 2][col + 2] = color
    for r in range(row, row + height):
      for c in range(col, col + 5):
        if (r == row + 1 and c != col + 2) or r == row + height - 1:
          grid[r][c] = common.blue()
      if r == row: continue
      for c in [col, col + 4]:
        grid[r][c] = common.blue()
  output = common.deepcopy(grid)
  for row, col, height, color in zip(rows, cols, heights, colors):
    for r in range(row + 1, row + height - 1):
      for c in range(col + 1, col + 4):
        if output[r][c] != common.blue():
          output[r][c] = color
  for row, col, height, color in zip(rows, cols, heights, colors):
    for r in range(row, row + height):
      for c in range(col, col + 5):
        output[r][c] = color
        if (r == row + 1 and c != col + 2) or r == row + height - 1:
          output[r][c] = common.blue()
      if r == row: continue
      for c in [col, col + 4]:
        output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0], cols=[1], heights=[6], colors=[2]),
      generate(rows=[1, 6], cols=[1, 4], heights=[5, 4], colors=[2, 3]),
      generate(rows=[0, 6], cols=[1, 4], heights=[5, 4], colors=[6, 8]),
  ]
  test = [
      generate(rows=[0, 5], cols=[0, 4], heights=[5, 5], colors=[4, 7]),
  ]
  return {"train": train, "test": test}
