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


def generate(wides=None, talls=None, brows=None, bcols=None, cdirs=None,
             thicks=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    cdirs: The directions of the boxes.
    thicks: The thicknesses of the boxes.
    colors: A list of colors.
    gsize: The side length of the (square) canvas.
  """

  if wides is None:
    if gsize is None:
      gsize = common.randint(10, 28)
    size_hi = min(12, gsize - 2)
    num_boxes = common.randint(1, 3)
    while True:
      ok = False
      for _ in range(400):
        wides = [common.randint(4, size_hi) for _ in range(num_boxes)]
        talls = [common.randint(4, size_hi) for _ in range(num_boxes)]
        brows = [common.randint(0, gsize - tall) for tall in talls]
        bcols = [common.randint(0, gsize - wide) for wide in wides]
        if not common.overlaps(brows, bcols, wides, talls, 1):
          ok = True
          break
      if ok: break
      num_boxes -= 1
    while True:
      cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
      if len(set(cdirs)) >= min(num_boxes, 2): break
    thicks = []
    for wide, tall, cdir in zip(wides, talls, cdirs):
      if cdir == 1 and tall % 2 == 1:
        thicks.append(1)
      elif cdir == 0 and wide % 2 == 1:
        thicks.append(1)
      else:
        thicks.append(common.randint(1, 2))
    colors = []
    for wide, tall, cdir, thick in zip(wides, talls, cdirs, thicks):
      subset = common.random_colors(3, exclude=[5])
      num_colors = thick * ((wide - 1) if cdir == 1 else (tall - 1))
      colors.extend(common.choices(subset, num_colors))

  if gsize is None:
    gsize = 10

  # Input: each box shows a seed line (color 5) plus a single `thick`-wide
  # period of the color pattern next to it (the leftmost columns for a
  # horizontal seed, the bottom rows for a vertical seed).
  grid = common.grid(gsize, gsize)
  offset = 0
  for wide, tall, brow, bcol, cdir, thick in zip(wides, talls, brows, bcols, cdirs, thicks):
    if cdir:
      for row in range(tall):
        grid[brow + row][bcol] = 5
        for col in range(1, wide):
          color = colors[offset + (row % thick) * (wide - 1) + col - 1]
          if row < thick: grid[brow + tall - 1 - row][bcol + col] = color
      offset += (wide - 1) * thick
    else:
      for col in range(wide):
        grid[brow][bcol + col] = 5
        for row in range(1, tall):
          color = colors[offset + (col % thick) * (tall - 1) + row - 1]
          if col < thick: grid[brow + row][bcol + col] = color
      offset += (tall - 1) * thick

  # Solve forward: fill in each box completely, one box per stage. For a box we
  # tile its seed period across the whole box, extending away from the seed line
  # (rightward for a horizontal seed, upward for a vertical seed) until full.
  output = common.deepcopy(grid)

  def tile_box(i):
    """Tiles box i's entire remaining pattern (all periods past the seed) at once."""
    nonlocal output
    off = 0
    for j in range(i):
      off += (wides[j] - 1) * thicks[j] if cdirs[j] else (talls[j] - 1) * thicks[j]
    wide, tall, brow, bcol, cdir, thick = (
        wides[i], talls[i], brows[i], bcols[i], cdirs[i], thicks[i])
    if cdir:
      for row in range(thick, tall):
        for col in range(1, wide):
          output[brow + tall - 1 - row][bcol + col] = colors[off + (row % thick) * (wide - 1) + col - 1]
    else:
      for col in range(thick, wide):
        for row in range(1, tall):
          output[brow + row][bcol + col] = colors[off + (col % thick) * (tall - 1) + row - 1]

  if len(wides) >= 1: tile_box(0)
  if len(wides) >= 2: tile_box(1)
  if len(wides) >= 3: tile_box(2)
  for i in range(3, len(wides)):
    tile_box(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[6], talls=[7], brows=[1], bcols=[1], cdirs=[0],
               thicks=[1], colors=[2, 1, 2, 6, 1, 1]),
      generate(wides=[7], talls=[8], brows=[1], bcols=[0], cdirs=[1],
               thicks=[2], colors=[7, 3, 7, 7, 3, 3, 4, 3, 3, 4, 4, 4]),
      generate(wides=[4, 5], talls=[7, 8], brows=[0, 1], bcols=[6, 0],
               cdirs=[0, 1], thicks=[1, 2],
               colors=[3, 3, 7, 3, 7, 7, 2, 2, 2, 2, 6, 3, 6, 3]),
      generate(wides=[7], talls=[4], brows=[2], bcols=[2], cdirs=[1],
               thicks=[1], colors=[6, 6, 6, 9, 9, 9]),
  ]
  test = [
      generate(wides=[5, 4], talls=[6, 8], brows=[1, 1], bcols=[0, 6],
               cdirs=[0, 1], thicks=[1, 2],
               colors=[4, 2, 2, 2, 1, 3, 3, 3, 8, 6, 8]),
  ]
  return {"train": train, "test": test}
