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


def generate(wides=None, talls=None, brows=None, bcols=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
  """

  def draw():
    if len(wides) < 6 or len(wides) > 10: return None, None
    grid, output = common.grids(gsize, gsize)
    def change(pixels, old_val, new_val):
      for r, c in pixels:
        if output[r][c] != old_val: return False
      for r, c in pixels:
        output[r][c] = new_val
      return True
    if common.overlaps(brows, bcols, wides, talls, 1): return None, None
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      common.hollow_rect(grid, wide, tall, brow, bcol, 3)
      common.hollow_rect(output, wide, tall, brow, bcol, 3)
    aligned = []
    for i in range(len(wides)):
      for j in range(len(wides)):
        if i == j: continue
        if brows[i] >= brows[j] and brows[i] + talls[i] <= brows[j] + talls[j]:
          if brows[i] - brows[j] != brows[j] + talls[j] - (brows[i] + talls[i]):
            return None, None  # Ill-defined.
          dist = max(bcols[j] - (bcols[i] + wides[i] - 1),
                     bcols[i] - (bcols[j] + wides[j] - 1))
          aligned.append((dist, 0, i, j))
        if bcols[i] >= bcols[j] and bcols[i] + wides[i] <= bcols[j] + wides[j]:
          if bcols[i] - bcols[j] != bcols[j] + wides[j] - (bcols[i] + wides[i]):
            return None, None  # Ill-defined.
          dist = max(brows[j] - (brows[i] + talls[i] - 1),
                     brows[i] - (brows[j] + talls[j] - 1))
          aligned.append((dist, 1, i, j))
    aligned.sort()
    merges, groups = 0, list(range(len(wides)))
    for _, cdir, i, j in aligned:
      if groups[i] == groups[j]: continue  # Already merged.
      merges += 1
      old_group = groups[j]
      groups = [group if group != old_group else groups[i] for group in groups]
      if cdir == 0:
        top_left_col = min(bcols[i] + wides[i] - 1, bcols[j] + wides[j] - 1)
        top_left_row = max(brows[i], brows[j]) + 1
        bot_rite_col = max(bcols[i], bcols[j])
        bot_rite_row = min(brows[i] + talls[i] - 1, brows[j] + talls[j] - 1) - 1
        for r in range(top_left_row + 1, bot_rite_row):
          if not change([(r, top_left_col), (r, bot_rite_col)], 3, 0):
            return None, None
        for c in range(top_left_col + 1, bot_rite_col):
          if not change([(top_left_row, c), (bot_rite_row, c)], 0, 3):
            return None, None
      else:
        top_left_col = max(bcols[i], bcols[j]) + 1
        top_left_row = min(brows[i] + talls[i] - 1, brows[j] + talls[j] - 1)
        bot_rite_col = min(bcols[i] + wides[i] - 1, bcols[j] + wides[j] - 1) - 1
        bot_rite_row = max(brows[i], brows[j])
        for c in range(top_left_col + 1, bot_rite_col):
          if not change([(top_left_row, c), (bot_rite_row, c)], 3, 0):
            return None, None
        for r in range(top_left_row + 1, bot_rite_row):
          if not change([(r, top_left_col), (r, bot_rite_col)], 0, 3):
            return None, None
    if len(set(groups)) != 1: return None, None  # All must merge!
    if merges < 5: return None, None
    return grid, output

  if wides is None:
    if gsize is None:
      gsize = common.randint(24, 30)
    while True:
      wide, tall = common.randint(3, 13), common.randint(3, 13)
      brow, bcol = (common.randint(0, gsize - tall),
                    common.randint(0, gsize - wide))
      wides, talls, brows, bcols = [wide], [tall], [brow], [bcol]
      queue = [(wide, tall, brow, bcol)]
      def maybe_add(w, t, r, c):
        nonlocal brows, bcols, wides, talls
        if r < 0 or r + t > gsize or c < 0 or c + w > gsize: return
        if common.overlaps(brows + [r], bcols + [c], wides + [w], talls + [t], 1):
          return
        wides, talls = wides + [w], talls + [t]
        brows, bcols = brows + [r], bcols + [c]
        queue.append((w, t, r, c))
      while queue:
        (wide, tall, brow, bcol) = queue.pop()
        w, t = common.randint(3, 13), 2 * common.randint(2, 5) + tall % 2
        r, c = brow + (tall - t) // 2, bcol - 1 - w - common.randint(0, 8)
        maybe_add(w, t, r, c)
        w, t = 2 * common.randint(2, 5) + wide % 2, common.randint(3, 13)
        r, c = brow - 1 - t - common.randint(0, 8), bcol + (wide - w) // 2
        maybe_add(w, t, r, c)
        w, t = common.randint(3, 13), 2 * common.randint(2, 5) + tall % 2
        r, c = brow + (tall - t) // 2, bcol + wide + 1 + common.randint(0, 8)
        maybe_add(w, t, r, c)
        w, t = 2 * common.randint(2, 5) + wide % 2, common.randint(3, 13)
        r, c = brow + tall + 1 + common.randint(0, 8), bcol + (wide - w) // 2
        maybe_add(w, t, r, c)
      grid, _ = draw()
      if grid: break
  elif gsize is None:
    gsize = 30

  # Build the input grid (draw() draws no randomness). For invalid explicit
  # params draw() yields None; mirror the original's graceful None return.
  grid, _ = draw()
  if grid is None:
    return {"input": None, "output": None}

  # Solve forward: the rooms (rectangles) that are aligned and facing get joined
  # by a corridor -- doorways are punched through the facing walls and the two
  # corridor rails are drawn between them. Reveal one corridor per connection,
  # closest pairs first, exactly as the rooms get linked into a single network.
  output = common.deepcopy(grid)

  def plan_corridors():
    """Replays draw()'s alignment + union-find, recording each merge's cell
    writes. Params are already valid (draw() succeeded), so no change() fails."""
    work = common.deepcopy(grid)
    corridors = []
    aligned = []
    for i in range(len(wides)):
      for j in range(len(wides)):
        if i == j: continue
        if brows[i] >= brows[j] and brows[i] + talls[i] <= brows[j] + talls[j]:
          dist = max(bcols[j] - (bcols[i] + wides[i] - 1),
                     bcols[i] - (bcols[j] + wides[j] - 1))
          aligned.append((dist, 0, i, j))
        if bcols[i] >= bcols[j] and bcols[i] + wides[i] <= bcols[j] + wides[j]:
          dist = max(brows[j] - (brows[i] + talls[i] - 1),
                     brows[i] - (brows[j] + talls[j] - 1))
          aligned.append((dist, 1, i, j))
    aligned.sort()
    groups = list(range(len(wides)))
    for _, cdir, i, j in aligned:
      if groups[i] == groups[j]: continue
      old_group = groups[j]
      groups = [group if group != old_group else groups[i] for group in groups]
      writes = []
      def change(pixels, old_val, new_val):
        for r, c in pixels:
          if work[r][c] != old_val: return False
        for r, c in pixels:
          work[r][c] = new_val
          writes.append((r, c, new_val))
        return True
      if cdir == 0:
        top_left_col = min(bcols[i] + wides[i] - 1, bcols[j] + wides[j] - 1)
        top_left_row = max(brows[i], brows[j]) + 1
        bot_rite_col = max(bcols[i], bcols[j])
        bot_rite_row = min(brows[i] + talls[i] - 1, brows[j] + talls[j] - 1) - 1
        for r in range(top_left_row + 1, bot_rite_row):
          change([(r, top_left_col), (r, bot_rite_col)], common.green(),
                 common.black())
        for c in range(top_left_col + 1, bot_rite_col):
          change([(top_left_row, c), (bot_rite_row, c)], common.black(),
                 common.green())
      else:
        top_left_col = max(bcols[i], bcols[j]) + 1
        top_left_row = min(brows[i] + talls[i] - 1, brows[j] + talls[j] - 1)
        bot_rite_col = min(bcols[i] + wides[i] - 1, bcols[j] + wides[j] - 1) - 1
        bot_rite_row = max(brows[i], brows[j])
        for c in range(top_left_col + 1, bot_rite_col):
          change([(top_left_row, c), (bot_rite_row, c)], common.green(),
                 common.black())
        for r in range(top_left_row + 1, bot_rite_row):
          change([(r, top_left_col), (r, bot_rite_col)], common.black(),
                 common.green())
      corridors.append(writes)
    return corridors

  corridors = plan_corridors()

  def draw_corridor(k):
    """Reveals connection k: its doorways and corridor rails."""
    if k >= len(corridors):
      return
    for r, c, val in corridors[k]:
      output[r][c] = val

  draw_corridor(0)
  draw_corridor(1)
  draw_corridor(2)
  draw_corridor(3)
  draw_corridor(4)
  draw_corridor(5)
  draw_corridor(6)
  for k in range(7, len(corridors)):
    draw_corridor(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[6, 4, 10, 8, 3, 12, 3], talls=[6, 4, 6, 6, 4, 7, 5],
               brows=[3, 4, 10, 10, 11, 19, 20],
               bcols=[2, 11, 0, 15, 26, 13, 8]),
      generate(wides=[8, 5, 6, 7, 11, 4], talls=[7, 7, 7, 5, 6, 4],
               brows=[4, 4, 4, 12, 18, 19], bcols=[2, 13, 23, 12, 10, 4]),
      generate(wides=[9, 6, 3, 7, 4, 5, 3], talls=[9, 7, 5, 6, 4, 3, 3],
               brows=[1, 2, 3, 11, 12, 19, 24], bcols=[7, 23, 3, 8, 17, 9, 10]),
  ]
  test = [
      generate(wides=[5, 6, 8, 4, 3, 8, 6, 3], talls=[11, 9, 7, 3, 3, 4, 6, 4],
               brows=[2, 3, 4, 13, 14, 17, 23, 24],
               bcols=[24, 15, 4, 16, 25, 4, 5, 1]),
  ]
  return {"train": train, "test": test}
