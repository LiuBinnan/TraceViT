# Copyright 2025 Google LLC
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


def generate(size=None, color=None, height=None, width=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    color: a digit representing a color to be used
    height: the number of rows; defaults to size (square fallback)
    width: the number of columns; defaults to size (square fallback)
    num_colors: how many distinct colors fill the surrounding noise field
  """
  if size is None:
    if height is None:
      height = 2 * common.randint(1, 14) + 1
    if width is None:
      width = 2 * common.randint(1, 14) + 1
    color = common.random_color()
    # Widen structural variation the way re_arc does for this task: overpaint
    # the canvas with a field of random colors (num_colors distinct hues, none
    # of them black). The lone black center still uniquely fixes where the X is
    # drawn, so the rule is unchanged -- the output is still the input with the
    # X through the center painted in the center cell's color.
    if num_colors is None:
      num_colors = common.randint(1, 9)
    palette = common.random_colors(num_colors)
  if height is None:
    height = size
  if width is None:
    width = size

  grid, output = common.grids(width, height, color)
  if num_colors is not None:
    for r in range(height):
      for c in range(width):
        if (r, c) == (height // 2, width // 2):
          continue
        noise_color = palette[common.randint(0, len(palette) - 1)]
        grid[r][c] = noise_color
        output[r][c] = noise_color
  grid[height // 2][width // 2] = common.black()
  # Draw the two diagonals through the center one at a time so the steps layer
  # can snapshot the output after the first diagonal, then after both.
  for r in range(height):
    for c in range(width):
      if (r - height // 2) == (c - width // 2):  # main diagonal "\"
        output[r][c] = common.black()
  for r in range(height):
    for c in range(width):
      if (r - height // 2) == -(c - width // 2):  # anti-diagonal "/"
        output[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, color=1),
      generate(size=5, color=2),
      generate(size=7, color=3),
  ]
  test = [
      generate(size=11, color=6),
  ]
  return {"train": train, "test": test}
