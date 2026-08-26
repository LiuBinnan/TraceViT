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


def generate(rows=None, cols=None, size=9, height=None, width=None,
             count=None, orange_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: the number of cyan clue pixels
    orange_count: the number of orange clue pixels
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    max_count = max(1, min(3, (height * width) // 144))
    if count is None:
      count = common.randint(1, max_count)
    if orange_count is None:
      orange_count = common.randint(1, max_count)
    count = min(count, max_count)
    orange_count = min(orange_count, max_count)
    cells = [(r, c) for r in range(height) for c in range(width)]

    def far_enough(cell, placed):
      r, c = cell
      return all(abs(r - pr) > 1 or abs(c - pc) > 1 for pr, pc in placed)

    total_count = count + orange_count
    pixels = []
    for _ in range(100):
      pixels = []
      for cell in common.sample(cells, len(cells)):
        if far_enough(cell, pixels):
          pixels.append(cell)
          if len(pixels) == total_count:
            break
      if len(pixels) == total_count:
        break
    if len(pixels) < total_count:
      pixels = []
      for cell in cells:
        if far_enough(cell, pixels):
          pixels.append(cell)
          if len(pixels) == total_count:
            break
    if len(pixels) < total_count:
      pixels = common.sample(cells, total_count)
    cyan_pixels = pixels[:count]
    orange_pixels = pixels[count:]
  else:
    cyan_pixels = [(rows[0], cols[0])]
    orange_pixels = [(rows[1], cols[1])]

  grid, output = common.grids(width, height)
  for r, c in cyan_pixels:
    grid[r][c] = common.cyan()
  for r, c in orange_pixels:
    grid[r][c] = common.orange()
  cyan_rows = {r for r, _ in cyan_pixels}
  cyan_cols = {c for _, c in cyan_pixels}
  orange_rows = {r for r, _ in orange_pixels}
  orange_cols = {c for _, c in orange_pixels}
  for r in range(height):
    for c in range(width):
      if r in cyan_rows or c in cyan_cols:
        output[r][c] = common.cyan()
  for r in range(height):
    for c in range(width):
      if r in orange_rows or c in orange_cols:
        output[r][c] = common.orange()
  for r in range(height):
    for c in range(width):
      if (r in cyan_rows or c in cyan_cols) and (
          r in orange_rows or c in orange_cols):
        output[r][c] = common.red()
  for r, c in cyan_pixels:
    output[r][c] = common.cyan()
  for r, c in orange_pixels:
    output[r][c] = common.orange()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 6], cols=[2, 6]),
      generate(rows=[1, 7], cols=[3, 6]),
  ]
  test = [
      generate(rows=[1, 6], cols=[4, 1]),
  ]
  return {"train": train, "test": test}
