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


def generate(size=None, bcol=None, blues=None, colors=None, extras=None,
             tree_odds=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    bcol: The column to start drawing lines.
    blues: Whether the lines have blue tips.
    colors: The colors of the background.
    extras: Extra offsets to add (to fix ambiguous cases).
    tree_odds: The orange-to-gray sampling odds for the forest.
  """

  def draw():
    grid, output = common.grids(size, size)
    # First, copy over the contents.
    for i, color in enumerate(colors):
      output[i // size][i % size] = grid[i // size][i % size] = color
    # Second, clear out the forest floor.
    for c in range(3):
      if blues[c]: continue
      for dc in range(-2, 3):
        common.draw(output, size - 1, bcol + c + dc, 7)
    # Third, draw the maroon lines.
    for c in range(3):
      for r in range(3):
        grid[r][bcol + c] = 9
        output[r][bcol + c] = 7
      if blues[c]: grid[2][bcol + c] = 1
      row = 2
      while row + 1 < size:
        if blues[c] and output[row + 1][bcol + c] == 5: break
        row += 1
      for r in range(3):
        offset = 0 if not extras else extras[c]
        output[row - r][bcol + c + offset] = 9
      if not blues[c]: continue
      output[row][bcol + c] = 1
      if row + 1 < size: continue
      # It's not clear if we should clear the forest floor for blue tips.
      for dc in range(-2, 3):
        if common.get_pixel(output, row, bcol + c + dc) == 5: return None, None
    return grid, output

  if size is None:
    size = common.randint(12, 24)
    bcol = common.randint(0, size - 3)
    if tree_odds is None:
      tree_odds = common.randint(9, 19)
    while True:
      blues = [common.randint(0, 1) for _ in range(3)]
      if sum(blues) == 0: continue
      colors = [
          7 if common.randint(0, tree_odds) else 5
          for _ in range(size * size)
      ]
      grid, _ = draw()
      if grid: break

  # Build the input: a forest floor (orange, with scattered gray trees) topped
  # by three maroon markers, some of them capped with a blue tip.
  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  for c in range(3):
    for r in range(3):
      grid[r][bcol + c] = common.maroon()
    if blues[c]:
      grid[2][bcol + c] = common.blue()

  # Solve it by letting each marker fall straight down its column. A plain
  # marker drops all the way to the forest floor, so first clear the trees out
  # of its landing strip (preparation, not itself a solving step).
  output = common.deepcopy(grid)

  def clear_landing_floor():
    for c in range(3):
      if blues[c]: continue
      for dc in range(-2, 3):
        common.draw(output, size - 1, bcol + c + dc, common.orange())

  clear_landing_floor()

  def drop_marker(c):
    """Column c's marker falls straight down: a plain maroon marker drops to
    the forest floor; a blue-tipped marker stops with its tip resting on the
    nearest tree below it."""
    for r in range(3):
      output[r][bcol + c] = common.orange()
    row = 2
    while row + 1 < size:
      if blues[c] and output[row + 1][bcol + c] == common.gray(): break
      row += 1
    offset = 0 if not extras else extras[c]
    for r in range(3):
      output[row - r][bcol + c + offset] = common.maroon()
    if blues[c]:
      output[row][bcol + c] = common.blue()

  drop_marker(0)
  drop_marker(1)
  drop_marker(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, bcol=13, blues=[1, 1, 1],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7,
                       7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7,
                       7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]),
      generate(size=14, bcol=5, blues=[0, 1, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 5, 5, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 7, 7, 7,
                       7, 7, 5, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7,
                       7, 5, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 7, 7]),
      generate(size=16, bcol=9, blues=[1, 1, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 5, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 5, 5, 7, 7, 7, 5,
                       7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 5, 5, 7,
                       7, 7, 5, 7, 7, 7, 5, 7, 7, 7, 5, 7, 7, 5, 7, 7,
                       5, 5, 5, 5, 7, 7, 5, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
               extras=[0, 0, 1]),
  ]
  test = [
      generate(size=16, bcol=3, blues=[1, 0, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       7, 7, 7, 5, 5, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]),
  ]
  return {"train": train, "test": test}
