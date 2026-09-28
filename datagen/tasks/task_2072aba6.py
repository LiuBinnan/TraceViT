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
    colors: A list of colors to use.
  """

  if colors is None:
    while True:
      colors = [common.randint(0, 1) for _ in range(9)]
      if sum(colors) >= 2 and sum(colors) <= 8: break

  grid = common.grid(3, 3)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = 5 * color
  active_indices = [i for i, color in enumerate(colors) if color]
  output = common.grid(6, 6)

  def tile_active_cell(order):
    """Expands one active input cell into a checker tile."""
    if order >= len(active_indices): return
    i = active_indices[order]
    row, col = i // 3, i % 3
    output[2 * row][2 * col] = common.blue()
    output[2 * row + 1][2 * col] = common.red()
    output[2 * row + 1][2 * col + 1] = common.blue()
    output[2 * row][2 * col + 1] = common.red()

  tile_active_cell(0)
  tile_active_cell(1)
  tile_active_cell(2)
  tile_active_cell(3)
  tile_active_cell(4)
  tile_active_cell(5)
  tile_active_cell(6)
  tile_active_cell(7)
  tile_active_cell(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 1]),
      generate(colors=[0, 1, 0, 1, 1, 1, 0, 1, 0]),
      generate(colors=[0, 1, 0, 0, 1, 1, 1, 1, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 1, 0, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
