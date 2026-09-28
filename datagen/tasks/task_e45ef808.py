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


def generate(lengths=None, ncols=None, nrows=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: A list of lengths to use.
    ncols: Number of columns in the chart (default 12).
    nrows: Number of rows in the chart (default 12).
  """

  if lengths is None:
    if ncols is None:
      ncols = common.randint(8, 24)
    if nrows is None:
      nrows = common.randint(10, 20)
    max_length = nrows - 5
    min_distinct = min(5, max(3, ncols // 3))
    while True:
      length, lengths = common.randint(1, max_length), []
      for _ in range(ncols):
        lengths.append(length)
        # Adjust the column.
        length += common.randint(-1, 1)
        # Sometimes, adjust it even more.
        if common.randint(0, 9): length += common.randint(-1, 1)
        if length < 1: length = 1
        if length > max_length: length = max_length
      if len(set(lengths)) >= min_distinct: break
  else:
    if ncols is None:
      ncols = 12
    if nrows is None:
      nrows = 12

  # Input: a bar chart - each column holds a magenta bar rising from the bottom
  # to height lengths[c], on a blue field under a black top border row.
  grid = common.grid(ncols, nrows, common.blue())
  for c in range(ncols):
    grid[0][c] = common.black()
  for c, length in enumerate(lengths):
    for r in range(length):
      grid[nrows - 1 - r][c] = common.pink()

  # Output: the same chart, then the two extreme bars get highlighted - the
  # column above the tallest bar is filled yellow, the column above the
  # shortest bar is filled maroon.
  output = common.deepcopy(grid)

  def mark_tallest():
    """Fills the column above the rightmost-tallest bar with yellow."""
    pos = 0
    for c in range(ncols):
      if lengths[c] >= lengths[pos]: pos = c
    for r in range(1, nrows - lengths[pos]):
      output[r][pos] = common.yellow()

  def mark_shortest():
    """Fills the column above the leftmost-shortest bar with maroon."""
    pos = ncols - 1
    for c in range(ncols - 1, -1, -1):
      if lengths[c] <= lengths[pos]: pos = c
    for r in range(1, nrows - lengths[pos]):
      output[r][pos] = common.maroon()

  mark_tallest()
  mark_shortest()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[5, 4, 3, 3, 2, 3, 4, 5, 7, 6, 5, 4]),
      generate(lengths=[1, 2, 3, 2, 2, 3, 4, 5, 4, 3, 4, 5]),
  ]
  test = [
      generate(lengths=[3, 4, 4, 3, 4, 5, 6, 5, 4, 4, 3, 2]),
  ]
  return {"train": train, "test": test}
