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


def generate(colors=None, nrows=None, ncols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    nrows: Number of block-rows in the panel (default 2).
    ncols: Number of block-columns in the panel (default 3).
  """

  if colors is None:
    if nrows is None:
      nrows = common.randint(2, 4)
    if ncols is None:
      ncols = common.randint(2, 4)
    grid = common.grid(3 * ncols + 1, 4 * nrows + 1)
    for row in range(nrows):
      for col in range(ncols):
        subset = common.random_colors(2)
        while True:
          block = common.choices(subset, 6)
          if block.count(subset[0]) in [1, 2]: break
        for r in range(3):
          for c in range(2):
            grid[row * 4 + 1 + r][col * 3 + 1 + c] = block[r * 2 + c]
    colors = common.flatten(grid)
  else:
    if nrows is None:
      nrows = 2
    if ncols is None:
      ncols = 3

  width = 3 * ncols + 1
  grid = common.grid(width, 4 * nrows + 1)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color

  # Bookkeeping (no randomness): the dominant color of each 3x2 block, walked in
  # the block layout order (nrows block-rows x ncols block-cols).
  blocks = []
  for row in range(nrows):
    for col in range(ncols):
      cell_colors = []
      for r in range(3):
        for c in range(2):
          cell_colors.append(grid[row * 4 + 1 + r][col * 3 + 1 + c])
      counts = {c: cell_colors.count(c) for c in cell_colors}
      blocks.append((row, col, max(counts, key=counts.get)))

  output = common.deepcopy(grid)

  def erase_noise():
    """Filters each block down to its dominant color by clearing the minority."""
    nonlocal output
    for row, col, majority in blocks:
      for r in range(3):
        for c in range(2):
          if grid[row * 4 + 1 + r][col * 3 + 1 + c] != majority:
            output[row * 4 + 1 + r][col * 3 + 1 + c] = common.black()

  erase_noise()

  output = common.grid(ncols + 2, nrows + 2)

  def read_row(band):
    """Summarizes block-row `band` into the answer grid, one dominant color/cell."""
    nonlocal output
    for row, col, majority in blocks:
      if row == band:
        output[row + 1][col + 1] = majority

  read_row(0)
  read_row(1)
  for band in range(2, nrows):
    read_row(band)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 0, 5, 5, 0, 4, 4, 0,
                       0, 1, 1, 0, 3, 3, 0, 4, 4, 0,
                       0, 3, 3, 0, 5, 5, 0, 4, 8, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 7, 1, 0, 9, 9, 0,
                       0, 2, 2, 0, 7, 7, 0, 1, 9, 0,
                       0, 2, 2, 0, 7, 1, 0, 9, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 6, 6, 0, 9, 7, 0,
                       0, 8, 3, 0, 6, 3, 0, 9, 7, 0,
                       0, 3, 8, 0, 3, 6, 0, 7, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 2, 2, 0, 6, 1, 0,
                       0, 2, 3, 0, 5, 5, 0, 1, 1, 0,
                       0, 2, 3, 0, 5, 5, 0, 1, 6, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 5, 0, 8, 4, 0, 7, 7, 0,
                       0, 5, 3, 0, 8, 8, 0, 7, 6, 0,
                       0, 3, 3, 0, 8, 4, 0, 6, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 2, 2, 0, 1, 3, 0,
                       0, 4, 3, 0, 2, 2, 0, 1, 1, 0,
                       0, 3, 3, 0, 1, 2, 0, 1, 3, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 0, 3, 3, 0, 4, 4, 0,
                       0, 3, 1, 0, 8, 3, 0, 4, 4, 0,
                       0, 1, 1, 0, 3, 8, 0, 8, 4, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 3, 5, 0, 2, 2, 0,
                       0, 6, 6, 0, 5, 5, 0, 2, 2, 0,
                       0, 2, 2, 0, 5, 3, 0, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
