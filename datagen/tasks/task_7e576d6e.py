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


def generate(start_row=None, start_col=None, end_row=None, end_col=None,
             rows=None, cols=None, colors=None, xpose=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    start_row: The start row.
    start_col: The start column.
    end_row: The end row.
    end_col: The end column.
    rows: The rows of the lines.
    cols: The columns of the centers.
    colors: The colors of the grid.
    xpose: Whether to transpose the grid.
    gsize: The side length of the square grid.
  """

  def draw():
    grid, output = common.grids(gsize, gsize, colors[0])
    for row in rows:
      for col in range(gsize):
        output[row][col] = grid[row][col] = colors[1]
    for row, col in zip(rows, cols):
      for c in [-1, 0, 1]:
        output[row][col + c] = grid[row][col + c] = colors[2]
    grid[start_row][start_col] = grid[end_row][end_col] = colors[3]
    output[start_row][start_col] = output[end_row][end_col] = colors[3]
    r, c = start_row, start_col
    last_cdir = 0
    for row, col in zip(rows, cols):
      while r + 1 < row:
        output[r][c] = colors[3]
        r += 1
      cdir = 1 if c < col else -1
      if last_cdir and last_cdir == cdir: return None, None
      last_cdir = cdir
      while c != col:
        output[r][c] = colors[3]
        c += cdir
    while r < end_row:
      output[r][c] = colors[3]
      r += 1
    cdir = 1 if c < end_col else -1
    if last_cdir and last_cdir == cdir: return None, None
    while c != end_col:
      output[r][c] = colors[3]
      c += cdir
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if start_col is None:
    if gsize is None:
      gsize = common.randint(22, 30)
    colors = common.random_colors(4)
    start_row, start_col = 1, common.randint(4, gsize - 5)
    end_row, end_col = common.randint(gsize - 5, gsize - 2), common.randint(
        4, gsize - 5)
    while True:
      row, rows = 0, []
      while True:
        row += common.randint(3, 8)
        if row + 7 >= gsize: break
        rows.append(row)
      if len(rows) not in [3, 4]: continue
      cols = common.sample(list(range(4, gsize - 4)), len(rows))
      if start_col in cols or end_col in cols: continue  # Undefined.
      grid, _ = draw()
      if grid: break
  elif gsize is None:
    gsize = 30

  # Final build: reconstruct the input (gated horizontal lines with start and
  # end markers) in canonical orientation, then solve the path.
  grid = common.grid(gsize, gsize, colors[0])
  for row in rows:
    for col in range(gsize):
      grid[row][col] = colors[1]
  for row, col in zip(rows, cols):
    for cc in [-1, 0, 1]:
      grid[row][col + cc] = colors[2]
  grid[start_row][start_col] = colors[3]
  grid[end_row][end_col] = colors[3]

  # Trace the snaking route: for each line descend to just above it and slide
  # across to its gate; then descend to the end row and slide to the end marker.
  r, c = start_row, start_col
  segments = []
  for row, col in zip(rows, cols):
    seg = []
    while r + 1 < row:
      seg.append((r, c)); r += 1
    cdir = 1 if c < col else -1
    while c != col:
      seg.append((r, c)); c += cdir
    segments.append(seg)
  final_seg = []
  while r < end_row:
    final_seg.append((r, c)); r += 1
  cdir = 1 if c < end_col else -1
  while c != end_col:
    final_seg.append((r, c)); c += cdir

  output = common.deepcopy(grid)

  def navigate_gate(i):
    """Routes the path down to line i and across to its gate."""
    if i >= len(segments): return
    for pr, pc in segments[i]:
      output[pr][pc] = colors[3]

  def navigate_to_end():
    """Routes the path down to the end row and across to the end marker."""
    for pr, pc in final_seg:
      output[pr][pc] = colors[3]

  # rows is constrained to 3 or 4 lines, so at most four gates precede the end.
  navigate_gate(0)
  navigate_gate(1)
  navigate_gate(2)
  navigate_gate(3)
  navigate_to_end()

  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(start_row=1, start_col=10, end_row=27, end_col=15,
               rows=[4, 11, 19], cols=[4, 18, 7], colors=[3, 2, 4, 8],
               xpose=True),
      generate(start_row=1, start_col=18, end_row=26, end_col=24,
               rows=[6, 11, 23], cols=[4, 17, 7], colors=[8, 6, 1, 3],
               xpose=True),
      generate(start_row=1, start_col=8, end_row=27, end_col=12,
               rows=[3, 8, 17, 23], cols=[6, 16, 9, 22], colors=[1, 2, 3, 9],
               xpose=False),
  ]
  test = [
      generate(start_row=1, start_col=4, end_row=28, end_col=10,
               rows=[3, 8, 19, 22], cols=[13, 6, 18, 5], colors=[8, 1, 6, 3],
               xpose=False),
  ]
  return {"train": train, "test": test}
