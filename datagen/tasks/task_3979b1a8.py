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


def _draw_seed_pattern(grid, colors, size):
  for r in range(size):
    for c in range(size):
      grid[r][c] = colors[1]
  grid[0][0] = grid[0][size - 1] = colors[2]
  grid[size - 1][0] = grid[size - 1][size - 1] = colors[2]
  center = size // 2
  grid[center - 1][center] = grid[center][center - 1] = colors[0]
  grid[center][center] = grid[center][center + 1] = colors[0]
  grid[center + 1][center] = colors[0]


def _draw_layer(output, colors, layer):
  size = len(output) // 2
  if layer >= 2 * size:
    return
  for c in range(layer + 1):
    output[layer][c] = colors[(layer + (1 if c == layer else 0)) % 3]
  for r in range(layer):
    output[r][layer] = colors[layer % 3]


def generate(colors=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors.
    size: The width and height of the seed grid.
  """

  if colors is None:
    colors = common.random_colors(3)
    if size is None:
      size = common.choice([5, 7, 9])

  if size is None:
    size = 5

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  _draw_seed_pattern(grid, colors, size)
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c]
  _draw_layer(output, colors, size + 0)
  _draw_layer(output, colors, size + 1)
  _draw_layer(output, colors, size + 2)
  _draw_layer(output, colors, size + 3)
  _draw_layer(output, colors, size + 4)
  for layer in range(size + 5, 2 * size):
    _draw_layer(output, colors, layer)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 3, 2]),
      generate(colors=[2, 8, 9]),
  ]
  test = [
      generate(colors=[9, 1, 5]),
  ]
  return {"train": train, "test": test}
