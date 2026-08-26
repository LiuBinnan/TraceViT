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


def generate(width=None, height=None, cell_count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    cell_count: how many noise cells to sprinkle into the grid
    num_colors: how many distinct noise colors to use
  """
  if width is None:
    width, height = common.randint(3, 30), common.randint(3, 30)
    if cell_count is None:
      cell_count = common.randint(0, width * height)
    if num_colors is None:
      num_colors = common.randint(1, 8)

  grid, output = common.grids(width, height)
  if cell_count:
    colors = common.random_colors(min(num_colors or 8, 8),
                                  exclude=[common.cyan()])
    pixels = common.sample(
        [(r, c) for r in range(height) for c in range(width)],
        min(cell_count, width * height))
    for r, c in pixels:
      grid[r][c] = output[r][c] = common.choice(colors)
  for r in range(height):
    output[r][0] = output[r][-1] = common.cyan()
  for c in range(width):
    output[0][c] = output[-1][c] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3),
      generate(width=3, height=4),
      generate(width=4, height=5),
      generate(width=6, height=5),
  ]
  test = [
      generate(width=6, height=7),
  ]
  return {"train": train, "test": test}
