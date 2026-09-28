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


def generate(size=None, rows=None, cols=None, widths=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the lines.
    width: The widths of the lines.
    color: The color of the lines.
  """

  if size is None:
    while True:
      size = common.randint(3, 14)
      rows, color = [], common.random_color(exclude=[5])
      row = common.randint(0, 1)
      while row < size:
        rows.append(row)
        row += common.randint(2, 4)
      # Each line needs its own distinct width out of range(2, size).
      if len(rows) <= size - 2: break
    widths = common.sample(range(2, size), len(rows))
    cols = [common.randint(0, size - width) for width in widths]

  grid = common.grid(size, size)
  for row, col, width in zip(rows, cols, widths):
    for c in range(width):
      common.draw(grid, row, col + c, color)
  output = common.deepcopy(grid)

  def paint_background():
    """Recolors the empty canvas gray, leaving the lines where the input has them."""
    lines = {(row, col + c) for row, col, width in zip(rows, cols, widths)
             for c in range(width)}
    for r in range(size):
      for c in range(size):
        if (r, c) not in lines:
          output[r][c] = common.gray()

  def slide_line(idx):
    """Lifts line #idx and sets it back down one cell to the left."""
    if idx >= len(rows): return
    row, col, width = rows[idx], cols[idx], widths[idx]
    for c in range(width):
      common.draw(output, row, col + c, common.gray())
    for c in range(width):
      common.draw(output, row, col + c - 1, color)

  paint_background()
  slide_line(0)
  slide_line(1)
  slide_line(2)
  slide_line(3)
  slide_line(4)
  for idx in range(5, len(rows)):
    slide_line(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, rows=[1, 4], cols=[2, 1], widths=[4, 2], color=3),
      generate(size=3, rows=[0], cols=[0], widths=[3], color=4),
      generate(size=7, rows=[0, 2, 4], cols=[0, 2, 1], widths=[4, 3, 5], color=7),
  ]
  test = [
      generate(size=10, rows=[0, 2, 4, 7], cols=[2, 6, 1, 4],
               widths=[5, 2, 3, 6], color=6),
  ]
  return {"train": train, "test": test}
