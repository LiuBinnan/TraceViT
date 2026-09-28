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


def generate(rows=None, cols=None, color=None, removals=None, height=3, width=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the input pixels.
    cols: The columns of the input pixels.
    color: The color of the input pixels.
    removals: The number of attempts to remove pixels from the input sprite.
    height: The height of the input sprite.
    width: The width of the input sprite.
  """

  if color is None:
    color = common.random_color()
    if removals is None:
      removals = common.randint(1, 12)
    rows, cols = common.conway_sprite(width, height, removals)

  grid = common.grid(width, height)
  for row, col in zip(rows, cols):
    grid[row][col] = color
  output = common.grid(width, height)

  def invert_sprite():
    """Shows the inverse of the input sprite."""
    for row in range(height):
      for col in range(width):
        output[row][col] = common.black() if grid[row][col] else color

  def expand_inverted_row(row):
    """Expands one input row using the inverted sprite mask."""
    nonlocal output
    if row >= height:
      return
    if len(output) == height:
      output = common.grid(width * width, height * height)
    for col in range(width):
      if grid[row][col] == common.black():
        continue
      for r in range(height):
        for c in range(width):
          output[height * row + r][width * col + c] = color
      for r, c in zip(rows, cols):
        output[height * row + r][width * col + c] = common.black()
    if row == 2:
      for remaining_row in range(3, height):
        expand_inverted_row(remaining_row)

  invert_sprite()
  expand_inverted_row(0)
  expand_inverted_row(1)
  expand_inverted_row(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2], cols=[2, 1, 0], color=6),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], color=7),
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 2, 2], color=4),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[2, 0, 1, 1], color=3),
  ]
  return {"train": train, "test": test}
