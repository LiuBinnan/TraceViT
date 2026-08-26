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


def generate(lengths=None, cols=None, mode=None, gravity=None, size=10,
             height=None, width=None, num_boxes=None, num_colors=None,
             bg_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: the lengths of the two rectangles
    cols: the columns where the rectangles are placed
    mode: one of three options (0=space at bottom, 1=space at top, 2=no space)
    gravity: determines where the "bottom" of the grid is placed
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    num_boxes: the number of rectangles to place
    num_colors: the number of foreground colors to use
    bg_color: the background color
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if lengths is None:
    if num_boxes is None:
      num_boxes = common.randint(1, 8)
    num_boxes = min(max(num_boxes, 1), 8)
    legal_colors = [
        common.black(), common.blue(), common.green(), common.yellow(),
        common.gray(), common.pink(), common.orange(), common.cyan(),
        common.maroon()]
    if bg_color is None:
      bg_color = common.choice(legal_colors)
    palette = [color for color in legal_colors if color != bg_color]
    if num_colors is None:
      num_colors = num_boxes
    num_colors = min(max(num_colors, 1), len(palette))
    box_colors = common.sample(palette, num_colors)

    grid = common.grid(width, height, bg_color)
    output = common.grid(width, height, bg_color)
    boxes = []
    trials = 0
    maxtrials = 12 * num_boxes
    while len(boxes) < num_boxes and trials < maxtrials:
      trials += 1
      bh = common.randint(3, 7)
      length = common.randint(3, 7)
      if bh > height or length > width:
        continue
      row = common.randint(0, height - bh)
      col = common.randint(0, width - length)
      touches = False
      for prev_row, prev_col, prev_length, prev_bh, _ in boxes:
        if (row + bh + 1 <= prev_row or prev_row + prev_bh + 1 <= row or
            col + length + 1 <= prev_col or
            prev_col + prev_length + 1 <= col):
          continue
        touches = True
      if touches:
        continue
      color = box_colors[len(boxes) % len(box_colors)]
      boxes.append((row, col, length, bh, color))

    for row, col, length, bh, color in boxes:
      for r in range(row, row + bh):
        for c in range(col, col + length):
          grid[r][c] = color
          output[r][c] = color
      for r in range(row + 1, row + bh - 1):
        for c in range(col + 1, col + length - 1):
          output[r][c] = common.red()
    return {"input": grid, "output": output}

  grid, output = common.grids(width, height)
  heights = [3, 6 if mode == 2 else 5]
  row = 1 if mode == 0 else 0
  boxes = []
  for length, col, bh in zip(lengths, cols, heights):
    for r in range(row, row + bh):
      for c in range(col, col + length):
        grid[r][c] = common.gray()
    boxes.append((row, col, length, bh))
    row += bh + 1
  grid = common.apply_gravity(grid, gravity)
  output = [row[:] for row in grid]

  def fill_box(box_idx):
    if box_idx >= len(boxes):
      return
    row, col, length, bh = boxes[box_idx]
    canvas = common.grid(width, height)
    for r in range(row, row + bh):
      for c in range(col, col + length):
        canvas[r][c] = common.gray()
    for r in range(row + 1, row + bh - 1):
      for c in range(col + 1, col + length - 1):
        canvas[r][c] = common.red()
    canvas = common.apply_gravity(canvas, gravity)
    for r in range(len(canvas)):
      for c in range(len(canvas[r])):
        if canvas[r][c]:
          output[r][c] = canvas[r][c]

  fill_box(0)
  fill_box(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[4, 5], cols=[3, 2], mode=0, gravity=3),
      generate(lengths=[5, 6], cols=[4, 1], mode=1, gravity=2),
  ]
  test = [
      generate(lengths=[6, 7], cols=[0, 3], mode=2, gravity=0),
  ]
  return {"train": train, "test": test}
