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


def generate(rows=None, cols=None, wides=None, talls=None, pattern=None,
             size=12, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    pattern: a pattern to be used along the side
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    start, num_boxes = common.randint(0, 1), common.randint(3, 4)
    while True:
      wides = [common.randint(2, 6) for _ in range(num_boxes)]
      talls = [common.randint(3, 7) for _ in range(num_boxes)]
      rows = [common.randint(start, height - tall) for tall in talls]
      cols = [common.randint(2, width - wide) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls): break
    color_list = common.random_colors(common.randint(2, 3),
                                      exclude=[common.gray()])
    pattern = [common.choice(color_list) for _ in range(start, height)]
    if start: pattern = [0] + pattern

  grid, output = common.grids(width, height)
  for r, color in enumerate(pattern):
    output[r][0] = grid[r][0] = color
  boxes = list(zip(rows, cols, wides, talls))
  for row, col, wide, tall in boxes:
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
  output = [row[:] for row in grid]

  def fill_box(box_idx):
    if box_idx >= len(boxes):
      return
    row, col, wide, tall = boxes[box_idx]
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        output[r][c] = pattern[r]

  fill_box(0)
  fill_box(1)
  fill_box(2)
  fill_box(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 5, 9], cols=[2, 8, 4], wides=[2, 2, 3], talls=[7, 7, 3],
               pattern=[0, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2]),
      generate(rows=[1, 2, 6], cols=[1, 7, 4], wides=[4, 5, 3], talls=[4, 8, 6],
               pattern=[0, 3, 3, 4, 4, 3, 4, 3, 3, 3, 4, 4]),
  ]
  test = [
      generate(rows=[0, 3, 6, 9], cols=[2, 9, 6, 2], wides=[6, 3, 3, 3],
               talls=[6, 4, 6, 3],
               pattern=[1, 8, 1, 1, 7, 7, 7, 7, 8, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
