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


def generate(rows=None, cols=None, colors=None, size=7, height=None, width=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid (square fallback)
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: the number of connected creature cells
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    # Creature lives in the interior (1-cell border on top/left; the bottom row
    # is reserved for the marker pixel).  Region is (width-2) x (height-2),
    # i.e. 5x5 for the original 7x7 grid.
    region_h, region_w = height - 2, width - 2
    cells = region_h * region_w
    max_count = min(cells, max(2, (2 * cells) // 3 + 1))
    if count is None:
      count = common.randint(2, max_count)
    # Cap the cell count to the available region so the creature always fits
    # (continuous_creature loops forever if asked for more cells than exist).
    count = min(max(1, count), max_count)
    start = (common.randint(0, region_h - 1), common.randint(0, region_w - 1))
    pixels, pixel_set = [start], {start}
    frontier, frontier_set = [], set()
    directions = [
        (1, 0), (0, 1), (-1, 0), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    for dr, dc in directions:
      nr, nc = start[0] + dr, start[1] + dc
      if 0 <= nr < region_h and 0 <= nc < region_w:
        frontier.append((nr, nc))
        frontier_set.add((nr, nc))
    while len(pixels) < count:
      idx = common.randint(0, len(frontier) - 1)
      pixel = frontier.pop(idx)
      frontier_set.remove(pixel)
      pixels.append(pixel)
      pixel_set.add(pixel)
      for dr, dc in directions:
        nr, nc = pixel[0] + dr, pixel[1] + dc
        if nr < 0 or nr >= region_h or nc < 0 or nc >= region_w:
          continue
        if (nr, nc) in pixel_set or (nr, nc) in frontier_set:
          continue
        frontier.append((nr, nc))
        frontier_set.add((nr, nc))
    rows, cols = [p[0] + 1 for p in pixels], [p[1] + 1 for p in pixels]
    colors = common.random_colors(2)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c], output[r][c] = colors[0], colors[1]
  grid[height - 1][0] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 5],
               cols=[1, 2, 3, 2, 1, 2, 3, 4, 2, 3, 4, 3], colors=[2, 4]),
      generate(rows=[1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5],
               cols=[3, 2, 3, 4, 1, 2, 3, 4, 1, 2, 2, 3], colors=[3, 6]),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5],
               cols=[1, 2, 3, 1, 2, 3, 4, 5, 3, 4, 2, 3, 2, 3, 4],
               colors=[8, 2]),
  ]
  return {"train": train, "test": test}
