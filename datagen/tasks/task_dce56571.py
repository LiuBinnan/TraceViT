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
    width: The width of the grids.
    height: The height of the grids.
    colors: The colors to use.
  """

  if width is None:
    width, height = common.randint(9, 30), 2 * common.randint(1, 6) + 1
    color = common.random_color(exclude=[8])
    while True:
      wide, tall = common.randint(3, width // 2), common.randint(3, height)
      pixels = []
      for row in range(tall):
        for col in range(wide):
          if common.randint(0, 1): pixels.append((row, col))
      if not pixels or not common.diagonally_connected(pixels): continue
      if len(pixels) % 2 == width % 2 and len(pixels) <= width: break
    grid = common.grid(width, height, 8)
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    for row in range(height):
      for col in range(width):
        if (row, col) in pixels: grid[brow + row][bcol + col] = color
    colors = common.flatten(grid)

  grid = common.grid(width, height, common.cyan())
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color

  # The answer is a centered bar whose length equals the count of colored
  # pixels. Build it as a running tally: scan the shape's filled rows top to
  # bottom, extending the bar by however many pixels each row contributes.
  hues = set(colors)
  hues.remove(8)
  hue = hues.pop()
  count = colors.count(hue)
  start = (width - count) // 2
  filled_rows = [r for r in range(height)
                 if any(grid[r][c] == hue for c in range(width))]
  chunk = [sum(1 for c in range(width) if grid[r][c] == hue) for r in filled_rows]
  offset = [0]
  for n in chunk:
    offset.append(offset[-1] + n)
  output = common.grid(width, height, common.cyan())

  def reveal_tally(j):
    """Extends the tally bar with the pixels counted in the j-th filled row."""
    if j >= len(chunk): return
    for k in range(chunk[j]):
      output[height // 2][start + offset[j] + k] = hue

  reveal_tally(0)
  reveal_tally(1)
  reveal_tally(2)
  reveal_tally(3)
  reveal_tally(4)
  reveal_tally(5)
  reveal_tally(6)
  reveal_tally(7)
  reveal_tally(8)
  reveal_tally(9)
  reveal_tally(10)
  for j in range(11, len(chunk)):
    reveal_tally(j)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=7,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 9, 9, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 9, 9, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 9, 9, 9, 8, 8, 8,
                       8, 8, 8, 8, 9, 8, 9, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(width=10, height=5,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 3, 8, 8, 8,
                       8, 8, 8, 8, 3, 3, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 3, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(width=15, height=9,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 8, 8,
                       8, 8, 8, 8, 8, 2, 8, 8, 2, 2, 8, 8, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 2, 8, 2, 2, 2, 8, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 2, 8, 8, 8, 2, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(width=28, height=11,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 5, 8, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
