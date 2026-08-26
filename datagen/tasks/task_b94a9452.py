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


def generate(width=None, height=None, row=None, col=None, thicks=None,
             colors=None, crh=None, crw=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinates where the square should be placed
    col: a horizontal coordinates where the square should be placed
    thicks: how thick the creme and the cookie should be
    colors: the colors of the creme and the cookie
    crh: the height of the inner creme block (defaults to thicks[0])
    crw: the width of the inner creme block (defaults to thicks[0])
  """
  if width is None:
    thicks = [common.randint(1, 2) for _ in range(2)]
    if crh is None:
      crh = common.randint(1, 2)
    if crw is None:
      crw = common.randint(1, 2)
    # sprite extent = creme extent + border on both sides
    gh = crh + 2 * thicks[1]
    gw = crw + 2 * thicks[1]
    # grid must be large enough to hold the sprite with a 1-cell margin
    height = common.randint(gh + 2, max(15, gh + 4))
    width = common.randint(gw + 2, max(15, gw + 4))
    row = common.randint(1, height - gh - 1)
    col = common.randint(1, width - gw - 1)
    colors = common.random_colors(2)

  if crh is None:
    crh = thicks[0]
  if crw is None:
    crw = thicks[0]
  gh = crh + 2 * thicks[1]
  gw = crw + 2 * thicks[1]
  grid, output = common.grid(width, height), common.grid(gw, gh)
  for r in range(gh):
    for c in range(gw):
      grid[row + r][col + c] = colors[1]
      output[r][c] = colors[0]
  for r in range(crh):
    for c in range(crw):
      grid[row + r + thicks[1]][col + c + thicks[1]] = colors[0]
      output[r + thicks[1]][c + thicks[1]] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=12, row=1, col=3, thicks=[2, 1], colors=[4, 2]),
      generate(width=11, height=12, row=2, col=4, thicks=[1, 1], colors=[3, 1]),
      generate(width=13, height=12, row=6, col=2, thicks=[1, 2], colors=[6, 4]),
  ]
  test = [
      generate(width=13, height=14, row=1, col=2, thicks=[2, 2], colors=[8, 3]),
  ]
  return {"train": train, "test": test}
