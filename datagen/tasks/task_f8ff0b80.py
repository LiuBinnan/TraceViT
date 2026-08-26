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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None,
             colors=None, size=12, num_boxes=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates where the sprites should be placed
    bcols: a list of horizontal coordinates where the sprites should be placed
    colors: a list of colors to be used
    size: the width and height of the (square) grid (fallback for height/width)
    num_boxes: the number of boxes to be placed
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if rows is None:
    # Widened structural variation (mirrors re_arc generate_f8ff0b80):
    # independent grid height/width, an area-scaled box count, distinct box
    # sizes (so the size-ordering answer stays unambiguous), and colors drawn
    # with repetition. A coverage budget keeps the background (0) the most
    # common color so the "order the box colors by size" rule stays well
    # defined for any placement.
    if height is None:
      height = common.randint(10, 30)
    if width is None:
      width = common.randint(10, 30)
    if num_boxes is None:
      num_boxes = common.randint(1, min(30, (height * width) // 25))
    num_boxes = max(1, min(num_boxes, 30, (height * width) // 25))
    # distinct, minimal box sizes (1..num_boxes) -> distinct object sizes -> the
    # size ordering (hence the answer) is unambiguous, and small boxes pack
    # densely so the box count can range widely.
    sizes = list(range(1, num_boxes + 1))
    budget = int(0.48 * height * width)
    placed, used = [], 0

    def fits(r0, c0, bh, bw):  # spacing-1 gap keeps boxes 8-connectivity-disjoint
      for prow, pcol, pbh, pbw, _, _ in placed:
        if not (prow + pbh + 1 <= r0 or r0 + bh + 1 <= prow or
                pcol + pbw + 1 <= c0 or c0 + bw + 1 <= pcol):
          return False
      return True

    for count in sizes:  # ascending: pack as many boxes as fit
      if used + count > budget:
        continue
      length = 1
      while length * length < count:
        length += 1
      pixels = common.continuous_creature(count, length, length)
      minr, maxr = min(p[0] for p in pixels), max(p[0] for p in pixels)
      minc, maxc = min(p[1] for p in pixels), max(p[1] for p in pixels)
      bh, bw = maxr - minr + 1, maxc - minc + 1
      npix = [(p[0] - minr, p[1] - minc) for p in pixels]  # normalized to (0,0)
      spot = None
      for _attempt in range(60):  # random placement keeps positions natural
        r0 = common.randint(0, height - bh)
        c0 = common.randint(0, width - bw)
        if fits(r0, c0, bh, bw):
          spot = (r0, c0)
          break
      if spot is None:  # first-fit fallback: place if any gap still remains
        for r0 in range(height - bh + 1):
          for c0 in range(width - bw + 1):
            if fits(r0, c0, bh, bw):
              spot = (r0, c0)
              break
          if spot is not None:
            break
      if spot is not None:
        placed.append((spot[0], spot[1], bh, bw, npix, count))
        used += count
    placed.sort(key=lambda box: box[5], reverse=True)  # largest box first
    rows, cols, idxs, brows, bcols = [], [], [], [], []
    for idx, (br0, bc0, bh, bw, npix, count) in enumerate(placed):
      for pr, pc in npix:
        rows.append(pr)
        cols.append(pc)
        idxs.append(idx)
      brows.append(br0)
      bcols.append(bc0)
    colors = [common.random_color() for _ in placed]

  if height is None:
    height = size
  if width is None:
    width = size
  grid, output = common.grid(width, height), common.grid(1, len(colors))
  for r, c, i in zip(rows, cols, idxs):
    grid[r + brows[i]][c + bcols[i]] = colors[i]
  for i, color in enumerate(colors):
    output[i][0] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 3, 0, 0, 1, 1, 1, 1, 2, 0, 1, 1, 2],
               cols=[1, 2, 1, 2, 1, 2, 3, 0, 1, 2, 0, 1, 2, 3, 1, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 6, 2], bcols=[1, 3, 8], colors=[3, 2, 8]),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 3, 0, 1, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[0, 1, 3, 0, 1, 2, 2, 3, 1, 2, 0, 1, 2, 1, 2, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 8, 7], bcols=[7, 8, 2], colors=[1, 7, 2]),
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 0, 1, 1, 1, 2, 2,
                     2, 0, 1, 1, 2, 2],
               cols=[2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 1, 2, 1, 2, 3, 0, 1,
                     2, 0, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                     1, 2, 2, 2, 2, 2],
               brows=[7, 1, 2], bcols=[3, 1, 8], colors=[4, 2, 1]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2, 2, 3, 0, 0, 1, 1, 1, 0, 1, 1],
               cols=[2, 1, 2, 0, 2, 3, 2, 1, 2, 0, 1, 2, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               brows=[8, 5, 1], bcols=[5, 3, 1], colors=[6, 1, 3]),
  ]
  return {"train": train, "test": test}
