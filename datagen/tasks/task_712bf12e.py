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


def generate(width=None, height=None, colors=None, count=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The number of columns in the grid.
    height: The number of rows in the grid.
    colors: The flattened input grid.
    count: The number of red path starters on the bottom row.
    density: The approximate percentage of gray obstacle cells.
  """

  def make_base():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    return grid, output

  def route_path(output, col):
    r, c = height - 1, col
    if output[r][c - 1] == 2:
      return False
    while True:
      if r == 0 or output[r - 1][c] == 0:
        r -= 1
      elif output[r - 1][c] == 5:
        c += 1
      else:
        return False
      if r < 0 or c >= width or output[r][c] == 5:
        break
      output[r][c] = 2
    return True

  def draw():
    grid, output = make_base()
    for col in range(width):
      if grid[height - 1][col] != 2:
        continue
      red_before = sum(row.count(2) for row in output)
      if (not route_path(output, col) or
          sum(row.count(2) for row in output) == red_before):
        return None, None
    return grid, output

  if colors is None:
    if width is None:
      width = common.randint(12, 24)
    if height is None:
      height = common.randint(12, 24)
    if count is None:
      count = common.randint(2, 5)
    if density is None:
      density = common.randint(15, 35)
    grid = None
    for _ in range(128):
      colors = [5 if common.randint(1, 100) <= density else 0
                for _ in range(width * height)]
      cols = sorted(common.sample(list(range(1, width - 1)), count))
      for col in cols:
        colors[width * (height - 1) + col] = 2
      grid, routed = draw()
      if grid:
        break
    if grid is None:
      # Guaranteed rule-faithful fallback: nonadjacent starters have clear
      # vertical corridors, while gray noise remains randomized elsewhere.
      cols = sorted(common.sample(list(range(1, width - 1, 2)), count))
      colors = [0 for _ in range(width * height)]
      eligible = [i for i in range(width * height) if i % width not in cols]
      gray_count = min(len(eligible), width * height * density // 100)
      for i in common.sample(eligible, gray_count):
        colors[i] = 5
      for col in cols:
        colors[width * (height - 1) + col] = 2

  grid, output = make_base()
  red_cols = [col for col in range(width) if grid[height - 1][col] == 2]

  def route_red(index):
    if index < len(red_cols):
      route_path(output, red_cols[index])

  route_red(0)
  route_red(1)
  route_red(2)
  for col in red_cols[3:]:
    route_path(output, col)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=13,
               colors=[0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       5, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5,
                       5, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0,
                       5, 0, 2, 0, 0, 2, 0, 5, 5, 0, 2, 0, 0, 0]),
      generate(width=13, height=12,
               colors=[0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0,
                       0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0]),
      generate(width=15, height=13,
               colors=[0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0,
                       5, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0,
                       0, 5, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0,
                       0, 5, 5, 2, 0, 0, 0, 2, 0, 2, 0, 0, 5, 5, 0]),
  ]
  test = [
      generate(width=13, height=13,
               colors=[0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       5, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0,
                       0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 5, 5, 0]),
  ]
  return {"train": train, "test": test}
