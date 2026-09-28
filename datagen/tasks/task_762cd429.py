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


def _draw_quadrants(grid, size, row, col, colors):
  common.rect(grid, size, size, row - size + 1, col, colors[0])
  common.rect(grid, size, size, row - size + 1, col + size, colors[1])
  common.rect(grid, size, size, row + 1, col, colors[2])
  common.rect(grid, size, size, row + 1, col + size, colors[3])


def generate(copies=None, colors=None, vertical_margin=None):
  """Returns input and output grids according to the given parameters.

  Args:
    copies: The number of copies.
    colors: The colors of the boxes.
    vertical_margin: Blank rows above and below the largest copy.
  """

  if copies is None:
    copies = common.randint(2, 4)
    if colors is None:
      colors = [common.random_color() for _ in range(4)]
  elif colors is None:
    colors = [common.random_color() for _ in range(4)]

  width = pow(2, copies + 1) - 2
  height = pow(2, copies) + 2 * (
      (1 if copies == 3 else 0)
      if vertical_margin is None else vertical_margin
  )
  grid, output = common.grids(width, height)
  row, col = height // 2 - 1, 0
  _draw_quadrants(grid, 1, row, col, colors)

  _draw_quadrants(output, 1, row, col, colors)
  col += 2

  _draw_quadrants(output, 2, row, col, colors)
  col += 4

  for i in range(2, copies):
    size = pow(2, i)
    _draw_quadrants(output, size, row, col, colors)
    col += pow(2, i + 1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(copies=3, colors=[2, 5, 5, 3]),
      generate(copies=3, colors=[2, 3, 1, 1]),
      generate(copies=4, colors=[1, 2, 3, 4]),
  ]
  test = [
      generate(copies=4, colors=[1, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
