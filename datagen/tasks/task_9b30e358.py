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


def generate(colors=None, height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    height: The number of grid rows. When omitted it is randomized in a
      rule-faithful band; validate() passes only `colors`, so the body defaults
      it to the original value 10 (byte-identical).
  """

  if colors is None:
    if height is None:
      height = common.randint(8, 26)
    width, bgcolor = common.randint(4, 9), common.random_color()
    subset = common.random_colors(2, exclude=[bgcolor])
    wide, line = common.randint(3, width), common.randint(4, min(5, height - 1))
    bcol, symm = common.randint(0, width - wide), common.randint(0, 1)
    grid = common.grid(width, height, bgcolor)
    for r in range(line):
      for c in common.sample(list(range(wide)), common.randint(1, wide)):
        color = common.choice(subset)
        grid[height - 1 - r][bcol + c] = color
        if symm: grid[height - 1 - r][bcol + wide - 1 - c] = color
    colors = common.flatten(grid)

  if height is None:
    height = 10
  width, bgcolor, line = len(colors) // height, colors[0], None
  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
    if line is None and color != bgcolor: line = height - i // width

  # The input holds a `line`-row pattern block at the bottom with a plain
  # background above. The answer repeats that block upward to tile the whole
  # grid, so the output keeps the block and grows it up one row at a time.
  output = common.deepcopy(grid)

  def tile_row(k):
    """Extend the block upward: fill the k-th background row above it."""
    row = height - 1 - line - k
    if row < 0: return
    src = height - 1 - ((height - 1 - row) % line)
    for col in range(width):
      output[row][col] = grid[src][col]

  tile_row(0)
  tile_row(1)
  tile_row(2)
  tile_row(3)
  tile_row(4)
  tile_row(5)
  for k in range(6, height - line):
    tile_row(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 2, 2, 2, 5,
                       5, 5, 2, 5, 5,
                       5, 8, 8, 5, 5,
                       5, 5, 8, 8, 5,
                       5, 5, 8, 5, 5]),
      generate(colors=[3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 9, 2, 9, 3,
                       3, 3, 3, 2, 9, 2, 3,
                       3, 3, 3, 9, 9, 9, 3,
                       3, 3, 3, 3, 9, 3, 3]),
  ]
  test = [
      generate(colors=[7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 6, 7, 6, 7,
                       6, 7, 2, 7, 6,
                       7, 2, 6, 2, 7,
                       7, 6, 7, 6, 7]),
  ]
  return {"train": train, "test": test}
