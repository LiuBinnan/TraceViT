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


def generate(width=None, height=None, rows=None, lefts=None, rights=None,
             cols=None, lows=None, highs=None, row_colors=None,
             col_colors=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates for flat sticks
    lefts: a list of left coordinates for flat sticks
    rights: a list of right coordinates for flat sticks
    cols: a list of horizontal coordinates for tall sticks
    lows: a list of low coordinates for tall sticks
    highs: a list of high coordinates for tall sticks
    row_colors: a list of digits representing colors for flat sticks
    col_colors: a list of digits representing colors for tall sticks
    count: number of sticks to draw (widens color/object/density variety)
  """
  if width is None:
    # Widen the structural tail toward re_arc: sample the grid size across the
    # full (6, 30) band (not just 10/20/30 multiples) and the stick count
    # across (2, ...) (not the fixed 5). The count is capped by the smaller
    # grid dimension so the corridor-rejection loop stays feasible, and by 8 so
    # every stick still receives a distinct non-background color. The unrolled
    # draw handlers below end with an open `range(4, len(sticks))` block, so no
    # stick is dropped when count exceeds the original 5.
    width = common.randint(6, 30)
    height = common.randint(6, 30)
    cap = min(8, min(width, height) - 3)
    if count is None:
      count = common.randint(2, cap)
    else:
      count = max(2, min(count, cap))
    success = False
    while not success:
      success = True
      rows, cols = [], []
      lefts, rights, lows, highs = [], [], [], []
      # First, pick directions and ensure they all get unique corridors.
      for _ in range(count):
        direction = common.randint(0, 1)
        if direction == 0:
          row = common.randint(0, height - 1)
          if row in rows: success = False
          rows.append(row)
        else:
          col = common.randint(0, width - 1)
          if col in cols: success = False
          cols.append(col)
      # Second, pick endpoints, and prevent clobbering with other sticks.
      for _ in rows:
        left, right = common.randint(0, width - 1), common.randint(0, width - 1)
        if abs(right - left) < 2 or left in cols or right in cols:
          success = False
        lefts.append(min(left, right))
        rights.append(max(left, right))
      for _ in cols:
        low, high = common.randint(0, height - 1), common.randint(0, height - 1)
        if abs(high - low) < 2 or low in rows or high in rows:
          success = False
        lows.append(min(low, high))
        highs.append(max(low, high))
    # Finally, pick a distinct color for each stick (one per corridor).
    colors = common.random_colors(len(rows) + len(cols))
    row_colors = colors[:len(rows)]
    col_colors = colors[len(rows):]

  grid, output = common.grids(width, height)
  sticks = (
      [("row", row, left, right, color)
       for row, left, right, color in zip(rows, lefts, rights, row_colors)] +
      [("col", col, low, high, color)
       for col, low, high, color in zip(cols, lows, highs, col_colors)])
  for idx in range(0, min(1, len(sticks))):
    orient, pos, start, end, color = sticks[idx]
    if orient == "row":
      grid[pos][start] = grid[pos][end] = color
      for c in range(start, end + 1):
        output[pos][c] = color
    else:
      grid[start][pos] = grid[end][pos] = color
      for r in range(start, end + 1):
        output[r][pos] = color
  for idx in range(1, min(2, len(sticks))):
    orient, pos, start, end, color = sticks[idx]
    if orient == "row":
      grid[pos][start] = grid[pos][end] = color
      for c in range(start, end + 1):
        output[pos][c] = color
    else:
      grid[start][pos] = grid[end][pos] = color
      for r in range(start, end + 1):
        output[r][pos] = color
  for idx in range(2, min(3, len(sticks))):
    orient, pos, start, end, color = sticks[idx]
    if orient == "row":
      grid[pos][start] = grid[pos][end] = color
      for c in range(start, end + 1):
        output[pos][c] = color
    else:
      grid[start][pos] = grid[end][pos] = color
      for r in range(start, end + 1):
        output[r][pos] = color
  for idx in range(3, min(4, len(sticks))):
    orient, pos, start, end, color = sticks[idx]
    if orient == "row":
      grid[pos][start] = grid[pos][end] = color
      for c in range(start, end + 1):
        output[pos][c] = color
    else:
      grid[start][pos] = grid[end][pos] = color
      for r in range(start, end + 1):
        output[r][pos] = color
  for idx in range(4, len(sticks)):
    orient, pos, start, end, color = sticks[idx]
    if orient == "row":
      grid[pos][start] = grid[pos][end] = color
      for c in range(start, end + 1):
        output[pos][c] = color
    else:
      grid[start][pos] = grid[end][pos] = color
      for r in range(start, end + 1):
        output[r][pos] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=30, rows=[6, 20], lefts=[3, 2], rights=[11, 7],
               cols=[4, 6, 14], lows=[18, 2, 12], highs=[27, 13, 17],
               row_colors=[3, 5], col_colors=[6, 2, 8]),
      generate(width=10, height=20, rows=[4, 8, 14], lefts=[2, 2, 1],
               rights=[7, 5, 6], cols=[3, 5], lows=[2, 12], highs=[10, 18],
               row_colors=[3, 7, 8], col_colors=[4, 9]),
  ]
  test = [
      generate(width=20, height=20, rows=[3, 7, 14], lefts=[1, 7, 8],
               rights=[16, 13, 14], cols=[3, 9], lows=[1, 2], highs=[18, 9],
               row_colors=[2, 7, 8], col_colors=[3, 5]),
  ]
  return {"train": train, "test": test}
