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


def generate(size=None, rows=None, cols=None, color=None, linecolor=None,
             height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    linecolor: a digit representing a color to be used for the line
    height: the (half) vertical extent of the grid; defaults to size
    width: the (half) horizontal extent of the grid; defaults to size
    count: the number of object pixels; defaults to a re_arc-style area band
  """
  if size is None:
    if height is None:
      height = common.randint(2, 14)
    if width is None:
      width = common.randint(2, 14)
    gh, gw = height, width
    max_count = max(1, gh * gw - 1)
    if count is None:
      count = common.randint(1, max_count)
    count = min(max(1, count), max_count)
    pixels = {(common.randint(0, gh - 1), common.randint(0, gw - 1))}
    while len(pixels) < count:
      candidates = set()
      for r, c in pixels:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
              continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < gh and 0 <= nc < gw and (nr, nc) not in pixels:
              candidates.add((nr, nc))
      pixels.add(common.choice(sorted(candidates)))
    rows, cols = zip(*sorted(pixels))
    color = common.random_color()
    linecolor = common.random_color(exclude=[color])
  else:
    gh = gw = size

  grid = common.grid(2 * gw + 1, 2 * gh + 1)
  output = common.grid(2 * gw, 2 * gh)
  for idx in range(2 * gw + 1):
    grid[gh][idx] = linecolor
  for idx in range(2 * gh + 1):
    grid[idx][gw] = linecolor
  for r, c in zip(rows, cols):
    grid[r][c] = color
  for r, c in zip(rows, cols):
    output[r][c] = linecolor
  for r, c in zip(rows, cols):
    output[r][2 * gw - c - 1] = linecolor
  for r, c in zip(rows, cols):
    output[2 * gh - r - 1][c] = linecolor
  for r, c in zip(rows, cols):
    output[2 * gh - r - 1][2 * gw - c - 1] = linecolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[1, 2, 2, 3, 3], cols=[1, 0, 1, 1, 2], color=1,
               linecolor=2),
      generate(size=4, rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 1, 0], color=3,
               linecolor=8),
      generate(size=3, rows=[0, 1, 1, 2], cols=[0, 1, 2, 1], color=2,
               linecolor=4),
  ]
  test = [
      generate(size=6, rows=[0, 1, 2, 2, 3, 4, 4], cols=[2, 1, 0, 2, 2, 2, 3],
               color=8, linecolor=3),
  ]
  return {"train": train, "test": test}
