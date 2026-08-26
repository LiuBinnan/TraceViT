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


def generate(wides=None, talls=None, colors=None, rows=None, cols=None,
             mostest=None, pcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: a list of widths of quadrants
    talls: a list of heights of quadrants
    colors: a list of colors to be used
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    mostest: the mostest color
    pcolor: the color used for the small pixels
  """
  if wides is None:
    # Structural widening (puzzle rule unchanged: the region holding the most
    # noise pixels wins). Variable quadrant-grid shape -> #colors / #objects;
    # area-scaled INTERIOR-only noise -> density; unique winner via a
    # re_arc-style tie-break. Interior-only placement keeps every region's
    # outer ring (hence its bounding box and majority color) intact, so the
    # verifier recovers the same winner.
    pcolor = common.random_color()
    ncells = common.randint(2, 9)
    divisors = [d for d in range(1, ncells + 1)
                if ncells % d == 0 and d <= 7 and ncells // d <= 7]
    qrows = common.sample(divisors, 1)[0]
    qcols = ncells // qrows
    wides = [common.randint(4, 30 // qcols) for _ in range(qcols)]
    talls = [common.randint(4, 30 // qrows) for _ in range(qrows)]
    colors = common.sample([c for c in range(10) if c != pcolor], qcols * qrows)
    # Non-adjacent interior cells (even sublattice) per quadrant: each noise
    # pixel is isolated, so it reads as its own object (spreads #objects) and
    # never breaks a region's outer ring -> the verifier's per-region bounding
    # box and majority color stay exact.
    subs = [[(r, c) for r in range(1, talls[ridx] - 1)
             for c in range(1, wides[cidx] - 1) if (r + c) % 2 == 0]
            for ridx in range(qrows) for cidx in range(qcols)]
    caps = [max(1, len(s)) for s in subs]
    meann = max(1, sum(caps) // len(caps))
    while True:
      counts = [common.randint(0, min(meann, cap)) for cap in caps]
      if max(counts) == 0:
        continue
      mx = max(counts)
      tied = [idx for idx, cnt in enumerate(counts) if cnt == mx]
      for idx in tied[1:]:
        counts[idx] -= 1
      if sum(1 for cnt in counts if cnt > 0) >= 2:
        break
    mostest = colors[tied[0]]
    rows, cols = [], []
    for ridx in range(qrows):
      for cidx in range(qcols):
        idx = ridx * qcols + cidx
        pixels = common.sample(subs[idx], counts[idx])
        rows.extend([p[0] + sum(talls[:ridx]) for p in pixels])
        cols.extend([p[1] + sum(wides[:cidx]) for p in pixels])

  grid = common.grid(sum(wides), sum(talls))
  for ridx, _ in enumerate(talls):
    for cidx, _ in enumerate(wides):
      for r in range(sum(talls[:ridx]), sum(talls[:ridx + 1])):
        for c in range(sum(wides[:cidx]), sum(wides[:cidx + 1])):
          grid[r][c] = colors[ridx * len(wides) + cidx]
  for row, col in zip(rows, cols):
    grid[row][col] = pcolor
  output = [row[:] for row in grid]
  counts = [0] * len(colors)
  for row, col in zip(rows, cols):
    ridx, cidx = 0, 0
    while row >= sum(talls[:ridx + 1]):
      ridx += 1
    while col >= sum(wides[:cidx + 1]):
      cidx += 1
    counts[ridx * len(wides) + cidx] += 1
  winner = max(range(len(counts)), key=lambda idx: counts[idx])
  output = common.grid(sum(wides), sum(talls))
  wridx, wcidx = divmod(winner, len(wides))
  for r in range(sum(talls[:wridx]), sum(talls[:wridx + 1])):
    for c in range(sum(wides[:wcidx]), sum(wides[:wcidx + 1])):
      output[r][c] = colors[winner]
  for row, col in zip(rows, cols):
    ridx, cidx = 0, 0
    while row >= sum(talls[:ridx + 1]):
      ridx += 1
    while col >= sum(wides[:cidx + 1]):
      cidx += 1
    if ridx == wridx and cidx == wcidx:
      output[row][col] = pcolor
  output = common.grid(1, 1, mostest)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[8, 5], talls=[7, 10], colors=[4, 0, 8, 1],
               rows=[2, 2, 4, 10, 11, 12, 15],
               cols=[3, 10, 5, 5, 11, 2, 5],
               mostest=8, pcolor=6),
      generate(wides=[7, 8], talls=[9, 7], colors=[3, 2, 8, 8],
               rows=[1, 1, 3, 4, 6, 12, 13], cols=[10, 13, 9, 2, 11, 11, 6],
               mostest=2, pcolor=1),
      generate(wides=[7, 10], talls=[8, 8], colors=[1, 5, 0, 6],
               rows=[1, 3, 5, 6, 9, 11, 11, 14],
               cols=[1, 3, 11, 2, 12, 10, 15, 13], mostest=6, pcolor=4),
      generate(wides=[7, 12], talls=[9, 7], colors=[1, 8, 1, 4],
               rows=[4, 13, 14], cols=[11, 9, 12], mostest=4, pcolor=2),
  ]
  test = [
      generate(wides=[9, 10], talls=[4, 8, 6], colors=[3, 3, 2, 8, 1, 8],
               rows=[1, 5, 5, 7, 8, 9, 9, 11, 14, 15, 16],
               cols=[7, 1, 7, 4, 2, 6, 14, 12, 14, 4, 1],
               mostest=2, pcolor=4),
  ]
  return {"train": train, "test": test}
