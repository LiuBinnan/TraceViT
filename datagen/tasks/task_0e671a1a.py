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


def generate(rows=None, cols=None, size=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    size: The width and height of the square grid.
    count: The number of colored points in the connector chain.
  """

  if rows is None:
    size = 13 if size is None else size
    count = 3 if count is None else count
    rows = common.sample(range(1, size - 1), count)
    cols = common.sample(range(1, size - 1), count)

  grid = common.grid(13 if size is None else size,
                     13 if size is None else size)
  for i in range(3 if count is None else count):
    grid[rows[i]][cols[i]] = (2, 3, 4, 6, 7, 8, 9)[i]
  output = common.deepcopy(grid)

  def connect_points(left, right, remaining=()):
    """Draws the horizontal-then-vertical gray path between two points."""
    pairs = [(left, right)]
    for next_point in remaining:
      pairs.append((pairs[-1][1], next_point))
    for left, right in pairs:
      row, col = rows[left], cols[left]
      col_diff = 1 if cols[right] > cols[left] else -1
      while col != cols[right]:
        col += col_diff
        output[row][col] = common.gray()
      row_diff = 1 if rows[right] > rows[left] else -1
      while row != rows[right]:
        output[row][col] = common.gray()
        row += row_diff

  connect_points(0, 2)
  connect_points(2, 1, range(3, 3 if count is None else count))
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[10, 4, 1], cols=[5, 11, 1]),
      generate(rows=[8, 1, 10], cols=[11, 5, 2]),
      generate(rows=[5, 11, 1], cols=[2, 9, 10]),
      generate(rows=[2, 11, 6], cols=[1, 3, 10]),
  ]
  test = [
      generate(rows=[5, 11, 2], cols=[1, 7, 10]),
  ]
  return {"train": train, "test": test}
