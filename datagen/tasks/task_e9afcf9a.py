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


def generate(colors=None, width=6, height=2, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: digits representing the colors to be used, one per row
    width: width of the input grid
    height: height of the input grid
    num_colors: how many distinct colors the row stripes draw from
  """
  if colors is None:
    if num_colors is None:
      num_colors = common.randint(1, min(9, height))
    num_colors = min(num_colors, 9)
    color_pool = common.random_colors(num_colors)
    colors = [common.choice(color_pool) for _ in range(height)]

  grid, output = common.grids(width, height)
  for c in range(width):
    for r in range(height):
      grid[r][c] = colors[r]
      output[r][c] = colors[r] if c % 2 == 0 else colors[height - 1 - r]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 9]),
      generate(colors=[4, 8]),
  ]
  test = [
      generate(colors=[6, 2]),
  ]
  return {"train": train, "test": test}
