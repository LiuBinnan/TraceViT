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


def generate(lengths=None, flip=None, xpose=None, gwidth=None, gheight=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: The lengths of the lines.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
    gwidth: The grid width; randomized when lengths are omitted.
    gheight: The grid height; randomized when lengths are omitted.
  """

  if lengths is None:
    if gwidth is None:
      gwidth = common.randint(6, 12)
    if gheight is None:
      gheight = common.randint(12, 24)
    lengths = []
    for _ in range(gheight):
      lengths.append(0 if lengths and lengths[-1] else common.randint(0, 2))
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
  else:
    if gwidth is None:
      gwidth = 8
    if gheight is None:
      gheight = 16

  grid, output = common.grids(gwidth, gheight, 7)
  for row, length in enumerate(lengths):
    grid[row][0] = 0
    if length == 1:
      grid[row][1] = 8
    if length == 2:
      grid[row][1] = grid[row][2] = 8

  for row in range(gheight):
    output[row][0] = 0

  for row, length in enumerate(lengths):
    if length == 1:
      output[row][1] = output[row][2] = 8

  for row, length in enumerate(lengths):
    if length == 2:
      output[row][gwidth - 2] = output[row][gwidth - 1] = 0

  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1], flip=False, xpose=False),
      generate(lengths=[0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], flip=False, xpose=True),
  ]
  test = [
      generate(lengths=[2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 2], flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
