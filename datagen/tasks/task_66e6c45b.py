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


def generate(colors=None, size=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    size: The height and width of the square grid.
    height: The height of the grid. Overrides size when provided.
    width: The width of the grid. Overrides size when provided.
  """

  if colors is None:
    colors = common.random_colors(4)
    if size is None and height is None and width is None:
      height, width = 2 * common.randint(2, 7), 2 * common.randint(2, 7)

  if size is None:
    size = 4
  if height is None:
    height = size
  if width is None:
    width = size

  grid, output = common.grids(width, height)
  for row in range(2):
    for col in range(2):
      grid[row + height // 2 - 1][col + width // 2 - 1] = colors[2 * row + col]
  for col in range(2):
    output[0][(width - 1) * col] = grid[height // 2 - 1][col + width // 2 - 1]
  for col in range(2):
    output[height - 1][(width - 1) * col] = grid[height // 2][col + width // 2 - 1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 6, 8, 3]),
      generate(colors=[3, 4, 7, 6]),
  ]
  test = [
      generate(colors=[2, 3, 4, 9]),
  ]
  return {"train": train, "test": test}
