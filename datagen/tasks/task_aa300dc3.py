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


def generate(tops=None, lefts=None, rights=None, bottoms=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: The lengths of the top lines.
    lefts: The lengths of the left lines.
    rights: The lengths of the right lines.
    bottoms: The lengths of the bottom lines.
    gsize: The side length of the (square) grid.
  """

  def draw(multi_diags=True):
    n = len(tops)
    grid, output = common.grids(n, n)
    def put(i, j):
      output[i][j] = grid[i][j] = common.gray()
    for i in range(n):
      for j in range(tops[i]): put(j, i)
      for j in range(lefts[i]): put(i, j)
      for j in range(rights[i]): put(i, n - 1 - j)
      for j in range(bottoms[i]): put(n - 1 - j, i)
    if not common.all_connected(grid, 0): return None, None
    longest, diags = -1, []
    for diag_dir in [1, -1]:
      for diag in range(-n, n):
        length = 0
        for r in range(n):
          c = (r - diag) if diag_dir == 1 else (n - 1 - r - diag)
          if c < 0 or c >= n: continue
          if grid[r][c] == 0: length += 1
        if length < longest: continue
        if length > longest: diags.clear()
        diags.append((diag_dir, diag))
        longest = length
    if not multi_diags and len(diags) > 1: return None, None
    while True:
      if len(diags) > 1: diags.pop()
      if len(diags) <= 1: break
      if len(diags) > 1: diags.pop(0)
      if len(diags) <= 1: break
    for diag in diags:
      diag_dir, diag_val = diag
      for r in range(n):
        for c in range(n):
          if diag_dir == 1:
            if output[r][c] == 0 and r - c == diag_val: output[r][c] = common.cyan()
          if diag_dir == -1:
            if output[r][c] == 0 and n - 1 - r - c == diag_val: output[r][c] = common.cyan()
    return grid, output

  if tops is None:
    if gsize is None:
      gsize = common.randint(8, 22)
    def build_lengths(side):
      hi = min(5, max(2, round(0.30 * side)))
      values = []
      for v in range(1, hi + 1):
        values.extend([v] * (hi + 1 - v))
      return values
    lengths = build_lengths(gsize)
    attempts = 0
    while True:
      tops = [common.choice(lengths) for _ in range(gsize)]
      lefts = [common.choice(lengths) for _ in range(gsize)]
      rights = [common.choice(lengths) for _ in range(gsize)]
      bottoms = [common.choice(lengths) for _ in range(gsize)]
      grid, _ = draw(multi_diags=False)
      if grid: break
      attempts += 1
      if attempts >= 2000:
        gsize = 10
        lengths = build_lengths(gsize)
        attempts = 0

  grid, solved = draw()
  if grid is None:
    return {"input": grid, "output": solved}
  output = common.deepcopy(grid)

  # Bookkeeping (no frame): the cells of the single longest all-empty diagonal
  # draw() selected -- exactly the cells it recoloured cyan.
  diagonal = [(r, c) for r in range(len(solved)) for c in range(len(solved[0]))
              if solved[r][c] == common.cyan()]

  def draw_diagonal():
    """Draws the longest all-empty diagonal in cyan (the solving move)."""
    nonlocal output
    for r, c in diagonal:
      output[r][c] = common.cyan()

  draw_diagonal()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[1, 1, 1, 1, 1, 1, 3, 2, 2, 1],
               lefts=[1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
               rights=[1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 2, 3, 3, 1, 2, 2, 1, 1]),
      generate(tops=[1, 3, 2, 1, 3, 1, 2, 1, 1, 1],
               lefts=[1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
               rights=[1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 1, 2, 1, 1, 2, 3, 3, 1]),
      generate(tops=[1, 4, 3, 1, 1, 1, 2, 3, 3, 1],
               lefts=[1, 3, 3, 2, 1, 1, 3, 2, 3, 1],
               rights=[1, 4, 3, 1, 2, 1, 1, 2, 2, 1],
               bottoms=[1, 4, 2, 1, 4, 4, 2, 1, 3, 1]),
      generate(tops=[1, 1, 1, 1, 2, 3, 1, 1, 2, 1],
               lefts=[1, 1, 2, 3, 2, 1, 2, 1, 1, 1],
               rights=[1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 1, 3, 2, 4, 1, 2, 1, 1]),
  ]
  test = [
      generate(tops=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               lefts=[1, 3, 2, 3, 1, 1, 1, 1, 1, 1],
               rights=[1, 2, 2, 1, 3, 4, 1, 1, 1, 1],
               bottoms=[1, 2, 2, 3, 3, 2, 2, 3, 1, 1]),
  ]
  return {"train": train, "test": test}
