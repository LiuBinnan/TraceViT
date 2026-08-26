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


def generate(colors=None, size=3, num=3, num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of each (square) panel
    num: the number of panels (2..4); each successive panel is a further
      90-degree clockwise rotation of the first, so the rule is unchanged
    num_colors: how many distinct pattern colors to draw the panel from
    density: fraction of panel cells that carry a pattern color (the rest stay
      background); randomized when omitted
  """
  if colors is None:
    # Cap the panel count so num panels + (num-1) separators stay within 30.
    k = min(4 if size < 7 else 3, 31 // (size + 1))
    num = common.randint(2, max(2, k))
    if num_colors is None:
      num_colors = common.randint(1, 8)
    palette = common.random_colors(num_colors, exclude=[common.gray()])
    if density is None:
      ncells = common.randint(1, size * size - 1)
    else:
      ncells = max(1, min(size * size - 1,
                          int(round(density * size * size))))
    positions = common.sample(range(size * size), ncells)
    colors = [common.black()] * (size * size)
    for pos in positions:
      colors[pos] = palette[common.randint(0, num_colors - 1)]

  grid, output = common.grids(num * size + num - 1, size)
  for c in range(size, num * size + num - 1, size + 1):
    for r in range(size):
      output[r][c] = grid[r][c] = common.gray()
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c] = colors[r * size + c]
  for r in range(size):
    for c in range(size):
      output[c][2 * size - r] = colors[r * size + c]
  if num > 2:
    for r in range(size):
      for c in range(size):
        output[size - 1 - r][3 * size + 1 - c] = colors[r * size + c]
  if num > 3:
    for r in range(size):
      for c in range(size):
        output[size - 1 - c][3 * (size + 1) + r] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 2, 4, 1, 1, 4, 4, 1]),
      generate(colors=[6, 3, 3, 6, 3, 3, 6, 3, 2]),
      generate(colors=[2, 7, 8, 7, 7, 8, 8, 8, 8]),
  ]
  test = [
      generate(colors=[3, 3, 9, 9, 9, 9, 2, 9, 9]),
  ]
  return {"train": train, "test": test}
