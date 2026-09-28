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


def generate(width=None, height=None, col=None, offset=None, flip=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    col: The column of the cyan.
    offset: The numeric offset.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid = common.grid(width, height)
    for r in range(height):
      for c in range(width):
        grid[r][c] = 1 if (r + c) % 2 == offset else 0
    if grid[height - 1][col] != 1: return None, None
    grid[height - 1][col] = 8
    if flip: grid = common.flip(grid)
    if xpose: grid = common.transpose(grid)
    return grid, None

  if width is None:
    width, height = common.randint(3, 14), common.randint(3, 14)
    offset = common.randint(0, 1)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    if width == 3 and offset != height % 2:
      offset = height % 2
    while True:
      col = common.randint(1, width - 2)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()
  if not grid:
    return {"input": grid, "output": None}
  output = common.deepcopy(grid)
  canonical_output = common.grid(width, height)
  blue_counts = [
      sum(1 for r in range(height) if (r + c) % 2 == offset)
      for c in range(width)
  ]

  def orient(ingrid):
    """Applies the sampled orientation to a canonical grid."""
    oriented = common.deepcopy(ingrid)
    if flip: oriented = common.flip(oriented)
    if xpose: oriented = common.transpose(oriented)
    return oriented

  def erase_checkerboard():
    """Clears the blue pattern to isolate the cyan reference cell."""
    for r in range(len(output)):
      for c in range(len(output[0])):
        if output[r][c] == common.blue():
          output[r][c] = common.black()

  erase_checkerboard()

  def settle_blue_columns():
    """Drops each column's blue cells to the canonical bottom edge."""
    nonlocal output
    for c, num_blue in enumerate(blue_counts):
      for r in range(num_blue):
        canonical_output[height - 1 - r][c] = common.blue()
    canonical_output[height - 1][col] = common.cyan()
    output = orient(canonical_output)

  settle_blue_columns()

  def reveal_maroon_trail():
    """Adds the maroon trail above the marked column's blue stack."""
    nonlocal output
    for r in range((height - 1) // 2):
      canonical_output[height - 1 - blue_counts[col] - r][col] = common.maroon()
    output = orient(canonical_output)

  reveal_maroon_trail()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=6, col=1, offset=0, flip=False, xpose=True),
      generate(width=7, height=7, col=4, offset=0, flip=True, xpose=True),
      generate(width=8, height=4, col=2, offset=1, flip=False, xpose=False),
      generate(width=3, height=3, col=1, offset=1, flip=True, xpose=False),
  ]
  test = [
      generate(width=5, height=5, col=2, offset=0, flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
