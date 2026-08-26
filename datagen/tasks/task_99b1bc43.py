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


def generate(rows=None, cols=None, size=4, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in each panel (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    top_pixels = common.random_pixels(width, height)
    bottom_pixels = common.random_pixels(width, height)
    top_rows, top_cols = zip(*top_pixels)
    bottom_rows, bottom_cols = zip(*bottom_pixels)
    bottom_rows = tuple([r + height + 1 for r in bottom_rows])
    rows, cols = top_rows + bottom_rows, top_cols + bottom_cols

  grid, output = common.grid(width, 2 * height + 1), common.grid(width, height)
  for c in range(width):
    grid[height][c] = common.yellow()
  for r, c in zip(rows, cols):
    grid[r][c] = common.blue() if r < height else common.red()

  for r, c in zip(rows, cols):
    if r < height:
      output[r][c] = (common.black() if output[r][c] != common.black()
                      else common.blue())
  for r, c in zip(rows, cols):
    if r > height:
      r -= height + 1
      if output[r][c] == common.blue():
        output[r][c] = common.gray()
      elif output[r][c] == common.gray():
        output[r][c] = common.blue()
      elif output[r][c] == common.red():
        output[r][c] = common.black()
      else:
        output[r][c] = common.red()
  for r in range(height):
    for c in range(width):
      if output[r][c] == common.gray():
        output[r][c] = common.black()
      elif output[r][c] != common.black():
        output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(
          rows=[0, 0, 1, 2, 2, 3, 5, 5, 6, 7, 7, 8, 8, 8],
          cols=[1, 3, 3, 0, 2, 3, 1, 3, 3, 0, 3, 0, 1, 2],
      ),
      generate(
          rows=[
              0,
              0,
              1,
              1,
              2,
              2,
              2,
              3,
              3,
              5,
              5,
              5,
              6,
              6,
              7,
              7,
              7,
              7,
              8,
              8,
              8,
              8,
          ],
          cols=[
              0,
              1,
              0,
              2,
              0,
              1,
              3,
              1,
              2,
              1,
              2,
              3,
              0,
              2,
              0,
              1,
              2,
              3,
              0,
              1,
              2,
              3,
          ],
      ),
      generate(
          rows=[0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 6, 6, 7, 7, 7, 8],
          cols=[1, 0, 2, 3, 0, 1, 2, 0, 1, 2, 1, 3, 0, 1, 3, 1],
      ),
      generate(
          rows=[0, 0, 0, 1, 2, 2, 3, 3, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8],
          cols=[0, 2, 3, 3, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 2, 3, 0, 1, 2, 3],
      ),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 5, 5, 5, 6, 7, 7, 8, 8],
               cols=[0, 2, 3, 1, 2, 3, 2, 0, 2, 3, 0, 1, 3, 2, 0, 3, 1, 3]),
  ]
  return {"train": train, "test": test}
