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


def _place_blocks(count, height, width, taken):
  """Pick up to `count` non-overlapping 2x2 block top-left corners.

  Each 2x2 footprint is kept at Chebyshev distance >= 1 from every previously
  taken footprint (recorded in `taken`), so blocks never touch.  Placement uses
  bounded rejection sampling and simply stops early if no free spot is found,
  which keeps the loop finite on dense / small grids.
  """
  corners = []
  for _ in range(count):
    placed = False
    for _attempt in range(200):
      r = common.randint(1, height - 2)
      c = common.randint(1, width - 2)
      ok = True
      for (tr, tc) in taken:
        if abs(r - tr) <= 2 and abs(c - tc) <= 2:
          ok = False
          break
      if ok:
        taken.append((r, c))
        corners.append((r, c))
        placed = True
        break
    if not placed:
      break
  return corners


def _draw_blocks(grid, output, corners, color):
  """Stamp a solid 2x2 block of `color` at each corner in both grids."""
  for (r0, c0) in corners:
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[r0 + dr][c0 + dc] = grid[r0 + dr][c0 + dc] = color


def generate(rows=None, cols=None, size=10, height=None, width=None,
             nblue=None, nred=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of two vertical coordinates where pixels should be placed
    cols: a list of two horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    nblue: how many blue (up-left ray) 2x2 blocks to place
    nred: how many red (down-right ray) 2x2 blocks to place
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    # Number of blocks of each color scales with the grid area but is bounded so
    # that placement (with a 1-cell separation ring) always succeeds quickly.
    cap = max(1, min(12, (height * width) // 28))
    if nblue is None: nblue = common.randint(1, cap)
    if nred is None: nred = common.randint(1, cap)
    taken = []
    blue_blocks = _place_blocks(nblue, height, width, taken)
    red_blocks = _place_blocks(nred, height, width, taken)
  else:
    # Backwards-compatible single-pair path (used by validate()): a blue block at
    # (rows[0], cols[0]) and a red block at (rows[1], cols[1]).
    blue_blocks = [(rows[0], cols[0])]
    red_blocks = [(rows[1], cols[1])]

  grid, output = common.grids(width, height)
  _draw_blocks(grid, output, blue_blocks, 1)
  _draw_blocks(grid, output, red_blocks, 2)
  for r0, c0 in blue_blocks:
    r, c = r0, c0
    while r >= 0 and c >= 0:
      output[r][c] = 1
      r, c = r - 1, c - 1
  for r0, c0 in red_blocks:
    r, c = r0, c0
    while r < height and c < width:
      output[r][c] = 2
      r, c = r + 1, c + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 6], cols=[2, 4]),
      generate(rows=[7, 0], cols=[6, 2]),
      generate(rows=[5, 2], cols=[3, 5]),
  ]
  test = [
      generate(rows=[3, 5], cols=[6, 2]),
  ]
  return {"train": train, "test": test}
