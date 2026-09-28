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


def generate(bgcolor=None, fgcolor=None, rows=None, cols=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    bgcolor: The background color.
    fgcolor: The foreground color.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    gsize: The even height and width of the grid.
  """

  def draw():
    half = gsize // 2
    grid = common.grid(gsize, gsize, 8)
    for row, col in zip(rows, cols):
      grid[half - 1 - row][col] = grid[half + row][col] = bgcolor
    for row in range(1, gsize - 1):
      for col in range(1, gsize - 1):
        cyans = 0
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
          if grid[row + dr][col + dc] == 8: cyans += 1
        if not cyans: grid[row][col] = fgcolor
    if len(set(common.flatten(grid))) != 3: return None, None
    return grid, grid

  if bgcolor is None:
    if gsize is None: gsize = 2 * common.randint(6, 14)
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 7, 9], 2)
    bgcolor, fgcolor = colors[0], colors[1]
    half = gsize // 2
    max_blob_width = half - 1
    while True:
      length = common.randint(3, max_blob_width)
      start = common.randint(1, half - length)
      rows, cols = [], []
      for row in range(min(5 + (gsize - 16) // 2, half - 2)):
        for col in range(start, start + length):
          rows.append(row)
          cols.append(col)
        length += common.randint(-2, 2)
        if length < 1: break
        if length > max_blob_width: length = max_blob_width
        start += common.randint(-1, 1)
        if start < 1: start = 1
        if start + length > half: start = half - length
      grid, _ = draw()
      if grid: break
  elif gsize is None:
    gsize = 16

  grid, _ = draw()
  output = common.grid(gsize, gsize, 8) if grid is not None else None

  def invert_colors():
    # Swap the blob's outline and interior colors in place; cyan stays cyan.
    if grid is None: return
    for row in range(gsize):
      for col in range(gsize):
        if grid[row][col] == bgcolor: output[row][col] = fgcolor
        if grid[row][col] == fgcolor: output[row][col] = bgcolor

  def separate_halves():
    # Slide the top half rightward until it clears the bottom half's columns.
    if grid is None: return
    half = gsize // 2
    while True:
      done = True
      for col in range(gsize):
        if output[half - 1][col] != 8 and output[half][col] != 8:
          done = False
      if done: break
      for col in range(gsize - 1, 0, -1):
        for row in range(half):
          output[row][col] = output[row][col - 1]

  invert_colors()
  separate_halves()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(bgcolor=0, fgcolor=5, rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3],
               cols=[3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 4]),
      generate(bgcolor=1, fgcolor=2, rows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3],
               cols=[1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 3, 2]),
  ]
  test = [
      generate(bgcolor=4, fgcolor=9,
               rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[1, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 3, 4, 5]),
  ]
  return {"train": train, "test": test}
