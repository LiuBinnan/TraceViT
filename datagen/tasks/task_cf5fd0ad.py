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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    subset = common.random_colors(common.randint(1, 4), exclude=[8])
    while True:
      colors = [common.randint(0, 2) for _ in range(9)]
      colors = [8 if color else common.choice(subset) for color in colors]
      if len(set(colors)) == len(subset) + 1: break

  grid = common.grid(3, 3)
  for row in range(3):
    for col in range(3):
      grid[row][col] = colors[row * 3 + col]
  output = common.grid(12, 12)

  def fill_bottom_right():
    """Copies the tile unchanged into the four bottom-right blocks (the base)."""
    nonlocal output
    for row in range(3):
      for col in range(3):
        for r in range(2, 4):
          for c in range(2, 4):
            output[r * 3 + row][c * 3 + col] = colors[row * 3 + col]

  def fill_top_right():
    """Reflects the tile into the top-right quadrant."""
    nonlocal output
    for row in range(3):
      for col in range(3):
        for r in range(2, 4):
          for c in range(0, 2):
            output[c * 3 + col][r * 3 + 2 - row] = colors[row * 3 + col]

  def fill_bottom_left():
    """Reflects the tile into the bottom-left quadrant."""
    nonlocal output
    for row in range(3):
      for col in range(3):
        for r in range(0, 2):
          for c in range(2, 4):
            output[c * 3 + 2 - col][r * 3 + row] = colors[row * 3 + col]

  def fill_top_left():
    """Reflects the tile into the top-left quadrant (180-degree turn)."""
    nonlocal output
    for row in range(3):
      for col in range(3):
        for r in range(0, 2):
          for c in range(0, 2):
            output[r * 3 + 2 - row][c * 3 + 2 - col] = colors[row * 3 + col]

  fill_bottom_right()
  fill_top_right()
  fill_bottom_left()
  fill_top_left()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 7, 8, 7, 8, 8, 8, 5, 1]),
      generate(colors=[6, 8, 8, 8, 6, 8, 8, 8, 8]),
      generate(colors=[1, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(colors=[8, 8, 8, 8, 8, 2, 8, 6, 4]),
  ]
  return {"train": train, "test": test}
