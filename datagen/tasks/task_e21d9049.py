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


def generate(width=None, height=None, row=None, col=None, colors=None,
             flip=None, offset=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinate where the center should be placed
    col: a horizontal coordinate where the center should be placed
    colors: a list of digits representing the colors to be used
    flip: whether to flip the diagonal calculation
    offset: the offset of the input sprite
    num_colors: the number of colors to sample when colors is None
  """
  if width is None:
    width = common.randint(10, 30)
  if height is None:
    height = common.randint(10, 30)
  if colors is None:
    if num_colors is None:
      num_colors = common.randint(2, min(9, width, height))
    colors = common.random_colors(num_colors)
  if offset is None:
    offset = common.randint(0, len(colors) - 1)
  if row is None:
    row = common.randint(offset, height - len(colors) + offset)
  if col is None:
    col = common.randint(offset, width - len(colors) + offset)
  if flip is None:
    flip = common.randint(0, 1)

  def coords(r, c):
    if flip: c = width - 1 - c
    return r, c

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      if r != row and c != col: continue
      if r + offset < row or r + offset >= row + len(colors): continue
      if c + offset < col or c + offset >= col + len(colors): continue
      rr, cc = coords(r, c)
      output[rr][cc] = grid[rr][cc] = colors[(r + c) % len(colors)]
  for c in range(width):
    rr, cc = coords(row, c)
    output[rr][cc] = colors[(row + c) % len(colors)]
  for r in range(height):
    rr, cc = coords(r, col)
    output[rr][cc] = colors[(r + col) % len(colors)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, row=4, col=2, colors=[2, 8, 3], flip=0,
               offset=2),
      generate(width=14, height=15, row=6, col=5, colors=[2, 4, 8, 3], flip=1,
               offset=2),
  ]
  test = [
      generate(width=20, height=20, row=6, col=6, colors=[2, 3, 1, 4], flip=0,
               offset=1),
  ]
  return {"train": train, "test": test}
