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
    colors: The colors of the input grid.
  """

  if colors is None:
    subset = common.random_colors(common.randint(2, 6))
    while True:
      colors = common.choices(subset, 9)
      if len(set(colors)) == len(subset): break

  num_colors = len(set(colors))
  grid = common.grid(3, 3)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = color
  output = common.grid(3 * num_colors, 3 * num_colors)

  def place_row_band(row):
    """Tiles the 3x3 input across every column of fractal macro-row `row`."""
    nonlocal output
    if row >= num_colors: return
    for col in range(num_colors):
      for i, color in enumerate(colors):
        output[row * 3 + i // 3][col * 3 + i % 3] = color

  place_row_band(0)
  place_row_band(1)
  place_row_band(2)
  place_row_band(3)
  for r in range(4, num_colors):
    place_row_band(r)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 7, 7, 7, 2, 2, 7, 7, 2]),
      generate(colors=[3, 4, 4, 3, 3, 3, 3, 4, 4]),
      generate(colors=[8, 2, 1, 1, 8, 3, 2, 1, 3]),
      generate(colors=[2, 3, 2, 3, 3, 2, 2, 2, 1]),
      generate(colors=[9, 7, 9, 9, 6, 7, 7, 6, 6]),
  ]
  test = [
      generate(colors=[4, 3, 2, 2, 1, 4, 3, 1, 2]),
  ]
  return {"train": train, "test": test}
