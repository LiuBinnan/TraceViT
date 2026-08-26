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


def generate(size=None, rows=None, cols=None, lengths=None, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths
    height: number of rows (defaults to size when omitted)
    width: number of columns (defaults to size when omitted)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if size is None and rows is None:
    if height is None:
      height = common.randint(5, 10)
    if width is None:
      width = common.randint(5, 10)
    rows, cols, lengths = [], [], []
    r = common.randint(0, 1)
    while r < height and len(rows) < 5:
      length = 2 * common.randint(1, (width // 2) - 1) + 1
      c = common.randint(0, width - length)
      rows.append(r)
      cols.append(c)
      lengths.append(length)
      rand = common.randint(0, 9)
      if rand in [0]:
        r += 1
      elif rand in [1, 2, 3]:
        r += 3
      else:
        r += 2

  grid, output = common.grids(width, height)
  for r, c, length in zip(rows, cols, lengths):
    for x in range(length):
      if x % 2 == 0:
        grid[r][c + x] = common.blue()
  output = [row[:] for row in grid]
  line_specs = list(zip(rows, cols, lengths))

  def fill_line(line_idx):
    if line_idx >= len(line_specs):
      return
    r, c, length = line_specs[line_idx]
    for x in range(length):
      output[r][c + x] = common.blue() if x % 2 == 0 else common.red()

  fill_line(0)
  fill_line(1)
  fill_line(2)
  fill_line(3)
  fill_line(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0, 3], cols=[0, 1], lengths=[3, 3]),
      generate(size=10, rows=[1, 4, 6, 8], cols=[1, 2, 6, 3],
               lengths=[7, 3, 3, 3]),
      generate(size=10, rows=[1, 2, 5, 7, 9], cols=[6, 1, 3, 4, 1],
               lengths=[3, 3, 5, 3, 3]),
  ]
  test = [
      generate(size=10, rows=[0, 2, 4, 5, 7], cols=[1, 2, 1, 5, 3],
               lengths=[3, 7, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
