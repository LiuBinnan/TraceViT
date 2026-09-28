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


def generate(width=None, height=None, wide=None, tall=None, line=None,
             bcol=None, flip=None, xpose=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wide: The width of the connected sprite.
    tall: The height of the connected sprite.
    line: The row of the dividing line.
    bcol: The starting column of the connected sprite.
    flip: Whether to flip the input grid.
    xpose: Whether to transpose the input grid.
    colors: The colors of the connected sprite.
  """

  if width is None:
    wide, tall = common.randint(3, 5), common.randint(3, 5)
    width = common.randint(7, 18)
    height = 2 * tall + 3 + common.randint(0, 7)
    line = common.randint(tall + 1, height - tall - 2)
    bcol = common.randint(1, width - 1 - wide)
    pixels = common.diagonally_connected_sprite(wide, tall, wide + tall)
    hues = common.random_colors(2, exclude=[1])
    while True:
      colors = [0] * (width * height)
      for r in range(tall):
        for c in range(wide):
          if (r, c) in pixels: colors[r * wide + c] = common.choice(hues)
      if len(set(colors)) == 3: break
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(width, height)
  for c in range(width):
    grid[line][c] = 1
  hues = list(set(colors))
  hues.remove(0)
  for i, color in enumerate(colors):
    if not color: continue
    grid[line - 1 - tall + i // wide][bcol + i % wide] = color
  if flip: grid = common.flip(grid)
  if xpose: grid = common.transpose(grid)
  output = common.grid(len(grid[0]), len(grid))

  def find_divider():
    for r, row in enumerate(grid):
      if all(color == 1 for color in row):
        return r, None
    for c in range(len(grid[0])):
      if all(row[c] == 1 for row in grid):
        return None, c

  def sprite_pixels():
    pixels = []
    for r, row in enumerate(grid):
      for c, color in enumerate(row):
        if color not in [0, 1]:
          pixels.append((r, c, color))
    return pixels

  def opposite(color):
    return hues[0] if color == hues[1] else hues[1]

  def draw_divider():
    div_row, div_col = find_divider()
    if div_row is not None:
      for c in range(len(output[0])):
        output[div_row][c] = 1
    else:
      for r in range(len(output)):
        output[r][div_col] = 1

  def recolor_source_sprite():
    for r, c, color in sprite_pixels():
      output[r][c] = opposite(color)

  def mirror_original_sprite():
    div_row, div_col = find_divider()
    for r, c, color in sprite_pixels():
      if div_row is not None:
        output[2 * div_row - r][c] = color
      else:
        output[r][2 * div_col - c] = color

  draw_divider()
  recolor_source_sprite()
  mirror_original_sprite()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, wide=3, tall=3, line=5, bcol=2, flip=1,
               xpose=1, colors=[8, 4, 8, 0, 8, 8, 8, 0, 8]),
      generate(width=9, height=12, wide=4, tall=3, line=4, bcol=2, flip=0,
               xpose=0, colors=[0, 2, 0, 2, 2, 3, 2, 2, 0, 0, 2, 0]),
      generate(width=11, height=14, wide=4, tall=3, line=5, bcol=2, flip=1,
               xpose=0, colors=[6, 0, 0, 6, 6, 6, 6, 6, 5, 6, 6, 5]),
  ]
  test = [
      generate(width=14, height=16, wide=4, tall=5, line=8, bcol=3, flip=0,
               xpose=1,
               colors=[0, 0, 0, 8, 2, 8, 2, 8, 0, 8, 0, 8, 0, 8, 0, 0, 2, 8, 2, 0]),
  ]
  return {"train": train, "test": test}
