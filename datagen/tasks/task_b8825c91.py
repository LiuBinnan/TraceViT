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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None, size=8,
             count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates for the cutouts
    cols: a list of horizontal coordinate for the cutouts
    wides: a list of widths of the cutouts
    talls: a list of heights of the cutouts
    colors: a list of colors to be used
    size: the width and height of one quarter of the grid
    count: number of cells in the source pattern
    num_colors: number of source-pattern colors to sample
  """
  if rows is None:
    full_size = True
    # TODO: Make sure we don't cut out the center.
    if count is None:
      count = common.randint(1, size * size)
    if num_colors is None:
      num_colors = common.randint(1, 8)
    count = max(1, min(size * size, count))
    legal_colors = [
        common.black(), common.blue(), common.red(), common.green(),
        common.gray(), common.pink(), common.orange(), common.cyan(),
        common.maroon()]
    background = common.choice(legal_colors)
    palette = common.sample(
        [color for color in legal_colors if color != background],
        min(num_colors, 8))
    cutout_size = max(1, size // 2)
    wides = [common.randint(1, cutout_size) for _ in range(2)]
    talls = [common.randint(1, cutout_size) for _ in range(2)]
    rows = [common.randint(0, cutout_size - tall) for tall in talls]
    cols = [common.randint(0, cutout_size - wide) for wide in wides]
    bitmap = common.grid(size, size, background)
    pixels = common.all_pixels(size, size)
    source = common.sample(pixels, count)
    for idx, (row, col) in enumerate(source):
      color = palette[idx % len(palette)]
      for rr, cc in [
          (row, col),
          (col, row),
          (row, size - col - 1),
          (size - col - 1, row),
          (size - row - 1, col),
          (col, size - row - 1),
          (size - row - 1, size - col - 1),
          (size - col - 1, size - row - 1)]:
        bitmap[rr][cc] = color
    colors = []
    for r in bitmap:
      colors.extend(r)

  target = common.grid(size if "full_size" in locals() else 2 * size,
                       size if "full_size" in locals() else 2 * size,
                       common.yellow())
  if "full_size" in locals():
    for r in range(size):
      for c in range(size):
        target[r][c] = colors[r * size + c]
  else:
    for r in range(size):
      for c in range(size):
        color = colors[r * size + c]
        target[r][c] = target[2 * size - r - 1][2 * size - c - 1] = color
        target[r][2 * size - c - 1] = target[2 * size - r - 1][c] = color
  grid = [row[:] for row in target]
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(tall):
      for c in range(wide):
        grid[row + r][col + c] = common.yellow()
  output = [row[:] for row in grid]
  cutouts = list(zip(rows, cols, wides, talls))

  def restore_cutout(cutout_idx):
    if cutout_idx >= len(cutouts):
      return
    row, col, wide, tall = cutouts[cutout_idx]
    for r in range(tall):
      for c in range(wide):
        output[row + r][col + c] = target[row + r][col + c]

  restore_cutout(0)
  restore_cutout(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[5, 10], cols=[10, 10], wides=[4, 3], talls=[3, 4],
               colors=[9, 9, 6, 5, 9, 6, 7, 7, 9, 1, 5, 5, 6, 1, 7, 9, 6, 5, 1,
                       9, 7, 7, 3, 3, 5, 5, 9, 3, 7, 9, 3, 3, 9, 6, 7, 7, 3, 8,
                       9, 1, 6, 1, 7, 9, 8, 3, 1, 1, 7, 7, 3, 3, 9, 1, 6, 6, 7,
                       9, 3, 3, 1, 1, 6, 1]),
      generate(rows=[2, 8], cols=[1, 11], wides=[2, 3], talls=[3, 2],
               colors=[9, 9, 6, 1, 8, 9, 6, 6, 9, 6, 1, 3, 9, 6, 6, 1, 6, 1, 5,
                       2, 6, 6, 8, 8, 1, 3, 2, 8, 6, 1, 8, 2, 8, 9, 6, 6, 7, 1,
                       5, 5, 9, 6, 6, 1, 1, 1, 5, 5, 6, 6, 8, 8, 5, 5, 9, 5, 6,
                       1, 8, 2, 5, 5, 5, 8]),
      generate(rows=[6, 11], cols=[12, 2], wides=[2, 4], talls=[4, 4],
               colors=[9, 3, 9, 9, 2, 8, 7, 8, 3, 9, 9, 3, 8, 8, 8, 5, 9, 9, 2,
                       8, 7, 8, 2, 2, 9, 3, 8, 8, 8, 5, 2, 1, 2, 8, 7, 8, 2, 5,
                       9, 7, 8, 8, 8, 5, 5, 5, 7, 6, 7, 8, 2, 2, 9, 7, 1, 1, 8,
                       5, 2, 1, 7, 6, 1, 3]),
      generate(rows=[1, 8], cols=[10, 3], wides=[4, 2], talls=[3, 3],
               colors=[2, 2, 7, 6, 8, 9, 9, 1, 2, 1, 6, 2, 9, 5, 1, 1, 7, 6, 3,
                       3, 9, 1, 6, 6, 6, 2, 3, 8, 1, 1, 6, 6, 8, 9, 9, 1, 1, 7,
                       1, 1, 9, 5, 1, 1, 7, 7, 1, 3, 9, 1, 6, 6, 1, 1, 3, 3, 1,
                       1, 6, 6, 1, 3, 3, 2]),
  ]
  test = [
      generate(rows=[2, 4], cols=[6, 10], wides=[3, 4], talls=[3, 4],
               colors=[7, 7, 8, 1, 9, 8, 2, 6, 7, 1, 1, 8, 8, 8, 6, 6, 8, 1, 6,
                       9, 2, 6, 6, 1, 1, 8, 9, 1, 6, 6, 1, 1, 9, 8, 2, 6, 8, 7,
                       6, 6, 8, 8, 6, 6, 7, 7, 6, 5, 2, 6, 6, 1, 6, 6, 5, 5, 6,
                       6, 1, 1, 6, 5, 5, 7]),
  ]
  return {"train": train, "test": test}
