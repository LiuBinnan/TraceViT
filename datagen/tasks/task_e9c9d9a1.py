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


def generate(widths=None, heights=None):
  """Returns input and output grids according to the given parameters.

  Args:
    widths: The widths of the sections.
    heights: The heights of the sections.
  """

  if widths is None:
    num_widths, num_heights = common.randint(3, 5), common.randint(3, 5)
    while True:
      widths = [common.randint(1, 6) for _ in range(num_widths)]
      heights = [common.randint(1, 6) for _ in range(num_heights)]
      width = sum(widths) + len(widths) - 1
      height = sum(heights) + len(heights) - 1
      if width <= 30 and height <= 30: break

  width = sum(widths) + len(widths) - 1
  height = sum(heights) + len(heights) - 1

  # Input: gray gridlines partition the canvas into a grid of empty cells.
  grid = common.grid(width, height)
  row = -1
  for h in heights:
    row += h + 1
    if row >= height: break
    for col in range(width):
      grid[row][col] = common.green()
  col = -1
  for w in widths:
    col += w + 1
    if col >= width: break
    for row in range(height):
      grid[row][col] = common.green()

  # Solve: paint each cell by its position role. The four corner cells take four
  # distinct colors; interior cells (off every edge) take orange; edge
  # non-corner cells stay empty.
  output = common.deepcopy(grid)

  def paint_cell(wi, hi, color):
    row = sum(heights[:hi]) + hi
    col = sum(widths[:wi]) + wi
    for r in range(heights[hi]):
      for c in range(widths[wi]):
        output[row + r][col + c] = color

  def paint_top_left():
    paint_cell(0, 0, common.red())

  def paint_top_right():
    paint_cell(len(widths) - 1, 0, common.yellow())

  def paint_bottom_left():
    paint_cell(0, len(heights) - 1, common.blue())

  def paint_bottom_right():
    paint_cell(len(widths) - 1, len(heights) - 1, common.cyan())

  def paint_interior():
    for wi in range(len(widths)):
      for hi in range(len(heights)):
        if wi not in [0, len(widths) - 1] and hi not in [0, len(heights) - 1]:
          paint_cell(wi, hi, common.orange())

  paint_top_left()
  paint_top_right()
  paint_bottom_left()
  paint_bottom_right()
  paint_interior()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(widths=[3, 3, 4], heights=[3, 6, 4]),
      generate(widths=[3, 2, 5], heights=[4, 2, 4, 6]),
      generate(widths=[3, 3, 3, 2, 1], heights=[2, 4, 2, 2, 4]),
  ]
  test = [
      generate(widths=[2, 3, 2, 5], heights=[3, 3, 2, 4]),
  ]
  return {"train": train, "test": test}
