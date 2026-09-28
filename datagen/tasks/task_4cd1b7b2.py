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


def generate(colors=None, num_zeroes=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: colors of the pixels.
    num_zeroes: number of cells to strip from the completed Latin square.
    size: height and width of the Latin square.
  """

  def create_grid():
    rows = []
    for _ in range(size):
      while True:
        candidate = common.shuffle(list(range(1, size + 1)))
        good = True
        for row in rows:
          for c in range(size):
            if row[c] == candidate[c]: good = False
        if good: break
      rows.append(candidate)
    return rows

  def strip_grid(grid):
    num_zeroed = 0
    strips = common.shuffle([
        (cdir, val) for cdir in range(2) for val in range(size)
    ])
    for strip in strips:
      cdir, val = strip
      if cdir == 1 and sum([grid[val][r] for r in range(size)]) == total:
        grid[val][common.randint(0, size - 1)] = 0
        num_zeroed += 1
      if cdir == 0 and sum([grid[c][val] for c in range(size)]) == total:
        grid[common.randint(0, size - 1)][val] = 0
        num_zeroed += 1
      if num_zeroed == num_zeroes:
        break
    return num_zeroed

  if colors is None:
    if size is None:
      size = common.randint(4, 6)
    total = size * (size + 1) // 2
    if num_zeroes is None:
      num_zeroes = common.randint(size, size + 3)
    while True:
      grid = create_grid()
      if strip_grid(grid) == num_zeroes: break
    colors = []
    for row in grid:
      colors.extend(row)

  if size is None:
    size = 4
  total = size * (size + 1) // 2
  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  output = [row[:] for row in grid]

  def fill_forced_rows():
    """Fills row gaps when all other row values are known."""
    for r in range(size):
      values = [output[r][c] for c in range(size) if output[r][c] != 0]
      if len(values) != size - 1: continue
      value = total - sum(values)
      for c in range(size):
        if output[r][c] == 0: output[r][c] = value

  def fill_forced_columns():
    """Fills column gaps when all other column values are known."""
    for c in range(size):
      values = [output[r][c] for r in range(size) if output[r][c] != 0]
      if len(values) != size - 1: continue
      value = total - sum(values)
      for r in range(size):
        if output[r][c] == 0: output[r][c] = value

  fill_forced_rows()
  fill_forced_columns()
  fill_forced_rows()
  fill_forced_columns()
  fill_forced_rows()
  fill_forced_columns()
  fill_forced_rows()
  fill_forced_columns()
  for _ in range(2 * size):
    fill_forced_rows()
    fill_forced_columns()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 4, 2, 3, 4, 1, 0, 2, 0, 3, 4, 0, 3, 0, 1, 4]),
      generate(colors=[1, 0, 3, 4, 0, 0, 2, 1, 2, 1, 4, 0, 0, 3, 1, 2]),
      generate(colors=[3, 0, 2, 1, 1, 0, 0, 0, 4, 3, 0, 2, 0, 1, 4, 3]),
  ]
  test = [
      generate(colors=[0, 1, 2, 3, 0, 3, 1, 0, 3, 0, 4, 1, 0, 4, 0, 2]),
  ]
  return {"train": train, "test": test}
