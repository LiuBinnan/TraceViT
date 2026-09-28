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


def generate(colors=None, flip=None, flop=None, xpose=None, gheight=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: colors of the pixels.
    flip: whether to flip the grid.
    flop: whether to flop the grid.
    xpose: whether to transpose the grid.
    gheight: rows per color group (board has 2*gheight+1 rows). Defaults to a
      rule-faithful band; the original behavior is gheight=3 (a 7-row board).
  """

  if colors is None:
    if gheight is None:
      gheight = common.randint(2, 3)
    nrows = 2 * gheight + 1
    colors = [0] * (6 * nrows)
    fgcolors = common.random_colors(2, exclude=[1, 8])
    for group in [0, 1]:
      for r in range(gheight):
        cols = common.sample([0, 1, 2], common.randint(1, 3))
        for col in cols:
          colors[(group * (gheight + 1) + r) * 6 + col] = fgcolors[group]
    for r in range(nrows):
      cols = common.sample([0, 1, 2], common.randint(1, 3))
      for col in cols:
        colors[r * 6 + col + 3] = 8
    flip = common.randint(0, 1)
    flop = common.randint(0, 1)
    xpose = common.randint(0, 1)
    pass

  grid = common.grid(30, 30)
  for c in range(30):
    grid[0][c] = 1
  for i, color in enumerate(colors):
    row, col = i // 6, i % 6
    if col > 2: col += 1
    for r, c in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
      grid[4 * row + r + 3][4 * col + c + 2 + (1 if flop else 0)] = color
  if flip: grid = common.flip(grid)
  if flop: grid = common.flop(grid)
  if xpose: grid = common.transpose(grid)

  # Bookkeeping (no randomness): the de-magnified 6x7 reading of the rings, in
  # the canonical (pre-reorientation) frame.
  raw = common.grid(6, len(colors) // 6)
  for i, color in enumerate(colors):
    raw[i // 6][i % 6] = color

  def reorient(subgrid):
    """Re-expresses a canonical-frame grid in the puzzle's final orientation."""
    subgrid = common.deepcopy(subgrid)
    if flip: subgrid = common.flip(subgrid)
    if flop: subgrid = common.flop(subgrid)
    if xpose: subgrid = common.transpose(subgrid)
    return subgrid

  output = common.grid(6, len(colors) // 6)

  def read_shapes():
    """Reads each ring into its cell (de-magnify), in the final orientation."""
    nonlocal output
    output = reorient(raw)

  def apply_gravity():
    """Slides every row's colors hard to the right, in the final orientation."""
    nonlocal output
    packed = common.deepcopy(raw)
    for r in range(len(raw)):
      target = 5
      for c in range(5, -1, -1):
        if packed[r][c] != 0:
          temp = packed[r][c]
          packed[r][c] = 0
          packed[r][target] = temp
          target -= 1
    output = reorient(packed)

  read_shapes()
  apply_gravity()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 2, 8, 8, 8,
                       0, 2, 0, 8, 0, 0,
                       2, 2, 2, 8, 8, 0,
                       0, 0, 0, 0, 8, 8,
                       3, 3, 3, 8, 8, 8,
                       0, 3, 3, 8, 0, 0,
                       0, 3, 3, 8, 8, 8],
               flip=False, flop=False, xpose=False),
      generate(colors=[4, 4, 4, 8, 8, 8,
                       4, 0, 4, 0, 8, 8,
                       4, 4, 4, 8, 8, 8,
                       0, 0, 0, 0, 8, 0,
                       6, 6, 0, 8, 8, 8,
                       6, 0, 6, 0, 8, 8,
                       6, 6, 0, 8, 8, 8],
               flip=True, flop=False, xpose=True),
      generate(colors=[4, 4, 4, 0, 8, 8,
                       0, 4, 4, 0, 0, 8,
                       4, 4, 0, 8, 8, 8,
                       0, 0, 0, 8, 0, 8,
                       0, 9, 0, 8, 0, 8,
                       9, 9, 9, 8, 8, 8,
                       9, 0, 9, 0, 0, 8],
               flip=True, flop=True, xpose=False),
  ]
  test = [
      generate(colors=[2, 2, 2, 8, 8, 8,
                       0, 0, 2, 0, 8, 0,
                       2, 2, 2, 0, 8, 8,
                       0, 0, 0, 0, 0, 8,
                       7, 0, 7, 0, 8, 0,
                       7, 7, 7, 8, 8, 8,
                       7, 0, 0, 0, 8, 8],
               flip=False, flop=True, xpose=True),
  ]
  return {"train": train, "test": test}
