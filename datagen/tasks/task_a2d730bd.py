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


def generate(width=None, height=None, bgcolor=None, wides=None, talls=None,
             brows=None, bcols=None, bcolors=None, prows=None, pcols=None,
             pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color of the grid.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row indices of the tops of the rectangles.
    bcols: The column indices of the left sides of the rectangles.
    bcolors: The colors of the rectangles.
    prows: The row indices of the tops of the patterns.
    pcols: The column indices of the left sides of the patterns.
    pcolors: The colors of the patterns.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls, 1): return None, None
    grid, output = common.grids(width, height, bgcolor)
    def put(g, r, c, color):
      if g[r][c] != bgcolor: return False
      g[r][c] = color
      return True
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      common.rect(grid, wide, tall, brow, bcol, bcolor)
      common.rect(output, wide, tall, brow, bcol, bcolor)
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      if not put(grid, prow, pcol, pcolor): return None, None
      for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if not put(output, prow + dr, pcol + dc, pcolor): return None, None
      idx, rows, cols = bcolors.index(pcolor), [], []
      if pcol >= bcols[idx] + wides[idx]:
        rows, cols = [prow - 1, prow + 1], [bcols[idx] + wides[idx]] * 2
        for c in range(bcols[idx] + wides[idx], pcol - 1):
          if not put(output, prow, c, pcolor): return None, None
      if pcol < bcols[idx]:
        rows, cols = [prow - 1, prow + 1], [bcols[idx] - 1] * 2
        for c in range(pcol + 2, bcols[idx]):
          if not put(output, prow, c, pcolor): return None, None
      if prow >= brows[idx] + talls[idx]:
        rows, cols = [brows[idx] + talls[idx]] * 2, [pcol - 1, pcol + 1]
        for r in range(brows[idx] + talls[idx], prow - 1):
          if not put(output, r, pcol, pcolor): return None, None
      if prow < brows[idx]:
        rows, cols = [brows[idx] - 1] * 2, [pcol - 1, pcol + 1]
        for r in range(prow + 2, brows[idx]):
          if not put(output, r, pcol, pcolor): return None, None
      for row, col in zip(rows, cols):
        if not put(output, row, col, pcolor): return None, None
    return grid, output

  if width is None:
    width, height = common.randint(12, 30), common.randint(12, 30)
    num_boxes = 1
    if width * height >= 250: num_boxes = common.randint(1, 2)
    if width * height >= 500: num_boxes = common.randint(2, 3)
    bgcolor = common.random_color()
    bcolors = common.random_colors(num_boxes, exclude=[bgcolor])
    while True:
      cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
      wides = [common.randint(2, 4) if d else common.randint(7, min(11, width - 4)) for d in cdirs]
      talls = [common.randint(7, min(11, height - 4)) if d else common.randint(2, 4) for d in cdirs]
      brows = [common.randint(2, height - tall - 2) for tall in talls]
      bcols = [common.randint(2, width - wide - 2) for wide in wides]
      prows, pcols, pcolors = [], [], []
      feasible = True
      for cdir, wide, tall, brow, bcol, bcolor in zip(cdirs, wides, talls, brows, bcols, bcolors):
        # Widened band: 1-3 -> 1-4 markers per box (more harpoons).
        num_pixels = common.randint(1, 4)
        if cdir:
          rpool = list(range(brow + 1, brow + tall - 1))
          cpool = list(range(1, bcol - 2)) + list(range(bcol + wide + 2, width - 1))
        else:
          rpool = list(range(1, brow - 2)) + list(range(brow + tall + 2, height - 1))
          cpool = list(range(bcol + 1, bcol + wide - 1))
        # Latent-bug repair (broken-sampler class): a box hugging an edge can
        # leave the marker pool smaller than num_pixels, which made the original
        # common.sample throw ValueError on ~9/500 seeds. Reject and resample the
        # whole configuration instead. validate()'s explicit path never enters
        # this block, so it stays byte-identical.
        if len(rpool) < num_pixels or len(cpool) < num_pixels:
          feasible = False
          break
        prows.extend(common.sample(rpool, num_pixels))
        pcols.extend(common.sample(cpool, num_pixels))
        pcolors.extend([bcolor] * num_pixels)
      if not feasible:
        continue
      grid, _ = draw()
      if grid: break

  # Input: the rectangles plus the scattered single-cell markers.
  grid = common.grid(width, height, bgcolor)
  for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
    common.rect(grid, wide, tall, brow, bcol, bcolor)
  for prow, pcol, pcolor in zip(prows, pcols, pcolors):
    grid[prow][pcol] = pcolor

  # Output: the same rectangles, then one harpoon per marker (built forward).
  output = common.grid(width, height, bgcolor)
  for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
    common.rect(output, wide, tall, brow, bcol, bcolor)

  def connect_marker(i):
    """Turns marker i into a harpoon aimed at its same-colored box.

    Draws the diamond aura around the marker, the straight shaft running along
    the marker's row/column to the box, and the crossbar where it meets the box.
    """
    nonlocal output
    if i >= len(prows): return
    prow, pcol, pcolor = prows[i], pcols[i], pcolors[i]
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
      output[prow + dr][pcol + dc] = pcolor
    idx, rows, cols = bcolors.index(pcolor), [], []
    if pcol >= bcols[idx] + wides[idx]:
      rows, cols = [prow - 1, prow + 1], [bcols[idx] + wides[idx]] * 2
      for c in range(bcols[idx] + wides[idx], pcol - 1):
        output[prow][c] = pcolor
    if pcol < bcols[idx]:
      rows, cols = [prow - 1, prow + 1], [bcols[idx] - 1] * 2
      for c in range(pcol + 2, bcols[idx]):
        output[prow][c] = pcolor
    if prow >= brows[idx] + talls[idx]:
      rows, cols = [brows[idx] + talls[idx]] * 2, [pcol - 1, pcol + 1]
      for r in range(brows[idx] + talls[idx], prow - 1):
        output[r][pcol] = pcolor
    if prow < brows[idx]:
      rows, cols = [brows[idx] - 1] * 2, [pcol - 1, pcol + 1]
      for r in range(prow + 2, brows[idx]):
        output[r][pcol] = pcolor
    for row, col in zip(rows, cols):
      output[row][col] = pcolor

  connect_marker(0)
  connect_marker(1)
  connect_marker(2)
  connect_marker(3)
  connect_marker(4)
  connect_marker(5)
  connect_marker(6)
  connect_marker(7)
  connect_marker(8)
  # CRITICAL GUARD (unroll overrun): widening num_pixels to 4 lets num_boxes*4
  # exceed the 9 unrolled calls above; drain any remaining markers so the output
  # is never a half-drawn grid.
  for extra in range(9, len(prows)):
    connect_marker(extra)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=22, bgcolor=3, wides=[3, 3], talls=[8, 7],
               brows=[2, 11], bcols=[4, 8], bcolors=[1, 4], prows=[3, 12, 15],
               pcols=[12, 13, 3], pcolors=[1, 4, 4]),
      generate(width=16, height=13, bgcolor=8, wides=[7], talls=[2], brows=[4],
               bcols=[3], bcolors=[3], prows=[1, 9], pcols=[7, 5],
               pcolors=[3, 3]),
      generate(width=16, height=22, bgcolor=1, wides=[11], talls=[3], brows=[8],
               bcols=[2], bcolors=[8], prows=[2, 3, 17], pcols=[9, 5, 8],
               pcolors=[8, 8, 8]),
  ]
  test = [
      generate(width=30, height=30, bgcolor=4, wides=[4, 3, 10],
               talls=[7, 7, 3], brows=[2, 11, 23], bcols=[10, 15, 4],
               bcolors=[2, 1, 3], prows=[3, 5, 13, 16, 19],
               pcols=[23, 4, 5, 26, 7], pcolors=[2, 2, 1, 1, 3]),
  ]
  return {"train": train, "test": test}
