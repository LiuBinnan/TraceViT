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


def generate(rows=None, cols=None, colors=None, vanishes=None, brow=None,
             bcol=None, bsize=None, nblocks=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
    vanishes: Whether the pixel is vanishing.
    brow: The row of the vanishing box.
    bcol: The column of the vanishing box.
    bsize: The height and width of each block.
    nblocks: The number of block rows and columns.
  """

  if rows is None:
    if bsize is None:
      bsize = common.randint(4, 7)
    if nblocks is None:
      nblocks = common.randint(3, 5)
    nblocks = min(nblocks, 31 // (bsize + 1))
    max_pixels = min(max(4, bsize * bsize // 3), bsize * bsize - 2)
    while True:
      pixels = common.random_pixels(bsize, bsize, 0.28)
      if 4 <= len(pixels) <= max_pixels: break
    rows, cols = zip(*pixels)
    colors = common.choices([0, 2, 4, 6], len(pixels))
    while True:
      vanishes = [common.randint(0, 1) for _ in range(len(pixels))]
      if len(set(vanishes)) == 2: break
    brow = common.randint(0, nblocks - 1)
    bcol = common.randint(0, nblocks - 1)
  else:
    if bsize is None:
      bsize = 5
    if nblocks is None:
      nblocks = 5

  # Input: an array of green-bordered blocks, each tiling the base pixel pattern,
  # except the vanishing box which is missing its vanishing pixels.
  grid = common.grid(nblocks * (bsize + 1) - 1,
                     nblocks * (bsize + 1) - 1, common.cyan())
  for r in range(bsize, len(grid), bsize + 1):
    for c in range(len(grid[0])):
      grid[r][c] = common.green()
  for r in range(len(grid)):
    for c in range(bsize, len(grid[0]), bsize + 1):
      grid[r][c] = common.green()
  for row in range(nblocks):
    for col in range(nblocks):
      for r, c, color, vanish in zip(rows, cols, colors, vanishes):
        if row == brow and col == bcol and vanish: continue
        grid[row * (bsize + 1) + r][col * (bsize + 1) + c] = color

  output = common.deepcopy(grid)

  def isolate_odd_block():
    """Erases every block but the vanishing box (the odd one out)."""
    for row in range(nblocks):
      for col in range(nblocks):
        if row == brow and col == bcol: continue
        for r, c, color, vanish in zip(rows, cols, colors, vanishes):
          output[row * (bsize + 1) + r][col * (bsize + 1) + c] = common.cyan()

  def place_survivors():
    """Extracts the surviving pixels of the odd block onto the answer."""
    nonlocal output
    output = common.grid(bsize, bsize, common.cyan())
    for r, c, color, vanish in zip(rows, cols, colors, vanishes):
      if not vanish:
        output[r][c] = color

  def mark_vanished():
    """Fills the pixels missing from the odd block with blue."""
    for r, c, color, vanish in zip(rows, cols, colors, vanishes):
      if vanish:
        output[r][c] = common.blue()

  isolate_odd_block()
  place_survivors()
  mark_vanished()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2, 2, 2, 3, 4], cols=[2, 0, 2, 4, 0, 4],
               colors=[4, 0, 2, 2, 0, 4], vanishes=[0, 0, 1, 0, 1, 0], brow=2,
               bcol=4),
      generate(rows=[0, 0, 0, 2, 2, 4, 4], cols=[0, 2, 4, 0, 2, 2, 4],
               colors=[0, 2, 4, 4, 6, 0, 2], vanishes=[0, 1, 0, 0, 0, 1, 1],
               brow=2, bcol=1),
      generate(rows=[0, 0, 1, 2, 3, 4, 4], cols=[0, 2, 0, 1, 3, 0, 4],
               colors=[0, 4, 4, 2, 2, 0, 0], vanishes=[0, 1, 1, 1, 1, 0, 0],
               brow=4, bcol=2),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 3, 4, 4], cols=[0, 2, 1, 2, 4, 2, 0, 4],
               colors=[2, 2, 0, 0, 6, 4, 2, 4],
               vanishes=[0, 0, 1, 1, 1, 0, 0, 0], brow=1, bcol=3),
  ]
  return {"train": train, "test": test}
