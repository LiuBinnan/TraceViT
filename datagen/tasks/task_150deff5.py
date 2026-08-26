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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             nobj=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where toys should be placed
    cols: a list of horizontal coordinates where toys should be placed
    idxs: a list of toy indices (0=box, 1=tall stick, 2=flat stick)
    nobj: the number of toys to scatter (area-scaled when omitted)
  """
  if width is None:
    # Structural widening (rule unchanged): decoupled wide grid sizes and an
    # area-scaled toy count, mirroring re_arc's h/w in [8, 30] and
    # noccs ~ (h * w) // 10.  Toys are scattered one at a time behind a 1-cell
    # moat so every gray shape stays a clean, separately recoverable component
    # -- a strict subset of the original (touching-allowed) placements.
    width = common.randint(8, 30)
    height = common.randint(8, 30)
    area = width * height
    if nobj is None:
      nobj = common.randint(2, max(2, area // 12))
    # Guarantee at least one box and one stick (as the original always had
    # both), then fill the remainder with a random mix; order is irrelevant to
    # the two rendering passes below.
    want = [0, common.randint(1, 2)]
    want += [common.randint(0, 2) for _ in range(max(0, nobj - 2))]
    rows, cols, idxs = [], [], []
    taken = set()
    for idx in want:
      pw, ph = (2, 2) if idx == 0 else ((1, 3) if idx == 1 else (3, 1))
      for _attempt in range(60):
        row = common.randint(1, height - ph - 1)
        col = common.randint(1, width - pw - 1)
        if idx == 0:
          cells = [(row + dr, col + dc) for dr in (0, 1) for dc in (0, 1)]
        elif idx == 1:
          cells = [(row + dr, col) for dr in (0, 1, 2)]
        else:
          cells = [(row, col + dc) for dc in (0, 1, 2)]
        halo = {(r + dr, c + dc) for (r, c) in cells
                for dr in (-1, 0, 1) for dc in (-1, 0, 1)}
        if halo & taken:
          continue
        taken.update(cells)
        rows.append(row)
        cols.append(col)
        idxs.append(idx)
        break

  grid, output = common.grids(width, height)
  for row, col, idx in zip(rows, cols, idxs):
    if idx != 0: continue
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      grid[row + dr][col + dc] = common.gray()
      output[row + dr][col + dc] = common.cyan()
  for row, col, idx in zip(rows, cols, idxs):
    if idx == 1:
      for dr, dc in [(0, 0), (1, 0), (2, 0)]:
        grid[row + dr][col + dc] = common.gray()
        output[row + dr][col + dc] = common.red()
    if idx == 2:
      for dr, dc in [(0, 0), (0, 1), (0, 2)]:
        grid[row + dr][col + dc] = common.gray()
        output[row + dr][col + dc] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=9, rows=[1, 3, 4, 3, 2, 6],
               cols=[2, 4, 6, 3, 4, 5], idxs=[0, 0, 0, 1, 2, 2]),
      generate(width=10, height=8, rows=[1, 1, 4, 1, 1, 4],
               cols=[1, 4, 5, 3, 6, 4], idxs=[0, 0, 0, 1, 1, 1]),
      generate(width=9, height=8, rows=[1, 4, 1, 3], cols=[4, 4, 1, 3],
               idxs=[0, 0, 2, 1]),
  ]
  test = [
      generate(width=11, height=8, rows=[0, 2, 5, 0, 2, 4, 1],
               cols=[2, 4, 5, 5, 1, 3, 6], idxs=[0, 0, 0, 2, 2, 2, 1]),
  ]
  return {"train": train, "test": test}
