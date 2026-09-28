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


def generate(width=None, height=None, fgcolor=None, xpose=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    fgcolor: The foreground color of the grid.
    xpose: Whether to transpose the grid.
    colors: A list of colors to use.
  """

  if width is None:
    width = common.randint(10, 16)
    height = common.randint(10, 16)
    colors = common.shuffle(list(range(1, 10)))
    fgcolor = colors.pop()
    topcolors = [colors.pop()]
    if common.randint(0, 3) == 0: topcolors.append(colors.pop())
    botcolors = [colors.pop()]
    if common.randint(0, 3) == 0: botcolors.append(colors.pop())
    length = width if common.randint(0, 3) else (width - 1)
    start = common.randint(0, width - length)
    top = bot = mid = (height + common.randint(-1, 1)) // 2
    reset = common.randint(1, 5)
    grid = common.grid(width, height)
    has_two_sided_column = False
    for col in range(start, start + length):
      topcolor, botcolor = common.choice(topcolors), common.choice(botcolors)
      for row in range(min(top, bot), max(top, bot) + 1):
        grid[row][col] = fgcolor
      if common.randint(0, 9) == 0:  # Sometimes draw nothing.
        pass
      elif common.randint(0, 1) == 0:  # Sometimes draw one of each.
        has_two_sided_column = True
        row = common.randint(0, min(top, bot) - 1)
        grid[row][col] = topcolor
        row = common.randint(max(top, bot) + 1, height - 1)
        grid[row][col] = botcolor
      elif common.randint(0, 1) == 0:  # Sometimes draw top.
        for _ in range(1 if common.randint(0, 3) else 2):
          row = common.randint(0, min(top, bot) - 1)
          grid[row][col] = topcolor
      else:  # Sometimes draw bottom.
        for _ in range(1 if common.randint(0, 3) else 2):
          row = common.randint(max(top, bot) + 1, height - 1)
          grid[row][col] = botcolor
      reset -= 1
      if reset == 0:
        top, bot = top + common.randint(-1, 1), bot + common.randint(-1, 1)
        if top < mid - 1: top = mid - 1
        if top > mid + 1: top = mid + 1
        if bot > mid + 1: bot = mid + 1
        if bot < mid - 1: bot = mid - 1
        reset = common.randint(1, 5)
    if not has_two_sided_column:
      col = common.randint(start, start + length - 1)
      fgrows = [row for row in range(height) if grid[row][col] == fgcolor]
      row = common.randint(0, fgrows[0] - 1)
      grid[row][col] = common.choice(topcolors)
      row = common.randint(fgrows[-1] + 1, height - 1)
      grid[row][col] = common.choice(botcolors)
    xpose = common.randint(0, 1)
    if xpose:
      grid = common.transpose(grid)
      width, height = height, width
    colors = common.flatten(grid)

  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  work_grid = common.transpose(grid) if xpose else grid
  work_width = height if xpose else width
  work_height = width if xpose else height
  output = common.grid(width, height)

  def read_output(row, col):
    """Reads the output through the normalized column view."""
    return output[col][row] if xpose else output[row][col]

  def paint_output(row, col, color):
    """Paints the output through the normalized column view."""
    if xpose:
      output[col][row] = color
    else:
      output[row][col] = color

  def column_strip(col):
    """Returns the distinct visible colors in one normalized column."""
    strip = [work_grid[row][col] for row in range(work_height)
             if work_grid[row][col]]
    return common.remove_duplicates(strip)

  def copy_foreground():
    """Copies the foreground band into the output."""
    for row in range(work_height):
      for col in range(work_width):
        if work_grid[row][col] == fgcolor:
          paint_output(row, col, fgcolor)

  def copy_sparse_columns():
    """Keeps columns that do not have colors on both sides of the band."""
    for col in range(work_width):
      if len(column_strip(col)) >= 3: continue
      for row in range(work_height):
        paint_output(row, col, work_grid[row][col])

  def drop_side_colors():
    """Drops side colors to touch their original side of the foreground band."""
    copy_foreground()
    copy_sparse_columns()
    for col in range(work_width):
      strip = column_strip(col)
      if len(strip) < 3: continue
      for row in range(1, work_height - 1):
        if (read_output(row, col) == common.black() and
            read_output(row + 1, col) == fgcolor):
          paint_output(row, col, strip[0])
        if (read_output(row - 1, col) == fgcolor and
            read_output(row, col) == common.black()):
          paint_output(row, col, strip[2])

  def flip_side_colors():
    """Flips the dropped side colors across the foreground band."""
    nonlocal output
    output = common.grid(width, height)
    copy_foreground()
    copy_sparse_columns()
    for col in range(work_width):
      strip = column_strip(col)
      if len(strip) < 3: continue
      for row in range(1, work_height - 1):
        if (read_output(row, col) == common.black() and
            read_output(row + 1, col) == fgcolor):
          paint_output(row, col, strip[2])
        if (read_output(row - 1, col) == fgcolor and
            read_output(row, col) == common.black()):
          paint_output(row, col, strip[0])

  drop_side_colors()
  flip_side_colors()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, fgcolor=8, xpose=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=12, height=12, fgcolor=3, xpose=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                       0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0,
                       3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                       2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=14, height=12, fgcolor=3, xpose=1,
               colors=[0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0]),
  ]
  test = [
      generate(width=14, height=12, fgcolor=4, xpose=1,
               colors=[0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 0, 3, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 3, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
