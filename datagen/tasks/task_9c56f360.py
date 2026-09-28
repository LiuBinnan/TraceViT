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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
  """

  if width is None:
    while True:
      width = common.randint(5, 18)
      height = width + common.randint(0, 2) - 1
      while True:
        row, rows, talls = common.randint(0, 4), [], []
        while True:
          tall = common.randint(2, 4)
          if row + tall >= height: break
          rows.append(row)
          talls.append(tall)
          row += tall + common.randint(1, 2)
        if talls: break
      wides = [common.randint(1, 2) for _ in talls]
      while True:
        pixels = common.random_pixels(width, height)
        if pixels: break
      colors = [0] * (width * height)
      for pixel in pixels:
        r, c = pixel
        colors[r * width + c] = 8
      good = False  # at least one green strip should move left.
      for wide, tall, row in zip(wides, talls, rows):
        for r in range(row, row + tall):
          if colors[r * width + width - wide - 1] == 0: good = True
          for c in range(width - wide, width):
            colors[r * width + c] = 3
      if good: break

  # Input: azure (8) pixels scattered about, plus green (3) strips anchored at
  # the right edge of some rows.
  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color

  # A green strip in a row slides left across empty cells until its left edge
  # meets the nearest azure pixel (or the wall). Precompute each strip that can
  # move (its row, width, and the column it settles at).
  strips = []
  for row in range(height):
    col = width - 1
    if grid[row][col] != 3: continue
    left = col
    while left >= 0 and grid[row][left] == 3:
      left -= 1
    start_left = left + 1
    target = start_left
    while target - 1 >= 0 and grid[row][target - 1] == 0:
      target -= 1
    if target < start_left:
      strips.append((row, width - start_left, target))
  cur = [width - wide for row, wide, target in strips]

  # Solve forward: the strips slide left one cell per frame until each rests
  # against its azure stop (the topmost strip sets off first).
  output = common.deepcopy(grid)

  def move_strip(k):
    """Slides strip k one cell left toward its azure stop."""
    if k >= len(strips) or cur[k] <= strips[k][2]:
      return
    row, wide, target = strips[k]
    cur[k] -= 1
    for c in range(target, width):
      output[row][c] = common.black()
    for c in range(cur[k], cur[k] + wide):
      output[row][c] = common.green()

  def slide_all():
    """Every strip that has not yet settled slides one more cell left."""
    for k in range(len(strips)):
      move_strip(k)

  move_strip(0)
  slide_all()
  slide_all()
  slide_all()
  slide_all()
  slide_all()
  slide_all()
  slide_all()
  slide_all()
  for _ in range(8, width):
    slide_all()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=7, colors=[0, 0, 0, 8, 0, 0, 8, 3,
                                          0, 8, 0, 0, 8, 0, 0, 3,
                                          8, 8, 0, 8, 0, 0, 8, 3,
                                          8, 8, 0, 0, 0, 0, 0, 3,
                                          0, 0, 0, 8, 8, 0, 0, 8,
                                          8, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 8, 8, 8, 0, 0]),
      generate(width=6, height=7, colors=[0, 0, 0, 8, 0, 0,
                                          0, 0, 8, 0, 0, 8,
                                          8, 0, 0, 0, 0, 8,
                                          0, 0, 8, 0, 8, 0,
                                          0, 0, 0, 0, 3, 3,
                                          8, 0, 8, 0, 3, 3,
                                          0, 8, 0, 8, 8, 0]),
      generate(width=8, height=9, colors=[0, 0, 0, 0, 8, 8, 8, 8,
                                          0, 0, 0, 8, 0, 8, 3, 3,
                                          8, 0, 0, 8, 0, 0, 3, 3,
                                          8, 8, 0, 0, 0, 0, 3, 3,
                                          8, 8, 0, 0, 8, 8, 0, 8,
                                          0, 0, 0, 8, 0, 8, 0, 3,
                                          0, 8, 0, 0, 0, 0, 0, 3,
                                          0, 0, 0, 8, 8, 0, 8, 3,
                                          8, 0, 0, 8, 8, 8, 0, 8]),
  ]
  test = [
      generate(width=9, height=9, colors=[0, 8, 8, 8, 8, 8, 8, 0, 8,
                                          8, 8, 8, 0, 0, 8, 8, 0, 8,
                                          0, 8, 8, 0, 8, 8, 0, 0, 8,
                                          0, 8, 0, 0, 0, 0, 0, 3, 3,
                                          0, 8, 0, 8, 0, 0, 0, 3, 3,
                                          8, 0, 0, 0, 0, 0, 0, 3, 3,
                                          0, 0, 8, 0, 8, 8, 0, 3, 3,
                                          0, 8, 8, 8, 0, 0, 0, 0, 0,
                                          0, 8, 0, 8, 0, 8, 8, 8, 0]),
  ]
  return {"train": train, "test": test}
