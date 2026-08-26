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


def generate(rows=None, height=3, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    height: the height of grid
    width: the width of grid
    count: the maximum number of marked pixels per column
  """
  if rows is None:
    if width is None:
      width = common.randint(2, 30)
    max_count = max(1, height // 2)
    if count is not None:
      max_count = min(max_count, count)
    rows = []
    for _ in range(width):
      num_rows = common.randint(1, max_count)
      rows.append(common.sample(list(range(height)), num_rows))

  width = len(rows)
  grid, output = common.grids(width, height)
  for c, col_rows in enumerate(rows):
    if isinstance(col_rows, int):
      col_rows = [col_rows]
    for r in col_rows:
      grid[r][c] = common.gray()
      output[r][c] = common.green() if c % 2 != width % 2 else common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 0, 2, 1, 0, 2, 1, 2, 0]),
      generate(rows=[1, 0, 2, 0, 1, 2, 0, 1, 0, 2, 1, 2]),
      generate(rows=[1, 2, 0, 2, 1, 0, 1, 0, 2, 1, 2, 0, 1]),
      generate(rows=[1, 2, 0, 2, 1, 0, 2, 0, 1, 0, 1, 0, 2, 1]),
  ]
  test = [
      generate(rows=[1, 2, 1, 0, 2, 1, 2, 0, 1, 0, 2, 1, 0, 2, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
