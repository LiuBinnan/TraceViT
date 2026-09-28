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


def generate(width=None, height=None, rows=None, lengths=None, pcol=None,
             flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the segments.
    lengths: The lengths of the segments.
    pcol: The column of the red pixel.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if width is None:
    width, height = common.randint(10, 28), common.randint(10, 24)
    pcol = common.randint(3, width - 4)
    row, rows, lengths = 0, [], []
    while True:
      row += common.randint(2, 3)
      if row + 2 >= height: break
      num_segments = common.randint(2, 4)
      attempts = 0
      while True:
        the_lengths = [common.randint(1, width) for _ in range(num_segments)]
        if sum(the_lengths) + num_segments - 1 == width: break
        attempts += 1
        if attempts >= 500:
          # Construct an exact positive split after a long rejection tail.
          usable = width - num_segments + 1
          cuts = sorted(common.sample(range(1, usable), num_segments - 1))
          the_lengths = [b - a for a, b in
                         zip([0] + cuts, cuts + [usable])]
          break
      rows.extend([row] * num_segments)
      lengths.extend(the_lengths)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  # Input: the horizontal platforms plus the single red source pixel that will
  # drip down from the top row.
  grid = common.grid(width, height)
  for row in set(rows):
    col = 0
    for length, r in zip(lengths, rows):
      if r != row: continue
      for c in range(length):
        grid[row][col + c] = common.cyan()
      col += length + 1
  grid[0][pcol] = common.red()

  # Trace the water: it falls straight down, and where a platform blocks it it
  # spreads along that row until it finds a gap to keep falling through. This
  # only reads the platforms, so it is deterministic bookkeeping (no frames).
  flow = common.grid(width, height)
  for row in set(rows):
    col = 0
    for length, r in zip(lengths, rows):
      if r != row: continue
      for c in range(length):
        flow[row][col + c] = common.cyan()
      col += length + 1
  wet_by_row = {}
  queue = [(0, pcol)]
  while queue:
    row, col = queue.pop()
    if flow[row][col] == common.red(): continue  # Already visited.
    flow[row][col] = common.red()
    wet_by_row.setdefault(row, []).append(col)
    if row + 1 >= height: continue
    if flow[row + 1][col] == 0: queue.append((row + 1, col))
    if flow[row + 1][col] == common.cyan():
      if col - 1 >= 0: queue.append((row, col - 1))
      if col + 1 < width: queue.append((row, col + 1))

  # Group the wet cells into depth bands: one band for the pooling-and-dripping
  # over each platform, plus a final band for the run-off down to the floor.
  levels = sorted(set(rows))
  bands = [[] for _ in range(len(levels) + 1)]
  for row in sorted(wet_by_row):
    band = sum(1 for level in levels if level < row)
    for col in wet_by_row[row]:
      bands[band].append((row, col))

  # Orient the input exactly as the original did, then paint every water frame
  # directly into that final orientation (so no frame needs re-orienting).
  if flip: grid = common.flip(grid)
  if xpose: grid = common.transpose(grid)

  def put(row, col, color):
    r, c = (height - 1 - row, col) if flip else (row, col)
    if xpose:
      output[c][r] = color
    else:
      output[r][c] = color

  output = common.deepcopy(grid)

  def flow_down(i):
    """Reveals the water pooling on platform i and dripping through its gaps."""
    if i >= len(bands): return
    for row, col in bands[i]:
      put(row, col, common.red())

  flow_down(0)
  flow_down(1)
  flow_down(2)
  flow_down(3)
  flow_down(4)
  flow_down(5)
  flow_down(6)
  for i in range(7, len(bands)):
    flow_down(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, rows=[2, 2, 2, 5, 5, 9, 9, 9],
               lengths=[5, 2, 2, 3, 7, 6, 1, 2], pcol=3, flip=False,
               xpose=True),
      generate(width=17, height=11, rows=[2, 2, 2, 4, 4, 4, 7, 7],
               lengths=[5, 3, 7, 2, 9, 4, 5, 11], pcol=7, flip=False,
               xpose=False),
      generate(width=10, height=13, rows=[3, 3, 3, 7, 7, 10, 10, 10, 10],
               lengths=[2, 2, 4, 8, 1, 1, 1, 4, 1], pcol=4, flip=True,
               xpose=True),
  ]
  test = [
      generate(width=14, height=15,
               rows=[2, 2, 4, 4, 4, 4, 7, 7, 7, 10, 10, 10, 10],
               lengths=[4, 9, 2, 4, 3, 2, 2, 6, 4, 4, 2, 3, 2], pcol=6,
               flip=False, xpose=False),
  ]
  return {"train": train, "test": test}
