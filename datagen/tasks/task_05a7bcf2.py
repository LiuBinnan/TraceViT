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


def generate(yrows=None, ycols=None, ytalls=None, brow=None, drow=None,
             dtalls=None, flip=None, xpose=None, num_groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    yrows: the rows of the (vertical) yellow lines.
    ycols: the columns of the yellow lines.
    ytalls: the heights of the yellow lines.
    brow: the row of the blue line.
    drow: the row of the red lines.
    dtalls: the heights of the red lines.
    flip: whether to flip the grid.
    xpose: whether to transpose the grid.
    num_groups: the number of separated yellow source groups.
  """

  if yrows is None:
    yrows, ycols, ytalls = [], [], []
    if num_groups is None:
      ycol = 0
      while True:
        ycol += common.randint(1, 5)
        wide = common.randint(2, 5)
        if ycol + wide + 1 >= 30: break
        yrow = common.randint(0, 7)
        ytall = min(common.randint(1, 3), yrow + 1)
        for col in range(ycol, ycol + wide):
          yrows.append(yrow)
          ycols.append(col)
          ytalls.append(common.randint(1, ytall))
        ycol += wide
    else:
      ycol = 0
      for group_index in range(num_groups):
        remaining_groups = num_groups - group_index - 1
        max_gap = min(5, 28 - ycol - 1 - 2 * remaining_groups)
        ycol += common.randint(1, max_gap)
        max_width = min(5, 28 - ycol - 2 * remaining_groups)
        wide = common.randint(1, max_width)
        yrow = common.randint(0, 7)
        ytall = min(common.randint(1, 3), yrow + 1)
        for col in range(ycol, ycol + wide):
          yrows.append(yrow)
          ycols.append(col)
          ytalls.append(common.randint(1, ytall))
        ycol += wide
    brow, drow = common.randint(9, 10), common.randint(19, 23)
    dtalls = common.choices([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5], 30)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(30, 30)
  # First, draw the yellow source boxes.
  for yrow, ycol, ytall in zip(yrows, ycols, ytalls):
    for row in range(ytall):
      grid[yrow - row][ycol] = common.yellow()
  # Second, draw the blue line
  for col in range(30):
    grid[brow][col] = common.cyan()
  # Third, draw the red shapes
  for col, dtall in enumerate(dtalls):
    for row in range(dtall):
      grid[drow - row][col] = common.red()
  if flip: grid = common.flip(grid)
  if xpose: grid = common.transpose(grid)

  output = common.deepcopy(grid)
  ycol_set = set(ycols)

  def paint(row, col, color):
    """Paints a cell after applying the puzzle's orientation transforms."""
    if flip:
      row = 29 - row
    if xpose:
      row, col = col, row
    output[row][col] = color

  def mark_yellow_sources():
    """Turns the source yellow cells green."""
    for yrow, ycol, ytall in zip(yrows, ycols, ytalls):
      for row in range(ytall):
        paint(yrow - row, ycol, common.green())

  mark_yellow_sources()

  def extend_yellow_to_line():
    """Extends each selected column from the yellow source to the separator."""
    for yrow, ycol, _ in zip(yrows, ycols, ytalls):
      for row in range(yrow + 1, brow):
        paint(row, ycol, common.yellow())

  extend_yellow_to_line()

  def extend_cyan_from_line():
    """Extends the separator color through each selected column."""
    for ycol in ycols:
      for row in range(brow + 1, 30):
        paint(row, ycol, common.cyan())

  extend_cyan_from_line()

  def move_red_stacks_to_edge():
    """Moves red stacks in selected columns to the far edge."""
    for col, dtall in enumerate(dtalls):
      if col not in ycol_set:
        continue
      for row in range(dtall):
        paint(29 - row, col, common.red())

  move_red_stacks_to_edge()

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(yrows=[3, 3, 2, 2, 5, 5, 5, 4], ycols=[4, 5, 11, 12, 18, 19, 20, 25],
               ytalls=[2, 2, 1, 1, 2, 2, 1, 2], brow=9, drow=20,
               dtalls=[1, 2, 3, 2, 1, 1, 3, 2, 4, 3, 1, 2, 3, 2, 1, 2, 1, 1, 2, 3, 3, 1, 1, 2, 1, 2, 1, 2, 2, 1],
               flip=False, xpose=True),
      generate(yrows=[5, 5, 4, 4, 4, 4, 4, 7, 7, 7],
               ycols=[3, 4, 9, 10, 17, 18, 19, 23, 24, 25],
               ytalls=[1, 1, 1, 2, 2, 2, 2, 1, 3, 3], brow=10, drow=21,
               dtalls=[2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 1, 3, 3, 2, 1, 1, 2, 1, 1],
               flip=False, xpose=False),
      generate(yrows=[2, 2, 2, 2, 2, 5, 5, 5, 5, 4, 4],
               ycols=[6, 7, 8, 9, 10, 16, 17, 18, 19, 25, 26],
               ytalls=[1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1], brow=9, drow=22,
               dtalls=[1, 1, 2, 2, 1, 2, 2, 3, 4, 4, 2, 1, 2, 1, 2, 4, 3, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1],
               flip=False, xpose=False),
  ]
  test = [
      generate(yrows=[4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 4],
               ycols=[1, 2, 3, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 26, 27],
               ytalls=[2, 2, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1], brow=10, drow=19,
               dtalls=[1, 3, 2, 2, 3, 2, 5, 4, 1, 1, 3, 2, 1, 3, 4, 2, 1, 2, 1, 2, 3, 5, 2, 3, 4, 2, 2, 3, 3, 1],
               flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
