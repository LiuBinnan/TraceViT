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


def generate(size=None, colors=None, cdir=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
    cdir: The direction of the columns.
  """

  if size is None:
    size = 2 * common.randint(2, 15)
    vals = common.random_colors(2)
    colors = [common.choice(vals) for _ in range(4)]
    pos = common.randint(0, 4)
    if pos < 4: colors[pos] = 0
    cdir = 1 if common.randint(0, 1) else -1

  # Input: a diagonal staircase of 2x2 colored blocks, one block per row-pair,
  # marching sideways in direction cdir as it descends.
  grid = common.grid(size, size)
  row, col1 = 0, 0 if cdir == 1 else size - 2
  while row < size:
    grid[row][col1] = colors[0]
    grid[row][col1 + 1] = colors[1]
    grid[row + 1][col1] = colors[2]
    grid[row + 1][col1 + 1] = colors[3]
    row, col1 = row + 2, col1 + 2 * cdir

  # Output: reflect the staircase across the vertical axis. Each block keeps its
  # internal 2x2 colors; only its column mirrors to the opposite side.
  output = common.grid(size, size)

  def reflect_block(i):
    """Places staircase block i onto its mirrored column of the output."""
    row = 2 * i
    if row >= size:
      return
    col2 = size - 2 - 2 * i if cdir == 1 else 2 * i
    output[row][col2] = colors[0]
    output[row][col2 + 1] = colors[1]
    output[row + 1][col2] = colors[2]
    output[row + 1][col2 + 1] = colors[3]

  def reflect_first_block():
    """Mirror the top block across the vertical axis (demonstrates the rule)."""
    reflect_block(0)

  def reflect_remaining_blocks():
    """Mirror every remaining block the same way to complete the staircase."""
    for i in range(1, size // 2):
      reflect_block(i)

  reflect_first_block()
  reflect_remaining_blocks()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, colors=[2, 2, 3, 2], cdir=-1),
      generate(size=12, colors=[8, 0, 2, 2], cdir=1),
      generate(size=10, colors=[2, 1, 1, 0], cdir=1),
  ]
  test = [
      generate(size=14, colors=[1, 8, 8, 1], cdir=-1),
  ]
  return {"train": train, "test": test}
