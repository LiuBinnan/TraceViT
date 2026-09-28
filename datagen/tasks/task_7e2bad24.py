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


def generate(rows=None, cols=None, lengths=None, colors=None, prow=None,
             pcol=None, shown=None, flip=None, flop=None, xpose=None,
             gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the lines.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    colors: The colors of the lines.
    prow: The row of the pixel.
    pcol: The column of the pixel.
    shown: How much of the line is shown.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
    xpose: Whether to transpose the grid.
    gsize: The side length of the square grid.
  """

  def draw():
    grid, output = common.grids(gsize, gsize)
    for row, col, length, color in zip(rows, cols, lengths, colors):
      for c in range(col, col + length):
        if grid[row][c] != 0: return None, None
        if common.get_pixel(grid, row - 1, c) not in [-1, 0]: return None, None
        if common.get_pixel(grid, row + 1, c) not in [-1, 0]: return None, None
        output[row][c] = grid[row][c] = color
    r, c, rdir, i, touches = prow, pcol, 1, 0, 0
    while c < gsize and r >= 0 and r < gsize:
      if output[r][c] != 0: touches += 1
      output[r][c] = 1
      if i < shown:
        if grid[r][c] != 0: return None, None
        grid[r][c] = 1
      if r + rdir < 0 or r + rdir >= gsize: break
      if grid[r + rdir][c] == 2: touches, rdir = touches + 1, rdir * -1
      r, c, i = r + rdir, c + 1, i + 1
    if i < gsize - 3 or touches == 0: return None, None
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if rows is None:
    if gsize is None:
      gsize = common.randint(12, 24)
    attempts = 0
    while True:
      rows, cols, lengths, colors = [], [], [], []
      for color in [2, 3]:
        row = common.randint(0, 4)
        while row < gsize:
          rows.append(row)
          lengths.append(common.randint(4, gsize - 2))
          cols.append(common.randint(1, gsize - 1 - lengths[-1]))
          colors.append(color)
          row += common.randint(3, 5)
      if common.randint(0, 1): prow, pcol = 0, common.randint(0, 6)
      else: prow, pcol = common.randint(0, 6), 0
      shown = common.randint(3, 6)
      grid, _ = draw()
      if grid: break
      attempts += 1
      if attempts < 256: continue
      # A central red wall guarantees one reflection and a nearly full-width
      # V-shaped path. A varied, separated green wall preserves both line roles
      # while bounding the rare whole-configuration rejection tail.
      red_row = common.randint(gsize // 2, gsize - 4)
      green_row = common.randint(red_row + 2, gsize - 2)
      green_length = common.randint(4, gsize - 2)
      rows = [red_row, green_row]
      cols = [1, common.randint(1, gsize - 1 - green_length)]
      lengths = [gsize - 2, green_length]
      colors = [2, 3]
      prow, pcol = 0, common.randint(0, 3)
      shown = common.randint(3, min(6, red_row))
      break
  else:
    if gsize is None:
      gsize = 16

  # Final build: reconstruct the input (non-touching horizontal lines plus the
  # revealed head of the beam) in canonical orientation, then solve the beam.
  grid = common.grid(gsize, gsize)
  for row, col, length, color in zip(rows, cols, lengths, colors):
    for c in range(col, col + length):
      grid[row][c] = color

  # Trace the whole beam: one column right per move, drifting down/up, and
  # reflecting whenever the next vertical cell is a red wall (green lines are
  # passed over). Only the first `shown` cells are revealed in the input.
  path, seg_ends = [], []
  r, c, rdir, i = prow, pcol, 1, 0
  while c < gsize and 0 <= r < gsize:
    path.append((r, c))
    if i < shown: grid[r][c] = common.blue()
    if r + rdir < 0 or r + rdir >= gsize: break
    if grid[r + rdir][c] == common.red():
      rdir = -rdir
      seg_ends.append(len(path) - 1)
    r, c, i = r + rdir, c + 1, i + 1
  seg_ends.append(len(path) - 1)
  # Segments buried inside the revealed head are already given; the solving
  # starts with the first segment that reaches past the shown cells.
  ext_ends = [e for e in seg_ends if e >= shown]

  output = common.deepcopy(grid)

  def extend_beam(k):
    """Extends the beam forward through the k-th unsolved segment (cumulative)."""
    if k >= len(ext_ends): return
    end = ext_ends[-1] if k == 7 else ext_ends[k]
    for br, bc in path[:end + 1]:
      output[br][bc] = common.blue()

  # Seven calls expose early segments; the eighth absorbs every remaining
  # reflection and the final tail, including on the widened canvases.
  extend_beam(0)
  extend_beam(1)
  extend_beam(2)
  extend_beam(3)
  extend_beam(4)
  extend_beam(5)
  extend_beam(6)
  extend_beam(7)

  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[6, 10], cols=[1, 4], lengths=[9, 9], colors=[3, 2], prow=0,
               pcol=1, shown=4, flip=True, flop=True, xpose=False),
      generate(rows=[7], cols=[1], lengths=[14], colors=[3], prow=0, pcol=1,
               shown=5, flip=True, flop=False, xpose=True),
      generate(rows=[8], cols=[2], lengths=[12], colors=[2], prow=0, pcol=0,
               shown=6, flip=False, flop=False, xpose=True),
  ]
  test = [
      generate(rows=[0, 4, 4, 7, 8, 10, 13], cols=[3, 1, 5, 9, 5, 5, 2],
               lengths=[9, 4, 9, 6, 4, 7, 6], colors=[2, 3, 2, 2, 3, 2, 3],
               prow=1, pcol=0, shown=3, flip=False, flop=False, xpose=True),
      generate(rows=[1, 5, 11], cols=[11, 6, 1],
               lengths=[4, 7, 14], colors=[2, 3, 2],
               prow=6, pcol=0, shown=3, flip=True, flop=False, xpose=True),
  ]
  return {"train": train, "test": test}
