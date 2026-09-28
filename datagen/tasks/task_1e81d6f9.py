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


def generate(target=None, colors=None, density=None, color_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    target: The target color.
    colors: The colors to use for the grid.
    density: The percentage of field cells that receive a non-black color.
    color_count: The number of non-black colors available in the field.
  """

  if target is None:
    target = common.random_color(exclude=[5])
    if density is None:
      density = common.randint(5, 40)
    if color_count is None:
      color_count = common.randint(2, 9)
    field_colors = [target]
    field_colors += common.random_colors(color_count - 1, exclude=[target])
    while True:
      colors = [0] * (15 * 15)
      for i in range(len(colors)):
        if common.randint(1, 100) <= density:
          colors[i] = field_colors[common.randint(0, len(field_colors) - 1)]
      if any(colors[row * 15 + col] == target
             for row in range(15) for col in range(15)
             if row >= 4 or col >= 4):
        break

  grid = common.grid(15, 15)
  for i, color in enumerate(colors):
    grid[i // 15][i % 15] = color
  common.rect(grid, 5, 5, -1, -1, 5)
  common.rect(grid, 3, 3, 0, 0, 0)
  grid[1][1] = target
  output = common.deepcopy(grid)

  def erase_target_row(row):
    """Erases target-colored cells in one scan row."""
    for col in range(15):
      if (row, col) == (1, 1): continue
      if output[row][col] == target:
        output[row][col] = common.black()

  erase_target_row(0)
  erase_target_row(1)
  erase_target_row(2)
  erase_target_row(3)
  erase_target_row(4)
  erase_target_row(5)
  erase_target_row(6)
  erase_target_row(7)
  erase_target_row(8)
  erase_target_row(9)
  erase_target_row(10)
  erase_target_row(11)
  erase_target_row(12)
  erase_target_row(13)
  erase_target_row(14)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(target=4, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 4, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                 0, 0, 3, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0,
                                 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 3, 2, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0,
                                 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                                 0, 0, 0, 0, 0, 3, 0, 7, 8, 0, 0, 0, 0, 0, 0]),
      generate(target=2, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 0, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 6, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]),
      generate(target=3, colors=[0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 9, 0, 0, 0, 9,
                                 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 9, 0, 1,
                                 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                                 0, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 9, 0, 0, 0, 0, 5, 0, 0, 0, 0, 2, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 0, 9,
                                 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0, 1, 0, 0, 8]),
  ]
  test = [
      generate(target=1, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 8, 0, 0, 0, 7,
                                 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 6, 2, 0,
                                 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 0,
                                 0, 0, 0, 1, 0, 8, 7, 0, 0, 0, 0, 0, 0, 3, 0,
                                 0, 0, 0, 0, 7, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 6, 6, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 0,
                                 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
