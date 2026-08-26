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


def generate(size=None, height=None, width=None, rows=None, cols=None,
             lengths=None, bg_color=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths of the boxes
    bg_color: the background color
    colors: a list of border colors for the boxes
  """
  legal_colors = [
      common.black(), common.blue(), common.green(), common.yellow(),
      common.gray(), common.pink(), common.cyan(), common.maroon()]
  if size is None:
    size = common.randint(10, 20)
    if height is None: height = size
    if width is None: width = size
    # Boxes are square, so each length must fit within the smaller extent.
    short = min(height, width)
    # SECONDARY-COUNT GUARD: at most 6 unrolled fill_box handlers, so both
    # bounds of the box count are capped at 6 (lo stays <= hi).
    num_boxes = common.randint(min(6, short // 4), min(6, short // 3))
    while True:
      lengths = [common.randint(3, min(10, short)) for _ in range(num_boxes)]
      rows = [common.randint(0, height - length) for length in lengths]
      cols = [common.randint(0, width - length) for length in lengths]
      if not common.overlaps(rows, cols, lengths, lengths, 1): break
    if bg_color is None:
      bg_color = common.choice(legal_colors)
    if colors is None:
      choices = [color for color in legal_colors if color != bg_color]
      colors = [common.choice(choices) for _ in range(num_boxes)]
  if height is None: height = size
  if width is None: width = size
  if bg_color is None:
    bg_color = common.black()
  if colors is None:
    colors = [common.blue() for _ in rows]

  grid, output = common.grids(width, height, bg_color)
  for row, col, length, color in zip(rows, cols, lengths, colors):
    for r in range(row, row + length):
      grid[r][col] = grid[r][col + length - 1] = color
      output[r][col] = output[r][col + length - 1] = color
    for c in range(col, col + length):
      grid[row][c] = grid[row + length - 1][c] = color
      output[row][c] = output[row + length - 1][c] = color
  def fill_box(box_idx):
    if box_idx >= len(rows):
      return
    row, col, length = rows[box_idx], cols[box_idx], lengths[box_idx]
    for r in range(row + 1, row + length - 1):
      for c in range(col + 1, col + length - 1):
        output[r][c] = common.orange() if length % 2 else common.red()

  fill_box(0)
  fill_box(1)
  fill_box(2)
  fill_box(3)
  fill_box(4)
  fill_box(5)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[0, 2, 5], cols=[0, 6, 0], lengths=[4, 3, 5]),
      generate(size=10, rows=[0, 0], cols=[0, 4], lengths=[3, 6]),
      generate(size=20, rows=[0, 1, 3, 9, 12], cols=[0, 6, 12, 2, 12],
               lengths=[5, 4, 6, 7, 8]),
      generate(size=11, rows=[1, 2, 6], cols=[1, 5, 0], lengths=[3, 4, 5]),
      generate(size=15, rows=[1, 9], cols=[1, 6], lengths=[7, 6]),
  ]
  test = [
      generate(size=20, rows=[0, 2, 7, 11], cols=[12, 1, 10, 1],
               lengths=[5, 8, 10, 7]),
  ]
  return {"train": train, "test": test}
