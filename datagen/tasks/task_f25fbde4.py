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


def generate(rows=None, cols=None, row=None, col=None, size=9, height=None,
             width=None, shape_height=None, shape_width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical offset for the submarine
    col: a horizontal offset for the submarine
    size: the width and height of the (square) grid
    height: the height of the input grid (defaults to size for fixed examples)
    width: the width of the input grid (defaults to size for fixed examples)
    shape_height: the height of the shape sampling area
    shape_width: the width of the shape sampling area
    count: the number of cells in the connected shape
  """
  if rows is None:
    if height is None:
      height = common.randint(2, 30)
    if width is None:
      width = common.randint(2, 30)
    max_shape_height = min(15, height - 1)
    max_shape_width = min(15, width - 1)
    if shape_height is None:
      shape_height = common.randint(1, max_shape_height)
    if shape_width is None:
      shape_width = common.randint(1, max_shape_width)
    shape_height = min(max(1, shape_height), max_shape_height)
    shape_width = min(max(1, shape_width), max_shape_width)
    max_count = max(1, min(shape_height * shape_width,
                           shape_height * shape_width // 2 + 1))
    if count is None:
      count = common.randint(1, max_count)
    count = min(max(1, count), max_count)
    pixels = {common.choice(common.all_pixels(shape_width, shape_height))}
    for _ in range(count - 1):
      candidates = []
      for pr, pc in pixels:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
              continue
            pixel = (pr + dr, pc + dc)
            if pixel in pixels:
              continue
            if 0 <= pixel[0] < shape_height and 0 <= pixel[1] < shape_width:
              candidates.append(pixel)
      pixels.add(common.choice(sorted(set(candidates))))
    rows, cols = zip(*pixels)
    rows, cols = [r - min(rows) for r in rows], [c - min(cols) for c in cols]
    shape_height, shape_width = max(rows) + 1, max(cols) + 1
    if row is None:
      row = common.randint(0, height - shape_height)
    if col is None:
      col = common.randint(0, width - shape_width)
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  shape_width, shape_height = max(cols) + 1, max(rows) + 1
  row = min(max(0, row), height - shape_height)
  col = min(max(0, col), width - shape_width)
  grid = common.grid(width, height)
  output = common.grid(2 * shape_width, 2 * shape_height)
  for r, c in zip(rows, cols):
    grid[row + r][col + c] = common.yellow()
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[2 * r + dr][2 * c + dc] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 2, 2], cols=[1, 2, 0, 1, 2, 3, 1, 2],
               row=2, col=1),
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 2], row=1, col=3),
      generate(rows=[0, 1, 1, 2, 3, 3], cols=[1, 0, 1, 1, 1, 2], row=4, col=1),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[1, 3, 0, 2, 4, 1, 3], row=1,
               col=3),
  ]
  return {"train": train, "test": test}
