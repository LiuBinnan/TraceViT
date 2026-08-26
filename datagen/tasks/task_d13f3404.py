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


def generate(rows=None, cols=None, colors=None, size=3, height=None, width=None,
             num=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digits representing colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the (rectangular) grid
    width: the number of columns of the (rectangular) grid
    num: how many pixels (each on a distinct down-right diagonal) to place
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    rows, cols, diags = [], [], []
    for (r, c) in common.shuffle(common.all_pixels(width, height)):
      diag = c - r
      if diag in diags: continue
      diags.append(diag)
      rows.append(r)
      cols.append(c)
    # Number of pixels: re_arc samples uniformly over [1, #distinct-diagonals]
    # (= width + height - 1 = len(rows)); each pixel takes an independent
    # non-background color (repeats allowed), so the color count varies too.
    if num is None:
      num = common.randint(1, len(rows))
    num = min(num, len(rows))
    rows, cols = rows[:num], cols[:num]
    colors = [common.random_color() for _ in range(num)]

  grid, output = common.grid(width, height), common.grid(2 * width, 2 * height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  for r, c, color in zip(rows[:1], cols[:1], colors[:1]):
    for idx in range(min(2 * height - r, 2 * width - c)):
      output[r + idx][c + idx] = color
  for r, c, color in zip(rows[1:2], cols[1:2], colors[1:2]):
    for idx in range(min(2 * height - r, 2 * width - c)):
      output[r + idx][c + idx] = color
  for r, c, color in zip(rows[2:3], cols[2:3], colors[2:3]):
    for idx in range(min(2 * height - r, 2 * width - c)):
      output[r + idx][c + idx] = color
  for r, c, color in zip(rows[3:], cols[3:], colors[3:]):
    for idx in range(min(2 * height - r, 2 * width - c)):
      output[r + idx][c + idx] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1], cols=[0, 1, 0], colors=[6, 1, 3]),
      generate(rows=[0, 1, 2], cols=[1, 1, 0], colors=[4, 8, 2]),
      generate(rows=[0, 1, 1], cols=[2, 0, 1], colors=[6, 1, 3]),
  ]
  test = [
      generate(rows=[0, 2, 2], cols=[2, 1, 2], colors=[3, 4, 9]),
  ]
  return {"train": train, "test": test}
