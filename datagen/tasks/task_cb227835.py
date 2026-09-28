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


def generate(width=None, height=None, prows=None, pcols=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    flip: Whether to flip the grid.
  """

  if width is None:
    width = 12 + common.randint(-2, 16)
    height = 12 + common.randint(-2, 16)
    while True:
      wide, tall = common.randint(3, width - 1), common.randint(3, height - 1)
      if abs(wide - tall) >= 2: break
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    prows = [brow, brow + tall - 1]
    pcols = [bcol, bcol + wide - 1]
    flip = common.randint(0, 1)

  row_diff, col_diff = pcols[1] - pcols[0], prows[1] - prows[0]

  def fr(row):
    """Row index, mirrored when flip is set (matches common.flip)."""
    return height - 1 - row if flip else row

  # Input: two azure endpoint pixels at opposite corners of the bounding box.
  grid = common.grid(width, height)
  for prow, pcol in zip(prows, pcols):
    grid[fr(prow)][pcol] = common.cyan()
  output = common.deepcopy(grid)

  # Output: two symmetric green connectors between the endpoints. Each is a
  # straight run from one endpoint that meets a 45-degree diagonal from the
  # other; the endpoint cells stay azure (drawn around, never over, them).
  def draw_path1():
    """Straight-then-diagonal connector between the two endpoints."""
    if row_diff > col_diff:
      for i in range(1, row_diff - col_diff + 1):
        output[fr(prows[0])][pcols[0] + i] = common.green()
      for i in range(1, col_diff):
        output[fr(prows[1] - i)][pcols[1] - i] = common.green()
    else:
      for i in range(1, col_diff - row_diff + 1):
        output[fr(prows[0] + i)][pcols[0]] = common.green()
      for i in range(1, row_diff):
        output[fr(prows[1] - i)][pcols[1] - i] = common.green()

  def draw_path2():
    """The mirror connector: diagonal from one endpoint, straight to the other."""
    if row_diff > col_diff:
      for i in range(1, col_diff):
        output[fr(prows[0] + i)][pcols[0] + i] = common.green()
      for i in range(1, row_diff - col_diff + 1):
        output[fr(prows[1])][pcols[1] - i] = common.green()
    else:
      for i in range(1, row_diff):
        output[fr(prows[0] + i)][pcols[0] + i] = common.green()
      for i in range(1, col_diff - row_diff + 1):
        output[fr(prows[1] - i)][pcols[1]] = common.green()

  draw_path1()
  draw_path2()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, prows=[4, 11], pcols=[2, 11], flip=True),
      generate(width=13, height=13, prows=[1, 10], pcols=[2, 8], flip=False),
      generate(width=14, height=11, prows=[2, 4], pcols=[2, 12], flip=True),
  ]
  test = [
      generate(width=14, height=13, prows=[1, 12], pcols=[1, 8], flip=False),
  ]
  return {"train": train, "test": test}
