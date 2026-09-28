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


def generate(width=None, height=None, colors=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the lines.
    length: The length of the grey line.
  """

  if width is None:
    colors = common.random_colors(common.randint(2, 3), exclude=[5])
    length = common.randint(1, 5)
    width = len(colors) + common.randint(3, 14)
    height = length * len(colors) + common.randint(1, 12)

  # Input: the grey ruler (its length is the band height) plus the color key
  # (the vertical legend lines on the right edge).
  grid = common.grid(width, height)
  for r in range(length):
    grid[r][0] = common.gray()
  for r in range(height):
    for i, color in enumerate(colors):
      grid[r][width - len(colors) + i] = color

  output = common.deepcopy(grid)
  legend_col = width - len(colors) - 1

  def erase_legend():
    """Clears the color key once it has been read."""
    for r in range(height):
      for i in range(len(colors)):
        output[r][width - len(colors) + i] = common.black()

  def reveal_color(k):
    """Stacks every band that decodes to legend color k down the new column."""
    if k >= len(colors):
      return
    for r in range(height):
      if (r // length) % len(colors) == k:
        output[r][legend_col] = colors[k]

  erase_legend()
  reveal_color(0)
  reveal_color(1)
  reveal_color(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=12, colors=[2, 3], length=4),
      generate(width=7, height=7, colors=[9, 8], length=3),
      generate(width=7, height=9, colors=[9, 6, 7], length=2),
      generate(width=6, height=14, colors=[2, 8, 4], length=1),
      generate(width=5, height=5, colors=[3, 1], length=1),
  ]
  test = [
      generate(width=9, height=9, colors=[4, 8, 3], length=2),
  ]
  return {"train": train, "test": test}
