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

from typing import cast

import common


def generate(rows=None, cols=None, deltas=None, size=15, b=0, dr=(-1, 0, 1, 0),
             dc=(0, 1, 0, -1), height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    deltas: a list of deltas for each flower and in each direction
    size: the width and height of the (square) grid
    b: the integer used for all background cells
    dr: a mapping of angles to row diffs
    dc: a mapping of angles to col diffs
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  def draw(grid, output):
    for idx in range(len(rows)):
      row, col = rows[idx], cols[idx]
      output[row][col] = grid[row][col] = 1 if idx else 2
    for d, delta in enumerate(deltas):
      if delta == -1: continue  # The petal flew off.
      idx, angle = d // 4, d % 4
      r, c = rows[idx] + dr[angle], cols[idx] + dc[angle]
      if output[r][c]: return False
      output[r][c] = 7 if idx else 3
      r, c = r + delta * dr[angle], c + delta * dc[angle]
      if grid[r][c]: return False
      grid[r][c] = 7 if idx else 3
    return True

  if rows is None:
    while True:
      # Choose centers for the flowers and deltas for their petals.
      rows = common.sample(range(2, height - 2), 2)
      cols = common.sample(range(2, width - 2), 2)
      deltas = []
      for idx in range(2):
        deltas.append(common.randint(1, rows[idx] - 1))
        deltas.append(common.randint(1, width - cols[idx] - 2))
        deltas.append(common.randint(1, height - rows[idx] - 2))
        deltas.append(common.randint(1, cols[idx] - 1))
      # Delete some random petals, and any petals that overlap with others.
      pixels_seen = {(rows[0], cols[0]), (rows[1], cols[1])}
      for d, delta in enumerate(deltas):
        idx, angle = d // 4, d % 4
        r = rows[idx] + dr[angle] * (delta + 1)
        c = cols[idx] + dc[angle] * (delta + 1)
        if (r, c) in pixels_seen or common.randint(0, 1): deltas[d] = -1
        pixels_seen.add((r, c))
      grid, output = common.grids(width, height, b)
      if draw(grid, output): break

  grid, output = common.grids(width, height, b)
  for idx in range(len(rows)):
    row, col = rows[idx], cols[idx]
    output[row][col] = grid[row][col] = 1 if idx else 2
  for d, delta in enumerate(deltas):
    if delta == -1:
      continue
    idx, angle = d // 4, d % 4
    r = rows[idx] + (delta + 1) * dr[angle]
    c = cols[idx] + (delta + 1) * dc[angle]
    grid[r][c] = 7 if idx else 3

  def move_flower(flower_idx):
    for angle in range(4):
      delta = deltas[4 * flower_idx + angle]
      if delta == -1:
        continue
      r = rows[flower_idx] + dr[angle]
      c = cols[flower_idx] + dc[angle]
      output[r][c] = 7 if flower_idx else 3

  move_flower(0)
  move_flower(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[4, 10], cols=[3, 11], deltas=[3, 4, 4, 2, 3, 2, 3, 5]),
      generate(rows=[10, 2], cols=[11, 3], deltas=[-1, -1, 3, 5, 1, 5, 5, 2]),
      generate(rows=[11, 6], cols=[6, 10], deltas=[10, 7, 2, -1, -1, -1, 7, 8]),
  ]
  test = [
      generate(rows=[3, 6], cols=[11, 5], deltas=[2, -1, 8, 10, -1, 8, -1, 4]),
  ]
  return {"train": train, "test": test}
