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


def generate(rows=None, cols=None, groups=None, colors=None, flip=None,
             xpose=None, ngroups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    groups: The groups of the pixels.
    colors: The colors of the groups.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
    ngroups: The number of framed swatch-and-sprite groups.
  """

  if rows is None:
    if ngroups is None:
      ngroups = common.randint(2, 7)
    colors = common.random_colors(ngroups, exclude=[1, 4])
    rows, cols, groups = [], [], []
    for group in range(ngroups):
      r, c = common.conway_sprite(3, 3)
      rows.extend(r)
      cols.extend(c)
      groups.extend([group] * len(r))
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
  elif ngroups is None:
    ngroups = 3

  # Input: groups framed by yellow lines; each group has a color swatch
  # on the top row and a blue shape below. Build it first, logic unchanged, then
  # orient it (flip/transpose) up front so output can be built already oriented.
  grid = common.grid(4 * ngroups - 1, 7)
  for col in range(4 * ngroups - 1):
    grid[3][col] = 4
  for row in range(7):
    for group in range(ngroups - 1):
      grid[row][4 * group + 3] = 4
  for group in range(ngroups):
    grid[1][4 * group + 1] = colors[group]
  for row, col, group in zip(rows, cols, groups):
    grid[row + 4][4 * group + col] = 1
  if flip: grid = common.flip(grid)
  if xpose: grid = common.transpose(grid)

  # The answer is the input with each column's blue shape repainted in that
  # column's swatch color. Start from a copy and route every recolor through
  # put(), which writes directly in the input's final orientation.
  output = common.deepcopy(grid)

  def put(r, c, value):
    if flip: r = 6 - r
    if xpose: r, c = c, r
    output[r][c] = value

  def recolor_column(group):
    for row, col, g in zip(rows, cols, groups):
      if g == group:
        put(row + 4, 4 * group + col, colors[group])

  recolor_column(0)
  recolor_column(1)
  recolor_column(2)
  for group in range(3, ngroups):
    recolor_column(group)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 0, 2, 0, 1, 2, 2, 0, 2, 0, 1, 1, 2], groups=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], colors=[7, 3, 8], flip=False, xpose=True),
      generate(rows=[0, 1, 2, 2, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2], cols=[0, 1, 0, 1, 2, 1, 0, 1, 2, 0, 2, 0, 2, 0, 2, 1], groups=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2], colors=[3, 2, 6], flip=False, xpose=False),
  ]
  test = [
      generate(rows=[1, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 1, 2, 2], cols=[1, 2, 0, 2, 0, 1, 1, 2, 2, 0, 1, 2, 0, 2], groups=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], colors=[6, 2, 8], flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
