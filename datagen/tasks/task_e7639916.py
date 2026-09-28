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


def generate(width=None, height=None, rows=None, cols=None, flip=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    flip: Whether to flip the output grid.
    flop: Whether to flop the output grid.
  """

  if width is None:
    width, height = common.randint(8, 28), common.randint(8, 28)
    wide, tall = common.randint(5, width - 2), common.randint(5, height - 2)
    r = common.randint(1, height - tall - 1)
    c = common.randint(1, width - wide - 1)
    rows = [r, r + common.randint(1, tall - 2), r + tall - 1]
    cols = [c, c + wide - 1, c + common.randint(1, wide - 2)]
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  # Build the input: three 8-dots marking the rectangle's top-left corner, a
  # point on its right edge and a point on its bottom edge.  Orient the input
  # up front so every output frame can be written directly in that orientation.
  grid = common.grid(width, height)
  for row, col in zip(rows, cols):
    grid[row][col] = 8
  if flip: grid = common.flip(grid)
  if flop: grid = common.flop(grid)

  # Solve forward: the three marks pin the four boundaries (top=rows[0],
  # bottom=rows[2], left=cols[0], right=cols[1]); trace the rectangle outline
  # side by side, flowing around the marks which stay 8.
  output = common.deepcopy(grid)

  def put(r, c, v):
    """Writes v at canonical (r, c) mapped into the output's orientation."""
    rr = height - 1 - r if flip else r
    cc = width - 1 - c if flop else c
    if output[rr][cc] == 0:
      output[rr][cc] = v

  def draw_top():
    """Draws the top edge from the corner across to the right column."""
    for col in range(cols[0], cols[1] + 1):
      put(rows[0], col, 1)

  def draw_right():
    """Draws the right edge down through the right-edge mark."""
    for row in range(rows[0], rows[2] + 1):
      put(row, cols[1], 1)

  def draw_bottom():
    """Draws the bottom edge back through the bottom-edge mark."""
    for col in range(cols[0], cols[1] + 1):
      put(rows[2], col, 1)

  def draw_left():
    """Draws the left edge up to close the rectangle."""
    for row in range(rows[0], rows[2] + 1):
      put(row, cols[0], 1)

  draw_top()
  draw_right()
  draw_bottom()
  draw_left()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=8, rows=[1, 4, 6], cols=[2, 9, 3],
               flip=True, flop=False),
      generate(width=20, height=10, rows=[1, 2, 8], cols=[3, 16, 10],
               flip=False, flop=False),
      generate(width=13, height=11, rows=[1, 4, 9], cols=[2, 10, 4],
               flip=True, flop=True),
  ]
  test = [
      generate(width=13, height=14, rows=[3, 5, 12], cols=[3, 11, 8],
               flip=False, flop=False),
  ]
  return {"train": train, "test": test}
