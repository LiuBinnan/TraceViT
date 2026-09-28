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

import math

import common


def generate(colors=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    size: The side length of the square grid.
  """

  if colors is None:
    if size is None:
      size = common.randint(5, 14)
    colors = [8 * common.randint(0, 1) for _ in range(size * size)]

  if size is None:
    size = math.isqrt(len(colors))

  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  output = common.deepcopy(grid)

  def mark_symmetric():
    """Recolors azure cells whose top-bottom mirror is also azure to red."""
    nonlocal output
    for row in range(size):
      for col in range(size):
        if grid[row][col] and grid[row][col] == grid[size - 1 - row][col]:
          output[row][col] = common.red()

  def mark_asymmetric():
    """Recolors azure cells whose top-bottom mirror is empty to gray."""
    nonlocal output
    for row in range(size):
      for col in range(size):
        if grid[row][col] and grid[row][col] != grid[size - 1 - row][col]:
          output[row][col] = common.gray()

  mark_symmetric()
  mark_asymmetric()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 8, 0, 8, 8, 8,
                       8, 8, 8, 8, 8, 0,
                       8, 0, 8, 0, 8, 0,
                       0, 8, 8, 8, 0, 8,
                       8, 8, 0, 8, 8, 0,
                       8, 8, 0, 0, 0, 8]),
      generate(colors=[8, 8, 0, 8, 8, 0,
                       8, 0, 8, 8, 8, 0,
                       0, 0, 8, 8, 8, 8,
                       0, 8, 0, 0, 8, 8,
                       8, 8, 0, 8, 0, 8,
                       8, 0, 0, 8, 0, 8]),
      generate(colors=[0, 8, 8, 0, 0, 8,
                       8, 8, 8, 0, 0, 0,
                       8, 8, 8, 0, 8, 0,
                       8, 0, 8, 8, 0, 8,
                       8, 8, 0, 0, 0, 0,
                       8, 8, 8, 8, 8, 0]),
      generate(colors=[8, 8, 8, 0, 0, 0,
                       0, 0, 8, 8, 0, 8,
                       0, 8, 0, 0, 0, 0,
                       8, 8, 0, 0, 8, 8,
                       8, 0, 8, 8, 8, 8,
                       0, 0, 0, 0, 8, 8]),
  ]
  test = [
      generate(colors=[0, 0, 0, 8, 0, 8,
                       8, 8, 8, 0, 8, 8,
                       8, 8, 8, 8, 0, 8,
                       8, 0, 0, 0, 8, 8,
                       0, 8, 0, 0, 0, 8,
                       8, 8, 8, 0, 8, 8]),
  ]
  return {"train": train, "test": test}
