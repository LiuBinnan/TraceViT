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


def generate(width=None, height=None, rows=None, cols=None, lines=None,
             xpose=None, num_lines=None, num_dots=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lines: the horizontal lines
    xpose: whether to transpose the grids
    num_lines: the number of horizontal lines
    num_dots: the number of red pixels
  """

  def draw(grid, output):
    for line in lines:
      for c in range(width):
        output[line][c] = grid[line][c] = common.cyan()
    for row, col in zip(rows, cols):
      grid[row][col] = common.red()
      for line in lines:
        r, dr = row, -1 if line < row else 1
        while r != line:
          if output[r][col] == common.cyan(): break
          output[r][col], r = common.red(), r + dr
        if r == line:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              output[r + dr][col + dc] = common.cyan()
          output[r][col] = common.red()
    return grid != output

  if width is None:
    while True:
      width, height = common.randint(4, 30), common.randint(4, 30)
      line_options = list(range(1, height - 1))
      if not line_options: continue
      target_lines = num_lines
      if target_lines is None:
        target_lines = common.randint(1, max(1, height // 4))
      target_lines = max(1, target_lines)
      lines = []
      for _ in range(target_lines):
        if not line_options: break
        line = common.choice(line_options)
        lines.append(line)
        line_options = [r for r in line_options if abs(r - line) > 2]
      lines = sorted(lines)
      frontiers = [-1] + lines + [height]
      def valid_row(r):
        left = max(line for line in frontiers if line < r)
        right = min(line for line in frontiers if line > r)
        if left == -1 or right == height:
          return True
        outer = [line for line in frontiers if line not in [left, right]]
        return max(abs(r - left), abs(r - right)) < min(
            abs(r - line) for line in outer)
      row_options = [r for r in range(height)
                     if all(abs(r - line) > 1 for line in lines)
                     and valid_row(r)]
      col_options = list(range(1, width - 1))
      if not row_options or not col_options: continue
      max_dots = min(len(row_options), max(1, width // 2))
      target_dots = num_dots
      if target_dots is None:
        target_dots = common.randint(1, max_dots)
      target_dots = max(1, min(target_dots, max_dots))
      rows, cols = [], []
      for _ in range(target_dots):
        if not col_options: break
        c = common.choice(col_options)
        r = common.choice(row_options)
        rows.append(r)
        cols.append(c)
        col_options = [col for col in col_options if abs(col - c) > 1]
      if not rows: continue
      if xpose is None:
        xpose = common.choice([False, True])
      grid, output = common.grids(width, height)
      if draw(grid, output): break

  def coords(r, c):
    if xpose: r, c = c, r
    return r, c

  final_width, final_height = (height, width) if xpose else (width, height)
  grid, output = common.grids(final_width, final_height)

  def paint(target, r, c, value):
    r, c = coords(r, c)
    common.draw(target, r, c, value)

  def pixel(target, r, c):
    r, c = coords(r, c)
    return common.get_pixel(target, r, c)

  for line in lines:
    for c in range(width):
      paint(output, line, c, common.cyan())
      paint(grid, line, c, common.cyan())
  for row, col in zip(rows, cols):
    paint(grid, row, col, common.red())
    paint(output, row, col, common.red())
  contacts = []
  for row, col in zip(rows, cols):
    for line in lines:
      r, dr = row, -1 if line < row else 1
      while r != line:
        if pixel(output, r, col) == common.cyan(): break
        paint(output, r, col, common.red())
        r += dr
      if r == line:
        contacts.append((r, col))
  for r, col in contacts:
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        paint(output, r + dr, col + dc, common.cyan())
    paint(output, r, col, common.red())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, rows=[2, 10], cols=[2, 8], lines=[6],
               xpose=0),
      generate(width=13, height=18, rows=[8], cols=[4], lines=[3, 14], xpose=1),
      generate(width=12, height=17, rows=[2, 10], cols=[8, 4], lines=[7, 13],
               xpose=0),
  ]
  test = [
      generate(width=17, height=19, rows=[1, 8, 15, 16], cols=[2, 8, 1, 14],
               lines=[4, 12], xpose=1),
  ]
  return {"train": train, "test": test}
