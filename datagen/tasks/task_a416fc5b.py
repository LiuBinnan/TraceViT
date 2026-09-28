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


def generate(index=None, invert=None, gsize=None, base_row=None, base_col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    index: The index of the red sprite.
    invert: Whether to invert the grids.
    gsize: Side of the square canvas. Must be 4*k+3 (11/15/19/23...) so the
      period-4 pink lattice tiles it exactly; wider canvases give a larger
      macro-grid of cells. Defaults to 11 (the original ARC-AGI-2 canvas).
    base_row: Macro-grid row of the center (base) sprite cell. On an 11x11
      canvas there is only the middle cell; wider canvases let the compass
      pattern sit at any interior cell (one with all 8 neighbours present),
      which is exactly the cell set the +3/+5 clockwise reveal rule needs.
    base_col: Macro-grid column of the base sprite cell (see base_row).
  """

  row_map = [-1, -1, -1, 0, 1, 1, 1, 0]
  col_map = [-1, 0, 1, 1, 1, 0, -1, -1]

  if index is None:
    index, invert = common.randint(0, 7), common.randint(0, 1)
    invert = 0  # Frozen: the invert branch reproduces ARC-AGI-2's own broken
                # train[2] (a blank 16x16 output), which is worthless as
                # synthetic data. validate() still passes invert=True
                # explicitly, so the reference example is still reproduced.
    if gsize is None:
      gsize = 4 * common.randint(2, 5) + 3

  if gsize is None:
    gsize = 11
  cells = (gsize - 3) // 4 + 1
  if base_row is None:
    base_row = common.randint(1, cells - 2)
  if base_col is None:
    base_col = common.randint(1, cells - 2)
  base_r, base_c = 4 * base_row + 1, 4 * base_col + 1

  def get_grey_coord():
    idx = (index + 3) % 8
    return row_map[idx], col_map[idx]

  def get_blue_coord():
    idx = (index + 5) % 8
    return row_map[idx], col_map[idx]

  def draw_sprite(g, row, col, color):
    """Stamps the four-armed sprite into the cell at offset (row, col)."""
    for r, c in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
      g[base_r + r + 4 * row][base_c + c + 4 * col] = color

  grid = common.grid(gsize, gsize, common.orange())
  for i in range(gsize):
    for j in range(3, gsize, 4):
      grid[i][j] = grid[j][i] = common.pink()
  draw_sprite(grid, 0, 0, common.red())
  draw_sprite(grid, row_map[index], col_map[index], common.red())
  output = common.deepcopy(grid)

  def reveal_grey():
    """Copies the sprite into the cell three compass steps clockwise."""
    row, col = get_grey_coord()
    draw_sprite(output, row, col, common.gray())

  def reveal_blue():
    """Copies the sprite into the cell five compass steps clockwise."""
    row, col = get_blue_coord()
    draw_sprite(output, row, col, common.cyan())

  reveal_grey()
  reveal_blue()
  if invert: grid, output = output, common.grid(16, 16, 7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(index=5, invert=False),
      generate(index=2, invert=False),
      generate(index=0, invert=True),
  ]
  test = [
      generate(index=3, invert=False),
  ]
  return {"train": train, "test": test}
