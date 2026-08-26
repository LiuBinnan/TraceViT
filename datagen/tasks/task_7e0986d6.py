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


def generate(width=None, height=None, rows=None, cols=None, color=None,
             boxrows=None, boxcols=None, wides=None, talls=None, boxcolor=None,
             num_boxes=None, num_box_colors=None, num_noise_colors=None,
             noise_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    boxrows: a list of vertical coordinates where boxes should be placed
    boxcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of boxes
    talls: a list of heights of boxes
    boxcolor: a digit representing a color to be used for boxes
    num_boxes: the number of boxes to be placed
    num_box_colors: the number of colors to use for boxes
    num_noise_colors: the number of colors to use for noise pixels
    noise_count: the number of isolated noise pixels to place
  """
  if (rows is None or cols is None or boxrows is None or boxcols is None or
      wides is None or talls is None):
    if width is None:
      width = common.randint(10, 30)
    if height is None:
      height = common.randint(10, 30)
    area = width * height
    max_boxes = min(5, max(1, area // 25))
    if num_boxes is None:
      num_boxes = common.randint(1, max_boxes)
    num_boxes = min(max(1, num_boxes), max_boxes)
    if num_box_colors is None:
      num_box_colors = common.randint(1, 5)
    num_box_colors = min(max(1, num_box_colors), 5)
    if num_noise_colors is None:
      num_noise_colors = common.randint(1, 9 - num_box_colors)
    num_noise_colors = min(max(1, num_noise_colors), 9 - num_box_colors)
    colors = common.random_colors(num_box_colors + num_noise_colors)
    box_palette = colors[:num_box_colors]
    color = colors[num_box_colors:]
    boxcolor = [common.choice(box_palette) for _ in range(num_boxes)]
    while True:
      wides = [common.randint(2, 7) for _ in range(num_boxes)]
      talls = [common.randint(2, 7) for _ in range(num_boxes)]
      boxrows = [common.randint(0, height - tall) for tall in talls]
      boxcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(boxrows, boxcols, wides, talls, 1): break
    if noise_count is None:
      noise_count = common.randint(1, max(1, area // 9))
    noise_count = min(max(1, noise_count), max(1, area // 9))
    pixels = []
    candidates = common.all_pixels(width, height)
    def base_color(pixel):
      row, col = pixel
      for idx, (boxrow, boxcol, wide, tall) in enumerate(
          zip(boxrows, boxcols, wides, talls)):
        if boxrow <= row < boxrow + tall and boxcol <= col < boxcol + wide:
          return boxcolor[idx]
      return 0
    while candidates and len(pixels) < noise_count:
      pixel = common.choice(candidates)
      candidates.remove(pixel)
      current_color = base_color(pixel)
      pixels.append(pixel)
      neighbors = []
      for other in candidates:
        if abs(pixel[0] - other[0]) + abs(pixel[1] - other[1]) != 1:
          continue
        if base_color(other) == current_color:
          neighbors.append(other)
      for neighbor in neighbors:
        candidates.remove(neighbor)
    if not pixels:
      pixels = [(0, 0)]
    rows, cols = zip(*pixels)

  grid, output = common.grids(width, height)
  for idx, (boxrow, boxcol, wide, tall) in enumerate(
      zip(boxrows, boxcols, wides, talls)):
    draw_color = boxcolor[idx] if isinstance(boxcolor, list) else boxcolor
    for r in range(boxrow, boxrow + tall):
      for c in range(boxcol, boxcol + wide):
        grid[r][c] = draw_color
  for r, c in zip(rows, cols):
    grid[r][c] = common.choice(color) if isinstance(color, list) else color

  def reveal_box(idx):
    if idx >= len(boxrows):
      return
    boxrow, boxcol, wide, tall = boxrows[idx], boxcols[idx], wides[idx], talls[idx]
    draw_color = boxcolor[idx] if isinstance(boxcolor, list) else boxcolor
    for r in range(boxrow, boxrow + tall):
      for c in range(boxcol, boxcol + wide):
        output[r][c] = draw_color

  reveal_box(0)
  reveal_box(1)
  reveal_box(2)
  reveal_box(3)
  reveal_box(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=13,
               rows=[0, 0, 0, 2, 2, 4, 5, 7, 7, 7, 8, 10, 10, 12, 12, 12],
               cols=[0, 4, 11, 8, 10, 7, 4, 1, 6, 12, 4, 4, 8, 1, 4, 13],
               color=8, boxrows=[0, 3, 6, 7, 10], boxcols=[6, 2, 9, 3, 0],
               wides=[5, 3, 5, 5, 3], talls=[5, 3, 4, 4, 3], boxcolor=3),
      generate(width=16, height=13,
               rows=[1, 2, 3, 5, 5, 8, 9, 9, 10, 10, 11, 11],
               cols=[6, 10, 3, 5, 14, 12, 1, 9, 3, 15, 9, 12], color=1,
               boxrows=[1, 2, 9], boxcols=[1, 9, 3], wides=[4, 7, 10],
               talls=[5, 5, 4], boxcolor=2),
  ]
  test = [
      generate(width=17, height=12,
               rows=[0, 1, 1, 2, 3, 5, 6, 7, 7, 9, 10, 11, 11],
               cols=[14, 1, 6, 2, 16, 7, 14, 5, 12, 15, 11, 3, 9], color=4,
               boxrows=[0, 2, 10], boxcols=[12, 1, 6], wides=[4, 8, 6],
               talls=[7, 6, 2], boxcolor=5),
  ]
  return {"train": train, "test": test}
