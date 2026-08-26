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


def generate(colors=None, width=None, height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: the list of colors to use
    width: the number of colors/columns in the pattern
    height: the total grid height
  """
  randomize_colors = colors is None
  if colors is None:
    if width is None:
      width = common.randint(2, 6)
    colors = common.random_colors(width, exclude=[common.gray()])
  else:
    width = len(colors)

  if height is None:
    if randomize_colors:
      height = common.randint(3, 30)
    else:
      height = 2 * len(colors) + 2
  grid, output = common.grids(width, height)
  for color_idx, color in enumerate(colors):
    grid[0][color_idx] = color
    grid[1][color_idx] = common.gray()
  output = [row[:] for row in grid]

  def reveal_color(color_idx):
    if color_idx >= len(colors):
      return
    color = colors[color_idx]
    for row in range(color_idx + 2, height, len(colors)):
      for c in range(width):
        output[row][c] = color

  reveal_color(0)
  reveal_color(1)
  reveal_color(2)
  reveal_color(3)
  reveal_color(4)
  reveal_color(5)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 1, 4]),
      generate(colors=[3, 2, 1, 4]),
      generate(colors=[8, 3]),
  ]
  test = [
      generate(colors=[1, 2, 3, 4, 8]),
  ]
  return {"train": train, "test": test}
