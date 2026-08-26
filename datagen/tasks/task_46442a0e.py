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


def generate(size=None, colors=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: the digits representing the colors to be used
    num_colors: how many distinct colors the grid is drawn from
  """
  if size is None:
    size = common.randint(1, 15)
    if num_colors is None:
      num_colors = common.randint(1, min(10, size * size))
    num_colors = max(1, min(num_colors, size * size))
    color_list = common.sample([common.black()] + common.random_colors(9),
                               num_colors)
    colors = [color_list[0]] * (size * size)
    cells = list(range(size * size))
    for color in color_list[1:]:
      num = common.randint(1, max(1, len(cells) // (num_colors - 1)))
      chosen = common.sample(cells, num)
      for cell in chosen:
        colors[cell] = color
      cells = [cell for cell in cells if cell not in chosen]

  grid = common.grid(size, size, 0)
  output = common.grid(2 * size, 2 * size, 0)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[r][c] = grid[r][c] = color
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[c][2 * size - r - 1] = color
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[2 * size - r - 1][2 * size - c - 1] = color
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[2 * size - c - 1][r] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, colors=[8, 6, 6, 8]),
      generate(size=3, colors=[7, 7, 8, 7, 7, 8, 8, 8, 8]),
      generate(size=3, colors=[6, 9, 9, 6, 4, 4, 6, 4, 4]),
  ]
  test = [
      generate(size=3, colors=[1, 4, 1, 4, 9, 4, 9, 1, 9]),
  ]
  return {"train": train, "test": test}
