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


def generate(width=None, height=None, length=None, first=None, second=None,
             rows=None, cols=None, flip=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    length: the length of the portals
    first: the row of the first portal
    second: the column of the first portal
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flip: whether to flip the input grid
    count: the number of marked portal rows
  """

  def draw_portals(grid, output):
    for r in range(length):
      grid[first + r][0] = grid[second + r][width - 1] = common.red()
      output[first + r][0] = output[second + r][width - 1] = common.red()

  def draw_paths(grid, output):
    num_yellow = 0
    for r, c in zip(rows, cols):
      grid[first + r][c] = common.cyan()
      output[first + r][c] = common.yellow()
      num_yellow += 1
      for col in range(c):
        output[first + r][col] = common.cyan() if col > 0 else common.red()
      for col in range(width):
        output[second + r][col] = common.cyan() if col + 1 < width else common.red()
    return num_yellow

  def draw_markers(grid, output):
    num_yellow = 0
    for r, c in zip(rows, cols):
      grid[first + r][c] = common.cyan()
      output[first + r][c] = common.yellow()
      num_yellow += 1
    return num_yellow

  def draw_first_paths(output):
    for r, c in zip(rows, cols):
      for col in range(c):
        output[first + r][col] = common.cyan() if col > 0 else common.red()

  def draw_second_paths(output):
    for r, c in zip(rows, cols):
      for col in range(width):
        output[second + r][col] = common.cyan() if col + 1 < width else common.red()

  def draw(grid, output):
    draw_portals(grid, output)
    num_yellow = draw_paths(grid, output)
    for r in range(height):
      if grid[r][0] == common.red() and grid[r][width - 1] == common.red():
        return False
    return num_yellow > 1

  if (width is None or height is None or length is None or first is None or
      second is None or rows is None or cols is None or flip is None):
    if width is None:
      width = common.randint(5, 30)
    if height is None:
      height = common.randint(5, 30)
    if flip is None:
      flip = common.randint(0, 1)
    max_length = max(1, (height - 1) // 2)
    if length is None:
      length = common.randint(2, max(2, max_length))
    length = min(length, max_length)
    if first is None or second is None:
      first = common.randint(0, height - 2 * length - 1)
      second = common.randint(first + length + 1, height - length)
    if rows is None or cols is None:
      marker_count = count if count is not None else common.randint(1, length)
      marker_count = min(length, marker_count)
      rows = sorted(common.sample(list(range(length)), marker_count))
      cols = [common.randint(2, width - 2) for _ in range(marker_count)]

  def final_col(c):
    return width - 1 - c if flip else c

  def set_both(r, c, color):
    c = final_col(c)
    output[r][c] = grid[r][c] = color

  def set_grid(r, c, color):
    grid[r][final_col(c)] = color

  def set_output(r, c, color):
    output[r][final_col(c)] = color

  def draw_final_portals():
    for r in range(length):
      set_both(first + r, 0, common.red())
      set_both(second + r, width - 1, common.red())

  def draw_final_markers():
    for r, c in zip(rows, cols):
      set_grid(first + r, c, common.cyan())
      set_output(first + r, c, common.yellow())

  def draw_final_first_paths():
    for r, c in zip(rows, cols):
      for col in range(c):
        set_output(first + r, col, common.cyan() if col > 0 else common.red())

  def draw_final_second_paths():
    for r, c in zip(rows, cols):
      for col in range(width):
        set_output(
            second + r, col,
            common.cyan() if col + 1 < width else common.red())

  grid, output = common.grids(width, height)
  draw_final_portals()
  draw_final_markers()
  draw_final_first_paths()
  draw_final_second_paths()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=19, length=4, first=1, second=11, rows=[2],
               cols=[4], flip=0),
      generate(width=10, height=20, length=5, first=1, second=11, rows=[1, 3],
               cols=[7, 5], flip=0),
      generate(width=10, height=20, length=6, first=3, second=13,
               rows=[1, 2, 4], cols=[3, 7, 5], flip=1),
  ]
  test = [
      generate(width=12, height=21, length=6, first=1, second=14,
               rows=[1, 2, 4], cols=[8, 7, 4], flip=0),
  ]
  return {"train": train, "test": test}
