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


def generate(width=None, colors=None, height=5, total_height=None,
             row_count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    colors: a list of colors to be used in the input grid
    height: half the height of the input grid
    total_height: randomized full grid height, used when colors are omitted
    row_count: number of colored prefix rows, used when colors are omitted
    num_colors: number of distinct colors to draw from, used when colors are
      omitted
  """
  if colors is None:
    if width is None:
      width = common.randint(3, 30)
    if total_height is None:
      total_height = common.randint(3, 30)
    total_height = max(2, min(30, total_height))
    max_rows = max(1, (total_height - 1) // 2)
    if num_colors is None:
      num_colors = common.randint(1, min(8, max_rows))
    num_colors = max(1, min(num_colors, 8, max_rows))
    if row_count is None:
      row_count = common.randint(num_colors, max_rows)
    row_count = max(num_colors, min(row_count, max_rows))
    palette = common.random_colors(num_colors)
    colors = [palette[r % num_colors] for r in range(row_count)]
    grid_height = total_height
  else:
    grid_height = 2 * height

  grid, output = common.grids(width, grid_height)
  for r, color in enumerate(colors):
    for c in range(width):
      output[grid_height - r - 1][c] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, colors=[2, 2, 3]),
      generate(width=5, colors=[2, 8]),
  ]
  test = [
      generate(width=6, colors=[3, 5, 5]),
  ]
  return {"train": train, "test": test}
