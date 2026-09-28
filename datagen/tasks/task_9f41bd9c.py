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


def generate(size=None, sky=None, roof=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    sky: The size of the sky.
    roof: The top of the roof.
    flop: Whether to flop the grid.
  """

  if size is None:
    size = common.randint(12, 28)
    sky = common.randint(5, size - 2)
    roof = common.randint(1, sky - 4)
    flop = common.randint(0, 1)

  # Build the input: a blue sky over pink ground, a gray roof bar, and three
  # vertical gray poles hanging beneath it. The whole scene is flopped when
  # the flop flag is set.
  grid = common.grid(size, size, common.pink())
  for row in range(sky):
    for c in range(size):
      grid[row][c] = common.blue()
  for row in range(roof, roof + 2):
    for col in range(5):
      grid[row][col] = common.gray()
  for row in range(roof + 2, sky):
    grid[row][0] = grid[row][2] = grid[row][4] = common.gray()
  if flop: grid = common.flop(grid)

  # Solve by re-casting the scene in the output's orientation: the roof, then
  # each vertical pole toppled into a diagonal shadow (shifting one column per
  # row), then the maroon shadow line where the poles reach the ground. When
  # flop is set the input was mirrored, so the output is laid down in the
  # opposite left-right orientation, handled per cell by xcol().
  output = common.grid(size, size, common.pink())
  for row in range(sky):
    for c in range(size):
      output[row][c] = common.blue()

  def xcol(col):
    return col if flop else size - 1 - col

  def place_roof():
    """Draws the gray roof bar."""
    for row in range(roof, roof + 2):
      for col in range(5):
        output[row][xcol(col)] = common.gray()

  def cast_pole(p):
    """Topples vertical pole p into a diagonal shadow, one column per row."""
    for row in range(roof + 2, sky):
      col = (row - roof - 2) + 2 * p
      output[row][xcol(col)] = common.gray()

  def draw_ground():
    """Draws the maroon shadow line where the poles reach the ground."""
    for col in range(sky - roof - 2, size):
      output[sky][xcol(col)] = common.maroon()

  place_roof()
  cast_pole(0)
  cast_pole(1)
  cast_pole(2)
  draw_ground()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=17, sky=11, roof=4, flop=True),
      generate(size=16, sky=11, roof=6, flop=False),
  ]
  test = [
      generate(size=18, sky=14, roof=3, flop=False),
  ]
  return {"train": train, "test": test}
