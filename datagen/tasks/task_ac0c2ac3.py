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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  if size is None:
    # Widened band for the odd-square side. The generator marks one
    # DISTINCT-colored pixel per Chebyshev ring, so the ring count size//2+1 is
    # bounded by common.random_colors' 9-color palette (num<=9). Hence size<=17
    # (9 rings). A side of 29 is infeasible without changing the
    # distinct-color sampling semantics, so the band caps at 17.
    size = 2 * common.randint(2, 8) + 1
    rows, cols = [], []
    for radius in range(0, size // 2 + 1):
      options = []
      for r in range(size):
        for c in range(size):
          if max(abs(size // 2 - r), abs(size // 2 - c)) == radius:
            options.append((r, c))
      option = common.choice(options)
      rows.append(option[0])
      cols.append(option[1])
    colors = common.random_colors(len(rows))
    colors = [color if color != 7 else 0 for color in colors]

  # Input: scatter each colored pixel onto the orange background.
  grid, output = common.grids(size, size, 7)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color

  # Answer: each pixel names the color for its whole concentric square ring
  # (Chebyshev distance from the center); fill the rings from the center out.
  def ring_color(radius):
    for row, col, color in zip(rows, cols, colors):
      if max(abs(size // 2 - row), abs(size // 2 - col)) == radius:
        return color
    return 7

  # Consolidate the size//2+1 concentric rings into <=5 outward BANDS (one frame
  # per band, center-outward) so the solving narrative stays short even at the
  # widened size 17 (9 rings). Band width = ceil((size//2+1)/5); five unrolled
  # calls cover every ring (5*band >= ring count), so the fully-filled output is
  # byte-identical to revealing the rings one radius at a time.
  band = (size // 2 + 1 + 4) // 5

  def reveal_band(b):
    """Fills the b-th outward band of concentric square rings (center-out)."""
    lo, hi = b * band, (b + 1) * band - 1
    for r in range(size):
      for c in range(size):
        radius = max(abs(size // 2 - r), abs(size // 2 - c))
        if lo <= radius <= hi and radius <= size // 2:
          output[r][c] = ring_color(radius)

  reveal_band(0)
  reveal_band(1)
  reveal_band(2)
  reveal_band(3)
  reveal_band(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, rows=[1, 2, 4, 5, 8], cols=[3, 6, 4, 4, 7],
               colors=[4, 3, 8, 1, 0]),
      generate(size=7, rows=[0, 3, 3, 3], cols=[0, 1, 3, 4],
               colors=[5, 8, 2, 9]),
      generate(size=11, rows=[1, 2, 5, 6, 7, 10], cols=[6, 6, 5, 5, 5, 1],
               colors=[0, 1, 5, 9, 6, 8]),
  ]
  test = [
      generate(size=13, rows=[0, 3, 4, 5, 6, 10, 11],
               cols=[12, 8, 8, 5, 6, 5, 1], colors=[0, 1, 8, 5, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
