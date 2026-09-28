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


def generate(width=None, height=None, row=None, col=None, color=None, flip=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the box.
    col: The column of the box.
    color: The color of the box.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
  """

  if width is None:
    width, height = 2 * common.randint(2, 8), 2 * common.randint(2, 8)
    row = common.randint(0, height // 2 - 1)
    col = common.randint(0, width // 2 - 1)
    while row == 0 and col == 0:
      row = common.randint(0, height // 2 - 1)
      col = common.randint(0, width // 2 - 1)
    color = common.random_color(exclude=[8])
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height, 8)
  anchor_row = height - 1 - row if flip else row
  anchor_col = width - 1 - col if flop else col
  extent_row = height - 1 if flip else 0
  extent_col = width - 1 if flop else 0
  target_rows = range(anchor_row, height) if flip else range(anchor_row + 1)
  target_cols = range(anchor_col, width) if flop else range(anchor_col + 1)
  grid[anchor_row][anchor_col] = color

  def mark_rectangle_extent():
    """Marks the far corner of the box implied by the colored input cell."""
    output[extent_row][extent_col] = color

  def add_anchor_corner():
    """Carries the input marker into the output as the opposite box corner."""
    output[anchor_row][anchor_col] = color

  def fill_box_between_corners():
    """Fills the rectangle spanned by the anchor and extent corners."""
    for r in target_rows:
      for c in target_cols:
        output[r][c] = color

  mark_rectangle_extent()
  add_anchor_corner()
  fill_box_between_corners()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=6, row=2, col=2, color=4, flip=True, flop=False),
      generate(width=6, height=6, row=2, col=1, color=9, flip=False, flop=True),
      generate(width=8, height=10, row=4, col=2, color=6, flip=False, flop=False),
      generate(width=4, height=4, row=0, col=1, color=6, flip=False, flop=True),
  ]
  test = [
      generate(width=10, height=10, row=2, col=1, color=4, flip=True, flop=True),
  ]
  return {"train": train, "test": test}
