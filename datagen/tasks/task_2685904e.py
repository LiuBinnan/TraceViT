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


def generate(length=None, colors=None, subset_size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length to match.
    colors: The colors to use.
    subset_size: The number of candidate colors used for a random row.
  """

  def draw():
    grid = common.grid(10, 10)
    for c in range(length):
      grid[0][c] = 8
    matches = False
    for c, color in enumerate(colors):
      grid[8][c] = color
      grid[6][c] = 5
      if colors.count(color) != length: continue
      matches = True
    if not matches: return None, None
    return grid, None

  if length is None:
    length = common.randint(1, 5)
    if subset_size is None:
      subset_size = common.randint(2, 5)
    subset = common.sample([1, 2, 3, 4, 6, 7, 8, 9], subset_size)
    while True:
      colors = common.choices(subset, 10)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()
  if grid is None: return {"input": grid, "output": None}
  output = common.grid(10, 10)

  def paint_reference_rows():
    for c in range(length):
      output[0][c] = common.cyan()
    for c in range(10):
      output[6][c] = common.gray()

  def reveal_matching_row(r):
    if r >= length: return
    if r == 0:
      for c, color in enumerate(colors):
        output[8][c] = color
    for c, color in enumerate(colors):
      if colors.count(color) == length:
        output[5 - r][c] = color

  paint_reference_rows()
  reveal_matching_row(0)
  reveal_matching_row(1)
  reveal_matching_row(2)
  reveal_matching_row(3)
  reveal_matching_row(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, colors=[2, 3, 3, 2, 3, 1, 1, 3, 1, 1]),
      generate(length=1, colors=[6, 6, 4, 6, 2, 1, 9, 2, 9, 4]),
      generate(length=3, colors=[4, 1, 4, 4, 6, 3, 1, 6, 3, 6]),
      generate(length=4, colors=[2, 1, 2, 1, 2, 1, 1, 2, 2, 2]),
      generate(length=3, colors=[8, 6, 4, 3, 4, 7, 3, 8, 3, 7]),
      generate(length=1, colors=[1, 3, 1, 1, 1, 1, 4, 1, 1, 1]),
  ]
  test = [
      generate(length=2, colors=[2, 3, 6, 4, 6, 2, 4, 4, 3, 9]),
  ]
  return {"train": train, "test": test}
