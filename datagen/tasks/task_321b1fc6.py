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


def generate(rows=None, cols=None, colors=None, megarows=None, megacols=None,
             size=10, num_boxes=4, height=None, width=None, count=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates for pixels in a sprite
    cols: a list of horizontal coordinates for pixels in a sprite
    colors: digits representing the colors to be used
    megarows: a list of vertical coordinates for the sprite locations
    megacols: a list of horizontal coordinates for the sprite locations
    size: the width and height of the (square) grid
    num_boxes: the number of boxes to be placed
    height: the height (number of rows) of the grid
    width: the width (number of columns) of the grid
    count: optional target number of sprite copies, including the original
    num_colors: optional number of non-cyan colors used in the original sprite
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    while True:
      while True:
        spritew, spriteh = common.randint(2, 5), common.randint(2, 5)
        if height >= 2 * spriteh + 1 or width >= 2 * spritew + 1:
          break
      all_pixels = common.all_pixels(spritew, spriteh)
      num_pixels = len(all_pixels)
      num_sampled = common.randint(num_pixels // 2, num_pixels)
      while True:
        pixels = common.sample(all_pixels, num_sampled)
        if common.connected(pixels): break
      max_boxes_by_bg = (height * width + len(pixels) - 1) // (2 * len(pixels))
      if max_boxes_by_bg >= 2:
        break
    rows, cols = zip(*pixels)
    max_colors = min(8, len(pixels))
    if num_colors is None:
      num_colors = common.randint(2, max_colors)
    num_colors = max(2, min(num_colors, max_colors))
    color_list = common.random_colors(num_colors, exclude=[common.cyan()])
    colors = common.shuffle(color_list + common.choices(
        color_list, k=len(pixels) - len(color_list)))
    if count is None:
      max_clones = max(1, (height * width) // (spritew * spriteh) // 2)
      num_boxes = common.randint(2, min(max_clones + 1, max_boxes_by_bg))
    else:
      num_boxes = min(max(2, count), max_boxes_by_bg)
    candidates = [(r, c) for r in range(height - spriteh + 1)
                  for c in range(width - spritew + 1)]
    megarows, megacols = [], []
    while candidates and len(megarows) < num_boxes:
      idx = common.randint(0, len(candidates) - 1)
      row, col = candidates.pop(idx)
      megarows.append(row)
      megacols.append(col)
      candidates = [
          (r, c) for r, c in candidates
          if not common.overlaps(
              megarows + [r], megacols + [c],
              [spritew] * (len(megarows) + 1),
              [spriteh] * (len(megarows) + 1), 1)
      ]

  grid, output = common.grids(width, height)
  for idx in range(len(megarows)):
    mr, mc = megarows[idx], megacols[idx]
    for r, c, color in zip(rows, cols, colors):
      grid[mr + r][mc + c] = color if idx == 0 else common.cyan()
  output = [row[:] for row in grid]
  mr, mc = megarows[0], megacols[0]
  for r, c, color in zip(rows, cols, colors):
    output[mr + r][mc + c] = common.black()
  for idx in range(1, len(megarows)):
    mr, mc = megarows[idx], megacols[idx]
    for r, c, color in zip(rows, cols, colors):
      output[mr + r][mc + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 0, 1], colors=[7, 6, 9, 4],
               megarows=[1, 4, 7, 8], megacols=[1, 5, 2, 8]),
      generate(rows=[0, 0, 1, 1, 1], cols=[0, 1, 0, 1, 2],
               colors=[7, 7, 6, 6, 6], megarows=[5, 1, 2, 7],
               megacols=[5, 1, 6, 3]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 1, 2], cols=[1, 2, 0, 1, 2, 3, 2],
               colors=[4, 4, 3, 4, 3, 3, 3], megarows=[5, 1, 1, 6],
               megacols=[0, 0, 5, 5]),
  ]
  return {"train": train, "test": test}
