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


def generate(width=None, height=None, wides=None, talls=None, rows=None,
             cols=None, colors=None, canvas_width=None, canvas_height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the boxes.
    canvas_width: Optional width used when sampling a new example.
    canvas_height: Optional height used when sampling a new example.
  """

  if width is None:
    width = (15 + common.randint(-1, 1)
             if canvas_width is None else canvas_width)
    height = (15 + common.randint(-1, 1)
              if canvas_height is None else canvas_height)
    wides, talls, rows, cols = [], [], [], []
    wides.append(common.randint(7, width - 3))
    talls.append(common.randint(7, height - 3))
    rows.append(common.randint(1, height - talls[0] - 1))
    cols.append(common.randint(1, width - wides[0] - 1))
    wides.append(common.randint(5, wides[0] - 2))
    talls.append(common.randint(5, talls[0] - 2))
    rows.append(common.randint(1, talls[0] - talls[1] - 1))
    cols.append(common.randint(1, wides[0] - wides[1] - 1))
    while True:
      colors = common.random_colors(4, exclude=[8])
      for i in range(4):
        if common.randint(0, 3) == 0: colors[i] = -1
      if colors[0] + colors[1] == -2 or colors[2] + colors[3] == -2: continue
      if colors[0] + colors[2] == -2 or colors[1] + colors[3] == -2: continue
      break

  grid, output = common.grid(width, height), common.grid(2, 2)
  common.rect(grid, wides[0], talls[0], rows[0], cols[0], 8)
  if colors[0] >= 0: common.rect(grid, 2, 2, sum(rows), sum(cols), colors[0])
  if colors[1] >= 0: common.rect(grid, 2, 2, sum(rows), sum(cols) + wides[1] - 2, colors[1])
  if colors[2] >= 0: common.rect(grid, 2, 2, sum(rows) + talls[1] - 2, sum(cols), colors[2])
  if colors[3] >= 0: common.rect(grid, 2, 2, sum(rows) + talls[1] - 2, sum(cols) + wides[1] - 2, colors[3])

  def extract_corner(i):
    """Reads one inner-rectangle corner marker into the 2x2 output."""
    out_row, out_col = i // 2, i % 2
    row = sum(rows) + out_row * (talls[1] - 2)
    col = sum(cols) + out_col * (wides[1] - 2)
    color = grid[row][col]
    if color != common.cyan():
      output[out_row][out_col] = color

  extract_corner(0)
  extract_corner(1)
  extract_corner(2)
  extract_corner(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=16, wides=[13, 7], talls=[10, 5], rows=[2, 2],
               cols=[1, 2], colors=[1, 3, -1, 2]),
      generate(width=15, height=13, wides=[8, 6], talls=[8, 6], rows=[1, 1],
               cols=[2, 1], colors=[2, -1, -1, 3]),
      generate(width=16, height=14, wides=[9, 6], talls=[12, 7], rows=[1, 2],
               cols=[1, 1], colors=[5, 4, 3, -1]),
  ]
  test = [
      generate(width=15, height=14, wides=[12, 8], talls=[10, 6], rows=[3, 3],
               cols=[2, 2], colors=[2, 6, 1, 3]),
  ]
  return {"train": train, "test": test}
