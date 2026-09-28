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


def generate(colors=None, target_lines=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    target_lines: The number of uniform rows/columns to create.
  """

  def make_grid():
    grid = common.grid(3, 3)
    for i, color in enumerate(colors):
      grid[i // 3][i % 3] = color
    return grid

  def find_targets(grid):
    rows, cols = [], []
    for r in range(3):
      if len(set([grid[r][c] for c in range(3)])) == 1: rows.append(r)
    for c in range(3):
      if len(set([grid[r][c] for r in range(3)])) == 1: cols.append(c)
    if len(rows) > 1 or len(cols) > 1: return None
    if len(rows) == 0 and len(cols) == 0: return None
    return [(row, col) for row in range(3) for col in range(3)
            if row in rows or col in cols]

  if colors is None:
    hues = common.random_colors(3)
    if target_lines == 2:
      target_row = common.randint(0, 2)
      target_col = common.randint(0, 2)
      other_colors = common.shuffle([hues[1]] * 2 + [hues[2]] * 2)
      colors = []
      for r in range(3):
        for c in range(3):
          if r == target_row or c == target_col:
            colors.append(hues[0])
          else:
            colors.append(other_colors.pop())
    else:
      while True:
        colors = common.shuffle([hues[0]] * 3 + [hues[1]] * 3 + [hues[2]] * 3)
        grid = make_grid()
        targets = find_targets(grid)
        if targets: break

  grid = make_grid()
  targets = find_targets(grid)
  if targets is None: return {"input": None, "output": None}
  output = common.grid(9, 9)

  def stamp_target(index):
    """Copies the input pattern into one selected output block."""
    if index >= len(targets): return
    row, col = targets[index]
    for r in range(3):
      for c in range(3):
        output[row * 3 + r][col * 3 + c] = grid[r][c]

  stamp_target(0)
  stamp_target(1)
  stamp_target(2)
  stamp_target(3)
  stamp_target(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 1, 6, 2, 2, 2, 2, 6]),
      generate(colors=[2, 4, 3, 2, 3, 4, 2, 3, 4]),
      generate(colors=[3, 1, 6, 3, 6, 1, 3, 1, 6]),
      generate(colors=[4, 4, 6, 3, 3, 3, 6, 6, 4]),
  ]
  test = [
      generate(colors=[6, 6, 3, 4, 4, 3, 4, 4, 3]),
  ]
  return {"train": train, "test": test}
