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


def generate(cols=None, size=5, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where towers are placed
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if cols is None:
    towers = common.randint(1, 2)
    while True:
      cols = common.sample(range(width), towers)
      if len(cols) == 1: break
      if abs(cols[0] - cols[1]) > 1: break

  grid, output = common.grids(width, height)
  for c in range(width):
    output[height - 1][c] = grid[height - 1][c] = common.gray()

  def draw_tower(idx):
    if idx >= len(cols):
      return
    c = cols[idx]
    output[height - 2][c] = grid[height - 2][c] = common.gray()
    output[height - 1][c] = grid[height - 3][c] = common.blue()

  draw_tower(0)
  draw_tower(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[2]),
      generate(cols=[1, 3]),
      generate(cols=[1, 4]),
  ]
  test = [
      generate(cols=[2, 4]),
  ]
  return {"train": train, "test": test}
