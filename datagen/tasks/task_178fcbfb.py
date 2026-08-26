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
             red_count=None, blue_count=None, green_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    colors: a list of digits representing the color of each pixel
    rows: a list of vertical coordinates where centers should be placed
    cols: a list of horizontal coordinates where centers should be placed
    red_count: the number of red vertical-line markers
    blue_count: the number of blue horizontal-line markers
    green_count: the number of green horizontal-line markers
  """
  if width is None or height is None or colors is None or rows is None or cols is None:
    if width is None:
      width = common.randint(3, 30)
    if height is None:
      height = common.randint(3, 30)
    if colors is None:
      if red_count is None:
        red_count = common.randint(1, width)
      if blue_count is None:
        blue_count = common.randint(1, max(1, height // 2))
      if green_count is None:
        green_count = common.randint(1, max(1, height // 2))
      red_count = min(red_count, width)
      blue_count = min(blue_count, max(1, height // 2))
      green_count = min(green_count, max(1, height // 2))
      colors = [2 for _ in range(red_count)]
      colors.extend([1 for _ in range(blue_count)])
      colors.extend([3 for _ in range(green_count)])
    if rows is None or cols is None:
      rows, cols = [], []
      red_count = colors.count(2)
      blue_count = colors.count(1)
      green_count = colors.count(3)
      red_cols = common.sample(range(width), min(red_count, width))
      occupied = set()
      row_counts = [0 for _ in range(height)]
      for col in red_cols:
        choices = [r for r in range(height) if row_counts[r] < width - 1]
        row = common.choice(choices)
        row_counts[row] += 1
        rows.append(row)
        cols.append(col)
        occupied.add((row, col))
      horizontal_rows = common.sample(range(height), min(blue_count + green_count, height))
      rows.extend(horizontal_rows[:blue_count])
      for row in horizontal_rows[:blue_count]:
        choices = [c for c in range(width) if (row, c) not in occupied]
        col = common.choice(choices)
        cols.append(col)
        occupied.add((row, col))
      rows.extend(horizontal_rows[blue_count:])
      for row in horizontal_rows[blue_count:]:
        choices = [c for c in range(width) if (row, c) not in occupied]
        col = common.choice(choices)
        cols.append(col)
        occupied.add((row, col))

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
  for r, c, color in zip(rows, cols, colors):
    if color == 2:  # red lines go up
      for i in range(height):
        output[i][c] = 2
  for r, c, color in zip(rows, cols, colors):
    if color == 1:  # blue lines go across
      for i in range(width):
        output[r][i] = color
  for r, c, color in zip(rows, cols, colors):
    if color == 3:  # green lines go across
      for i in range(width):
        output[r][i] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, colors=[2, 1, 3], rows=[2, 6, 4],
               cols=[2, 3, 7]),
      generate(width=8, height=10, colors=[2, 1, 3, 3], rows=[7, 6, 1, 4],
               cols=[5, 1, 1, 3]),
      generate(width=11, height=10, colors=[2, 2, 1, 3, 3],
               rows=[8, 9, 1, 3, 6], cols=[3, 9, 1, 8, 2]),
  ]
  test = [
      generate(width=11, height=12, colors=[2, 2, 1, 1, 3, 3],
               rows=[1, 5, 7, 9, 0, 3], cols=[9, 4, 1, 8, 3, 5]),
  ]
  return {"train": train, "test": test}
