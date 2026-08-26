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


def generate(rows=None, cols=None, idxs=None, color=None, size=10,
             height=None, width=None, count=None, acolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of angles where the arrows are pointing
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size for square grids)
    width: the number of columns (defaults to size for square grids)
    count: how many arrows to place (defaults to an area-scaled random count)
    acolors: per-arrow colors (defaults to a single `color` for every arrow)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    max_count = max(1, (height * width) // 8)
    if count is None:
      count = common.randint(1, max_count)
    count = max(1, min(count, max_count))
    # Greedily pack `count` well-separated arrows (repeated angles allowed),
    # reserving each arrow's block, its ray and the block's orthogonal halo so
    # every arrow stays an isolated object and no two colored cells overlap.
    free = set((r, c) for r in range(height) for c in range(width))
    rows, cols, idxs = [], [], []
    trials, max_trials = 0, 4 * count
    while len(rows) < count and trials < max_trials:
      trials += 1
      r = common.randint(1, height - 3)
      c = common.randint(1, width - 3)
      idx = common.randint(0, 3)
      dr, dc = -1 if idx in [0, 1] else 1, -1 if idx in [0, 2] else 1
      nr, nc = r if dr == -1 else r + 1, c if dc == -1 else c + 1
      block = [cell for cell in [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
               if cell != (nr, nc)]
      ray, rr, cc = [], nr, nc
      while True:
        rr, cc = rr + dr, cc + dc
        if rr < 0 or rr >= height or cc < 0 or cc >= width: break
        ray.append((rr, cc))
      occupied = set(block) | set(ray)
      if not occupied.issubset(free): continue
      halo = set()
      for br, bc in block:
        halo.update([(br - 1, bc), (br + 1, bc), (br, bc - 1), (br, bc + 1)])
      rows.append(r)
      cols.append(c)
      idxs.append(idx)
      free -= occupied
      free -= halo
    if not rows:
      rows, cols, idxs = [1], [1], [common.randint(0, 3)]
    acolors = [common.random_color() for _ in rows]
  if acolors is None:
    acolors = [color] * len(rows)

  grid, output = common.grids(width, height)
  for j, (r, c, idx) in enumerate(zip(rows, cols, idxs)):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[r + dr][c + dc] = grid[r + dr][c + dc] = acolors[j]
    dr, dc = -1 if idx in [0, 1] else 1, -1 if idx in [0, 2] else 1
    r, c = r if dr == -1 else r + 1, c if dc == -1 else c + 1
    grid[r][c] = output[r][c] = common.black()

  def extend_arrow(arrow_idx):
    if arrow_idx >= len(rows):
      return
    r, c, idx = rows[arrow_idx], cols[arrow_idx], idxs[arrow_idx]
    dr, dc = -1 if idx in [0, 1] else 1, -1 if idx in [0, 2] else 1
    r, c = r if dr == -1 else r + 1, c if dc == -1 else c + 1
    while True:
      r, c = r + dr, c + dc
      if r < 0 or r >= height or c < 0 or c >= width: break
      output[r][c] = acolors[arrow_idx]

  extend_arrow(0)
  extend_arrow(1)
  extend_arrow(2)
  for k in range(3, len(rows)):
    extend_arrow(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 4], cols=[1, 6], idxs=[1, 2], color=7),
      generate(rows=[1, 6], cols=[3, 3], idxs=[2, 1], color=9),
  ]
  test = [
      generate(rows=[2, 4, 6], cols=[3, 7, 2], idxs=[0, 3, 2], color=8),
  ]
  return {"train": train, "test": test}
