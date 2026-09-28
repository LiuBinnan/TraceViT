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


def generate(colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    gsize: The side length of the square grid.
  """

  if colors is None:
    if gsize is None:
      gsize = 10
    grid = common.grid(gsize, gsize)
    for row in range(gsize):
      for col in range(gsize):
        if common.randint(0, 9) == 0:
          grid[row][col] = grid[row][gsize - 1 - col] = 5
        elif common.randint(0, 9) == 0:
          grid[row][col] = 5
    colors = common.flatten(grid)
  elif gsize is None:
    gsize = 10

  grid, output = common.grids(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color

  def reveal_symmetric():
    """Highlights in blue every filled cell whose mirror is also filled."""
    nonlocal output
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col] and grid[row][gsize - 1 - col]:
          output[row][col] = common.blue()

  def reveal_lone():
    """Marks gray every filled cell whose mirror across the axis is empty."""
    nonlocal output
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col] and not grid[row][gsize - 1 - col]:
          output[row][col] = common.gray()

  reveal_symmetric()
  reveal_lone()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 5, 0, 5, 5, 5, 0, 0, 0,
                       0, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                       5, 0, 0, 0, 5, 5, 0, 0, 0, 5]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 5, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 5, 5, 5, 0, 0, 0,
                       0, 5, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                       0, 0, 0, 5, 0, 0, 5, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       5, 0, 0, 0, 5, 5, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 0, 0, 5]),
      generate(colors=[0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 5, 5, 5, 5, 5, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 5, 0, 0, 0, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 5, 5, 5, 5, 0, 5, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 5, 0, 0,
                       0, 0, 5, 5, 5, 5, 5, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
