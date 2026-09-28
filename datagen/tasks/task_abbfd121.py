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


def generate(width=None, height=None, size=None, wides=None, talls=None,
             brows=None, bcols=None, bcolors=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    size: The size of the pattern.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row offsets of the rectangles.
    bcols: The column offsets of the rectangles.
    bcolors: The colors of the rectangles.
    pattern: The pattern to use.
  """

  if width is None:
    width, height = common.randint(16, 28), common.randint(16, 28)
    size = common.randint(2, 5)
    colors = common.shuffle(list(range(10)))
    subset = [colors.pop() for _ in range(common.randint(3, 5))]
    pattern = common.choices(subset, size * size)
    # A small tile can come out solid-colored; resample until the texture
    # actually has a pattern to continue (else the puzzle is degenerate).
    while len(set(pattern)) < 2:
      pattern = common.choices(subset, size * size)
    bcolors = [colors.pop() for _ in range(common.randint(2, 4))]
    # Larger rectangles reach the grid edge for 2-3 boxes; a 4th box needs a
    # tighter per-box ceiling so the non-overlapping packing stays feasible.
    ncount = len(bcolors)
    wcap = (width // 2 + 1) if ncount >= 4 else min(16, width - 3)
    tcap = (height // 2 + 1) if ncount >= 4 else min(16, height - 3)
    while True:
      wides = sorted([common.randint(3, wcap) for _ in bcolors])
      talls = sorted([common.randint(3, tcap) for _ in bcolors])
      good = True
      for i in range(1, len(bcolors)):
        if wides[i] == wides[i - 1] and talls[i] == talls[i - 1]: good = False
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not good or common.overlaps(brows, bcols, wides, talls, 1): continue
      # Reject a degenerate puzzle: the reconstructed patch under the largest
      # rectangle must show >=2 texture colors (else the hidden texture is a
      # solid swatch with nothing to continue).
      window = {pattern[((brows[-1] + row) % size) * size
                        + ((bcols[-1] + col) % size)]
                for row in range(talls[-1]) for col in range(wides[-1])}
      if len(window) >= 2: break

  # Input: lay down the periodic texture, then occlude it with the rectangles.
  grid = common.grid(width, height)
  for row in range(height):
    for col in range(width):
      grid[row][col] = pattern[(row % size) * size + (col % size)]
  for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
    common.rect(grid, wide, tall, brow, bcol, bcolor)

  # Answer: reconstruct the texture hidden beneath the largest rectangle by
  # continuing its periodicity one tile-height band at a time.
  output = common.grid(wides[-1], talls[-1])

  def reveal_band(band):
    """Extends the periodic texture into this band of the answer's rows."""
    start = band * size
    if start >= talls[-1]: return
    for row in range(start, min(start + size, talls[-1])):
      for col in range(wides[-1]):
        output[row][col] = pattern[((brows[-1] + row) % size) * size
                                   + ((bcols[-1] + col) % size)]

  reveal_band(0)
  reveal_band(1)
  reveal_band(2)
  reveal_band(3)
  # Guard: a widened tall / small tile size can need more than 4 bands (up to
  # ceil(tall/size)); reveal every remaining band so the answer is never a
  # half-reconstructed strip.  A no-op when 4 bands already cover the box.
  for band in range(4, talls[-1]):
    reveal_band(band)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=22, size=4, wides=[6, 7], talls=[5, 7],
               brows=[8, 13], bcols=[3, 13], bcolors=[2, 1],
               pattern=[3, 3, 3, 3, 3, 4, 5, 6, 3, 5, 3, 5, 3, 6, 5, 4]),
      generate(width=19, height=23, size=3, wides=[6, 10], talls=[5, 10],
               brows=[18, 6], bcols=[13, 3], bcolors=[8, 3],
               pattern=[0, 0, 0, 1, 2, 2, 2, 1, 1]),
      generate(width=22, height=21, size=3, wides=[3, 6, 12], talls=[3, 6, 6],
               brows=[1, 6, 9], bcols=[16, 0, 9], bcolors=[3, 8, 2],
               pattern=[4, 4, 4, 4, 6, 5, 4, 5, 6]),
  ]
  test = [
      generate(width=22, height=23, size=3, wides=[5, 9, 9], talls=[6, 7, 8],
               brows=[2, 14, 4], bcols=[1, 2, 11], bcolors=[3, 9, 4],
               pattern=[8, 6, 7, 6, 7, 8, 7, 8, 6]),
  ]
  return {"train": train, "test": test}
