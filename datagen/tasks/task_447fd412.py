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
             brows=None, bcols=None, bmags=None, count=None, wide=None,
             tall=None, num_pixels=None, num_markers=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    bmags: a list of box magnifiers
    count: the number of sprite instances
    wide: the width of the base sprite
    tall: the height of the base sprite
    num_pixels: the number of pixels in the base sprite
    num_markers: the number of red marker pixels
  """
  if width is None:
    width = common.randint(12, 30)
  if height is None:
    height = common.randint(12, 30)

  if (rows is None or cols is None or colors is None or brows is None or
      bcols is None or bmags is None):
    if wide is None:
      wide = common.randint(1, 4)
    if tall is None:
      tall = common.randint(1, 4)
    if wide * tall < 3:
      if common.randint(0, 1):
        wide = common.randint(3, 4)
      else:
        tall = common.randint(3, 4)
    if num_pixels is None:
      num_pixels = common.randint(3, wide * tall)
    if num_markers is None:
      max_markers = num_pixels // 2 if num_pixels % 2 else num_pixels // 2 - 1
      num_markers = common.randint(1, max(1, max_markers))
    if count is None:
      by_cells = 1 + max(1, (width * height) // (4 * num_pixels))
      by_box = max(2, (width * height) // ((wide + 1) * (tall + 1)))
      count = common.randint(2, min(32, by_cells, by_box))
    # First, choose sprite magnifiers & locations.
    while True:
      max_bmag = min(3, max(1, width // wide), max(1, height // tall))
      if count > 10:
        max_bmag = 1
      elif count > 6:
        max_bmag = min(max_bmag, 2)
      bmags = [common.randint(1, max_bmag) for _ in range(count)]
      bmags[0] = 1  # First one should have no magnifier.
      wides = [bmag * wide for bmag in bmags]
      talls = [bmag * tall for bmag in bmags]
      brows, bcols = [], []
      for box_wide, box_tall in zip(wides, talls):
        spots = []
        for row in range(height - box_tall + 1):
          for col in range(width - box_wide + 1):
            if common.overlaps(brows + [row], bcols + [col],
                               wides[:len(brows)] + [box_wide],
                               talls[:len(brows)] + [box_tall], 1):
              continue
            spots.append((row, col))
        if not spots:
          break
        row, col = common.choice(spots)
        brows.append(row)
        bcols.append(col)
      if len(brows) == count:
        break
      count = max(2, count - 1)
    # Second, choose sprite contents.
    pixels = common.continuous_creature(num_pixels, wide, tall)
    rows, cols = zip(*pixels)
    colors = [common.blue()] * num_pixels
    for idx in common.sample(list(range(num_pixels)), num_markers):
      colors[idx] = common.red()

  grid, output = common.grids(width, height)
  for idx in range(len(bmags)):
    brow, bcol, bmag = brows[idx], bcols[idx], bmags[idx]
    for row, col, color in zip(rows, cols, colors):
      for dr in range(bmag):
        for dc in range(bmag):
          r, c = brow + row * bmag + dr, bcol + col * bmag + dc
          if idx and color == common.blue(): continue
          common.draw(grid, r, c, color)
  output = [row[:] for row in grid]

  def reveal_sprite(idx):
    if idx >= len(bmags):
      return
    stop = len(bmags) if idx == 3 else idx + 1
    for box_idx in range(idx, stop):
      brow, bcol, bmag = brows[box_idx], bcols[box_idx], bmags[box_idx]
      for row, col, color in zip(rows, cols, colors):
        for dr in range(bmag):
          for dc in range(bmag):
            r, c = brow + row * bmag + dr, bcol + col * bmag + dc
            common.draw(output, r, c, color)

  reveal_sprite(1)
  reveal_sprite(2)
  reveal_sprite(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=14, rows=[0, 0, 0, 0, 1, 2, 2, 2],
               cols=[0, 1, 2, 3, 2, 1, 2, 3], colors=[2, 1, 1, 2, 1, 1, 1, 1],
               brows=[2, 8], bcols=[1, 3], bmags=[1, 2]),
      generate(width=12, height=14, rows=[0, 1, 1, 1, 2, 3],
               cols=[1, 0, 1, 2, 1, 1], colors=[2, 1, 1, 1, 1, 2],
               brows=[3, 8, 9], bcols=[5, 1, 8], bmags=[1, 1, 1]),
      generate(width=12, height=14, rows=[0, 0, 0, 0],
               cols=[0, 1, 2, 3], colors=[1, 1, 1, 2],
               brows=[2, 7], bcols=[1, -2], bmags=[1, 3]),
  ]
  test = [
      generate(width=21, height=17, rows=[0, 1, 1, 2, 2, 2],
               cols=[0, 0, 2, 0, 1, 2], colors=[1, 1, 2, 1, 1, 1],
               brows=[2, 1, 5, 9], bcols=[2, 10, 11, 1], bmags=[1, 1, 3, 2]),
  ]
  return {"train": train, "test": test}
