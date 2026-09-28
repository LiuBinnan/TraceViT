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


def generate(colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    gsize: The height and width of the square grids.
  """

  if colors is None:
    if gsize is None:
      gsize = common.randint(8, 20)
    while True:
      colors = [0] * (gsize * gsize)
      for color in range(1, 5):
        for _ in range(common.randint(2, min(12, gsize - 1))):
          colors[common.randint(0, gsize * gsize - 1)] = color
      good = True
      for color in range(1, 5):
        if not colors.count(color): good = False
      if good: break
  elif gsize is None:
    gsize = 10

  # Build the input grid: the scattered colored pixels.
  grid, output = common.grids(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color

  # Solve forward by summarizing: every colored pixel participates in the count,
  # so there is nothing to erase first. Tally each color 1..4 in turn and stack
  # its count as a bar rising from the bottom of its own column (color 1 -> col
  # 0, ... color 4 -> col 3). One frame per color/bar; the four colors are always
  # present (the sampler guarantees a nonzero count for each), so four frames.
  def tally(color):
    """Counts `color`'s pixels and stacks them as a bar in column color-1."""
    for r in range(colors.count(color)):
      output[gsize - 1 - r][color - 1] = color

  tally(1)
  tally(2)
  tally(3)
  tally(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 4, 0, 3, 3, 0, 0, 1, 3, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 0, 0, 0, 2, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 4,
                       3, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0,
                       4, 0, 1, 0, 1]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                       0, 2, 0, 0, 0, 0, 3, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0,
                       0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 4,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0,
                       0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 0,
                       0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 2, 4, 0, 0,
                       0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3, 4, 0, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 0, 1, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 2,
                       4, 0, 2, 4, 2]),
  ]
  return {"train": train, "test": test}
