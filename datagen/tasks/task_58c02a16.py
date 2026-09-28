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


def generate(wide=None, tall=None, mult=None, offset=None, colors=None,
             bcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the inner rectangle.
    tall: The height of the inner rectangle.
    mult: The multiplier for the inner rectangle.
    offset: The offset for the inner rectangle.
    colors: The colors of the inner rectangle.
    bcolor: The border color.
  """
  if wide is None:
    while True:
      wide, tall = common.randint(2, 4), common.randint(2, 4)
      mult, offset = common.randint(3, 7), common.randint(0, 2)
      if wide * mult + offset <= 29 and tall * mult + offset <= 29:
        break
    bcolor = common.random_color(exclude=[7])
    fcolor = common.random_color(exclude=[7, bcolor])
    while True:
      colors = [common.randint(0, 1) for _ in range(wide * tall)]
      if sum(colors) >= 2 and sum(colors) <= wide * tall - 2: break
    colors = [fcolor if color else -1 for color in colors]

  width = wide * mult + offset
  height = tall * mult + offset
  grid, output = common.grids(width, height, 7)
  for i, color in enumerate(colors):
    if color != -1:
      grid[i // wide][i % wide] = color
  common.hollow_rect(grid, wide + 2, tall + 2, -1, -1, bcolor)
  active_cells = [(r, c) for r in range(tall) for c in range(wide)
                  if colors[r * wide + c] != -1]
  active_set = set(active_cells)

  def expand_active_mask():
    for row in range(height):
      for col in range(width):
        if (row % tall, col % wide) in active_set:
          output[row][col] = bcolor

  def color_repeated_tiles():
    for row in range(height):
      for col in range(width):
        if (row % tall, col % wide) not in active_set:
          continue
        tile_r = (row // tall) % tall
        tile_c = (col // wide) % wide
        color = colors[tile_r * wide + tile_c]
        if color != -1:
          output[row][col] = color

  expand_active_mask()
  color_repeated_tiles()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=2, tall=2, mult=3, offset=1, colors=[3, -1, -1, 3],
               bcolor=4),
      generate(wide=3, tall=3, mult=3, offset=0,
               colors=[2, 2, -1, -1, 2, 2, 2, -1, -1], bcolor=8),
      generate(wide=2, tall=3, mult=4, offset=0,
               colors=[9, -1, -1, -1, -1, 9], bcolor=0),
  ]
  test = [
      generate(wide=3, tall=3, mult=5, offset=1,
               colors=[4, -1, 4, 4, 4, -1, 4, -1, 4], bcolor=5),
  ]
  return {"train": train, "test": test}
