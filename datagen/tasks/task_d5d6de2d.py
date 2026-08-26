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


def generate(size=None, height=None, width=None,
             rows=None, cols=None, wides=None, talls=None,
             num_boxes=None, background_color=None, box_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
  """
  sampled = rows is None
  if size is None:
    size = common.randint(10, 30)
    if height is None:
      height = size
    if width is None:
      width = size
    if num_boxes is None:
      num_boxes = common.randint(1, 16)
    rows, cols, wides, talls = [], [], [], []
    max_trials = 4 * num_boxes
    trials = 0
    while len(rows) < num_boxes and trials <= max_trials:
      wide = common.randint(1, min(7, width))
      tall = common.randint(1, min(7, height))
      row = common.randint(0, height - tall)
      col = common.randint(0, width - wide)
      if not common.overlaps(rows + [row], cols + [col],
                             wides + [wide], talls + [tall], 1):
        rows.append(row)
        cols.append(col)
        wides.append(wide)
        talls.append(tall)
      trials += 1
  if height is None:
    height = size
  if width is None:
    width = size

  if background_color is None:
    if sampled:
      background_color = common.randint(0, 9)
      while background_color == common.green():
        background_color = common.randint(0, 9)
    else:
      background_color = common.black()
  if box_colors is None:
    if sampled:
      box_colors = [
          common.random_color(exclude=[background_color, common.green()])
          for _ in rows
      ]
    else:
      box_colors = [common.red() for _ in rows]

  grid, output = common.grids(width, height, background_color)
  boxes = list(zip(rows, cols, wides, talls))
  for box_color, (row, col, wide, tall) in zip(box_colors, boxes):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = box_color

  def fill_box(box_idx):
    if box_idx >= len(boxes):
      return
    row, col, wide, tall = boxes[box_idx]
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        grid[r][c] = common.black()
        output[r][c] = common.green()

  fill_box(0)
  fill_box(1)
  fill_box(2)
  fill_box(3)
  fill_box(4)
  fill_box(5)
  fill_box(6)
  fill_box(7)
  fill_box(8)
  fill_box(9)
  fill_box(10)
  fill_box(11)
  fill_box(12)
  fill_box(13)
  fill_box(14)
  fill_box(15)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[1, 5], cols=[1, 4], wides=[3, 4], talls=[3, 5]),
      generate(size=10, rows=[1], cols=[4], wides=[3], talls=[4]),
      generate(size=15, rows=[1, 7], cols=[1, 10], wides=[5, 2], talls=[5, 2]),
  ]
  test = [
      generate(size=10, rows=[0, 4], cols=[0, 1], wides=[3, 8], talls=[3, 6]),
      generate(size=25, rows=[1, 7, 9, 18], cols=[1, 4, 15, 1],
               wides=[7, 2, 9, 5], talls=[3, 2, 4, 6]),
  ]
  return {"train": train, "test": test}
