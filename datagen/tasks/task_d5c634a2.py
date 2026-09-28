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


def generate(width=None, height=None, rows=None, cols=None, cdirs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    rows: A list of rows of red inputs.
    cols: A list of cols of red inputs.
    cdirs: A list of red input directions.
  """

  def draw():
    grid, output = common.grid(width, height), common.grid(6, 3)
    ids = common.grid(width, height, -1)
    # Draw the red inputs.
    for i, (row, col, cdir) in enumerate(zip(rows, cols, cdirs)):
      for dc in [-1, 0, 1]:
        grid[row][col + dc] = 2
        ids[row][col + dc] = i
      grid[row - 2 * cdir + 1][col] = 2
      ids[row - 2 * cdir + 1][col] = i
    # Check the red inputs for adjacencies.
    for r in range(1, height - 1):
      for c in range(1, width - 1):
        if ids[r][c] == -1: continue
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          if ids[r + dr][c + dc] not in [-1, ids[r][c]]: return None, None
    # Draw the output colors.
    if cdirs.count(1) >= 1: output[0][0] = 3
    if cdirs.count(1) >= 2: output[2][0] = 3
    if cdirs.count(1) >= 3: output[0][2] = 3
    if cdirs.count(1) >= 4: output[2][2] = 3
    if cdirs.count(0) >= 1: output[0][3] = 1
    if cdirs.count(0) >= 2: output[2][3] = 1
    if cdirs.count(0) >= 3: output[0][5] = 1
    if cdirs.count(0) >= 4: output[2][5] = 1
    return grid, output

  if width is None:
    width, height = common.randint(4, 19), common.randint(4, 19)
    num_boxes = min(8, max(2, (width + height) // 4))
    while True:
      cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
      if cdirs.count(0) < 1 or cdirs.count(0) > 4: continue
      if cdirs.count(1) < 1 or cdirs.count(1) > 4: continue
      rows = [common.randint(cdir, height - 2 + cdir) for cdir in cdirs]
      cols = [common.randint(1, width - 2) for _ in cdirs]
      # Reject exact-coincident arrows: two arrows sharing (row, col, cdir)
      # overlap perfectly, so the input shows one arrow while the output
      # counts two, making the example unsolvable. (Partial overlaps are
      # already rejected by draw()'s adjacency check.)
      if len(set(zip(rows, cols, cdirs))) != len(cdirs): continue
      grid, _ = draw()
      if grid: break

  # Build the input grid (adjacency-validated); the output is derived below as a
  # forward tally, so draw()'s own output copy is discarded.
  grid, _ = draw()
  output = common.deepcopy(grid)

  def classify_arrows():
    """Recolors each red arrow by its pointing direction: up green, down blue."""
    for row, col, cdir in zip(rows, cols, cdirs):
      color = common.green() if cdir == 1 else common.blue()
      for dc in [-1, 0, 1]:
        output[row][col + dc] = color
      output[row - 2 * cdir + 1][col] = color

  def reveal_up(k):
    """Tallies the (k+1)-th up-pointing arrow as a green mark (left half)."""
    if cdirs.count(1) < k + 1: return
    r, c = [(0, 0), (2, 0), (0, 2), (2, 2)][k]
    output[r][c] = common.green()

  def reveal_down(k):
    """Tallies the (k+1)-th down-pointing arrow as a blue mark (right half)."""
    if cdirs.count(0) < k + 1: return
    r, c = [(0, 3), (2, 3), (0, 5), (2, 5)][k]
    output[r][c] = common.blue()

  # Stage 1: classify the arrows by direction, in the input's frame.
  classify_arrows()
  # Switch to the 3x6 answer canvas (plain init, not a solving step).
  output = common.grid(6, 3)
  # Stages 2..: tally the up-arrows (green), then the down-arrows (blue).
  reveal_up(0)
  reveal_up(1)
  reveal_up(2)
  reveal_up(3)
  reveal_down(0)
  reveal_down(1)
  reveal_down(2)
  reveal_down(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=6, rows=[0, 1, 3, 5], cols=[5, 1, 5, 2],
               cdirs=[0, 1, 0, 1]),
      generate(width=7, height=8, rows=[0, 3, 3, 6], cols=[2, 5, 1, 3],
               cdirs=[0, 1, 0, 0]),
      generate(width=7, height=8, rows=[1, 2, 4, 5, 7], cols=[1, 5, 2, 5, 1],
               cdirs=[1, 1, 1, 0, 1]),
      generate(width=4, height=5, rows=[0, 4], cols=[1, 1], cdirs=[0, 1]),
      generate(width=5, height=6, rows=[0, 3, 5], cols=[1, 3, 1],
               cdirs=[0, 0, 1]),
      generate(width=7, height=8, rows=[1, 3, 6, 7], cols=[1, 5, 2, 5],
               cdirs=[0, 1, 1, 1]),
      generate(width=15, height=15, rows=[2, 4, 5, 8, 10, 10, 12],
               cols=[3, 8, 1, 6, 2, 13, 7], cdirs=[1, 0, 0, 0, 1, 1, 0]),
  ]
  test = [
      generate(width=11, height=10, rows=[2, 2, 4, 6, 8],
               cols=[2, 8, 3, 7, 2], cdirs=[1, 0, 0, 0, 1]),
      generate(width=9, height=10, rows=[0, 2, 3, 5, 5, 7, 8],
               cols=[7, 1, 5, 3, 7, 1, 5], cdirs=[0, 1, 1, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
