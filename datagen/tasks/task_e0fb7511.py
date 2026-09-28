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
    colors: A list of colors to use.
    gsize: The side length of the square grid.
  """

  if gsize is None:
    gsize = 13

  def draw():
    grid, output = common.grids(gsize, gsize)
    for i, color in enumerate(colors):
      output[i // gsize][i % gsize] = grid[i // gsize][i % gsize] = color
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col]: continue
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          if common.get_pixel(grid, row + dr, col + dc) == 0:
            output[row][col] = 8
    if common.flatten(output).count(8) < gsize: return None, None
    return grid, output

  if colors is None:
    while True:
      colors = [common.randint(0, 7) for _ in range(gsize * gsize)]
      colors = [1 if color else 0 for color in colors]
      grid, _ = draw()
      if grid: break

  # The solving story: cyan floods every background gap, then drains back out
  # of the isolated single-cell pockets, so only background cells that touch
  # another background cell (connected gaps) stay cyan.
  grid, _ = draw()
  output = common.deepcopy(grid)

  def flood_gaps():
    """Cyan floods every background gap in the grid."""
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col] == 0:
          output[row][col] = common.cyan()

  def drain_isolated():
    """Cyan drains back out of the lone, isolated background pockets."""
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col] != 0: continue
        lonely = True
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          if common.get_pixel(grid, row + dr, col + dc) == 0:
            lonely = False
        if lonely:
          output[row][col] = common.black()

  flood_gaps()
  drain_isolated()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1,
                       1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1,
                       1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                       1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1,
                       1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1,
                       1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                       1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
                       0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                       1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1]),
      generate(colors=[1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
                       1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0,
                       1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                       0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,
                       0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                       1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1,
                       0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1]),
      generate(colors=[1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,
                       0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1,
                       1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                       1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0,
                       0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                       1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
                       0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1]),
  ]
  test = [
      generate(colors=[1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1,
                       0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0,
                       1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0,
                       0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                       1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                       1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0,
                       1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
                       1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0,
                       1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0,
                       1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1,
                       0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1,
                       1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0,
                       1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
