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


def generate(rows=None, cols=None, lengths=None, size=12, height=None,
             width=None, count=None, num_colors=None, bg_color=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    lengths: a list of *total* lengths (not the creme fillings)
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: how many boxes to attempt to place (defaults to an area-scaled
      random count)
    num_colors: number of outline colors to draw from
    bg_color: background color for the grid
    colors: a list of outline colors for the boxes
  """
  random_sized = rows is None and height is None and width is None
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if random_sized:
      height = common.randint(10, 30)
      width = common.randint(10, 30)
    if count is None:
      count = common.randint(1, max(1, (height * width) // 20))
    legal_colors = [
        common.black(), common.blue(), common.red(), common.green(),
        common.yellow(), common.gray(), common.maroon()]
    if bg_color is None:
      bg_color = common.sample(legal_colors, 1)[0]
    palette = [color for color in legal_colors if color != bg_color]
    if num_colors is None:
      num_colors = common.randint(1, len(palette))
    if colors is None:
      colors = common.sample(palette, min(num_colors, len(palette)))
    rows, cols, lengths, outline_colors = [], [], [], []
    available = set(common.all_pixels(width, height))
    maxtrials = 4 * count
    trials = 0
    while len(lengths) < count and trials <= maxtrials:
      length = common.sample([3, 4, 5], 1)[0]
      trials += 1
      spots = []
      for r, c in sorted(available):
        if r > height - length or c > width - length: continue
        block = [(r + dr, c + dc)
                 for dr in range(length) for dc in range(length)]
        if all(pixel in available for pixel in block):
          spots.append((r, c))
      if not spots: continue
      r, c = common.choice(spots)
      rows.append(r)
      cols.append(c)
      lengths.append(length)
      outline_colors.append(common.choice(colors))
      for rr in range(r - 1, r + length + 1):
        for cc in range(c - 1, c + length + 1):
          available.discard((rr, cc))
    colors = outline_colors
  if bg_color is None:
    bg_color = common.black()
  if colors is None:
    colors = [common.gray()] * len(lengths)

  def draw_block(idx):
    r, c, length = rows[idx], cols[idx], lengths[idx]
    for dr in range(length):
      for dc in range(length):
        output[r + dr][c + dc] = grid[r + dr][c + dc] = colors[idx]
    for dr in range(length - 2):
      for dc in range(length - 2):
        grid[r + dr + 1][c + dc + 1] = bg_color
        output[r + dr + 1][c + dc + 1] = common.gray() + length - 2

  grid, output = common.grids(width, height, bg_color)
  for idx in range(min(1, len(lengths))):
    draw_block(idx)
  for idx in range(1, min(2, len(lengths))):
    draw_block(idx)
  for idx in range(2, len(lengths)):
    draw_block(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 6, 2], cols=[7, 6, 2], lengths=[5, 4, 3]),
      generate(rows=[4, 0, 7], cols=[6, 1, 1], lengths=[5, 4, 3]),
      generate(rows=[1, 7], cols=[1, 4], lengths=[5, 4]),
  ]
  test = [
      generate(rows=[1, 8, 4], cols=[1, 4, 8], lengths=[5, 4, 3]),
  ]
  return {"train": train, "test": test}
