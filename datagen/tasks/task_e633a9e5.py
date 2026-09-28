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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors.
  """

  if colors is None:
    colors = [common.random_color() for _ in range(9)]

  # Input: the 3x3 color grid.
  grid = common.grid(3, 3)
  for i in range(9):
    grid[i // 3][i % 3] = colors[i]
  output = common.grid(5, 5)

  # Each input row/col expands into the 5x5 with repeat pattern [2, 1, 2]:
  # the outer rows/cols double, the center stays single.
  span = {0: (0, 1), 1: (2, 2), 2: (3, 4)}

  def place_row_band(band):
    """Expands one input row into its output row band (doubled at borders)."""
    row_lo, row_hi = span[band]
    for j in range(3):
      col_lo, col_hi = span[j]
      for orow in range(row_lo, row_hi + 1):
        for ocol in range(col_lo, col_hi + 1):
          output[orow][ocol] = colors[3 * band + j]

  place_row_band(0)
  place_row_band(1)
  place_row_band(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 3, 5, 1, 2, 8, 8, 3, 8]),
      generate(colors=[6, 5, 5, 5, 1, 7, 4, 5, 2]),
      generate(colors=[2, 3, 7, 2, 1, 6, 1, 5, 7]),
  ]
  test = [
      generate(colors=[1, 2, 5, 7, 3, 6, 7, 6, 5]),
  ]
  return {"train": train, "test": test}
