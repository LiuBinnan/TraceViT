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
             input_colors=None, num_boxes=None, num_colors=None,
             background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if rows is None:
    if height is None: height = common.randint(10, 30)
    if width is None: width = common.randint(10, 30)
    if num_boxes is None:
      num_boxes = common.randint(3, max(3, (height * width) // 10))
    if background is None:
      background = common.choice([0, 3, 4, 5, 7, 8, 9])
    if num_colors is None: num_colors = common.randint(1, 6)
    palette = [c for c in [0, 3, 4, 5, 7, 8, 9] if c != background]
    palette = common.sample(palette, min(num_colors, len(palette)))
    rows, cols, colors, input_colors = [], [], [], []
    free = set((r, c) for r in range(height) for c in range(width))
    placed, tries = 0, 0
    while placed < num_boxes and tries < 5 * num_boxes:
      tries += 1
      stype, pixels, color = common.randint(0, 2), [], -1
      if stype == 0:
        wide, tall = common.randint(2, 6), common.randint(2, 6)
        pixels, color = common.rand_sprite("el", wide, tall), common.blue()
      if stype == 1:
        wide, tall = common.randint(3, 6), common.randint(2, 6)
        pixels, color = common.rand_sprite("you", wide, tall), common.pink()
      if stype == 2:
        wide, tall = common.randint(3, 6), common.randint(3, 6)
        pixels, color = common.rand_sprite("aitch", wide, tall), common.red()
      tall = max(p[0] for p in pixels) + 1
      wide = max(p[1] for p in pixels) + 1
      if tall > height or wide > width: continue
      row = common.randint(0, height - tall)
      col = common.randint(0, width - wide)
      placed_pixels = [(row + p[0], col + p[1]) for p in pixels]
      if any(p not in free for p in placed_pixels): continue
      placed += 1
      paint = common.choice(palette)
      rows.extend([p[0] for p in placed_pixels])
      cols.extend([p[1] for p in placed_pixels])
      colors.extend([color] * len(placed_pixels))
      input_colors.extend([paint] * len(placed_pixels))
      for r, c in placed_pixels:
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
          free.discard((r + dr, c + dc))

  grid, output = common.grids(
      width, height, common.black() if background is None else background)
  for r, c, color, input_color in zip(
      rows, cols, colors, input_colors or [common.green()] * len(rows)):
    if color == common.blue():
      output[r][c] = color
      grid[r][c] = input_color
  for r, c, color, input_color in zip(
      rows, cols, colors, input_colors or [common.green()] * len(rows)):
    if color == common.red():
      output[r][c] = color
      grid[r][c] = input_color
  for r, c, color, input_color in zip(
      rows, cols, colors, input_colors or [common.green()] * len(rows)):
    if color == common.pink():
      output[r][c] = color
      grid[r][c] = input_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=19,
               rows=[0, 0, 1, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 6, 7, 7, 7, 9,
                     9, 10, 10, 10, 11, 11, 12, 12, 12, 13, 13, 13, 13, 13, 13,
                     13, 13, 13, 14, 15, 15, 15, 15, 16, 16, 17, 17, 17, 18, 18,
                     18],
               cols=[17, 18, 18, 18, 3, 6, 3, 4, 5, 6, 12, 13, 14, 3, 12, 12,
                     12, 13, 14, 1, 2, 1, 16, 17, 1, 17, 1, 16, 17, 0, 1, 2, 3,
                     6, 7, 8, 9, 10, 6, 6, 15, 16, 17, 15, 17, 2, 15, 17, 1, 2,
                     17],
               colors=[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 6, 6, 6, 2, 6, 6, 6, 6, 6,
                       2, 2, 2, 6, 6, 2, 6, 2, 6, 6, 2, 2, 2, 2, 1, 1, 1, 1, 1,
                       1, 1, 6, 6, 6, 6, 6, 1, 6, 6, 1, 1, 6]),
      generate(width=11, height=10,
               rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6, 6, 6, 6,
                     7, 8, 9, 9, 9],
               cols=[0, 1, 2, 2, 6, 7, 8, 9, 2, 6, 9, 6, 9, 6, 9, 0, 1, 2, 3, 4,
                     2, 2, 2, 3, 4],
               colors=[1, 1, 1, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2]),
      generate(width=12, height=14,
               rows=[1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 7, 8, 8, 8, 9, 9,
                     10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13],
               cols=[1, 9, 1, 9, 10, 11, 1, 5, 1, 2, 3, 4, 5, 7, 5, 6, 7, 5, 7,
                     5, 7, 0, 1, 2, 2, 9, 11, 9, 10, 11],
               colors=[6, 1, 6, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2,
                       2, 2, 1, 1, 1, 1, 6, 6, 6, 6, 6]),
  ]
  test = [
      generate(width=16, height=14,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 5, 6, 6,
                     6, 6, 6, 6, 6, 6, 7, 8, 8, 8, 8, 10, 11, 11, 11, 11, 11,
                     11, 11, 12, 12, 12, 12, 13],
               cols=[1, 3, 12, 1, 3, 12, 1, 2, 3, 12, 13, 14, 12, 14, 6, 7, 14,
                     6, 3, 4, 5, 6, 7, 10, 11, 12, 12, 9, 10, 11, 12, 11, 1, 2,
                     3, 4, 5, 6, 11, 6, 11, 12, 13, 6],
               colors=[6, 6, 2, 6, 6, 2, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
