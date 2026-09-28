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


def generate(inwidth=None, inheight=None, outwidth=None, outheight=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    inwidth: The width of the input grid.
    inheight: The height of the input grid.
    outwidth: The width of the output grid.
    outheight: The height of the output grid.
    colors: The colors of the input grid.
  """

  def draw():
    grid = common.grid(inwidth, inheight)
    output = common.grid(outwidth, outheight)
    for i, color in enumerate(colors):
      grid[i // inwidth][i % inwidth] = color
    outrow = 0
    for row in range(inheight):
      if 8 not in grid[row]: continue
      for col in range(outwidth):
        output[outrow][col] = grid[row][grid[row].index(8) + 2 + col]
      outrow += 1
    if len(set(common.flatten(output))) == 1: return None, None
    return grid, output

  if inwidth is None:
    inwidth, inheight = common.randint(10, 28), common.randint(10, 28)
    segments = common.randint(1, (inheight + 1) // 4)
    outwidth, outheight = common.randint(3, min(8, inwidth - 4)), 2 * segments
    while True:
      brows = [common.randint(0, inheight - 2) for _ in range(segments)]
      if not common.overlaps_1d(brows, [3] * segments): break
    while True:
      grid = common.grid(inwidth, inheight)
      for row in range(inheight):
        for col in range(inwidth):
          if common.randint(0, 1): continue
          grid[row][col] = common.choice([1, 2, 3, 4, 5, 6, 7, 9])
      for brow in brows:
        bcol = common.randint(0, inwidth - outwidth - 4)
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          grid[brow + dr][bcol + dc] = 8
          grid[brow + dr][bcol + 2 + outwidth + dc] = 8
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, solved = draw()
  if grid is None:
    return {"input": grid, "output": solved}

  # Bookkeeping (no frame): the bracket rows, ascending.  Each 88...88 pair
  # spans two consecutive rows, so the rows come in pairs and the k-th pair
  # feeds answer rows 2k and 2k+1.
  marker_rows = [row for row in range(inheight) if common.cyan() in grid[row]]

  # Stage 1 (input space): erase the noise, keeping only the bracket markers
  # and the window each pair encloses -- the cells that feed the answer.
  output = common.deepcopy(grid)

  def keep_brackets():
    """Blanks every cell except the 88 markers and their enclosed windows."""
    nonlocal output
    keep = set()
    for row in marker_rows:
      start = grid[row].index(common.cyan())
      for c in range(start, start + outwidth + 4):
        keep.add((row, c))
    for r in range(inheight):
      for c in range(inwidth):
        if (r, c) not in keep:
          output[r][c] = common.black()

  keep_brackets()

  # Rebind to the answer canvas, then read out one bracket pair's window per
  # frame (its two rows become answer rows 2k and 2k+1).
  output = common.grid(outwidth, outheight)

  def extract_pair(k):
    """Copies bracket pair k's two windows into answer rows 2k and 2k+1."""
    nonlocal output
    for j, row in enumerate(marker_rows[2 * k:2 * k + 2]):
      start = grid[row].index(common.cyan())
      for col in range(outwidth):
        output[2 * k + j][col] = grid[row][start + 2 + col]

  extract_pair(0)
  extract_pair(1)
  extract_pair(2)
  extract_pair(3)
  extract_pair(4)
  # CRITICAL GUARD: taller grids (inheight up to 28 -> segments up to 7) can
  # produce more than 5 bracket pairs; the five unrolled calls above only cover
  # k=0..4.  This catch-all extracts every remaining pair so no window is
  # silently dropped from the answer.
  for k in range(5, (len(marker_rows) + 1) // 2):
    extract_pair(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(inwidth=17, inheight=12, outwidth=5, outheight=6,
               colors=[9, 2, 1, 5, 3, 4, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 8, 8, 3, 0, 7, 0, 7, 8, 8, 4, 0, 7, 2, 0, 0, 0,
                       1, 8, 8, 0, 2, 0, 0, 6, 8, 8, 0, 0, 0, 0, 0, 7, 0,
                       1, 0, 0, 0, 0, 4, 1, 3, 9, 1, 0, 7, 5, 9, 4, 7, 0,
                       0, 0, 3, 2, 2, 0, 2, 6, 0, 4, 9, 2, 4, 0, 3, 0, 5,
                       0, 6, 8, 8, 3, 0, 1, 9, 2, 8, 8, 0, 3, 0, 4, 0, 0,
                       0, 0, 8, 8, 0, 7, 9, 2, 9, 8, 8, 0, 9, 3, 0, 0, 9,
                       0, 0, 0, 4, 0, 7, 5, 7, 5, 0, 1, 3, 0, 2, 0, 0, 0,
                       0, 0, 9, 9, 3, 6, 4, 0, 4, 7, 2, 0, 9, 0, 0, 9, 0,
                       9, 1, 9, 0, 0, 7, 1, 5, 7, 1, 0, 5, 0, 5, 9, 6, 9,
                       0, 0, 3, 7, 2, 0, 8, 8, 9, 0, 0, 0, 0, 8, 8, 1, 0,
                       6, 7, 0, 4, 0, 4, 8, 8, 0, 4, 0, 2, 0, 8, 8, 5, 0]),
      generate(inwidth=15, inheight=12, outwidth=4, outheight=2,
               colors=[0, 4, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 0, 0, 7, 9, 0, 7, 7, 0, 0, 1, 3, 0,
                       2, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 8, 8, 3, 5, 9, 1, 8, 8, 0, 2, 0,
                       0, 0, 0, 0, 8, 8, 1, 0, 0, 6, 8, 8, 3, 0, 0,
                       2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 9, 2, 0, 0, 2,
                       0, 0, 9, 0, 4, 9, 9, 9, 0, 2, 9, 6, 1, 4, 0,
                       0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 0, 0, 0, 0, 5,
                       1, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 5, 0, 6, 0,
                       2, 1, 0, 0, 6, 0, 6, 2, 7, 0, 4, 0, 0, 0, 7,
                       0, 9, 0, 0, 2, 0, 5, 0, 1, 0, 0, 0, 0, 5, 3,
                       4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0]),
      generate(inwidth=10, inheight=12, outwidth=6, outheight=2,
               colors=[9, 0, 0, 5, 0, 0, 0, 0, 4, 4,
                       9, 4, 0, 0, 0, 0, 0, 0, 5, 0,
                       2, 2, 0, 6, 0, 0, 5, 0, 5, 3,
                       2, 9, 0, 2, 6, 4, 0, 1, 0, 0,
                       0, 0, 2, 9, 0, 4, 9, 1, 1, 3,
                       8, 8, 1, 0, 9, 7, 7, 0, 8, 8,
                       8, 8, 4, 0, 0, 5, 6, 4, 8, 8,
                       0, 5, 9, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 0, 5, 0, 0, 3, 0,
                       0, 9, 0, 0, 0, 0, 0, 7, 0, 9,
                       0, 0, 5, 1, 7, 0, 0, 0, 9, 9,
                       0, 0, 9, 0, 0, 1, 0, 0, 0, 7]),
      generate(inwidth=16, inheight=13, outwidth=3, outheight=4,
               colors=[0, 7, 2, 7, 0, 2, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 6, 0, 0, 2, 0, 0, 7, 3, 1,
                       0, 0, 8, 8, 6, 5, 2, 8, 8, 1, 0, 2, 4, 5, 0, 0,
                       0, 0, 8, 8, 0, 0, 2, 8, 8, 0, 0, 7, 1, 0, 0, 7,
                       0, 0, 0, 0, 4, 0, 0, 0, 9, 0, 7, 0, 0, 0, 0, 0,
                       8, 8, 1, 3, 0, 8, 8, 0, 0, 0, 0, 9, 0, 3, 0, 1,
                       8, 8, 0, 0, 9, 8, 8, 0, 0, 0, 0, 0, 3, 0, 9, 2,
                       0, 0, 7, 0, 0, 0, 0, 0, 0, 9, 3, 4, 0, 0, 0, 0,
                       4, 0, 0, 9, 0, 9, 0, 0, 7, 3, 0, 6, 0, 4, 0, 5,
                       6, 0, 0, 0, 4, 0, 0, 3, 0, 0, 2, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 0, 4, 0, 0, 0, 0,
                       4, 5, 0, 0, 6, 0, 4, 0, 0, 0, 0, 0, 5, 2, 0, 2,
                       0, 9, 0, 6, 0, 0, 0, 7, 2, 0, 9, 3, 0, 0, 0, 6]),
      generate(inwidth=17, inheight=13, outwidth=5, outheight=4,
               colors=[0, 2, 0, 0, 0, 0, 4, 5, 0, 0, 1, 0, 6, 5, 0, 0, 0,
                       9, 0, 4, 3, 0, 0, 9, 0, 4, 7, 9, 4, 6, 0, 2, 7, 0,
                       0, 7, 3, 0, 0, 0, 9, 0, 0, 9, 0, 0, 9, 9, 9, 5, 0,
                       0, 5, 5, 3, 0, 3, 0, 6, 0, 4, 7, 2, 3, 2, 0, 3, 0,
                       0, 8, 8, 0, 0, 0, 7, 0, 8, 8, 9, 0, 0, 6, 0, 0, 4,
                       0, 8, 8, 6, 4, 3, 1, 9, 8, 8, 0, 0, 0, 0, 0, 0, 7,
                       9, 0, 0, 9, 5, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1,
                       0, 2, 9, 9, 0, 0, 9, 0, 7, 1, 0, 0, 0, 9, 0, 0, 0,
                       0, 7, 0, 8, 8, 0, 4, 0, 6, 0, 8, 8, 9, 0, 0, 0, 0,
                       0, 2, 4, 8, 8, 0, 3, 0, 0, 6, 8, 8, 6, 5, 7, 9, 0,
                       0, 0, 9, 2, 0, 2, 0, 0, 0, 7, 9, 0, 0, 0, 5, 7, 1,
                       1, 0, 0, 3, 0, 1, 0, 4, 1, 4, 0, 0, 0, 0, 1, 0, 9,
                       1, 0, 6, 2, 1, 4, 6, 0, 0, 1, 9, 0, 3, 0, 1, 4, 0]),
  ]
  test = [
      generate(inwidth=17, inheight=15, outwidth=4, outheight=8,
               colors=[0, 0, 6, 9, 0, 0, 0, 9, 0, 0, 7, 0, 9, 0, 0, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 4, 4, 0, 9, 0, 0, 0, 0, 0, 2, 0, 1, 0, 5, 1,
                       2, 1, 0, 8, 8, 4, 1, 5, 0, 8, 8, 0, 1, 0, 4, 0, 0,
                       0, 7, 3, 8, 8, 0, 9, 0, 0, 8, 8, 0, 6, 0, 4, 7, 2,
                       2, 5, 0, 4, 0, 0, 0, 0, 7, 9, 0, 9, 5, 0, 4, 0, 1,
                       8, 8, 5, 9, 0, 4, 8, 8, 4, 0, 3, 7, 0, 0, 0, 0, 5,
                       8, 8, 7, 7, 0, 0, 8, 8, 6, 4, 7, 0, 6, 0, 0, 0, 4,
                       0, 6, 9, 0, 4, 0, 0, 3, 0, 9, 0, 3, 0, 0, 0, 3, 4,
                       0, 5, 2, 0, 0, 0, 0, 2, 9, 0, 0, 6, 0, 4, 5, 0, 0,
                       0, 7, 0, 3, 8, 8, 4, 5, 4, 3, 8, 8, 9, 5, 0, 3, 0,
                       0, 0, 0, 0, 8, 8, 0, 0, 7, 0, 8, 8, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 5, 0,
                       0, 9, 2, 0, 0, 0, 9, 8, 8, 0, 0, 6, 0, 8, 8, 0, 6,
                       0, 0, 0, 9, 0, 0, 0, 8, 8, 0, 7, 0, 4, 8, 8, 0, 0]),
  ]
  return {"train": train, "test": test}
