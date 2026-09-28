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


def generate(
    row=None,
    col=None,
    color=None,
    row_offset=None,
    col_offset=None,
    nrects=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if row is None:
    if nrects is None:
      nrects = common.randint(5, 9)
    row, col = common.randint(1, nrects - 2), common.randint(1, nrects - 2)
    color = common.random_color(exclude=[1])
    row_offset, col_offset = common.randint(0, 1), common.randint(0, 1)
  elif nrects is None:
    nrects = 7

  grid = common.grid(3 * nrects - 1, 3 * nrects - 1)
  for r in range(nrects):
    for c in range(nrects):
      hue = color if row == r and col == c else 1
      common.hollow_rect(grid, 2, 2, r * 3 - row_offset, c * 3 - col_offset, hue)

  output = [line[:] for line in grid]

  for c in range(nrects):
    common.hollow_rect(output, 2, 2, row * 3 - row_offset, c * 3 - col_offset, color)

  for r in range(nrects):
    common.hollow_rect(output, 2, 2, r * 3 - row_offset, col * 3 - col_offset, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=4, color=3, row_offset=1, col_offset=1),
      generate(row=2, col=2, color=2, row_offset=0, col_offset=0),
  ]
  test = [
      generate(row=2, col=5, color=8, row_offset=1, col_offset=0),
  ]
  return {"train": train, "test": test}
