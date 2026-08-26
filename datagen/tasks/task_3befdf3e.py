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


def generate(size=None, rows=None, cols=None, lengths=None, colors=None,
             height=None, width=None, object_count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: the lengths of the flower centers
    colors: two digits representing the colors to be used
    height: the number of rows of the grid (independent of width)
    width: the number of columns of the grid (independent of height)
    object_count: the target number of flower objects to place
    num_colors: the number of foreground colors to sample
  """
  if size is None:
    if height is None: height = common.randint(10, 30)
    if width is None: width = common.randint(10, 30)
    if num_colors is None: num_colors = common.randint(2, 9)
    if object_count is None:
      object_count = common.randint(1, max(1, height * width // 40))
    colors = common.random_colors(num_colors)
    rows, cols, lengths = [], [], []
    color_pairs = []
    occupied = set()
    attempts = 0
    while len(rows) < object_count and attempts < 5 * object_count:
      attempts += 1
      length = common.randint(1, 2)
      row = common.randint(length + 1, height - length * 2 - 1)
      col = common.randint(length + 1, width - length * 2 - 1)
      full_object = set()
      for r in range(row - length - 1, row + 2 * length + 1):
        for c in range(col - length - 1, col + 2 * length + 1):
          full_object.add((r, c))
      if occupied.intersection(full_object): continue
      rows.append(row)
      cols.append(col)
      lengths.append(length)
      color_pairs.append(common.sample(colors, 2))
      occupied.update(full_object)
  else:
    height = width = size
    color_pairs = [colors for _ in rows]

  grid = common.grid(width, height)
  for row, col, length, color_pair in zip(rows, cols, lengths, color_pairs):
    for r in range(row - 1, row + length + 1):
      for c in range(col - 1, col + length + 1):
        grid[r][c] = color_pair[1]
    for r in range(row, row + length):
      for c in range(col, col + length):
        grid[r][c] = color_pair[0]
  output = common.deepcopy(grid)
  for row, col, length, color_pair in zip(rows, cols, lengths, color_pairs):
    for r in range(row - 1, row + length + 1):
      for c in range(col - 1, col + length + 1):
        output[r][c] = color_pair[0]
    for r in range(row, row + length):
      for c in range(col, col + length):
        output[r][c] = color_pair[1]
  for row, col, length, color_pair in zip(rows, cols, lengths, color_pairs):
    for r in range(row - length - 1, row + 2 * length + 1):
      for c in range(col - length - 1, col + 2 * length + 1):
        if r < row - 1 or r > row + length:  # skip the corners
          if c < col - 1 or c > col + length:
            continue
        if row - 1 <= r <= row + length and col - 1 <= c <= col + length:
          continue
        output[r][c] = color_pair[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[4], cols=[4], lengths=[1], colors=[6, 4]),
      generate(size=10, rows=[4], cols=[4], lengths=[2], colors=[7, 2]),
      generate(size=10, rows=[4], cols=[3], lengths=[2], colors=[1, 3]),
  ]
  test = [
      generate(size=12, rows=[2, 7], cols=[2, 7], lengths=[1, 2],
               colors=[3, 8]),
  ]
  return {"train": train, "test": test}
