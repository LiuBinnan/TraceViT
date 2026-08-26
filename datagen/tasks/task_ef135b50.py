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


def generate(rows=None, cols=None, wides=None, talls=None, size=10,
             height=None, width=None, num_boxes=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    size: the width and height of the (square) grid
    height: the number of rows; defaults to size
    width: the number of columns; defaults to size
    num_boxes: the number of boxes to place
    num_colors: the number of box colors to use
  """
  if height is None: height = size
  if width is None: width = size

  def draw(grid, output):
    box_colors = set(rect_colors)
    for row, col, wide, tall, color in zip(rows, cols, wides, talls, rect_colors):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          output[r][c] = grid[r][c] = color
    for r in range(height):
      last_red, danger = width, False  # "Danger": we'd touch a box above / below
      for c in range(width):
        if output[r][c] not in box_colors:
          danger = danger or common.get_pixel(output, r - 1, c) in box_colors
          danger = danger or common.get_pixel(output, r + 1, c) in box_colors
          continue
        for col in range(last_red + 1, c):
          output[r][col] = common.maroon() if not danger else common.black()
        last_red, danger = c, False
    # Avoid maroons in top or bottom row.
    if common.maroon() in output[0] or common.maroon() in output[-1]:
      return False
    # For all other rows, many sure there's no open space between red's.
    for r in range(1, height - 1):
      state = 0
      for color in output[r]:
        if state == 0 and color in box_colors: state = 1
        if state == 1 and color == common.black(): state = 2
        if state == 2 and color in box_colors: return False
    if not any(common.maroon() in row for row in output):
      return False
    covered = sorted({r for row, tall in zip(rows, talls)
                      for r in range(row, row + tall)})
    bands = []
    for r in covered:
      if bands and bands[-1][-1] == r - 1:
        bands[-1].append(r)
      else:
        bands.append([r])
    return len(bands) <= 5

  if rows is None:
    while True:
      box_count = num_boxes
      if box_count is None:
        box_count = common.randint(2, max(2, (height * width) // 30))
      color_count = num_colors
      if color_count is None:
        color_count = common.randint(1, 8)
      color_count = min(max(1, color_count), 8, box_count)
      colors = common.random_colors(color_count, exclude=[common.maroon()])
      rect_colors = common.shuffle(
          [colors[idx % color_count] for idx in range(box_count)])
      rows, cols, wides, talls = [], [], [], []
      for _ in range(box_count):
        placed = False
        for _ in range(100):
          wide = common.randint(1, min(4, width))
          tall = common.randint(2, min(6, height))
          row = common.randint(0, height - tall)
          col = common.randint(0, width - wide)
          if common.overlaps(rows + [row], cols + [col],
                             wides + [wide], talls + [tall], 1):
            continue
          rows.append(row)
          cols.append(col)
          wides.append(wide)
          talls.append(tall)
          placed = True
          break
        if not placed:
          break
      if len(rows) != box_count:
        continue
      grid, output = common.grids(width, height)
      if not draw(grid, output): continue
      break
  else:
    rect_colors = [common.red() for _ in rows]

  grid, box_colors = common.grid(width, height), set(rect_colors)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, rect_colors):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = color
  output = common.deepcopy(grid)

  covered = sorted({r for row, tall in zip(rows, talls)
                    for r in range(row, row + tall)})
  bands = []
  for r in covered:
    if bands and bands[-1][-1] == r - 1:
      bands[-1].append(r)
    else:
      bands.append([r])

  def bridge_row(idx):
    if idx >= len(bands):
      return
    for r in bands[idx]:
      last_red, danger = width, False  # "Danger": we'd touch a box above / below
      for c in range(width):
        if output[r][c] not in box_colors:
          danger = danger or common.get_pixel(output, r - 1, c) in box_colors
          danger = danger or common.get_pixel(output, r + 1, c) in box_colors
          continue
        for col in range(last_red + 1, c):
          output[r][col] = common.maroon() if not danger else common.black()
        last_red, danger = c, False

  bridge_row(0)
  bridge_row(1)
  bridge_row(2)
  bridge_row(3)
  bridge_row(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 3, 6], cols=[0, 7, 3], wides=[3, 2, 2],
               talls=[3, 5, 4]),
      generate(rows=[0, 2, 5, 8], cols=[0, 7, 3, 6], wides=[2, 3, 2, 4],
               talls=[4, 4, 4, 2]),
      generate(rows=[0, 1, 3, 6, 7], cols=[6, 0, 5, 9, 0],
               wides=[4, 4, 3, 1, 4], talls=[2, 3, 6, 4, 3]),
  ]
  test = [
      generate(rows=[0, 1, 3, 5], cols=[0, 6, 1, 5], wides=[3, 4, 3, 4],
               talls=[2, 3, 5, 2]),
  ]
  return {"train": train, "test": test}
