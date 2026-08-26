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


def generate(row=None, col=None, size=13, height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the pixel should be placed
    col: a horizontal coordinate where the pixel should be placed
    size: square fallback (keeps validate() byte-identical)
    height: number of rows (independent of width when given)
    width: number of columns (independent of height when given)
    count: number of input pixels to place when row/col are sampled
  """
  if height is None: height = size
  if width is None: width = size
  if count is None:
    count = common.randint(1, min(height, width)) if row is None else 1

  grid, output = common.grids(width, height)
  directions = [(-1, 1), (1, -1)]

  def path_cells(seed_row, seed_col):
    cells = set()
    for dr, dc in directions:
      v, h, r, c = 2, 0, seed_row, seed_col
      while True:
        if v:
          r, v = r + dr, v - 1
          if r < 0 or r >= height: break
          cells.add((r, c))
          if not v: h = 2
        else:
          c, h = c + dc, h - 1
          if c < 0 or c >= width: break
          cells.add((r, c))
          if not h: v = 2
    return cells

  seeds = []
  if row is None:
    available = {(r, c) for r in range(height) for c in range(width)}
    while len(seeds) < count and available:
      ordered = sorted(available)
      candidate = ordered[common.randint(0, len(ordered) - 1)]
      seeds.append(candidate)
      available -= path_cells(*candidate) | {candidate}
  else:
    seeds.append((row, col))

  for seed_row, seed_col in seeds:
    output[seed_row][seed_col] = grid[seed_row][seed_col] = common.cyan()

  def draw_path(seed_row, seed_col, direction_idx):
    if direction_idx >= len(directions):
      return
    dr, dc = directions[direction_idx]
    v, h, r, c = 2, 0, seed_row, seed_col
    while True:
      if v:
        r, v = r + dr, v - 1
        if r < 0 or r >= height: break
        output[r][c] = common.gray()
        if not v: h = 2
      else:
        c, h = c + dc, h - 1
        if c < 0 or c >= width: break
        output[r][c] = common.gray()
        if not h: v = 2

  for seed_row, seed_col in seeds:
    draw_path(seed_row, seed_col, 0)
    draw_path(seed_row, seed_col, 1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4),
      generate(row=7, col=6),
  ]
  test = [
      generate(row=5, col=5),
  ]
  return {"train": train, "test": test}
