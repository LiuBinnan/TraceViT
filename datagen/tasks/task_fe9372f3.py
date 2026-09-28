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


def generate(width=None, height=None, row=None, col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the output grid.
    height: The height of the output grid.
    row: The row of the plus.
    col: The column of the plus.
  """

  if width is None:
    width, height = common.randint(7, 30), common.randint(7, 30)
    row = common.randint(3, height - 4)
    col = common.randint(3, width - 4)

  grid, output = common.grids(width, height)
  for r, c in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]:
    grid[row + r][col + c] = common.red()
  output = common.deepcopy(grid)
  plus = {(row - 1, col), (row, col - 1), (row, col), (row, col + 1),
          (row + 1, col)}

  def draw_main_diagonal():
    # Emit the "\" diagonal ray (blue) through the plus, leaving the plus intact.
    for r in range(height):
      for c in range(width):
        if c - r == col - row and (r, c) not in plus:
          output[r][c] = common.blue()

  def draw_anti_diagonal():
    # Emit the "/" diagonal ray (blue), completing the X.
    for r in range(height):
      for c in range(width):
        if c + r == col + row and (r, c) not in plus:
          output[r][c] = common.blue()

  def draw_horizontal():
    # Emit the horizontal ray as a yellow/cyan period-3 dash pattern.
    for c in range(width):
      if (row, c) not in plus:
        output[row][c] = common.yellow() if abs(col - c) % 3 == 1 else common.cyan()

  def draw_vertical():
    # Emit the vertical ray as a yellow/cyan period-3 dash pattern.
    for r in range(height):
      if (r, col) not in plus:
        output[r][col] = common.yellow() if abs(row - r) % 3 == 1 else common.cyan()

  draw_main_diagonal()
  draw_anti_diagonal()
  draw_horizontal()
  draw_vertical()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=7, row=3, col=3),
      generate(width=10, height=12, row=4, col=4),
  ]
  test = [
      generate(width=17, height=30, row=11, col=7)
  ]
  return {"train": train, "test": test}
