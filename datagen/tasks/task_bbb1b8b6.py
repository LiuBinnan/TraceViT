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
    colors: The flattened colors of the input grid.
    gsize: The side length of each square piece.
  """

  if colors is None:
    if gsize is None:
      gsize = common.randint(3, 8)
    color = common.random_color(exclude=[1, 5])
    grid = common.grid(2 * gsize + 1, gsize)
    area = gsize * gsize
    min_fill = round(0.25 * area)
    max_fill = round(0.75 * area)
    while True:
      pattern = [common.randint(0, 1) for _ in range(area)]
      if sum(pattern) >= min_fill and sum(pattern) <= max_fill: break
    other = [1 - p for p in pattern]
    if common.randint(0, 1):
      while True:
        other = [common.randint(0, 1) for _ in range(area)]
        if sum(other) >= min_fill and sum(other) <= max_fill: break
    for r in range(gsize): grid[r][gsize] = 5
    for i, p in enumerate(pattern):
      grid[i // gsize][i % gsize] = p
    for i, p in enumerate(other):
      grid[i // gsize][i % gsize + gsize + 1] = p * color
    colors = common.flatten(grid)
  elif gsize is None:
    gsize = 4

  grid = common.grid(2 * gsize + 1, gsize)
  for i, color in enumerate(colors):
    grid[i // (2 * gsize + 1)][i % (2 * gsize + 1)] = color
  exact = True
  for r in range(gsize):
    for c in range(gsize):
      if (grid[r][c] == 0) == (grid[r][c + gsize + 1] == 0):
        exact = False

  # Solve the puzzle forward: keep only the cells that feed the answer, lay down
  # the blue key, then stack the complementary colored piece into its holes one
  # row at a time.
  output = common.deepcopy(grid)

  def isolate_pieces():
    """Keeps only the answer-relevant cells: always drops the gray divider, and
    also the right piece when it does not complete the key."""
    nonlocal output
    for r in range(gsize):
      output[r][gsize] = 0
      if not exact:
        for c in range(gsize + 1, 2 * gsize + 1):
          output[r][c] = 0

  def place_key():
    """Lays the blue key (the left mask) onto the answer canvas."""
    nonlocal output
    output = common.grid(gsize, gsize)
    for r in range(gsize):
      for c in range(gsize):
        output[r][c] = grid[r][c]

  def stack_piece_row(row):
    """Stacks one row of the complementary colored piece into the key's holes,
    only when the piece completes the key exactly."""
    nonlocal output
    if row >= gsize or not exact:
      return
    for c in range(gsize):
      output[row][c] = grid[row][c] + grid[row][c + gsize + 1]

  isolate_pieces()
  place_key()
  stack_piece_row(0)
  stack_piece_row(1)
  stack_piece_row(2)
  stack_piece_row(3)
  stack_piece_row(4)
  stack_piece_row(5)
  stack_piece_row(6)
  stack_piece_row(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 1, 1, 5, 0, 0, 0, 0,
                       1, 0, 0, 1, 5, 0, 6, 6, 0,
                       1, 0, 0, 1, 5, 0, 6, 6, 0,
                       1, 1, 1, 1, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 1, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 1, 5, 0, 0, 0, 0,
                       1, 1, 1, 1, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 1, 1, 5, 0, 0, 0, 0,
                       1, 0, 0, 0, 5, 0, 7, 7, 7,
                       1, 0, 1, 1, 5, 0, 7, 0, 0,
                       1, 0, 1, 0, 5, 0, 7, 0, 7]),
      generate(colors=[0, 0, 0, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 0, 5, 2, 2, 0, 0,
                       1, 1, 0, 0, 5, 0, 2, 2, 0,
                       1, 1, 1, 0, 5, 0, 2, 2, 0]),
      generate(colors=[1, 1, 0, 0, 5, 0, 0, 3, 3,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       1, 1, 0, 0, 5, 0, 0, 3, 3]),
      generate(colors=[1, 1, 1, 1, 5, 3, 3, 0, 0,
                       1, 0, 0, 1, 5, 3, 3, 0, 0,
                       1, 0, 0, 1, 5, 3, 0, 0, 0,
                       1, 0, 0, 1, 5, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 1, 5, 2, 2, 2, 0,
                       1, 0, 0, 0, 5, 0, 2, 2, 2,
                       1, 1, 0, 0, 5, 0, 0, 2, 2,
                       1, 1, 1, 0, 5, 0, 0, 0, 2]),
  ]
  test = [
      generate(colors=[1, 1, 1, 1, 5, 2, 0, 0, 0,
                       0, 1, 1, 0, 5, 2, 2, 2, 2,
                       0, 1, 1, 0, 5, 2, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 0, 0, 5, 0, 0, 3, 3,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       0, 0, 0, 1, 5, 3, 3, 3, 0,
                       0, 1, 1, 1, 5, 3, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
