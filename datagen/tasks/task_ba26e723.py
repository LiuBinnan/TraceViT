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


def generate(width=None, height=3, flip=0, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    flip: do we want to flip the grid?
    num_colors: how many foreground colors the widened, multi-color scatter
      variant uses. None keeps the original single-color (yellow) domino
      pattern that validate() relies on.
  """
  if width is None:
    width = common.randint(10, 20)
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  if num_colors is None:
    for c in range(width):
      grid[1][c] = grid[2 * ((c + flip) % 2)][c] = common.yellow()
      color = common.pink() if c % 3 == 0 else common.yellow()
      output[1][c] = output[2 * ((c + flip) % 2)][c] = color
  else:
    # Same rule (every third column recolored to pink), but the foreground is
    # a random multi-color vertical scatter per column instead of a fixed
    # 2-cell yellow domino. Widens object count / #colors / density toward the
    # re_arc band without changing what the puzzle asks for.
    num_colors = min(8, max(1, num_colors))
    palette = common.random_colors(num_colors, exclude=[common.pink()])
    for c in range(width):
      count = common.randint(1, max(1, height - 1))
      for r in common.sample(range(height), count):
        grid[r][c] = common.choice(palette)
        output[r][c] = common.pink() if c % 3 == 0 else grid[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, flip=0),
      generate(width=11, flip=1),
      generate(width=11, flip=0),
      generate(width=13, flip=0),
      generate(width=14, flip=1),
  ]
  test = [
      generate(width=17, flip=1),
  ]
  return {"train": train, "test": test}
