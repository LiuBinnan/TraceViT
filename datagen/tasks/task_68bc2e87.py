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


def generate(wides=None, talls=None, brows=None, bcols=None, colors=None,
             gwidth=None, gheight=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row coordinates of the top of each rectangle.
    bcols: The column coordinates of the left of each rectangle.
    colors: The colors of the rectangles.
    gwidth: The width of a randomized input canvas.
    gheight: The height of a randomized input canvas.
  """

  def draw_input():
    width = 19 if gwidth is None else gwidth
    height = 18 if gheight is None else gheight
    grid = common.grid(width, height, 8)
    last_color = None
    specials = []
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      seen = False
      for r in range(tall):
        for c in range(wide):
          if r in [0, tall - 1] or c in [0, wide - 1]:
            if grid[brow + r][bcol + c] == last_color:
              if (brow + r, bcol + c) in specials: return None
              specials.append((brow + r, bcol + c))
              seen = True
            grid[brow + r][bcol + c] = color
      if last_color is not None and not seen: return None
      last_color = color
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      corners = 0
      for r in [0, tall - 1]:
        for c in [0, wide - 1]:
          if grid[brow + r][bcol + c] == color: corners += 1
      if corners < 3: return None
    return grid

  if wides is None:
    if gwidth is None:
      gwidth = common.randint(14, 28)
    if gheight is None:
      gheight = common.randint(12, 26)
    colors = common.random_colors(common.randint(4, 6), exclude=[8])
    attempts = 0
    while True:
      wides = [common.randint(3, gwidth - 2) for _ in range(len(colors))]
      talls = [common.randint(3, gheight - 1) for _ in range(len(colors))]
      brows = [common.randint(0, gheight - t) for t in talls]
      bcols = [common.randint(0, gwidth - w) for w in wides]
      grid = draw_input()
      if grid: break
      attempts += 1
      if attempts < 256: continue
      # A diagonal staircase of equal-sized rectangles guarantees a fresh
      # overlap with the preceding rectangle at every depth.  Its intersections
      # avoid reused overlap pixels and overwrite at most one corner per box.
      shift_count = len(colors) - 1
      wide = common.randint(3, gwidth - shift_count)
      tall = common.randint(3, gheight - shift_count)
      row_step = -1 if common.randint(0, 1) else 1
      col_step = -1 if common.randint(0, 1) else 1
      if row_step > 0:
        first_row = common.randint(0, gheight - tall - shift_count)
      else:
        first_row = common.randint(shift_count, gheight - tall)
      if col_step > 0:
        first_col = common.randint(0, gwidth - wide - shift_count)
      else:
        first_col = common.randint(shift_count, gwidth - wide)
      wides = [wide] * len(colors)
      talls = [tall] * len(colors)
      brows = [first_row + row_step * i for i in range(len(colors))]
      bcols = [first_col + col_step * i for i in range(len(colors))]
      grid = draw_input()
      if grid: break
  else:
    grid = draw_input()

  # Build the depth-ordered column on the same canvas color (8) the input
  # uses, so every intermediate frame shares the input's background instead of
  # black. The column height equals len(colors) and every cell is overwritten
  # below, so the final output is byte-identical; only the not-yet-filled cells
  # of the intermediate steps change (black -> canvas), keeping the post-hoc
  # background recolor consistent across input, steps and output.
  output = common.grid(1, len(colors), 8)
  if len(colors) > 0:
    output[0][0] = colors[0]
  if len(colors) > 1:
    output[1][0] = colors[1]
  if len(colors) > 2:
    output[2][0] = colors[2]
  if len(colors) > 3:
    output[3][0] = colors[3]
  if len(colors) > 4:
    output[4][0] = colors[4]
  if len(colors) > 5:
    output[5][0] = colors[5]
  for i in range(6, len(colors)):
    output[i][0] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[5, 16, 4, 8, 3], talls=[16, 12, 12, 9, 5],
               brows=[1, 3, 5, 7, 5], bcols=[1, 3, 7, 9, 12],
               colors=[3, 6, 4, 2, 5]),
      generate(wides=[15, 12, 9, 5, 3], talls=[9, 11, 6, 6, 2],
               brows=[8, 3, 1, 5, 10], bcols=[2, 4, 1, 7, 10],
               colors=[2, 3, 7, 6, 9]),
      generate(wides=[16, 13, 9, 5], talls=[6, 16, 12, 5], brows=[4, 1, 6, 3],
               bcols=[1, 3, 5, 7], colors=[2, 3, 6, 4]),
      generate(wides=[6, 12, 5, 4], talls=[6, 7, 7, 5], brows=[1, 3, 7, 11],
               bcols=[2, 5, 9, 11], colors=[1, 2, 4, 6]),
  ]
  test = [
      generate(wides=[17, 14, 13, 5, 3], talls=[8, 16, 6, 7, 2],
               brows=[7, 1, 0, 3, 9], bcols=[1, 3, 1, 6, 5],
               colors=[2, 4, 1, 6, 5]),
  ]
  return {"train": train, "test": test}
