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


def generate(colors=None, cols=None, size=10, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a pair of digits representing two different colors
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if colors is None:
    colors = common.random_colors(2)
    cols = [common.randint(2, width - 3) for _ in range(2)]

  grid, output = common.grids(width, height)
  grid[2][cols[0]] = colors[0]
  grid[height - 3][cols[1]] = colors[1]
  for r in range(0, (height + 1) // 2):
    output[r][0] = output[r][width - 1] = colors[0]
  for r in range(0, (width + 1) // 2):
    output[0][r] = output[0][width - 1 - r] = colors[0]
    output[2][r] = output[2][width - 1 - r] = colors[0]
  for r in range(0, height // 2):
    output[height - 1 - r][0] = output[height - 1 - r][width - 1] = colors[1]
  for r in range(0, (width + 1) // 2):
    output[height - 1][r] = output[height - 1][width - 1 - r] = colors[1]
    output[height - 3][r] = output[height - 3][width - 1 - r] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 7], cols=[2, 7]),
      generate(colors=[1, 4], cols=[6, 5]),
  ]
  test = [
      generate(colors=[2, 8], cols=[4, 6]),
  ]
  return {"train": train, "test": test}
