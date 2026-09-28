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


def generate(colors=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the grid.
    length: The length of the vertical strip.
  """

  if colors is None:
    if length is None:
      length = common.choice([5, 7, 9])
    colors = common.sample(list(range(10)), length)
  elif length is None:
    length = len(colors)

  grid = common.grid(1, length)
  for i in range(length):
    grid[i][0] = colors[i]
  output = common.deepcopy(grid)

  def swap_top_pair():
    """Swaps the top two cells of the strip (rows 0 and 1)."""
    output[0][0], output[1][0] = grid[1][0], grid[0][0]

  def swap_bottom_pair():
    """Swaps the bottom two cells of the strip."""
    output[length - 2][0], output[length - 1][0] = (
        grid[length - 1][0], grid[length - 2][0])

  swap_top_pair()
  swap_bottom_pair()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 0, 1, 6, 8]),
      generate(colors=[4, 3, 6, 2, 8]),
  ]
  test = [
      generate(colors=[4, 5, 6, 7, 2]),
  ]
  return {"train": train, "test": test}
