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


def generate(tops=None, bottoms=None, rows=None, cols=None, color=None,
             flop=None, xpose=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: The top colors.
    bottoms: The bottom colors.
    rows: The rows of the dust.
    cols: The columns of the dist.
    color: The color of the dust.
    flop: Whether to flop the grids.
    xpose: Whether to transpose the grids.
    density: The dust-placement denominator; dust appears with probability
      1 / (density + 1).
  """

  if tops is None:
    if density is None:
      density = 19
    color = common.random_color()
    remaining = list(range(10))
    remaining.remove(color)
    tops, bottoms = common.choices(remaining, 5), common.choices(remaining, 5)
    rows, cols = [], []
    for r in range(11):
      for c in range(abs(5 - r) + 1, 10 - abs(5 - r)):
        if c == 5 or common.randint(0, density): continue
        rows.append(r)
        cols.append(c)
    flop, xpose = common.randint(0, 1), common.randint(0, 1)
    pass

  # Input: a red diamond with a strip of colors along the top-right edge (tops)
  # and the bottom-left edge (bottoms), plus scattered "dust" pixels. Each
  # edge color beams straight into the diamond; the dust blocks the beams.
  grid = common.grid(11, 11)
  for row, col in zip(rows, cols):
    grid[row][col] = color
  for i in range(5):
    grid[i][5 - i] = grid[5 + i][i] = grid[10 - i][5 + i] = grid[5 - i][10 - i] = 2
    grid[0][10 - i], grid[10][i] = tops[i], bottoms[i]
  output = common.deepcopy(grid)

  def project_top_edge():
    """Beams each top-edge color straight down until a pixel blocks it."""
    for i in range(5):
      for r in range(6 - i, 5 + i):
        if output[r][10 - i]: break
        output[r][10 - i] = tops[i]

  def project_bottom_edge():
    """Beams each bottom-edge color straight up until a pixel blocks it."""
    for i in range(5):
      for r in range(4 + i, 5 - i, -1):
        if output[r][i]: break
        output[r][i] = bottoms[i]

  project_top_edge()
  project_bottom_edge()
  if flop: grid, output = common.flop(grid), common.flop(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[9, 8, 6, 5, 4], bottoms=[4, 7, 9, 1, 4], rows=[4, 4, 6],
               cols=[6, 7, 3], color=3, flop=False, xpose=False),
      generate(tops=[9, 8, 6, 5, 4], bottoms=[4, 0, 9, 1, 4], rows=[], cols=[],
               color=0, flop=False, xpose=False),
      generate(tops=[0, 0, 1, 1, 0], bottoms=[0, 9, 1, 0, 0], rows=[], cols=[],
               color=0, flop=True, xpose=True),
  ]
  test = [
      generate(tops=[6, 8, 8, 1, 7], bottoms=[9, 8, 7, 6, 0], rows=[3, 5, 6, 6],
               cols=[3, 3, 2, 6], color=4, flop=True, xpose=False),
  ]
  return {"train": train, "test": test}
