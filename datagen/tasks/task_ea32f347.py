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


def generate(rows=None, cols=None, lengths=None, ups=None, size=10,
             colors=(2, 4, 1), height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of line lengths (in increasing order)
    ups: a list of 0/1 values indicating whether the lines are standing up
    size: the width and height of the (square) grid (square fallback)
    colors: the colors of the three lines
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    lengths = common.sample(range(2, 10), 3)
    lengths.sort()
    ups = [common.randint(0, 1) for _ in lengths]
    while True:
      # Keep choosing coordinates until the lines don't overlap.
      # For a vertical line (up=1) the line extends along rows -> the variable
      # (start) coordinate is the row, clamped by height; the fixed coordinate
      # is the column, clamped by width. For a horizontal line (up=0) it is the
      # other way around.
      rows = [common.randint(0, height - lengths[idx]) if ups[idx]
              else common.randint(0, height - 1) for idx in range(len(ups))]
      cols = [common.randint(0, width - 1) if ups[idx]
              else common.randint(0, width - lengths[idx])
              for idx in range(len(ups))]
      overlaps = False
      for j in range(len(lengths)):
        for i in range(len(lengths)):
          if i == j: continue
          if ups[i] == 1 and ups[j] == 1:
            overlaps = overlaps or abs(cols[j] - cols[i]) < 2
          if ups[i] == 0 and ups[j] == 0:
            overlaps = overlaps or abs(rows[j] - rows[i]) < 2
          if ups[i] == 1 and ups[j] == 0:  # Don't need to handle fourth case!
            if rows[i] > rows[j] + 1: continue
            if rows[i] + lengths[i] + 1 < rows[j]: continue
            if cols[i] + 1 < cols[j]: continue
            if cols[j] + lengths[j] + 1 < cols[i]: continue
            overlaps = True
      if not overlaps: break

  grid, output = common.grids(width, height)
  for idx in range(min(1, len(rows))):
    r, c, length, up = rows[idx], cols[idx], lengths[idx], ups[idx]
    for i in range(length):
      rr, cc = r + (i if up else 0), c + (0 if up else i)
      grid[rr][cc] = common.gray()
      output[rr][cc] = colors[idx]
  for idx in range(1, min(2, len(rows))):
    r, c, length, up = rows[idx], cols[idx], lengths[idx], ups[idx]
    for i in range(length):
      rr, cc = r + (i if up else 0), c + (0 if up else i)
      grid[rr][cc] = common.gray()
      output[rr][cc] = colors[idx]
  for idx in range(2, len(rows)):
    r, c, length, up = rows[idx], cols[idx], lengths[idx], ups[idx]
    for i in range(length):
      rr, cc = r + (i if up else 0), c + (0 if up else i)
      grid[rr][cc] = common.gray()
      output[rr][cc] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[4, 2, 1], cols=[7, 4, 1], lengths=[3, 5, 6],
               ups=[1, 1, 1]),
      generate(rows=[5, 3, 1], cols=[7, 1, 4], lengths=[2, 4, 6],
               ups=[1, 1, 1]),
      generate(rows=[7, 3, 2], cols=[2, 7, 0], lengths=[3, 5, 6],
               ups=[0, 1, 0]),
      generate(rows=[2, 5, 1], cols=[1, 1, 7], lengths=[4, 5, 7],
               ups=[0, 0, 1]),
  ]
  test = [
      generate(rows=[1, 8, 5], cols=[3, 0, 4], lengths=[3, 5, 6],
               ups=[1, 0, 0]),
  ]
  return {"train": train, "test": test}
