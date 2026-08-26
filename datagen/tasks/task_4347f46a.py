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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None, num_boxes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of digits representing the colors to be used
    num_boxes: the requested number of boxes
  """
  if width is None:
    height = common.randint(10, 30)
    width = common.randint(10, 30)
    if num_boxes is None:
      num_boxes = common.randint(1, 9)
    while True:
      rows, cols, wides, talls = [], [], [], []
      trials = 0
      max_trials = 4 * num_boxes
      while len(rows) < num_boxes and trials <= max_trials:
        wide = common.randint(3, 7)
        tall = common.randint(3, 7)
        if wide > width - 2 or tall > height - 2:
          trials += 1
          continue  # Too big.
        row = common.randint(1, height - tall - 1)
        col = common.randint(1, width - wide - 1)
        if not common.overlaps(rows + [row], cols + [col],
                               wides + [wide], talls + [tall], 1):
          rows.append(row)
          cols.append(col)
          wides.append(wide)
          talls.append(tall)
        trials += 1
      if rows: break
    colors = common.random_colors(len(rows))

  def draw_box(idx):
    row, col, wide, tall, color = (
        rows[idx], cols[idx], wides[idx], talls[idx], colors[idx])
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = color
        output[r][c] = color
        if row < r < row + tall - 1 and col < c < col + wide - 1:
          output[r][c] = common.black()

  grid, output = common.grids(width, height)
  for idx in range(min(1, len(colors))):
    draw_box(idx)
  for idx in range(1, min(2, len(colors))):
    draw_box(idx)
  for idx in range(2, len(colors)):
    draw_box(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=18, rows=[1, 3, 10, 10], cols=[1, 6, 2, 12],
               wides=[4, 7, 7, 3], talls=[3, 5, 4, 5], colors=[8, 3, 6, 7]),
      generate(width=7, height=8, rows=[1], cols=[1], wides=[5], talls=[4],
               colors=[2]),
      generate(width=12, height=11, rows=[1, 6], cols=[2, 1], wides=[8, 6],
               talls=[4, 4], colors=[5, 4]),
  ]
  test = [
      generate(width=19, height=17, rows=[1, 1, 5, 6, 13],
               cols=[1, 11, 2, 10, 5], wides=[6, 4, 6, 8, 5],
               talls=[3, 3, 7, 6, 3], colors=[8, 6, 4, 1, 3]),
  ]
  return {"train": train, "test": test}
