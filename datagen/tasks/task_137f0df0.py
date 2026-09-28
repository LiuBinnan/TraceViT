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


def generate(rows=None, cols=None, size=None, spacing_max=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    size: The height and width of the square grid.
    spacing_max: The largest step between consecutive box positions.
  """

  if rows is None:
    if size is None:
      size = common.randint(8, 30)
    if spacing_max is None:
      spacing_max = common.randint(4, 8)
    row, col = common.randint(0, 2), common.randint(0, 2)
    rows, cols = [row], [col]
    while size - 2 - row >= 3:
      row += common.randint(3, min(spacing_max, size - 2 - row))
      rows.append(row)
    while size - 2 - col >= 3:
      col += common.randint(3, min(spacing_max, size - 2 - col))
      cols.append(col)

  grid, output = common.grids(10 if size is None else size,
                              10 if size is None else size)
  for row in rows:
    for col in cols:
      for r in range(2):
        for c in range(2):
          grid[row + r][col + c] = 5

  def paint_horizontal_gap_guides():
    """Marks the rows that separate consecutive box rows."""
    for i in range(1, len(rows)):
      for row in range(rows[i - 1] + 2, rows[i]):
        for col in range(len(output[0])):
          output[row][col] = 1

  def paint_vertical_gap_guides():
    """Marks the columns that separate consecutive box columns."""
    for i in range(1, len(cols)):
      for col in range(cols[i - 1] + 2, cols[i]):
        for row in range(len(output)):
          output[row][col] = 1

  def fill_box_envelope():
    """Fills the rectangle spanned by the corner boxes."""
    for row in range(rows[0], rows[-1] + 2):
      for col in range(cols[0], cols[-1] + 2):
        output[row][col] = 2

  def restore_boxes():
    """Places the original gray boxes on top of the filled envelope."""
    for row in rows:
      for col in cols:
        for r in range(2):
          for c in range(2):
            output[row + r][col + c] = 5

  paint_horizontal_gap_guides()
  paint_vertical_gap_guides()
  fill_box_envelope()
  restore_boxes()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 3, 6], cols=[2, 6]),
      generate(rows=[0, 3, 6], cols=[0, 3, 6]),
      generate(rows=[0, 4, 8], cols=[1, 4, 7]),
  ]
  test = [
      generate(rows=[1, 4, 7], cols=[1, 5, 8]),
  ]
  return {"train": train, "test": test}
