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


def generate(prow=None, pcol=None, brows=None, bcols=None, sizes=None,
             colors=None, num_boxes=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the plus.
    pcol: The column of the plus.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    sizes: The sizes of the boxes.
    colors: The colors of the boxes.
    num_boxes: The number of boxes in a random instance.
    gsize: The side length of the (square) grid.
  """

  def draw(alignment=None):
    grid = common.grid(gsize, gsize, common.orange())
    # Draw the boxes.
    row_aligned, col_aligned = False, False
    for brow, bcol, size in zip(brows, bcols, sizes):
      common.rect(grid, size, size, brow, bcol, colors[1])
      if size % 2 == 1:
        if brow + size // 2 == prow: row_aligned = True
        if bcol + size // 2 == pcol: col_aligned = True
    # Avoid this case, it isn't defined in the problem suite.
    if row_aligned != col_aligned: return None, None
    if alignment is not None and row_aligned != alignment: return None, None
    # Draw the plus.
    for dr, dc in [(-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)]:
      grid[prow + dr][pcol + dc] = colors[0]
    return grid, row_aligned

  if prow is None:
    if gsize is None:
      gsize = common.randint(14, 24)
    if num_boxes is None:
      num_boxes = common.randint(5, 10)
    # Keep the box count feasible for the chosen grid so packing never spins.
    num_boxes = min(num_boxes, max(4, gsize * gsize // 28))
    colors = common.random_colors(2, exclude=[7])
    alignment = True if common.randint(0, 1) else False
    # Place boxes one at a time so dense samples cannot spin indefinitely.  For
    # aligned samples the first two odd boxes constructively witness the plus's
    # row and column; relying on both coincidences made these samples vanishingly
    # unlikely.  The caps are only a backstop for unusually crowded layouts.
    for _ in range(200):
      prow, pcol = common.randint(1, gsize - 2), common.randint(1, gsize - 2)
      brows, bcols, sizes = [], [], []
      for i in range(num_boxes):
        for _ in range(200):
          size = common.randint(1, 7)
          if alignment and i == 0:
            if size % 2 == 0: continue
            brow = prow - size // 2
            if brow < 0 or brow + size > gsize: continue
            bcol = common.randint(0, gsize - size)
          elif alignment and i == 1:
            if size % 2 == 0: continue
            bcol = pcol - size // 2
            if bcol < 0 or bcol + size > gsize: continue
            brow = common.randint(0, gsize - size)
          else:
            brow = common.randint(0, gsize - size)
            bcol = common.randint(0, gsize - size)
            if (not alignment and size % 2 == 1 and
                (brow + size // 2 == prow or bcol + size // 2 == pcol)):
              continue
          if common.overlaps(brows + [brow, prow - 1],
                             bcols + [bcol, pcol - 1],
                             sizes + [size, 3], sizes + [size, 3], 1):
            continue
          brows.append(brow)
          bcols.append(bcol)
          sizes.append(size)
          break
        else:
          break
      if len(sizes) != num_boxes: continue
      grid, _ = draw(alignment)
      if grid: break
    else:
      raise RuntimeError("unable to place a valid box configuration")

  if gsize is None:
    gsize = 16

  grid, aligned = draw()
  if grid is None:
    return {"input": grid, "output": None}
  output = common.deepcopy(grid)

  def erase_plus():
    """Removes the query plus before testing its alignment."""
    for dr, dc in [(-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)]:
      output[prow + dr][pcol + dc] = common.orange()

  erase_plus()

  def mark_size(target_size):
    """Marks the center of every odd box whose side length == target_size."""
    for brow, bcol, size in zip(brows, bcols, sizes):
      if size % 2 == 1 and size == target_size:
        output[brow + size // 2][bcol + size // 2] = colors[0]

  mark_size(1)
  mark_size(3)
  mark_size(5)
  mark_size(7)

  def restore_aligned_plus():
    """Restores the query plus when both center alignments exist."""
    if not aligned:
      return
    for dr, dc in [(-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)]:
      output[prow + dr][pcol + dc] = colors[0]

  restore_aligned_plus()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=3, pcol=5, brows=[3, 7, 7, 13, 14],
               bcols=[11, 3, 12, 13, 2], sizes=[3, 2, 4, 1, 2], colors=[8, 9]),
      generate(prow=14, pcol=14, brows=[0, 0, 0, 0, 5, 5],
               bcols=[0, 2, 5, 9, 0, 6], sizes=[1, 2, 3, 4, 5, 6],
               colors=[1, 8]),
      generate(prow=1, pcol=14, brows=[0, 3, 4, 6, 10, 11, 11, 14],
               bcols=[6, 2, 13, 5, 11, 1, 4, 13],
               sizes=[3, 1, 3, 2, 1, 1, 4, 2], colors=[3, 1]),
  ]
  test = [
      generate(prow=9, pcol=3, brows=[0, 1, 3, 5, 7, 9, 10, 11, 12, 14, 14],
               bcols=[0, 14, 13, 10, 10, 8, 10, 7, 5, 1, 14],
               sizes=[7, 1, 3, 1, 2, 1, 3, 2, 1, 1, 2], colors=[4, 8]),
  ]
  return {"train": train, "test": test}
