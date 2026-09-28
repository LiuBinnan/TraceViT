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


def generate(size=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    cols: The columns of the grey boxes.
    colors: The colors of the grid.
  """

  def column_final_color(col):
    color = 5
    for r in range(size - 1, -1, -1):
      if colors[r * size + col]: color = colors[r * size + col]
    return color

  def valid_columns():
    if not cols: return False
    return all(column_final_color(col) != 5 for col in cols)

  if size is None:
    size = common.randint(7, 30)
    while True:
      colors = [0] * (size * size)
      for row in range(size - 1):
        for col in range(size):
          if common.randint(0, 9): continue
          colors[row * size + col] = common.random_color(exclude=[5])
      col, cols = common.randint(2, 5), []
      while col + 3 < size:
        cols.append(col)
        col += common.randint(3, 5)
      if valid_columns(): break

  if not valid_columns(): return {"input": None, "output": None}
  grid, output = common.grids(size, size)

  def seed_input_and_output():
    """Seeds clues and keeps the gray bottom markers in intermediate frames."""
    for i, color in enumerate(colors):
      if not color: continue
      output[i // size][i % size] = grid[i // size][i % size] = color
    for col in cols:
      grid[size - 1][col] = 5
      if not output[size - 1][col]:
        output[size - 1][col] = 5

  def fill_column(index):
    """Marks one selected input column and fills its output colors upward."""
    if index >= len(cols): return
    col = cols[index]
    color = grid[size - 1][col] = 5
    for r in range(size - 1, -1, -1):
      if output[r][col]: color = output[r][col]
      else: output[r][col] = color

  def fill_gray_bases():
    """Extends gray upward below the lowest colored clue in each marked column."""
    for col in cols:
      for r in range(size - 1, -1, -1):
        if output[r][col] and output[r][col] != 5:
          break
        output[r][col] = 5

  seed_input_and_output()
  fill_gray_bases()
  fill_column(0)
  fill_column(1)
  fill_column(2)
  fill_column(3)
  fill_column(4)
  fill_column(5)
  fill_column(6)
  fill_column(7)
  fill_column(8)
  fill_column(9)
  fill_column(10)
  fill_column(11)
  fill_column(12)
  fill_column(13)
  fill_column(14)
  fill_column(15)
  fill_column(16)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, cols=[2, 8],
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(size=13, cols=[4, 8],
               colors=[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 6,
                       0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 2, 0,
                       0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 4, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 0, 0, 6, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(size=7, cols=[3],
               colors=[0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0]),
      generate(size=17, cols=[5, 9, 14],
               colors=[0, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 9, 0, 0, 0, 7, 0, 0, 0, 0, 0, 4, 0,
                       0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
                       7, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                       0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0,
                       6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 8, 0, 0, 0, 2, 0, 0, 0, 0, 7, 0, 0, 0, 6, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(size=17, cols=[5, 8, 11],
               colors=[0, 0, 0, 0, 2, 3, 0, 9, 0, 4, 0, 0, 0, 3, 0, 0, 8,
                       0, 0, 3, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 9, 4, 9, 0, 0,
                       0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 1, 0, 6, 0, 0, 0, 7,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 7, 0, 3, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0,
                       0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 1, 9, 0, 0, 0, 7, 0, 0, 1, 2, 0,
                       0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 4, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 6, 0, 0, 4, 9, 0, 3, 0, 3,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
