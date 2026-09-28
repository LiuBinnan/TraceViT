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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the crosses.
    cols: The columns of the crosses.
  """

  def draw():
    matches = 0
    grid, output = common.grids(width, height)
    def redify(r, c):
      # We should always write to black, and never adjacent to another red cell.
      if output[r][c] != 0: return False
      for dr, dc in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]:
        if common.get_pixel(output, r + dr, c + dc) == 2: return False
      output[r][c] = 2
      return True
    for row, col in zip(rows, cols):
      for dr, dc in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]:
        output[row + dr][col + dc] = grid[row + dr][col + dc] = 3
    for j in range(len(rows)):
      for i in range(j):
        if rows[i] - cols[i] == rows[j] - cols[j]:
          matches += 1
          diff = 1 if rows[j] > rows[i] else -1
          row, col = rows[i] + diff, cols[i] + diff
          while row != rows[j]:
            if not redify(row, col): return None, None, None
            row, col = row + diff, col + diff
        if rows[i] + cols[i] == rows[j] + cols[j]:
          matches += 1
          diff = 1 if rows[j] > rows[i] else -1
          row, col = rows[i] + diff, cols[i] - diff
          while row != rows[j]:
            if not redify(row, col): return None, None, None
            row, col = row + diff, col - diff
    return grid, output, matches

  if width is None:
    width, height = common.randint(9, 22), common.randint(9, 22)
    num_crosses = 3 if width * height <= 144 else 4
    expected_matches = common.randint(1, 2)
    attempts = 0
    while True:
      attempts += 1
      if attempts > 1000:
        # Bound the rejection tail with separated crosses having exactly the
        # requested number of shared diagonals.  The 4-cross/two-match layout
        # is rotated when the canvas is narrow.
        if num_crosses == 3 and expected_matches == 1:
          centers = [(1, 1), (1, 5), (5, 1)]
        elif num_crosses == 3:
          centers = [(1, 1), (1, 7), (4, 4)]
        elif expected_matches == 1:
          centers = [(1, 1), (1, 5), (5, 1), (5, 6)]
        else:
          centers = [(1, 1), (1, 5), (1, 9), (5, 5)]
          if width < 11:
            centers = [(col, row) for row, col in centers]
        rows = [row - 1 for row, _ in centers]
        cols = [col - 1 for _, col in centers]
        break
      rows = [common.randint(0, height - 3) for _ in range(num_crosses)]
      cols = [common.randint(0, width - 3) for _ in range(num_crosses)]
      lengths = [3] * num_crosses
      if common.overlaps(rows, cols, lengths, lengths): continue
      if common.some_abutted(rows, cols, lengths, lengths): continue
      grid, _, matches = draw()
      if not grid: continue
      if matches != expected_matches: continue
      break
    rows, cols = [row + 1 for row in rows], [col + 1 for col in cols]

  grid, output = common.grids(width, height)
  for row, col in zip(rows, cols):
    for dr, dc in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]:
      output[row + dr][col + dc] = grid[row + dr][col + dc] = 3
  bridges = []
  for j in range(len(rows)):
    for i in range(j):
      if rows[i] - cols[i] == rows[j] - cols[j]:
        diff = 1 if rows[j] > rows[i] else -1
        bridge = []
        row, col = rows[i] + diff, cols[i] + diff
        while row != rows[j]:
          bridge.append((row, col))
          row, col = row + diff, col + diff
        bridges.append(bridge)
      if rows[i] + cols[i] == rows[j] + cols[j]:
        diff = 1 if rows[j] > rows[i] else -1
        bridge = []
        row, col = rows[i] + diff, cols[i] - diff
        while row != rows[j]:
          bridge.append((row, col))
          row, col = row + diff, col - diff
        bridges.append(bridge)

  def paint_bridge(index):
    if index >= len(bridges):
      return
    for row, col in bridges[index]:
      output[row][col] = 2

  paint_bridge(0)
  paint_bridge(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=14, rows=[1, 2, 5, 10], cols=[3, 10, 7, 10]),
      generate(width=10, height=14, rows=[2, 7, 11], cols=[2, 7, 3]),
      generate(width=13, height=12, rows=[1, 3, 6, 8], cols=[10, 6, 3, 10]),
  ]
  test = [
      generate(width=13, height=17, rows=[1, 7, 11, 14], cols=[2, 8, 4, 10]),
  ]
  return {"train": train, "test": test}
