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


def generate(rows=None, cols=None, size=9, height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: number of foreground dots to place when rows/cols are omitted
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    rows, cols = [], []
    cells = [(r, c) for r in range(height) for c in range(width)]
    max_count = min(12, (height * width) // 36)
    max_count = max(1, min(max_count, len(cells)))
    if count is None:
      count = common.randint(1, max_count)
    count = max(1, min(count, max_count))
    sampled = []
    for _ in range(20):
      sampled = []
      for r, c in common.sample(cells, len(cells)):
        if all(max(abs(r - pr), abs(c - pc)) >= 2 for pr, pc in sampled):
          sampled.append((r, c))
          if len(sampled) == count:
            break
      if len(sampled) == count:
        break
    if len(sampled) < count:
      sampled = common.sample(cells, count)
    for r, c in sampled:
      rows.append(r)
      cols.append(c)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c] = common.gray()

  output = [row[:] for row in grid]

  def expand_dot_pair(idx):
    chunk = max(1, (len(rows) + 4) // 5)
    start = idx * chunk
    stop = min(start + chunk, len(rows))
    if start >= len(rows):
      return
    for i in range(start, stop):
      r, c = rows[i], cols[i]
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          nr, nc = r + dr, c + dc
          if 0 <= nr < height and 0 <= nc < width:
            output[nr][nc] = common.blue()
    for i in range(len(rows)):
      r, c = rows[i], cols[i]
      output[r][c] = common.gray()

  expand_dot_pair(0)
  expand_dot_pair(1)
  expand_dot_pair(2)
  expand_dot_pair(3)
  expand_dot_pair(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 4, 7], cols=[6, 3, 1]),
      generate(rows=[1, 2, 5, 7], cols=[7, 3, 7, 3]),
  ]
  test = [
      generate(rows=[1, 2, 4, 7, 7], cols=[1, 7, 3, 1, 5]),
  ]
  return {"train": train, "test": test}
