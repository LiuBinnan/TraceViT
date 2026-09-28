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


def generate(colors=None, count=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    count: Minimum number of strokes used to construct the body.
    size: The height and width of the square grid.
  """

  if size is None:
    size = common.randint(8, 16)
  if colors is None:
    if count is None:
      count = 10
    legend = common.random_colors(4)
    while True:
      grid = common.grid(size, size)
      i = 0
      while i < count or len(set(common.flatten(grid))) < 5:
        color = common.choice(legend + [0])
        if common.randint(0, 1):
          row = common.randint(0, size - 3)
          length = common.randint(1, size - 4)
          col = common.randint(0, size - 4 - length)
          for c in range(col, col + length):
            grid[1 + row][2 + c] = color
        else:
          col = common.randint(0, size - 5)
          length = common.randint(1, size - 2)
          row = common.randint(0, size - 2 - length)
          for r in range(row, row + length):
            grid[1 + r][2 + col] = color
        i += 1
      if grid[0][2] or grid[1][2] or grid[2][2]: continue
      pixels = []
      for r in range(size):
        for c in range(size):
          if grid[r][c]: pixels.append((r, c))
      if common.connected(pixels): break
    grid[0][0] = legend[0]
    grid[0][1] = legend[1]
    grid[1][0] = legend[2]
    grid[1][1] = legend[3]
    colors = common.flatten(grid)

  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  output = common.deepcopy(grid)

  def replace_legend_color(src_row, src_col):
    """Replaces one legend color across the body with its paired color."""
    src = grid[src_row][src_col]
    dst_col = 1 - src_col
    dst = grid[src_row][dst_col]
    for r in range(size):
      for c in range(size):
        if r < 2 and c < 2: continue
        if grid[r][c] == src:
          output[r][c] = dst

  replace_legend_color(0, 0)
  replace_legend_color(0, 1)
  replace_legend_color(1, 0)
  replace_legend_color(1, 1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 8, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
                       0, 0, 3, 3, 3, 3, 1, 8, 0, 0,
                       0, 0, 3, 3, 2, 0, 8, 8, 0, 0,
                       0, 0, 0, 0, 2, 0, 8, 8, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[4, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       3, 7, 0, 0, 0, 0, 4, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 4, 4, 0, 0,
                       0, 0, 0, 0, 0, 3, 2, 4, 0, 0,
                       0, 0, 0, 7, 7, 3, 2, 4, 0, 0,
                       0, 0, 0, 7, 3, 3, 2, 0, 0, 0,
                       0, 0, 0, 7, 0, 0, 2, 2, 0, 0,
                       0, 0, 0, 7, 7, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[9, 4, 0, 0, 0, 0, 0, 0, 0, 0,
                       7, 6, 0, 0, 0, 9, 9, 0, 0, 0,
                       0, 0, 0, 0, 0, 7, 9, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 7, 4, 0, 0, 0, 0,
                       0, 0, 0, 6, 6, 7, 0, 0, 0, 0,
                       0, 0, 0, 7, 6, 6, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[8, 9, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 4, 0, 0, 0, 9, 9, 0, 0, 0,
                       0, 0, 0, 8, 8, 8, 9, 0, 0, 0,
                       0, 0, 0, 2, 8, 8, 9, 0, 0, 0,
                       0, 0, 0, 2, 4, 2, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 4, 0, 0, 0, 0,
                       0, 0, 0, 2, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 9, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  ]
  return {"train": train, "test": test}
