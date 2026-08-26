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


def generate(tops=None, bottoms=None, col=None, size=10, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: a list of column sizes for the tops
    bottoms: a list of column sizes for the bottoms
    col: how much space to leave on the left side
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if tops is None:
    col, loc = common.randint(1, 3), common.randint(1, 3)
    tops, bottoms = [], []
    # Cap the number of columns to the 9 unrolled move_column handlers so a
    # widened width never silently drops a column (and its forward step).
    last = min(width - loc, col + 9)
    for _ in range(col, last):
      top = common.randint(1, min(5, height - 1))
      bottom = 0 if top >= 4 else common.randint(1, min(6, height - top))
      tops.append(top)
      bottoms.append(bottom)

  grid, output = common.grids(width, height)
  for idx in range(len(tops)):
    top, bottom = tops[idx], bottoms[idx]
    for r in range(top):
      output[r][col + idx] = grid[r][col + idx] = common.blue()
    for r in range(bottom):
      grid[height - r - 1][col + idx] = common.red()

  def move_column(idx):
    if idx >= len(tops):
      return
    top, bottom = tops[idx], bottoms[idx]
    for r in range(bottom):
      output[top + r][col + idx] = common.red()

  move_column(0)
  move_column(1)
  move_column(2)
  move_column(3)
  move_column(4)
  move_column(5)
  move_column(6)
  move_column(7)
  move_column(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[4, 4, 2, 4, 4], bottoms=[0, 0, 3, 0, 0], col=2),
      generate(tops=[4, 4, 1, 4, 2, 5, 5], bottoms=[0, 0, 1, 0, 4, 0, 0],
               col=2),
      generate(tops=[4, 4, 1, 3, 4, 3, 4, 2, 4],
               bottoms=[0, 0, 3, 2, 0, 4, 0, 3, 0], col=1),
  ]
  test = [
      generate(tops=[4, 1, 5, 2, 3, 2, 4, 1, 5],
               bottoms=[0, 3, 0, 2, 4, 1, 0, 6, 0], col=1),
  ]
  return {"train": train, "test": test}
