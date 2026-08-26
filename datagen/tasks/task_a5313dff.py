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


def generate(size=None, rows=None, cols=None, wides=None, talls=None,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of widths of the target boxes
    talls: a list of heights of the target boxes
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """

  def draw(grid, output):
    # Draw the target outsides.
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          common.draw(grid, r, c, common.red())
          common.draw(output, r, c, common.red())
      for r in range(row + 1, row + tall - 1):
        for c in range(col + 1, col + wide - 1):
          common.draw(grid, r, c, common.black())
          common.draw(output, r, c, common.black())
    # Draw the blues.
      if row >= 0 and col >= 0 and row + tall <= height and col + wide <= width:
        for r in range(row + 1, row + tall - 1):
          for c in range(col + 1, col + wide - 1):
            output[r][c] = common.blue()
    # Draw the target insides.
      for r in range(row + 2, row + tall - 2):
        for c in range(col + 2, col + wide - 2):
          output[r][c] = grid[r][c] = common.red()
    if grid == output: return False  # Need to draw at least one blue.
    # Check that we haven't formed any rectangles by accident.
    boxes = list(zip(rows, cols))
    for row in range(height):
      for col in range(width):
        if (row, col) in boxes: continue
        for wide in range(3, width - col):
          for tall in range(3, height - row):
            is_rect = True
            for r in range(row + 1, row + tall - 1):
              if grid[r][col] != common.red(): is_rect = False
              if grid[r][col + wide - 1] != common.red(): is_rect = False
            for c in range(col + 1, col + wide - 1):
              if grid[row][c] != common.red(): is_rect = False
              if grid[row + tall - 1][c] != common.red(): is_rect = False
            if is_rect: return False
    return True

  if size is None:
    num_boxes = common.randint(1, 4)
    draw_height, draw_width = height is None, width is None
    while True:
      if draw_height:
        height = common.randint(8, 12)
      if draw_width:
        width = common.randint(8, 12)
      wides = [common.randint(4, 6) for _ in range(num_boxes)]
      talls = [common.randint(4, 6) for _ in range(num_boxes)]
      rows = [common.randint(-1, height - tall + 1) for tall in talls]
      cols = [common.randint(-1, width - wide + 1) for wide in wides]
      if common.overlaps(rows, cols, wides, talls, -1): continue
      grid, output = common.grids(width, height)
      if draw(grid, output): break
  else:
    height = width = size

  grid = common.grid(width, height)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        common.draw(grid, r, c, common.red())
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        common.draw(grid, r, c, common.black())
    for r in range(row + 2, row + tall - 2):
      for c in range(col + 2, col + wide - 2):
        common.draw(grid, r, c, common.red())
  output = [row[:] for row in grid]

  def fill_box(box_idx):
    if box_idx >= len(rows):
      return
    row, col = rows[box_idx], cols[box_idx]
    wide, tall = wides[box_idx], talls[box_idx]
    if row < 0 or col < 0 or row + tall > height or col + wide > width:
      return
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        output[r][c] = common.blue()
    for r in range(row + 2, row + tall - 2):
      for c in range(col + 2, col + wide - 2):
        output[r][c] = common.red()

  fill_box(0)
  fill_box(1)
  fill_box(2)
  fill_box(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, rows=[1], cols=[1], wides=[5], talls=[5]),
      generate(size=8, rows=[-1, 3], cols=[-1, 2], wides=[5, 5], talls=[5, 5]),
      generate(size=12, rows=[0, 4, 2, 9], cols=[3, 3, 7, 7],
               wides=[5, 5, 4, 5], talls=[5, 5, 5, 5]),
  ]
  test = [
      generate(size=9, rows=[0, 3, 6], cols=[2, 0, 4],
               wides=[5, 5, 6], talls=[4, 5, 4]),
  ]
  return {"train": train, "test": test}
