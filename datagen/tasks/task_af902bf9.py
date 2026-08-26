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


def _place_boxes(width, height, count, palette):
  """Places up to `count` non-overlapping boxes at random and returns their
  (rows, cols, wides, talls, box_colors) parallel lists (at least one box)."""
  rows, cols, wides, talls, box_colors = [], [], [], [], []
  occupied = set()
  placed, attempts, max_attempts = 0, 0, 5 * count
  while placed < count and attempts < max_attempts:
    attempts += 1
    wide = common.randint(3, min(6, width))
    tall = common.randint(3, min(6, height))
    row = common.randint(0, height - tall)
    col = common.randint(0, width - wide)
    cells = {(row + dr, col + dc) for dr in range(tall) for dc in range(wide)}
    if cells & occupied:
      continue
    occupied |= cells
    rows.append(row)
    cols.append(col)
    wides.append(wide)
    talls.append(tall)
    box_colors.append(common.choice(palette))
    placed += 1
  if not rows:
    wide = common.randint(3, min(6, width))
    tall = common.randint(3, min(6, height))
    row = common.randint(0, height - tall)
    col = common.randint(0, width - wide)
    rows.append(row)
    cols.append(col)
    wides.append(wide)
    talls.append(tall)
    box_colors.append(common.choice(palette))
  return rows, cols, wides, talls, box_colors


def _count_corner_boxes(input_grid, background):
  """Counts every 3x3..6x6 rectangle whose four corners share a single non-
  background color and whose remaining cells are all background -- exactly the
  boxes the solving rule detects (corners marked, interior to be filled)."""
  height, width = len(input_grid), len(input_grid[0])
  total = 0
  for r1 in range(height):
    row1 = input_grid[r1]
    for c1 in range(width):
      color = row1[c1]
      if color == background:
        continue
      for tall in range(3, min(6, height - r1) + 1):
        r2 = r1 + tall - 1
        if input_grid[r2][c1] != color:
          continue
        row2 = input_grid[r2]
        for wide in range(3, min(6, width - c1) + 1):
          c2 = c1 + wide - 1
          if row1[c2] != color or row2[c2] != color:
            continue
          clean = True
          for i in range(r1, r2 + 1):
            gri = input_grid[i]
            edge_row = i == r1 or i == r2
            for j in range(c1, c2 + 1):
              if gri[j] == background:
                continue
              if edge_row and (j == c1 or j == c2):
                continue
              clean = False
              break
            if not clean:
              break
          if clean:
            total += 1
  return total


def _boxes_consistent(width, height, rows, cols, wides, talls, box_colors):
  """True iff the only corner-rectangles the rule would detect are the placed
  boxes (i.e. no accidental rectangle forms from corners of different boxes)."""
  background = common.black()
  input_grid = common.grid(width, height, background)
  for row, col, wide, tall, box_color in zip(
      rows, cols, wides, talls, box_colors):
    for dr, dc in [(0, 0), (0, wide - 1), (tall - 1, 0), (tall - 1, wide - 1)]:
      input_grid[row + dr][col + dc] = box_color
  return _count_corner_boxes(input_grid, background) == len(rows)


def generate(rows=None, cols=None, wides=None, talls=None, flip=None, size=10,
             height=None, width=None, count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths for the boxes
    talls: a list of heights for the boxes
    flip: whether to flip the boxes vertically
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: the number of boxes to place (defaults to an area-scaled random draw)
    num_colors: how many distinct corner colors to draw from (defaults random)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    # Choose the number of boxes (area-scaled) and a palette of corner colors,
    # then place non-overlapping boxes, re-sampling until no accidental rectangle
    # forms from corners of different boxes (which the rule would also fill).
    if count is None:
      count = common.randint(1, max(1, (width * height) // 20))
    if num_colors is None:
      num_colors = common.randint(1, 8)
    palette = common.random_colors(num_colors, exclude=[common.red()])
    target, attempt = count, 0
    while True:
      rows, cols, wides, talls, box_colors = _place_boxes(
          width, height, target, palette)
      if _boxes_consistent(width, height, rows, cols, wides, talls, box_colors):
        break
      attempt += 1
      if attempt % 3 == 0 and target > 1:
        target -= 1
    flip = common.randint(0, 1)
  else:
    box_colors = [common.yellow()] * len(rows)

  grid, output = common.grids(width, height)

  def map_row(r):
    return height - 1 - r if flip else r

  for row, col, wide, tall, box_color in zip(
      rows, cols, wides, talls, box_colors):
    for dr, dc in [(0, 0), (0, wide - 1), (tall - 1, 0), (tall - 1, wide - 1)]:
      grid[map_row(row + dr)][col + dc] = box_color
      output[map_row(row + dr)][col + dc] = box_color
  boxes = list(zip(rows, cols, wides, talls))

  def fill_box(box_idx):
    if box_idx >= len(boxes):
      return
    row, col, wide, tall = boxes[box_idx]
    for dr in range(1, tall - 1):
      for dc in range(1, wide - 1):
        output[map_row(row + dr)][col + dc] = common.red()

  fill_box(0)
  for box_idx in range(1, len(boxes)):
    fill_box(box_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3], cols=[3], wides=[3], talls=[3], flip=0),
      generate(rows=[1], cols=[1], wides=[6], talls=[6], flip=0),
      generate(rows=[1, 6], cols=[1, 4], wides=[3, 6], talls=[3, 4], flip=0),
  ]
  test = [
      generate(rows=[1, 5], cols=[0, 5], wides=[4, 5], talls=[4, 5], flip=1),
  ]
  return {"train": train, "test": test}
