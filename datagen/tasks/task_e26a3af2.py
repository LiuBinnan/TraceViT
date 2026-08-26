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


def generate(height=None, rows=None, cols=None, colors=None, wides=None,
             stripes=None, xpose=None, stripe_count=None, width=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    wides: a list of widths of the stripes
    stripes: a list of stripe colors
    xpose: whether to transpose the grid
    stripe_count: the number of stripes
    width: the total width of the stripe field before optional transpose
    density: the noise probability, or an integer percentage
  """
  if rows is None or cols is None or colors is None or wides is None or stripes is None:
    if height is None: height = common.randint(4, 30)
    if stripe_count is None: stripe_count = common.randint(1, 9)
    stripe_count = max(1, min(stripe_count, 9))
    if width is None: width = common.randint(max(4, 2 * stripe_count), 30)
    width = max(4, min(width, 30))
    stripe_count = min(stripe_count, max(1, width // 2))
    wides = [2 for _ in range(stripe_count)]
    for _ in range(width - 2 * stripe_count):
      wides[common.randint(0, stripe_count - 1)] += 1
    if density is None: density = common.randint(5, 50)
    if density > 1: density = density / 100.0
    stripes = common.random_colors(len(wides))
    pixels = common.random_pixels(sum(wides), height, prob=density)
    if not pixels:
      pixels = [(common.randint(0, height - 1), common.randint(0, sum(wides) - 1))]
    rows, cols = zip(*pixels)
    colors = []
    for col in cols:
      idx = 0
      while col >= sum(wides[:idx + 1]): idx += 1
      colors.append(common.random_color(exclude=[stripes[idx]]))
    if xpose is None: xpose = common.randint(0, 1)

  width = sum(wides)
  grid = common.grid(width, height)
  for idx, wide in enumerate(wides):
    for r in range(height):
      for c in range(sum(wides[:idx]), sum(wides[:idx]) + wide):
        grid[r][c] = stripes[idx]
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
  if xpose: grid = common.transpose(grid)
  output = common.deepcopy(grid)

  def stripe_color(r, c):
    pos, idx = r if xpose else c, 0
    while pos >= sum(wides[:idx + 1]): idx += 1
    return stripes[idx]

  def erase_noise():
    for r in range(len(output)):
      for c in range(len(output[0])):
        if output[r][c] != stripe_color(r, c): output[r][c] = common.black()

  def repair_color(idx):
    if idx >= len(stripes): return
    for r in range(len(output)):
      for c in range(len(output[0])):
        if output[r][c] != common.black(): continue
        if stripe_color(r, c) == stripes[idx]: output[r][c] = stripes[idx]

  erase_noise()
  repair_color(0)
  repair_color(1)
  repair_color(2)
  repair_color(3)
  repair_color(4)
  repair_color(5)
  repair_color(6)
  repair_color(7)
  repair_color(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=13,
               rows=[0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5,
                     6, 6, 6, 6, 7, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 10, 11, 12,
                     12, 12, 12],
               cols=[15, 0, 1, 3, 0, 3, 7, 10, 13, 16, 7, 0, 4, 10, 12, 0, 2, 5,
                     14, 16, 4, 8, 12, 14, 6, 11, 16, 3, 0, 3, 5, 8, 12, 13, 16,
                     14, 10, 1, 3, 13, 15],
               colors=[8, 9, 5, 5, 4, 2, 5, 8, 8, 7, 2, 9, 8, 4, 8, 4, 2, 7, 6,
                       9, 9, 9, 4, 6, 5, 4, 3, 9, 6, 8, 5, 4, 6, 4, 7, 6, 7, 2,
                       4, 9, 1],
               wides=[5, 3, 4, 5], stripes=[1, 8, 3, 2], xpose=0),
      generate(height=13,
               rows=[0, 1, 2, 3, 3, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9,
                     10, 10, 10, 11, 11, 12, 12, 12],
               cols=[7, 2, 7, 6, 8, 10, 3, 10, 13, 1, 2, 5, 5, 7, 13, 3, 6, 8,
                     11, 4, 6, 8, 11, 13, 1, 9, 11],
               colors=[1, 8, 9, 9, 6, 5, 6, 5, 6, 6, 4, 9, 6, 7, 2, 6, 3, 5, 3,
                       5, 2, 5, 8, 3, 8, 3, 9],
               wides=[5, 6, 3], stripes=[2, 8, 1], xpose=0),
      generate(height=14,
               rows=[1, 5, 8, 3, 7, 11, 2, 5, 6, 9, 10, 13, 0, 4, 12, 13, 5, 12,
                     13, 6, 11, 3, 4, 10, 12, 11, 3, 7, 8, 3, 10, 10],
               cols=[0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8,
                     8, 9, 9, 9, 10, 11, 12, 12, 12, 13, 13, 14],
               colors=[4, 2, 2, 9, 2, 9, 4, 2, 8, 3, 3, 4, 9, 3, 8, 2, 5, 5, 8,
                       3, 2, 4, 6, 9, 9, 3, 4, 7, 9, 5, 9, 9],
               wides=[4, 6, 3, 2], stripes=[3, 7, 8, 1], xpose=1),
  ]
  test = [
      generate(height=15,
               rows=[0, 3, 1, 4, 9, 0, 4, 0, 5, 7, 10, 12, 2, 4, 8, 11, 13, 1,
                     4, 5, 6, 10, 12, 10, 12, 0, 6, 4, 10, 14, 10, 8, 12, 6, 7,
                     13, 2, 10, 2, 3, 0, 1, 4],
               cols=[0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
                     5, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 10, 10, 11, 11, 11, 12,
                     12, 13, 13, 14, 14, 14],
               colors=[6, 5, 4, 9, 5, 5, 4, 7, 6, 9, 4, 4, 9, 1, 3, 8, 7, 5, 5,
                       6, 6, 3, 5, 6, 8, 1, 9, 1, 7, 9, 4, 5, 1, 7, 3, 2, 7, 8,
                       1, 9, 8, 6, 8],
               wides=[3, 4, 4, 2, 2], stripes=[1, 2, 8, 4, 3], xpose=1),
  ]
  return {"train": train, "test": test}
