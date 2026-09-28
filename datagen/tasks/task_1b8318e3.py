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


def generate(size=None, brows=None, bcols=None, prows=None, pcols=None,
             pcolors=None, extra_idxs=None, extra_rows=None, extra_cols=None,
             num_boxes=None, num_pixels=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    pcolors: The colors of the pixels.
    extra_idxs: The indices of the extra pixels (for ambiguous cases).
    extra_rows: The rows of the extra pixels (for ambiguous cases).
    extra_cols: The columns of the extra pixels (for ambiguous cases).
    num_boxes: The number of gray boxes in a generated example.
    num_pixels: The number of colored pixels in a generated example.
  """

  def draw():
    # First, match the pixels with the box sites.
    orows, ocols = [-1] * len(prows), [-1] * len(prows)
    for _ in range(len(prows)):  # An upper bound on the number of rounds.
      matches = []
      for p, (prow, pcol) in enumerate(zip(prows, pcols)):
        if orows[p] != -1: continue
        min_dist, min_list = None, []
        for brow, bcol in zip(brows, bcols):
          r, c = prow, pcol
          if pcol < bcol: c = bcol - 1
          if prow < brow: r = brow - 1
          if pcol > bcol + 1: c = bcol + 2
          if prow > brow + 1: r = brow + 2
          if (r, c) in list(zip(orows, ocols)): continue
          dist = abs(r - prow) + abs(c - pcol)
          if dist > 4: continue
          if min_dist is not None and min_dist < dist: continue
          if min_dist is not None and min_dist > dist: min_list = []
          min_dist, min_list = dist, min_list + [(dist, p, r, c)]
        if len(min_list) == 1: matches.append(min_list[0])
      matches.sort()
      for _, p, r, c in sorted(matches):
        if (r, c) not in list(zip(orows, ocols)): orows[p], ocols[p] = r, c
    if -1 in orows: return None, None
    # Second, fix the answer for a few examples that don't seem to be correct.
    if extra_idxs is not None:
      for idx, row, col in zip(extra_idxs, extra_rows, extra_cols):
        orows[idx], ocols[idx] = row, col
    # Third, draw all boxes and pixels.
    grid, output = common.grids(size, size)
    for brow, bcol in zip(brows, bcols):
      for r in range(2):
        for c in range(2):
          if grid[brow + r][bcol + c] != 0: return None, None
          if output[brow + r][bcol + c] != 0: return None, None
          output[brow + r][bcol + c] = grid[brow + r][bcol + c] = 5
    for prow, pcol, orow, ocol, pcolor in zip(prows, pcols, orows, ocols, pcolors):
      if grid[prow][pcol] != 0 or output[orow][ocol] != 0: return None, None
      output[orow][ocol] = grid[prow][pcol] = pcolor
    return grid, output

  if size is None:
    base = common.randint(2, 3)
    if num_boxes is None:
      num_boxes = base + common.randint(1, 2)
    if num_boxes > 4 or (num_pixels is not None and num_pixels > 12):
      # A 10x10 canvas cannot fit more than four well-separated 2x2 boxes,
      # nor reliably expose more than twelve unambiguous perimeter targets.
      base = 3
    size = 5 * base
    grid = None
    for _ in range(32):
      brows = [common.randint(1, size - 3) for _ in range(num_boxes)]
      bcols = [common.randint(1, size - 3) for _ in range(num_boxes)]
      if common.overlaps(brows, bcols, [2] * num_boxes, [2] * num_boxes, 2):
        continue
      count = (common.randint(size, 3 * size)
               if num_pixels is None else num_pixels)
      prows = [common.randint(0, size - 1) for _ in range(count)]
      pcols = [common.randint(0, size - 1) for _ in range(count)]
      pcolors = [common.random_color(exclude=[5]) for _ in range(count)]
      grid, _ = draw()
      if grid: break

    if grid is None:
      # Keep the original rejection sampler's random box layout when possible,
      # but construct collision-free pixels after its bounded attempt budget.
      # If even box placement missed, a shuffled lattice is guaranteed to fit.
      if common.overlaps(brows, bcols, [2] * num_boxes, [2] * num_boxes, 2):
        sites = [(r, c) for r in range(1, size - 2, 4)
                 for c in range(1, size - 2, 4)]
        sites = common.sample(sites, num_boxes)
        brows = [r for r, _ in sites]
        bcols = [c for _, c in sites]

      box_pixels = {
          (brow + dr, bcol + dc)
          for brow, bcol in zip(brows, bcols)
          for dr in range(2) for dc in range(2)
      }
      candidates = [[] for _ in range(num_boxes)]
      for prow in range(size):
        for pcol in range(size):
          if (prow, pcol) in box_pixels:
            continue
          matches = []
          for b, (brow, bcol) in enumerate(zip(brows, bcols)):
            r, c = prow, pcol
            if pcol < bcol:
              c = bcol - 1
            if prow < brow:
              r = brow - 1
            if pcol > bcol + 1:
              c = bcol + 2
            if prow > brow + 1:
              r = brow + 2
            dist = abs(r - prow) + abs(c - pcol)
            if dist <= 4:
              matches.append((dist, b, r, c))
          if not matches:
            continue
          min_dist = min(match[0] for match in matches)
          matches = [match for match in matches if match[0] == min_dist]
          if len(matches) != 1:
            continue
          _, b, orow, ocol = matches[0]
          if (prow, pcol) != (orow, ocol):
            candidates[b].append((prow, pcol, orow, ocol))

      count = (common.randint(size, 3 * size)
               if num_pixels is None else num_pixels)
      chosen, used_outputs = [], set()
      if count >= num_boxes:
        # Make every gray box an active solving stage when the count permits.
        for options in candidates:
          options = [item for item in options
                     if item[2:] not in used_outputs]
          if not options:
            continue
          item = common.choice(options)
          chosen.append(item)
          used_outputs.add(item[2:])
      remaining = [item for options in candidates for item in options
                   if item[2:] not in used_outputs]
      remaining = common.shuffle(remaining)
      for item in remaining:
        if len(chosen) >= count:
          break
        if item[2:] in used_outputs:
          continue
        chosen.append(item)
        used_outputs.add(item[2:])
      prows = [item[0] for item in chosen]
      pcols = [item[1] for item in chosen]
      pcolors = [common.random_color(exclude=[5]) for _ in chosen]
      grid, _ = draw()
      assert grid is not None

  grid, target = draw()

  def match_pixels():
    """Replays the deterministic assignment and records each owning box."""
    orows, ocols = [-1] * len(prows), [-1] * len(prows)
    oboxes = [-1] * len(prows)
    for _ in range(len(prows)):
      matches = []
      for p, (prow, pcol) in enumerate(zip(prows, pcols)):
        if orows[p] != -1:
          continue
        min_dist, min_list = None, []
        for b, (brow, bcol) in enumerate(zip(brows, bcols)):
          r, c = prow, pcol
          if pcol < bcol:
            c = bcol - 1
          if prow < brow:
            r = brow - 1
          if pcol > bcol + 1:
            c = bcol + 2
          if prow > brow + 1:
            r = brow + 2
          if (r, c) in list(zip(orows, ocols)):
            continue
          dist = abs(r - prow) + abs(c - pcol)
          if dist > 4:
            continue
          if min_dist is not None and min_dist < dist:
            continue
          if min_dist is not None and min_dist > dist:
            min_list = []
          min_dist = dist
          min_list.append((dist, p, r, c, b))
        if len(min_list) == 1:
          matches.append(min_list[0])
      matches.sort()
      for _, p, r, c, b in matches:
        if (r, c) not in list(zip(orows, ocols)):
          orows[p], ocols[p], oboxes[p] = r, c, b
    if extra_idxs is not None:
      for idx, row, col in zip(extra_idxs, extra_rows, extra_cols):
        orows[idx], ocols[idx] = row, col
        for b, (brow, bcol) in enumerate(zip(brows, bcols)):
          on_horizontal = (row in (brow - 1, brow + 2)
                           and bcol - 1 <= col <= bcol + 2)
          on_vertical = (col in (bcol - 1, bcol + 2)
                         and brow - 1 <= row <= brow + 2)
          if on_horizontal or on_vertical:
            oboxes[idx] = b
            break
    return orows, ocols, oboxes

  orows, ocols, oboxes = match_pixels()
  active = {
      oboxes[p] for p in range(len(prows))
      if (prows[p], pcols[p]) != (orows[p], ocols[p])
  }
  box_order = sorted(range(len(brows)),
                     key=lambda b: (b not in active, brows[b], bcols[b]))
  processed = []
  output = common.deepcopy(grid)

  def move_box(i):
    """Moves all colored pixels assigned to one gray box."""
    nonlocal output
    if i >= len(box_order):
      return
    box = box_order[i]
    processed.extend(p for p in range(len(prows)) if oboxes[p] == box)
    output = common.deepcopy(grid)
    for p in processed:
      output[prows[p]][pcols[p]] = common.black()
    for p in processed:
      output[orows[p]][ocols[p]] = pcolors[p]

  move_box(0)
  move_box(1)
  move_box(2)
  move_box(3)
  move_box(4)
  move_box(5)
  assert output == target
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, brows=[2, 4, 10, 11], bcols=[10, 3, 10, 2],
               prows=[1, 2, 4, 5, 6, 6, 7, 9, 10, 12, 14, 14],
               pcols=[3, 7, 6, 11, 11, 13, 14, 2, 8, 6, 8, 12],
               pcolors=[1, 3, 2, 9, 2, 1, 3, 2, 6, 2, 4, 7],
               extra_idxs=[10], extra_rows=[12], extra_cols=[10]),
      generate(size=10, brows=[1, 1, 7], bcols=[1, 7, 7],
               prows=[1, 4, 5, 5, 7, 7, 8], pcols=[4, 4, 2, 7, 0, 4, 2],
               pcolors=[3, 4, 8, 6, 3, 2, 7]),
      generate(size=15, brows=[1, 1, 5, 6, 10, 10], bcols=[2, 11, 6, 13, 2, 11],
               prows=[2, 4, 8, 8, 12], pcols=[5, 14, 3, 8, 9],
               pcolors=[8, 6, 1, 9, 6]),
  ]
  test = [
      generate(size=15, brows=[1, 2, 6, 11, 13], bcols=[2, 12, 3, 8, 0],
               prows=[0, 1, 5, 7, 7, 9, 9, 13, 13],
               pcols=[8, 11, 1, 8, 13, 8, 11, 4, 13],
               pcolors=[4, 9, 7, 2, 8, 8, 9, 3, 6]),
  ]
  return {"train": train, "test": test}
