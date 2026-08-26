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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             noise_count=None, marker_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    noise_count: the number of gray distractor cells to place
    marker_count: the number of red/green marker pairs to place
  """
  if rows is None or cols is None or colors is None:
    if width is None:
      width = common.randint(3, 30)
    if height is None:
      height = common.randint(3, 30)
    area = width * height
    if noise_count is None:
      noise_count = common.randint(0, max(1, area // 3))
    if marker_count is None:
      marker_count = common.randint(1, max(1, area // 20))
    noise_count = min(max(0, noise_count), max(1, area // 3))
    marker_count = min(max(1, marker_count), max(1, area // 20))
    bitmap, _ = common.grids(width, height)
    all_pixels = [(r, c) for r in range(height) for c in range(width)]
    for r, c in common.sample(all_pixels, noise_count):
      bitmap[r][c] = common.gray()
    for r, c in common.sample(all_pixels, marker_count):
      bitmap[r][c] = common.red()
      neighbors = []
      for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if common.get_pixel(bitmap, r + dr, c + dc) != -1:
          neighbors.append((r + dr, c + dc))
      nr, nc = common.choice(neighbors)
      bitmap[nr][nc] = common.green()
    eats = False
    for r in range(height):
      for c in range(width):
        if bitmap[r][c] != common.green(): continue
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
          if common.get_pixel(bitmap, r + dr, c + dc) == common.red():
            eats = True
    if not eats:
      bitmap[0][0] = common.red()
      bitmap[0][1] = common.green()
    # Extract pixels from the bitmap.
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid = common.grid(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  output, eaters = common.deepcopy(grid), []

  def consume_reds():
    for r, c, color in zip(rows, cols, colors):
      if color != common.red(): continue
      adjacent_eaters = []
      for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if common.get_pixel(grid, r + dr, c + dc) != common.green(): continue
        adjacent_eaters.append((r + dr, c + dc))
      if not adjacent_eaters: continue
      output[r][c] = common.black()
      eaters.extend(adjacent_eaters)

  def recolor_eaters():
    for r, c in eaters:
      output[r][c] = common.cyan()

  consume_reds()
  recolor_eaters()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 0, 2], cols=[0, 1, 1],
               colors=[3, 2, 5]),
      generate(width=6, height=7, rows=[0, 1, 1, 3, 3, 4, 5, 5],
               cols=[0, 2, 3, 1, 5, 1, 0, 3], colors=[5, 3, 2, 3, 2, 2, 5, 3]),
      generate(width=7, height=7, rows=[0, 1, 1, 2, 2, 2, 4, 5, 5, 5, 6],
               cols=[5, 0, 6, 0, 2, 3, 5, 0, 1, 5, 3],
               colors=[2, 3, 3, 5, 2, 3, 2, 3, 2, 3, 5]),
  ]
  test = [
      generate(width=9, height=7,
               rows=[0, 0, 1, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 6, 6],
               cols=[4, 8, 1, 6, 7, 1, 4, 8, 0, 3, 7, 0, 1, 5, 7],
               colors=[2, 5, 2, 3, 2, 3, 5, 2, 5, 2, 3, 5, 3, 5, 2]),
  ]
  return {"train": train, "test": test}
