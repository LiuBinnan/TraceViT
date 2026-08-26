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


def _has_free_interior(lengths, width, height):
  """True if the edge lines drawn from `lengths` leave a free interior row or
  column (so green will be painted and input != output). Used only to reject
  degenerate synthetic draws -- mirrors the actual edge-fill below."""
  occupied = [[0] * width for _ in range(height)]
  idx = 0
  for c in range(width):
    for r in range(lengths[idx]):
      occupied[r][c] = 1
    idx += 1
  for r in range(height):
    for c in range(width - lengths[idx], width):
      occupied[r][c] = 1
    idx += 1
  for c in range(width - 1, -1, -1):
    for r in range(height - lengths[idx], height):
      occupied[r][c] = 1
    idx += 1
  for r in range(height - 1, -1, -1):
    for c in range(lengths[idx]):
      occupied[r][c] = 1
    idx += 1
  free_row = any(all(occupied[r][c] == 0 for c in range(1, width - 1))
                 for r in range(1, height - 1))
  free_col = any(all(occupied[r][c] == 0 for r in range(1, height - 1))
                 for c in range(1, width - 1))
  return free_row or free_col


def generate(size=None, numred=None, flip=None, xpose=None, lengths=None,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    numred: the number of red columns
    flip: whether to flip the grid
    xpose: whether to transpose the grid
    lengths: the lengths of the columns
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if size is None:
    if height is None:
      height = common.randint(7, 30)
    if width is None:
      width = common.randint(7, 30)
    numred = common.randint(5 * (width + height) // 6, 7 * (width + height) // 6)
    lengths = [max(1, common.randint(0, 3)) for _ in range(2 * width + 2 * height)]
    while not _has_free_interior(lengths, width, height):
      lengths = [max(1, common.randint(0, 3)) for _ in range(2 * width + 2 * height)]
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
  else:
    height = width = size

  raw_grid, raw_output = common.grids(width, height)
  def orient(thegrid):
    thegrid = thegrid[::-1] if flip else thegrid
    return common.transpose(thegrid) if xpose else thegrid

  output = orient(raw_output)
  idx = 0
  for c in range(width):
    for r in range(lengths[idx]):
      color = common.red() if idx < numred else common.cyan()
      raw_output[r][c] = raw_grid[r][c] = color
    idx += 1
  output = orient(raw_output)
  for r in range(height):
    for c in range(width - lengths[idx], width):
      color = common.red() if idx < numred else common.cyan()
      raw_output[r][c] = raw_grid[r][c] = color
    idx += 1
  output = orient(raw_output)
  for c in range(width - 1, -1, -1):
    for r in range(height - lengths[idx], height):
      color = common.red() if idx < numred else common.cyan()
      raw_output[r][c] = raw_grid[r][c] = color
    idx += 1
  output = orient(raw_output)
  for r in range(height - 1, -1, -1):
    for c in range(lengths[idx]):
      color = common.red() if idx < numred else common.cyan()
      raw_output[r][c] = raw_grid[r][c] = color
    idx += 1
  output = orient(raw_output)
  def draw_green_rows():
    nonlocal output
    for r in range(1, height - 1):
      free = True
      for c in range(1, width - 1):
        if raw_grid[r][c]: free = False
      if not free: continue
      for c in range(1, width - 1):
        raw_output[r][c] = common.green()
    output = orient(raw_output)

  def draw_green_cols():
    nonlocal output
    for c in range(1, width - 1):
      free = True
      for r in range(1, height - 1):
        if raw_grid[r][c]: free = False
      if not free: continue
      for r in range(1, height - 1):
        raw_output[r][c] = common.green()
    output = orient(raw_output)

  draw_green_rows()
  draw_green_cols()
  grid = orient(raw_grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, numred=19, flip=0, xpose=0,
               lengths=[1, 1, 1, 1, 2, 3, 1, 2, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 3, 2, 1, 1, 2, 3, 1, 1, 3,
                        2, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
      generate(size=12, numred=27, flip=0, xpose=1,
               lengths=[0, 1, 2, 1, 1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2,
                        1, 1, 2, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                        2, 3, 4, 2, 1, 1, 1, 1, 1, 1]),
      generate(size=10, numred=20, flip=1, xpose=0,
               lengths=[0, 2, 1, 1, 1, 2, 3, 3, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1,
                        1, 0, 1, 2, 1, 2, 3, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1,
                        1, 1, 1]),
  ]
  test = [
      generate(size=14, numred=27, flip=1, xpose=0,
               lengths=[0, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 3, 3, 3, 3, 2, 1, 1,
                        1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1,
                        2, 3, 3, 3, 3, 3, 3, 1, 3, 2, 1, 2, 2, 2, 1, 2, 2, 1]),
  ]
  return {"train": train, "test": test}
