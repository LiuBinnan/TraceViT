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


def generate(wides=None, talls=None, brows=None, bcols=None, styles=None,
             color=None, num_boxes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    color: The color of the boxes.
    num_boxes: The number of boxes to generate.
  """

  def draw():
    grid, output = common.grids(10, 10, 7)
    # First, draw the boxes.
    for wide, tall, brow, bcol, style in zip(wides, talls, brows, bcols, styles):
      if style == 0:
        common.hollow_rect(grid, wide, tall, brow, bcol, color)
        common.hollow_rect(output, wide, tall, brow, bcol, color)
      if style == 1:
        for i in range(wide):
          r, c = brow + i, bcol + i
          output[r][c] = grid[r][c] = color
      if style == 2:
        for i in range(wide):
          r, c = brow + i, bcol + wide - 1 - i
          output[r][c] = grid[r][c] = color
    # Second, check that each box has a "safe" outer border.
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      for r in range(brow - 1, brow + tall + 1):
        for c in range(bcol - 1, bcol + wide + 1):
          if r in [brow - 1, brow + tall] or c in [bcol - 1, bcol + wide]:
            if common.get_pixel(grid, r, c) not in [-1, 7]: return None, None
    # Third, add the red boxes where appropriate.
    num_squares = 0
    for wide, tall, brow, bcol, style in zip(wides, talls, brows, bcols, styles):
      if wide != tall or style != 0: continue
      num_squares += 1
      coords = []
      coords += [(brow - 1, bcol)]
      coords += [(brow - 1, bcol + wide - 1)]
      coords += [(brow, bcol - 1)]
      coords += [(brow, bcol + wide)]
      coords += [(brow + tall - 1, bcol - 1)]
      coords += [(brow + tall - 1, bcol + wide)]
      coords += [(brow + tall, bcol)]
      coords += [(brow + tall, bcol + wide - 1)]
      for r, c in coords:
        if common.get_pixel(output, r, c) in [-1, 2]: return None, None
        output[r][c] = 2
    if num_squares == 0: return None, None
    return grid, output

  if wides is None:
    sample_num_boxes = num_boxes is None
    if num_boxes is None:
      num_boxes = common.randint(2, 5)
    color = common.random_color(exclude=[2, 7])
    while True:
      max_side = 3 if not sample_num_boxes and num_boxes >= 5 else 4
      wides = [common.randint(1, max_side) for _ in range(num_boxes)]
      talls = [common.randint(1 if wide > 2 else 2, max_side) for wide in wides]
      if sample_num_boxes or num_boxes < 5:
        for i in range(num_boxes):  # Sometimes we will make one eight units long.
          if common.randint(0, 4) == 0: wides[i] = 8
          if common.randint(0, 4) == 0: talls[i] = 8
      brows = [common.randint(0, 10 - tall) for tall in talls]
      bcols = [common.randint(0, 10 - wide) for wide in wides]
      styles = [0 if wide != tall else common.randint(0, 2) for wide, tall in zip(wides, talls)]
      num_squares = 0
      for i, (wide, tall, style) in enumerate(zip(wides, talls, styles)):
        if wide == tall and style == 0:
          num_squares += 1
          if num_squares > 5:
            styles[i] = common.randint(1, 2)
      grid, _ = draw()
      if grid: break

  grid, final = draw()
  if grid is None:
    return {"input": grid, "output": final}
  output = [row[:] for row in grid]
  square_boxes = [
      (wide, brow, bcol) for wide, tall, brow, bcol, style
      in zip(wides, talls, brows, bcols, styles)
      if wide == tall and style == 0
  ]

  def add_top_bottom_markers(idx):
    if idx >= len(square_boxes): return
    wide, brow, bcol = square_boxes[idx]
    for r, c in [
        (brow - 1, bcol), (brow - 1, bcol + wide - 1),
        (brow + wide, bcol), (brow + wide, bcol + wide - 1)]:
      output[r][c] = 2

  def add_side_markers(idx):
    if idx >= len(square_boxes): return
    wide, brow, bcol = square_boxes[idx]
    for r, c in [
        (brow, bcol - 1), (brow, bcol + wide),
        (brow + wide - 1, bcol - 1), (brow + wide - 1, bcol + wide)]:
      output[r][c] = 2

  add_top_bottom_markers(0)
  add_side_markers(0)
  add_top_bottom_markers(1)
  add_side_markers(1)
  add_top_bottom_markers(2)
  add_side_markers(2)
  add_top_bottom_markers(3)
  add_side_markers(3)
  add_top_bottom_markers(4)
  add_side_markers(4)
  return {"input": grid, "output": output}

def validate():
  """Validates the generator."""
  train = [
      generate(wides=[4, 2, 2, 4], talls=[4, 2, 2, 2], brows=[1, 1, 7, 7], bcols=[1, 7, 1, 5], styles=[0, 2, 2, 0], color=6),
      generate(wides=[3, 1, 3], talls=[3, 3, 1], brows=[2, 2, 7], bcols=[2, 7, 2], styles=[0, 0, 0], color=6),
      generate(wides=[8, 2], talls=[8, 2], brows=[1, 4], bcols=[1, 4], styles=[0, 0], color=8),
  ]
  test = [
      generate(wides=[3, 2, 3, 2, 8], talls=[3, 2, 3, 2, 1], brows=[1, 1, 5, 6, 9], bcols=[1, 6, 5, 1, 1], styles=[0, 0, 0, 0, 0], color=6),
  ]
  return {"train": train, "test": test}
