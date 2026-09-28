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


def generate(width=None, height=None, prow=None, pcol=None, drs=None, dcs=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prow: The row of the gray pixel.
    pcol: The column of the gray pixel.
    drs: The row offsets of the pixels.
    dcs: The column offsets of the pixels.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    def put(g, r, c, color):
      if r < 0 or r >= height or c < 0 or c >= width: return False
      g[r][c] = color
      return True
    for dr, dc, color in zip(drs, dcs, colors):
      if not put(output, prow - dr, pcol - dc, color): return None, None
      if not put(grid, prow + dr, pcol + dc, color): return None, None
    output[prow][pcol] = grid[prow][pcol] = 5
    return grid, output

  if width is None:
    while True:
      width, height = common.randint(3, 16), common.randint(3, 16)
      wide = common.randint(3, min(width, 7))
      tall_cap = 7 if wide <= 4 else (5 if wide == 5 else 4)
      tall = common.randint(3, min(height, tall_cap))
      prow = common.randint(0, height - tall)
      pcol = common.randint(0, width - wide)
      pixels = common.diagonally_connected_sprite(wide, tall, wide + tall)
      drs, dcs = zip(*pixels)
      subset = common.random_colors(common.randint(2, 4), exclude=[5])
      colors = common.choices(subset, len(pixels))
      r, c = pixels[0]
      drs, dcs = [dr - r for dr in drs], [dc - c for dc in dcs]
      prow, pcol = prow + tall - 1 - r, pcol + wide - 1 - c
      grid, _ = draw()
      if grid: break

  # Input: the colored sprite laid out around the gray pixel (draw() also builds
  # the reference output, which we rebuild forward below).
  grid, _ = draw()

  # Output: rotate the sprite 180 degrees about the gray pixel. Mark the pivot,
  # then point-reflect each color group through it (output pixel (prow-dr,
  # pcol-dc) is the reflection of input pixel (prow+dr, pcol+dc)).
  output = common.grid(width, height)
  palette = []
  for color in colors:
    if color not in palette:
      palette.append(color)

  def place_pivot():
    """Marks the gray pivot -- the center of the 180-degree rotation."""
    output[prow][pcol] = common.gray()

  def reflect_color(k):
    """Point-reflects every pixel of the k-th color through the pivot."""
    if k >= len(palette):
      return
    for dr, dc, color in zip(drs, dcs, colors):
      if color != palette[k]:
        continue
      r, c = prow - dr, pcol - dc
      if r == prow and c == pcol:
        continue  # the pivot stays gray
      if 0 <= r < height and 0 <= c < width:
        output[r][c] = color

  place_pivot()
  reflect_color(0)
  reflect_color(1)
  reflect_color(2)
  reflect_color(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, prow=1, pcol=1, drs=[-1, 0, 1, 1],
               dcs=[-1, -1, -1, 0], colors=[6, 2, 2, 1]),
      generate(width=9, height=7, prow=3, pcol=4, drs=[0, 0, 1, 1, 2, 2],
               dcs=[-2, -1, -2, -1, -3, -2], colors=[3, 2, 3, 3, 1, 4]),
      generate(width=9, height=9, prow=2, pcol=3, drs=[0, 0, 1, 1, 2],
               dcs=[-2, -1, -3, -2, -3], colors=[3, 3, 1, 1, 2]),
  ]
  test = [
      generate(width=9, height=9, prow=5, pcol=4, drs=[0, 1, 1, 1, 2, 2, 2, 3],
               dcs=[-4, -3, -2, -1, -3, -2, -1, -4],
               colors=[8, 3, 3, 2, 3, 2, 2, 1]),
  ]
  return {"train": train, "test": test}
