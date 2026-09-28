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


def generate(size=None, angle=None, val=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if size is None:
    size = common.randint(8, 28)
    colors = [common.randint(0, 1) for _ in range(size * size)]
    angle = common.randint(0, 3)
    val = common.randint(1, size - 2)

  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color

  # The two red markers define a straight line; collect the cells it covers,
  # endpoint-first and endpoint-last (pure bookkeeping, no frame).
  if angle == 0:
    line = [(val, c) for c in range(size)]
  if angle == 1:
    line = [(r, val) for r in range(size)]
  if angle == 2:
    line = [(i, i) for i in range(size)]
  if angle == 3:
    line = [(i, size - 1 - i) for i in range(size)]
  grid[line[0][0]][line[0][1]] = grid[line[-1][0]][line[-1][1]] = 2

  # Solve the puzzle forward: connect the two markers with the line, then light
  # up green wherever it crosses a filled cell.
  output = common.deepcopy(grid)

  def connect_dots():
    """Draws the straight red line linking the two markers."""
    nonlocal output
    for r, c in line:
      output[r][c] = 2

  def light_up_hits():
    """Turns the line green where it crosses a filled cell; endpoints stay
    red."""
    nonlocal output
    for r, c in line[1:-1]:
      if grid[r][c]:
        output[r][c] = 3

  connect_dots()
  light_up_hits()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, angle=0, val=8,
               colors=[0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0,
                       0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0,
                       1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1,
                       1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1,
                       0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0]),
      generate(size=16, angle=2, val=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                       0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
                       1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1,
                       1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0,
                       0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
                       1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1,
                       0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
      generate(size=10, angle=1, val=6,
               colors=[0, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                       1, 0, 1, 0, 1, 1, 1, 0, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 1, 1, 1, 0,
                       1, 1, 1, 0, 0, 0, 1, 0, 0, 1,
                       1, 1, 1, 1, 1, 1, 0, 0, 1, 0,
                       0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
                       1, 0, 0, 0, 1, 0, 1, 1, 0, 1,
                       0, 1, 1, 1, 1, 0, 0, 1, 1, 1,
                       0, 1, 0, 1, 0, 0, 0, 1, 1, 0]),
  ]
  test = [
      generate(size=18, angle=3, val=0,
               colors=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                       1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0,
                       1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1,
                       0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1,
                       1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1,
                       0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0,
                       1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1,
                       1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0,
                       1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0,
                       1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
