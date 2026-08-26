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


def _unique(pixels):
  """Returns pixels with duplicates removed while preserving order."""
  result = []
  for pixel in pixels:
    if pixel not in result: result.append(pixel)
  return result


def _draw(grid, pixels, row, col, color):
  for dr, dc in pixels:
    grid[row + dr][col + dc] = color


def _normalize(pixels):
  row0 = min(r for r, _ in pixels)
  col0 = min(c for _, c in pixels)
  return [(r - row0, c - col0) for r, c in pixels]


def generate(rows=None, cols=None, colors=None, size=13, minisize=4,
             height=None, width=None, output_height=None, output_width=None,
             split_rows=None, split_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) input grid
    minisize: the width and height of the (square) output grid
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
    output_height: the number of rows of the output grid
    output_width: the number of columns of the output grid
    split_rows: the row cutoffs for the left and right border fragments
    split_cols: the column cutoffs for the top and bottom border fragments
  """
  randomize = rows is None
  if randomize:
    if output_height is None: output_height = common.randint(4, 15)
    if output_width is None: output_width = common.randint(4, 15)
    if height is None: height = common.randint(2 * output_height, 30)
    if width is None: width = common.randint(2 * output_width, 30)
    height = max(height, 2 * output_height)
    width = max(width, 2 * output_width)
    colors = common.random_colors(4) if colors is None else colors
  else:
    if output_height is None: output_height = minisize
    if output_width is None: output_width = minisize
    if height is None: height = size
    if width is None: width = size
  if split_rows is None:
    mid = max(2, min(output_height - 2, output_height // 2))
    split_rows = [mid, mid]
    if randomize:
      split_rows = [common.randint(2, output_height - 2) for _ in range(2)]
  if split_cols is None:
    mid = max(2, min(output_width - 2, output_width // 2))
    split_cols = [mid, mid]
    if randomize:
      split_cols = [common.randint(2, output_width - 2) for _ in range(2)]
  upper_left = _unique([(r, 0) for r in range(split_rows[0])] +
                       [(0, c) for c in range(split_cols[0])])
  upper_right = _unique([(0, c) for c in range(split_cols[0], output_width)] +
                        [(r, output_width - 1) for r in range(split_rows[1])])
  lower_left = _unique([(r, 0) for r in range(split_rows[0], output_height)] +
                       [(output_height - 1, c) for c in range(split_cols[1])])
  lower_right = _unique(
      [(output_height - 1, c) for c in range(split_cols[1], output_width)] +
      [(r, output_width - 1) for r in range(split_rows[1], output_height)])
  output_objects = [upper_left, upper_right, lower_left, lower_right]
  input_objects = [_normalize(obj) for obj in output_objects]
  if rows is None:
    while True:
      rows, cols, occupied = [], [], set()
      for obj in input_objects:
        tall = max(r for r, _ in obj) + 1
        wide = max(c for _, c in obj) + 1
        row = common.randint(0, height - tall)
        col = common.randint(0, width - wide)
        shifted = {(r + row, c + col) for r, c in obj}
        if occupied & shifted: break
        rows.append(row)
        cols.append(col)
        occupied |= shifted
      if len(rows) == 4: break

  grid = common.grid(width, height)
  output = common.grid(output_width, output_height)
  _draw(output, output_objects[0], 0, 0, colors[0])
  _draw(grid, input_objects[0], rows[0], cols[0], colors[0])
  _draw(output, output_objects[1], 0, 0, colors[1])
  _draw(grid, input_objects[1], rows[1], cols[1], colors[1])
  _draw(output, output_objects[2], 0, 0, colors[2])
  _draw(grid, input_objects[2], rows[2], cols[2], colors[2])
  _draw(output, output_objects[3], 0, 0, colors[3])
  _draw(grid, input_objects[3], rows[3], cols[3], colors[3])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3, 9, 7], cols=[6, 1, 3, 7], colors=[8, 2, 3, 1]),
      generate(rows=[3, 1, 9, 5], cols=[2, 8, 4, 7], colors=[1, 8, 4, 2]),
  ]
  test = [
      generate(rows=[9, 2, 6, 2], cols=[2, 10, 6, 2], colors=[3, 8, 1, 6]),
  ]
  return {"train": train, "test": test}
