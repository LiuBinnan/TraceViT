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


def generate(wides=None, talls=None, rows=None, cols=None, colors=None,
             size=10, width=None, height=None, num_boxes=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: a list of box widths
    talls: a list of box heights
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    width: the width of the grid
    height: the height of the grid
    num_boxes: the number of boxes to try to place
    num_colors: the number of non-red colors used inside each box
  """
  if wides is None:
    if width is None: width = common.randint(10, 30)
    if height is None: height = common.randint(10, 30)
    if num_boxes is None: num_boxes = common.randint(1, 10)
    if num_colors is None: num_colors = common.randint(1, 7)

    wides, talls, rows, cols = [], [], [], []
    max_trials = 12 * num_boxes
    trials = 0
    while len(wides) < num_boxes and trials < max_trials:
      trials += 1
      wide, tall = common.randint(3, 8), common.randint(3, 8)
      if wide > width or tall > height: continue
      row = common.randint(0, height - tall)
      col = common.randint(0, width - wide)
      cwides, ctalls = wides + [wide], talls + [tall]
      crows, ccols = rows + [row], cols + [col]
      if common.overlaps(crows, ccols, cwides, ctalls, 1): continue
      wides, talls, rows, cols = cwides, ctalls, crows, ccols

    pad_color = common.random_color(exclude=[common.red()])
    palette = common.random_colors(num_colors, exclude=[common.red(), pad_color])
    colors = []
    red_bound = None
    for idx in range(len(wides)):
      wide, tall = wides[idx], talls[idx]
      area = wide * tall
      if idx == 0:
        red_bound = common.randint(1, area - num_colors)
        num_red = red_bound
      else:
        num_red = common.randint(0, min(area, red_bound - 1))
      pixels = [None] * area
      reds = common.sample(range(area), num_red)
      for red in reds:
        pixels[red] = common.red()
      nonreds = [idx for idx in range(area) if pixels[idx] is None]
      for idx, cell in enumerate(nonreds):
        pixels[cell] = palette[idx % num_colors]
      colors.extend(pixels)
  else:
    if width is None: width = size
    if height is None: height = size

  grid, output = common.grid(width, height), common.grid(wides[0], talls[0])
  i = 0
  for idx in range(len(wides)):
    wide, tall, row, col = wides[idx], talls[idx], rows[idx], cols[idx]
    for r in range(tall):
      for c in range(wide):
        grid[row + r][col + c] = colors[i]
        if not idx: output[r][c] = colors[i]
        i += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[4, 4, 6], talls=[5, 4, 4], rows=[0, 1, 6], cols=[6, 1, 3],
               colors=[8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 2, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 2, 8, 8, 8, 2, 8, 1, 8, 8, 8, 1, 8,
                       8, 8, 8]),
      generate(wides=[3, 4, 5], talls=[3, 5, 7], rows=[7, 0, 1], cols=[1, 0, 5],
               colors=[8, 2, 2, 2, 2, 1, 2, 1, 8, 1, 1, 1, 8, 1, 8, 1, 1, 8, 2,
                       8, 1, 1, 1, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 2,
                       8, 8, 8, 8, 8, 1, 8, 1, 2, 8, 2, 8, 8, 8, 1, 8, 1, 1, 8,
                       1, 8, 8, 1, 1, 8, 2]),
      generate(wides=[4, 4], talls=[6, 6], rows=[0, 3], cols=[0, 6],
               colors=[2, 8, 8, 8, 8, 8, 1, 8, 1, 8, 8, 8, 8, 8, 8, 2, 8, 2, 8,
                       1, 8, 1, 8, 8, 1, 8, 8, 2, 8, 8, 1, 8, 8, 2, 8, 8, 8, 8,
                       8, 1, 1, 8, 8, 8, 8, 8, 1, 8]),
  ]
  test = [
      generate(wides=[3, 4, 4], talls=[6, 4, 3], rows=[1, 0, 6], cols=[6, 0, 1],
               colors=[2, 8, 1, 8, 8, 8, 2, 1, 8, 8, 8, 2, 2, 8, 1, 1, 8, 8, 2,
                       8, 8, 8, 8, 8, 1, 8, 1, 2, 8, 1, 8, 8, 8, 8, 1, 2, 8, 2,
                       8, 8, 1, 8, 1, 2, 8, 1]),
  ]
  return {"train": train, "test": test}
