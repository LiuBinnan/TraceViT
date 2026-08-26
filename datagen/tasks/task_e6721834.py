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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             colors=None, brows=None, bcols=None, bidxs=None, bsides=None,
             wides=None, talls=None, backs=None, forecolor=None, horiz=None,
             foreside=None, num_boxes=None, density=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indicies into the sprite list
    colors: a list of digit representing the color to be used
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    bidxs: a list of box indices into the sprite list
    bsides: a list of sides (either 0 or 1)
    wides: a list of widths of boxes
    talls: a list of heights of boxes
    backs: a list of background colors
    forecolor: a foreground color
    horiz: whether the two grids are horitonally positioned
    foreside: which side has the foreground colors
    num_boxes: the number of box templates to place
    density: percentage of each box covered by colored dots
    num_colors: number of dot colors to draw from
  """
  if rows is None:
    # Choose grid dimensions, colors, # of boxes, and foreground side / horiz.
    if height is None:
      height = common.randint(6, 15)
    else:
      height = min(max(height, 6), 15)
    if horiz is None:
      horiz = common.randint(0, 1) if width is None or width <= 15 else 0
    if width is None:
      width = common.randint(8, 15 if horiz else 30)
    else:
      width = min(max(width, 8), 15 if horiz else 30)
    backs = common.sample(range(10), 2)
    forecolor = common.random_color(exclude=backs)
    max_boxes = max(1, min(14, (width * height) // 16))
    if num_boxes is None:
      num_boxes = common.randint(1, max_boxes)
    else:
      num_boxes = min(max(num_boxes, 1), max_boxes)
    max_colors = len([c for c in range(1, 10)
                      if c not in backs + [forecolor]])
    if num_colors is None:
      num_colors = common.randint(1, max_colors)
    else:
      num_colors = min(max(num_colors, 1), max_colors)
    color_pool = common.random_colors(num_colors, exclude=backs + [forecolor])
    if foreside is None:
      foreside = common.randint(0, 1)
    # Choose box sizes and positions.
    while True:
      max_wide = min(6, max(3, width // 2))
      max_tall = min(6, max(3, height // 2))
      wides = [common.randint(3, max_wide) for _ in range(num_boxes)]
      talls = [common.randint(3, max_tall) for _ in range(num_boxes)]
      brows, bcols, bidxs, bsides = [], [], [], []
      placed = {0: [], 1: []}
      placed_all = True
      for side in range(2):
        for idx in range(num_boxes):
          if side != foreside and idx and not common.randint(0, 2): continue
          wide, tall = wides[idx], talls[idx]
          found = False
          for _ in range(80):
            brow = common.randint(0, height - tall)
            bcol = common.randint(0, width - wide)
            overlaps = False
            for prow, pcol, pwide, ptall in placed[side]:
              if brow + tall < prow - 1: continue
              if prow + ptall < brow - 1: continue
              if bcol + wide < pcol - 1: continue
              if pcol + pwide < bcol - 1: continue
              overlaps = True
            if overlaps: continue
            found = True
            break
          if not found:
            placed_all = False
            break
          placed[side].append((brow, bcol, wide, tall))
          brows.append(brow)
          bcols.append(bcol)
          bidxs.append(idx)
          bsides.append(side)
        if not placed_all: break
      if placed_all: break
      if num_boxes > 1:
        num_boxes -= 1
    # Choose box contents.
    rows, cols, idxs, colors = [], [], [], []
    seen_patterns = set()
    for idx in range(num_boxes):
      wide, tall = wides[idx], talls[idx]
      if density is None:
        num_pixels = common.randint(1, max(1, (wide * tall) // 2))
      else:
        num_pixels = max(1, min(wide * tall,
                                (wide * tall * density + 99) // 100))
      pool = [(row, col) for row in range(1, tall - 1)
              for col in range(1, wide - 1)]
      if density is None or density <= 35:
        pool = [p for p in pool if (p[0] + p[1]) % 2 == 0]
      if not pool:
        pool = common.all_pixels(wide, tall)
      num_pixels = min(max(1, num_pixels), len(pool))
      color = color_pool[idx % len(color_pool)]
      for _ in range(20):
        pixels = common.sample(pool, num_pixels)
        key = (tuple(sorted(pixels)), color)
        if key not in seen_patterns: break
      seen_patterns.add(key)
      row_list, col_list = zip(*pixels)
      rows.extend(row_list)
      cols.extend(col_list)
      idxs.extend([idx for _ in pixels])
      colors.extend([color for _ in pixels])

  inwidth, inheight = width * (2 if horiz else 1), height * (1 if horiz else 2)
  grid = common.grid(inwidth, inheight, backs[0 if foreside else 1])
  _, output = common.grids(width, height, backs[0 if foreside else 1])
  # Draw the appropriate background colors.
  for row in range(height):
    for col in range(width):
      r, c = row, col
      if foreside and horiz: c += width
      if foreside and not horiz: r += height
      grid[r][c] = backs[1 if foreside else 0]
  for brow, bcol, bidx, bside in zip(brows, bcols, bidxs, bsides):
    # Draw full boxes on the foreground side, and only dots on the other side.
    wide, tall = wides[bidx], talls[bidx]
    if bside == foreside:
      for row in range(brow, brow + tall):
        for col in range(bcol, bcol + wide):
          r, c = row, col
          if bside and horiz: c += width
          if bside and not horiz: r += height
          grid[r][c] = forecolor
    for row, col, idx, color in zip(rows, cols, idxs, colors):
      if idx != bidx: continue
      r, c = brow + row, bcol + col
      if bside and horiz: c += width
      if bside and not horiz: r += height
      grid[r][c] = color

  def stamp_box_bodies():
    for brow, bcol, bidx, bside in zip(brows, bcols, bidxs, bsides):
      if bside == foreside: continue
      wide, tall = wides[bidx], talls[bidx]
      for row in range(brow, brow + tall):
        for col in range(bcol, bcol + wide):
          output[row][col] = forecolor

  def stamp_box_dots():
    for brow, bcol, bidx, bside in zip(brows, bcols, bidxs, bsides):
      if bside == foreside: continue
      for row, col, idx, color in zip(rows, cols, idxs, colors):
        if idx != bidx: continue
        output[brow + row][bcol + col] = color

  stamp_box_bodies()
  stamp_box_dots()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=15, rows=[1, 0, 1, 0, 1, 3, 4, 0, 1, 1, 2],
               cols=[1, 3, 5, 2, 1, 1, 2, 3, 1, 3, 1],
               idxs=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               colors=[2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2],
               brows=[4, 7, 8, 1, 9], bcols=[2, 2, 10, 8, 2],
               bidxs=[0, 1, 2, 0, 1], bsides=[0, 0, 0, 1, 1],
               wides=[7, 4, 5], talls=[2, 5, 3], backs=[8, 0], forecolor=1,
               horiz=0, foreside=0),
      generate(width=10, height=11, rows=[1, 1, 0, 1],
               cols=[0, 2, 3, 1],
               idxs=[0, 0, 1, 1],
               colors=[8, 8, 2, 2],
               brows=[2, 8, 0, 6], bcols=[2, 4, 5, 1],
               bidxs=[0, 1, 0, 1], bsides=[0, 0, 1, 1],
               wides=[3, 4], talls=[4, 3], backs=[6, 1], forecolor=3,
               horiz=1, foreside=0),
      generate(width=8, height=10, rows=[1, 3, 0],
               cols=[0, 0, 2],
               idxs=[0, 0, 1],
               colors=[2, 2, 6],
               brows=[1, 8, 1, 7], bcols=[4, 0, 1, 2],
               bidxs=[0, 1, 0, 1], bsides=[0, 0, 1, 1],
               wides=[3, 3], talls=[4, 2], backs=[4, 8], forecolor=1,
               horiz=1, foreside=1),
  ]
  test = [
      generate(width=12, height=12, rows=[1, 2, 1, 0, 1, 2],
               cols=[3, 4, 0, 2, 0, 2],
               idxs=[0, 0, 1, 2, 2, 2],
               colors=[1, 1, 1, 1, 1, 1],
               brows=[2, 6, 3, 7, 8], bcols=[4, 1, 3, 1, 6],
               bidxs=[0, 2, 0, 1, 2], bsides=[0, 0, 1, 1, 1],
               wides=[5, 2, 5], talls=[3, 4, 3], backs=[4, 2], forecolor=8,
               horiz=0, foreside=1),
  ]
  return {"train": train, "test": test}
