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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None,
             xpose=None, size=10, count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    colors: a list of colors of the boxes
    xpose: whether to transpose the grid
    size: the width and height of the (square) grid
    count: number of boxes to place when rows/cols are omitted
    num_colors: number of distinct box colors to use when colors are omitted
  """
  if rows is None:
    if count is None:
      count = common.randint(1, 9)
    if num_colors is None:
      num_colors = count
    count = max(1, min(count, num_colors, 9))
    rows, cols, wides, talls, areas = [], [], [], [], []
    colors = common.random_colors(count)
    occupied = set()
    trials, maxtrials = 0, 8 * count
    while len(rows) < count and trials <= maxtrials:
      tall, wide = common.randint(3, 7), common.randint(3, 7)
      if tall > size or wide > size:
        trials += 1
        continue
      area = tall * wide
      if area in areas:
        trials += 1
        continue
      row = common.randint(0, size - tall)
      col = common.randint(0, size - wide)
      box = set()
      for r in range(row, row + tall):
        box.add((r, col))
        box.add((r, col + wide - 1))
      for c in range(col, col + wide):
        box.add((row, c))
        box.add((row + tall - 1, c))
      if occupied.intersection(box):
        trials += 1
        continue
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
      areas.append(area)
      occupied.update(box)
      trials += 1
    colors = colors[:len(rows)]
    if xpose is None:
      xpose = common.randint(0, 1)

  grid, output = common.grid(size, size), common.grid(2, 2)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      grid[r][col + wide - 1] = grid[r][col] = color
    for c in range(col, col + wide):
      grid[row][c] = grid[row + tall - 1][c] = color
  winner = max(range(len(wides)), key=lambda idx: wides[idx] * talls[idx])
  if xpose: grid = common.transpose(grid)
  output = [row[:] for row in grid]
  output = common.grid(size, size)
  row, col, wide, tall, color = rows[winner], cols[winner], wides[winner], talls[winner], colors[winner]
  for r in range(row, row + tall):
    output[r][col + wide - 1] = output[r][col] = color
  for c in range(col, col + wide):
    output[row][c] = output[row + tall - 1][c] = color
  if xpose: output = common.transpose(output)
  output = common.grid(2, 2, colors[winner])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 5], cols=[1, 3], wides=[4, 5], talls=[4, 4],
               colors=[7, 8], xpose=0),
      generate(rows=[0, 5], cols=[0, 2], wides=[5, 6], talls=[4, 4],
               colors=[6, 7], xpose=0),
      generate(rows=[0, 7], cols=[1, 7], wides=[6, 3], talls=[7, 3],
               colors=[4, 2], xpose=0),
  ]
  test = [
      generate(rows=[0, 6], cols=[0, 0], wides=[9, 10], talls=[5, 4],
               colors=[3, 9], xpose=1),
  ]
  return {"train": train, "test": test}
