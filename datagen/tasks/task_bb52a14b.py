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


def generate(colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    gsize: The width and height of the square grid.
  """

  def draw():
    grid = common.grid(gsize, gsize)
    prow, pcol = 0, 0
    for i, color in enumerate(colors):
      grid[i // gsize][i % gsize] = color
      if color == 4: prow, pcol = max(prow, i // gsize), max(pcol, i % gsize)
    prow, pcol = prow - 1, pcol - 1
    coords = []
    for row in range(0, gsize):
      for col in range(0, gsize):
        match, bad = True, False
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if nr < 0 or nr >= gsize or nc < 0 or nc >= gsize: continue
            if grid[prow + dr][pcol + dc] == 4:
              if grid[nr][nc] not in [0, 4]: bad = True
            elif grid[prow + dr][pcol + dc] != grid[nr][nc]: match = False
        if not match: continue
        if bad: return None, None
        if row < 1 or row >= gsize - 1 or col < 1 or col >= gsize - 1: return None, None
        coords.append((row, col))
    rows, cols = zip(*coords)
    if common.overlaps(rows, cols, [7] * len(coords), [7] * len(coords)):
      return None, None
    return grid, (coords, prow, pcol)

  if colors is None:
    if gsize is None:
      gsize = common.randint(18, 28)
    pattern = [common.choice([1, 8]) for _ in range(9)]
    if common.randint(0, 1):
      pattern[0] = pattern[2] = pattern[6] = pattern[8] = 0
      if common.randint(0, 1): pattern[4] = 0
    else:
      pattern[1] = pattern[3] = pattern[5] = pattern[7] = 0
    pattern[common.choice([0, 1, 2, 3, 5, 6, 7, 8])] = 0  # Avoid middle.
    num_boxes = common.randint(2, 3)
    while True:
      rows = [common.randint(1, gsize - 2) for _ in range(num_boxes)]
      cols = [common.randint(1, gsize - 2) for _ in range(num_boxes)]
      if not common.overlaps(rows, cols, [7] * num_boxes, [7] * num_boxes):
        grid = common.grid(gsize, gsize)
        for i, (row, col) in enumerate(zip(rows, cols)):
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              color = pattern[(dr + 1) * 3 + dc + 1]
              grid[row + dr][col + dc] = 4 if not i and not color else color
        colors = common.flatten(grid)
        grid, _ = draw()
        if grid: break
    while True:
      grid = common.grid(gsize, gsize)
      for row in range(gsize):
        for col in range(gsize):
          grid[row][col] = 0 if common.randint(0, 4) else common.choice([1, 8])
      for i, (row, col) in enumerate(zip(rows, cols)):
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            color = pattern[(dr + 1) * 3 + dc + 1]
            grid[row + dr][col + dc] = 4 if not i and not color else color
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break
  elif gsize is None:
    gsize = 22

  grid, match_data = draw()
  coords, prow, pcol = match_data
  targets = [coord for coord in coords if coord != (prow, pcol)]
  marker_offsets = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                    if grid[prow + dr][pcol + dc] == common.yellow()]
  output = common.deepcopy(grid)

  def copy_match(index):
    """Restores the complete marker stencil onto one matching 3x3 patch."""
    if index >= len(targets): return
    row, col = targets[index]
    for dr, dc in marker_offsets:
      output[row + dr][col + dc] = common.yellow()

  copy_match(0)
  copy_match(1)
  copy_match(2)
  copy_match(3)
  copy_match(4)
  copy_match(5)
  copy_match(6)
  copy_match(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8,
                       0, 0, 8, 0, 0, 0, 0, 0, 8, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 8, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 4, 8, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 8, 1, 1, 8, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 1, 0, 0,
                       0, 0, 0, 4, 1, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                       0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 8, 0, 0, 0,
                       1, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 8, 0, 0, 0, 8, 8, 0, 0,
                       0, 0, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,
                       0, 1, 0, 0, 4, 8, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 8, 1, 0, 1,
                       0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0,
                       1, 8, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 1, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                       0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 8, 0,
                       0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       8, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 4, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 1, 0, 8,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 4, 4, 4, 0, 0,
                       0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 8, 1,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 8, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 8, 0,
                       0, 0, 0, 1, 0, 0, 1, 8, 8, 1, 0, 0, 0, 0, 8, 8, 0, 0, 0, 1, 0, 0,
                       0, 0, 8, 0, 0, 8, 8, 0, 0, 0, 1, 8, 1, 0, 0, 8, 0, 0, 0, 1, 0, 0,
                       0, 8, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 8, 0, 0,
                       0, 1, 0, 0, 4, 8, 4, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 8,
                       8, 0, 0, 0, 4, 8, 8, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 1, 0, 8, 1, 0,
                       0, 0, 0, 0, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0,
                       0, 8, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 8,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0,
                       0, 0, 8, 8, 8, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 1, 0, 0, 0, 0,
                       1, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 8, 0,
                       0, 8, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 8, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1, 0, 8, 0, 8, 1, 0, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
