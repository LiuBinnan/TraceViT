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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, prows=None, pcols=None, pidxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    base = common.randint(13, 24)
    width = base + common.randint(-1, 1)
    height = base + common.randint(-1, 1)
    num_boxes = common.randint(6, 7)
    packs = 0
    while True:
      wides = [common.randint(2, 6) for _ in range(num_boxes)]
      talls = [common.randint(2, 6) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
      packs += 1
      if packs >= 8000:
        # Packing-feasibility guard: fitting 6-7 boxes (each 2-6) with a 1-cell
        # gap into a small grid is a heavy-tail rejection that can spin for
        # hundreds of thousands of iterations.  After the cap, place the same
        # number of boxes on a gap-separated 3-column shelf, each box randomly
        # sized (clamped to its slot) and randomly jittered within the slot's
        # slack -- a legal, non-overlapping, naturally scattered layout by
        # construction, semantics unchanged.
        cols = 3
        rows = (num_boxes + cols - 1) // cols
        slot_w = (width - (cols - 1)) // cols
        slot_h = (height - (rows - 1)) // rows
        wides, talls, brows, bcols = [], [], [], []
        for k in range(num_boxes):
          r, c = divmod(k, cols)
          w = min(common.randint(2, 6), slot_w)
          t = min(common.randint(2, 6), slot_h)
          wides.append(w)
          talls.append(t)
          brows.append(r * (slot_h + 1) + common.randint(0, slot_h - t))
          bcols.append(c * (slot_w + 1) + common.randint(0, slot_w - w))
        break
    attempts = 0
    while True:
      prows, pcols, pidxs, num_small = [], [], [], 0
      for i in range(num_boxes):
        for r in range(talls[i]):
          for c in range(wides[i]):
            if common.randint(0, 9): continue
            prows.append(r)
            pcols.append(c)
            pidxs.append(i)
        if pidxs.count(i) < 2: num_small += 1
      if num_small == 3: break
      attempts += 1
      if attempts >= 200:
        # Heavy-tail guard: demanding EXACTLY three < 2-dot boxes under
        # 1/10-per-cell speckling is a combinatorial rejection that spins
        # forever on some seeds.  After the cap, repair the last sampled dots
        # into a legal config with the SAME semantics: take the three smallest
        # boxes as the < 2-dot keepers (trim each to <= 1 dot) and top every
        # other box up to >= 2 dots at its first empty cells.
        keepers = set(sorted(range(num_boxes),
                             key=lambda i: wides[i] * talls[i])[:3])
        occupied = {i: set() for i in range(num_boxes)}
        rprows, rpcols, rpidxs = [], [], []
        for r, c, i in zip(prows, pcols, pidxs):
          if i in keepers and len(occupied[i]) >= 1: continue
          if (r, c) in occupied[i]: continue
          occupied[i].add((r, c))
          rprows.append(r)
          rpcols.append(c)
          rpidxs.append(i)
        for i in range(num_boxes):
          if i in keepers: continue
          for r in range(talls[i]):
            for c in range(wides[i]):
              if len(occupied[i]) >= 2: break
              if (r, c) in occupied[i]: continue
              occupied[i].add((r, c))
              rprows.append(r)
              rpcols.append(c)
              rpidxs.append(i)
            if len(occupied[i]) >= 2: break
        prows, pcols, pidxs = rprows, rpcols, rpidxs
        break

  # Draw the input: every box in blue, speckled with cyan dots.
  grid = common.grid(width, height)
  for i, (wide, tall, brow, bcol) in enumerate(zip(wides, talls, brows, bcols)):
    common.rect(grid, wide, tall, brow, bcol, 1)
  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    brow, bcol = brows[pidx], bcols[pidx]
    grid[brow + prow][bcol + pcol] = 8

  # Solve by discarding every box that holds two or more dots, keeping only the
  # boxes speckled with fewer than two dots.  Start from the full input and
  # erase the over-speckled boxes one at a time.
  output = common.deepcopy(grid)
  rejects = [i for i in range(len(wides)) if pidxs.count(i) >= 2]

  def erase_box(k):
    """Erases the k-th over-speckled box (>= 2 dots) back to background."""
    nonlocal output
    if k >= len(rejects): return
    i = rejects[k]
    common.rect(output, wides[i], talls[i], brows[i], bcols[i], common.black())

  erase_box(0)
  erase_box(1)
  erase_box(2)
  erase_box(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=14, wides=[3, 2, 4, 4, 4, 4],
               talls=[3, 3, 3, 3, 4, 4], brows=[0, 0, 2, 5, 7, 10],
               bcols=[5, 11, 0, 9, 3, 10],
               prows=[0, 1, 0, 1, 2, 1, 2, 0, 1, 2, 2],
               pcols=[1, 1, 2, 1, 3, 2, 1, 1, 3, 1, 2],
               pidxs=[0, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5]),
      generate(width=14, height=14, wides=[3, 3, 2, 3, 3, 3],
               talls=[2, 4, 2, 3, 3, 4], brows=[1, 2, 2, 5, 7, 9],
               bcols=[1, 5, 10, 11, 1, 7], prows=[0, 1, 1, 2, 3, 0, 1, 0, 1, 2],
               pcols=[1, 2, 1, 2, 0, 1, 1, 2, 0, 0],
               pidxs=[0, 0, 1, 1, 1, 2, 3, 4, 4, 5]),
      generate(width=15, height=13, wides=[4, 2, 4, 4, 5, 3, 4],
               talls=[4, 2, 3, 3, 3, 4, 3], brows=[0, 0, 1, 3, 6, 9, 10],
               bcols=[5, 11, 0, 11, 2, 9, 2],
               prows=[1, 1, 3, 0, 1, 1, 1, 0, 1, 2, 0, 1, 3, 3],
               pcols=[0, 3, 2, 0, 1, 1, 1, 2, 3, 1, 2, 1, 0, 2],
               pidxs=[0, 0, 0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 5]),
  ]
  test = [
      generate(width=12, height=13, wides=[4, 3, 3, 4, 6, 3],
               talls=[3, 3, 4, 4, 4, 2], brows=[0, 1, 3, 6, 8, 11],
               bcols=[8, 0, 4, 8, 1, 8], prows=[0, 2, 2, 1, 0, 2, 1, 1, 2],
               pcols=[1, 1, 3, 0, 0, 2, 2, 4, 1],
               pidxs=[0, 0, 0, 1, 2, 2, 3, 4, 4]),
  ]
  return {"train": train, "test": test}
