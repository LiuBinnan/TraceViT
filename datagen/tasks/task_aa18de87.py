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


def generate(width=None, height=None, bottom=None, top=None, start=None,
             cdir=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    # Local cursors so repeated draw() calls are idempotent: the None-block
    # validates a config with one draw() and the top level re-draws the same
    # config.  The explicit-parameter path (validate) draws once and is
    # behavior-identical.
    s, d = start, cdir
    grid, output = common.grids(width, height)
    for c in range(width):
      common.draw(grid, s, c, color)
      common.draw(output, s, c, color)
      if s == bottom: d = 1
      if s + 1 == top: d = -1
      s += d
    good = False
    for row in range(height):
      for col in range(width):
        if grid[row][col]: continue
        if color not in [grid[row][c] for c in range(col)]: continue
        if color not in [grid[row][c] for c in range(col + 1, width)]: continue
        output[row][col] = 2
        good = True
    if not good: return None, None
    return grid, output

  if width is None:
    color = common.random_color(exclude=[2])
    while True:
      width, height = common.randint(8, 26), common.randint(3, 8)
      bottom = common.randint(-2, 0)
      top = height + common.randint(0, 2)
      start = common.randint(bottom, top)
      cdir = 2 * common.randint(0, 1) - 1
      grid, _ = draw()
      if grid: break

  grid, _ = draw()
  if grid is None:
    return {"input": grid, "output": None}
  output = common.deepcopy(grid)

  # Bookkeeping (no frame): for each row, the interior cells the zig-zag line
  # encloses -- empty cells with a line pixel both to their left and their
  # right in that row.  Solving fills those cells red, row by row.
  row_fills = []
  for r in range(height):
    cols = [col for col in range(width)
            if not grid[r][col]
            and color in [grid[r][c] for c in range(col)]
            and color in [grid[r][c] for c in range(col + 1, width)]]
    if cols:
      row_fills.append((r, cols))

  def fill_row(k):
    """Fills the k-th zig-zag-crossed row's interior with red."""
    nonlocal output
    if k >= len(row_fills): return
    r, cols = row_fills[k]
    for col in cols:
      output[r][col] = common.red()

  fill_row(0)
  fill_row(1)
  fill_row(2)
  fill_row(3)
  fill_row(4)
  for k in range(5, height):
    fill_row(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=5, bottom=0, top=5, start=1, cdir=-1, color=8),
      generate(width=8, height=3, bottom=-2, top=3, start=-1, cdir=1, color=4),
      generate(width=8, height=5, bottom=0, top=5, start=0, cdir=1, color=1),
      generate(width=8, height=4, bottom=0, top=5, start=3, cdir=-1, color=3),
  ]
  test = [
      generate(width=9, height=4, bottom=0, top=4, start=2, cdir=-1, color=6),
  ]
  return {"train": train, "test": test}
