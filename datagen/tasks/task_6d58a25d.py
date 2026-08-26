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


def generate(rows=None, cols=None, row=None, col=None, color=None, kite=None,
             size=20, height=None, width=None, noise_count=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical coordinates where the kite should be placed
    col: a horizontal coordinates where the kite should be placed
    color: a digit representing a color for the pixels
    kite: a digit representing a color for the kite
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    noise_count: the number of non-kite pixels to sample
    density: the percentage of non-kite cells to sample as noise
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    while True:
      row = common.randint(0, height - 4)
      col = common.randint(3, width - 4)
      kite_pixels = [
          (row, col), (row + 1, col - 1), (row + 1, col),
          (row + 1, col + 1), (row + 2, col - 2), (row + 2, col - 1),
          (row + 2, col + 1), (row + 2, col + 2), (row + 3, col - 3),
          (row + 3, col + 3)
      ]
      candidates = [
          (r, c) for r in range(height) for c in range(width)
          if (r, c) not in kite_pixels
      ]
      max_noise = max(1, len(candidates) // 2 - 1)
      if noise_count is None:
        if density is None:
          nnoise = common.randint(1, max_noise)
        else:
          nnoise = len(candidates) * density // 100
      else:
        nnoise = noise_count
      nnoise = min(max(1, nnoise), max_noise)
      pixels = common.sample(candidates, nnoise)
      pixel_set = set(pixels)
      active = False
      for r, c in pixels:
        if (r, c) in kite_pixels:
          continue
        kite_rows = [kr for kr, kc in kite_pixels if kc == c and kr <= r]
        if not kite_rows:
          continue
        bottom = max(kite_rows)
        if any((rr, c) not in pixel_set for rr in range(bottom + 1, height)):
          active = True
      if active:
        break
    rows, cols = zip(*pixels)
    colors = common.random_colors(2)
    color, kite = colors[0], colors[1]

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = color
  output[row][col] = grid[row][col] = kite
  output[row + 1][col - 1] = grid[row + 1][col - 1] = kite
  output[row + 1][col] = grid[row + 1][col] = kite
  output[row + 1][col + 1] = grid[row + 1][col + 1] = kite
  output[row + 2][col - 2] = grid[row + 2][col - 2] = kite
  output[row + 2][col - 1] = grid[row + 2][col - 1] = kite
  output[row + 2][col + 1] = grid[row + 2][col + 1] = kite
  output[row + 2][col + 2] = grid[row + 2][col + 2] = kite
  output[row + 3][col - 3] = grid[row + 3][col - 3] = kite
  output[row + 3][col + 3] = grid[row + 3][col + 3] = kite
  def kite_above(r, c):
    if grid[r][c] == kite: return False  # edge case (we're inside the kite!)
    while r >= 0:
      if grid[r][c] == kite: return True
      r -= 1
    return False

  active_cols = []
  for r, c in zip(rows, cols):
    if kite_above(r, c) and c not in active_cols and len(active_cols) < 20:
      active_cols.append(c)

  def fill_column(idx):
    if idx >= len(active_cols):
      return
    c = active_cols[idx]
    r = height - 1
    while output[r][c] != kite:
      output[r][c] = color
      r -= 1

  fill_column(0)
  fill_column(1)
  fill_column(2)
  fill_column(3)
  fill_column(4)
  fill_column(5)
  fill_column(6)
  fill_column(7)
  fill_column(8)
  fill_column(9)
  fill_column(10)
  fill_column(11)
  fill_column(12)
  fill_column(13)
  fill_column(14)
  fill_column(15)
  fill_column(16)
  fill_column(17)
  fill_column(18)
  fill_column(19)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 3, 4, 10, 10, 13, 18, 19],
               cols=[5, 16, 3, 1, 18, 9, 15, 1], row=5, col=9, color=8, kite=9),
      generate(rows=[1, 2, 4, 4, 9, 10, 10, 12, 14, 17, 18],
               cols=[8, 2, 13, 16, 17, 1, 9, 6, 16, 14, 1], row=5, col=7,
               color=2, kite=7),
      generate(rows=[1, 2, 2, 4, 5, 5, 7, 9, 10, 12, 12, 12, 12, 15, 16, 17, 17,
                     18, 18, 18],
               cols=[14, 5, 10, 1, 7, 18, 4, 10, 2, 0, 7, 13, 18, 4, 12, 1, 16,
                     7, 13, 19],
               row=4, col=12, color=3, kite=4),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 3, 5, 5, 7, 7, 8, 8, 10, 12, 12, 12, 14, 16,
                     16, 18, 19],
               cols=[4, 10, 18, 11, 2, 13, 18, 7, 16, 0, 4, 5, 1, 11, 16, 18,
                     7, 14, 17, 10],
               row=3, col=6, color=6, kite=1),
  ]
  return {"train": train, "test": test}
