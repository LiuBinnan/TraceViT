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


def generate(size=None, rows=None, cols=None, wides=None, talls=None,
             grows=None, gcols=None, height=None, width=None,
             num_boxes=None, num_colors=None, object_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    grows: a list of vertical coordinates where gaps should be placed
    gcols: a list of horizontal coordinates where gaps should be placed
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_boxes: number of objects to attempt to place
    num_colors: number of foreground colors to sample
    object_colors: colors for the placed objects
  """
  if size is None:
    if height is None:
      height = common.randint(10, 30)  # widened to re_arc band (10, 30)
    if width is None:
      width = common.randint(10, 30)  # widened to re_arc band (10, 30)
    if num_boxes is None:
      num_boxes = common.randint(3, max(3, (height * width) // 10))
    if num_colors is None:
      num_colors = common.randint(1, 6)
    if object_colors is None:
      object_palette = common.random_colors(num_colors, exclude=[common.green()])
    else:
      object_palette = object_colors[:]
    while True:
      rows, cols, wides, talls, grows, gcols, object_colors = [], [], [], [], [], [], []
      tries, max_tries, some_closed = 0, max(25, 10 * num_boxes), False
      while len(rows) < num_boxes and tries < max_tries:
        tries += 1
        wide = common.randint(1, 5)
        tall = common.randint(1, 5)
        row = common.randint(0, height - tall)
        col = common.randint(0, width - wide)
        if common.overlaps(rows + [row], cols + [col],
                           wides + [wide], talls + [tall], 1):
          continue
        if wide == 1 or tall == 1:  # Never take a chunk of flat shapes.
          grow, gcol = -1, -1
        elif wide != 2 and tall != 2 and common.randint(0, 1):
          grow, gcol = -1, -1
          some_closed = True
        elif min(wide, tall) >= 3:  # Don't take a corner if shape has a hole.
          if common.randint(0, 1):
            grow = 0 if common.randint(0, 1) else (tall - 1)
            gcol = common.randint(1, wide - 2)
          else:
            grow = common.randint(1, tall - 2)
            gcol = 0 if common.randint(0, 1) else (wide - 1)
        else:  # Take chunks from any 2xH or Wx2 boxes, and half of all others.
          grow = 0 if common.randint(0, 1) else (tall - 1)
          gcol = 0 if common.randint(0, 1) else (wide - 1)
        rows.append(row)
        cols.append(col)
        wides.append(wide)
        talls.append(tall)
        grows.append(grow)
        gcols.append(gcol)
        object_colors.append(common.choice(object_palette))
      if some_closed: break
  else:
    height = width = size
  if object_colors is None:
    object_colors = [common.blue() for _ in rows]
  elif len(object_colors) < len(rows):
    object_colors = [object_colors[idx % len(object_colors)]
                     for idx in range(len(rows))]

  grid = common.grid(width, height)
  for row, col, w, t, grow, gcol, color in zip(
      rows, cols, wides, talls, grows, gcols, object_colors):
    for r in range(row, row + t):
      common.draw(grid, r, col, color)
      common.draw(grid, r, col + w - 1, color)
    for c in range(col, col + w):
      common.draw(grid, row, c, color)
      common.draw(grid, row + t - 1, c, color)
    if grow > -1 and gcol > -1:
      grid[row + grow][col + gcol] = common.black()
  output = [row[:] for row in grid]
  closed_boxes = [
      idx for idx, (w, t, grow, gcol) in enumerate(zip(wides, talls, grows, gcols))
      if w >= 3 and t >= 3 and grow == -1 and gcol == -1
  ]

  def recolor_closed_box(box_idx):
    if box_idx >= len(closed_boxes):
      return
    idx = closed_boxes[box_idx]
    row, col, w, t = rows[idx], cols[idx], wides[idx], talls[idx]
    for r in range(row, row + t):
      common.draw(output, r, col, common.green())
      common.draw(output, r, col + w - 1, common.green())
    for c in range(col, col + w):
      common.draw(output, row, c, common.green())
      common.draw(output, row + t - 1, c, common.green())

  for box_idx in range(len(closed_boxes)):
    recolor_closed_box(box_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, rows=[1, 2, 6, 7, 7, 10, 12, 13],
               cols=[10, 2, 12, 3, 6, 0, 10, 5],
               wides=[3, 4, 2, 1, 4, 3, 4, 2],
               talls=[3, 3, 2, 1, 4, 4, 3, 1],
               grows=[2, -1, 1, -1, -1, -1, -1, -1],
               gcols=[1, -1, 1, -1, -1, -1, -1, -1]),
      generate(size=15, rows=[3, 3, 8, 8],
               cols=[4, 10, 4, 9],
               wides=[3, 1, 1, 4],
               talls=[3, 2, 1, 3],
               grows=[-1, -1, -1, 0],
               gcols=[-1, -1, -1, 1]),
      generate(size=9, rows=[2, 6, 7], cols=[1, -1, 4],
               wides=[5, 3, 2],
               talls=[3, 3, 1],
               grows=[-1, 2, -1],
               gcols=[-1, 1, -1]),
  ]
  test = [
      generate(size=12, rows=[0, 1, 6, 7, 8, 8],
               cols=[7, 1, 1, 4, 1, 11],
               wides=[5, 4, 2, 5, 1, 1],
               talls=[5, 3, 1, 4, 1, 1],
               grows=[4, -1, -1, -1, -1, -1],
               gcols=[2, -1, -1, -1, -1, -1]),
  ]
  return {"train": train, "test": test}
