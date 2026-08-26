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


def _paint_box(output, row, col):
  for rr in range(row - 1, row + 2):
    for cc in range(col - 1, col + 2):
      output[rr][cc] = common.blue()


def generate(rows=None, cols=None, size=3, height=None, width=None,
             density=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of each (square) cell block
    height: the number of block-rows in the grid (defaults to size)
    width: the number of block-cols in the grid (defaults to size)
    density: optional marker density percent for synthetic examples
    count: optional number of marker pixels for synthetic examples
  """
  if rows is None and (height is not None or width is not None or
                       density is not None or count is not None):
    if height is None: height = common.randint(3, 30)
    if width is None: width = common.randint(3, 30)
    grid, output = common.grids(width, height)
    candidates = []
    for r in range(1, height - 1):
      for c in range(1, width - 1):
        candidates.append((r, c))
    max_count = min(len(candidates), max(1, (height * width) // 3))
    if count is None:
      if density is None:
        count = common.randint(1, max_count)
      else:
        count = max(1, round(height * width * density / 100))
    count = min(max_count, count)
    for r, c in common.sample(candidates, count):
      grid[r][c] = common.gray()
      _paint_box(output, r, c)
    return {"input": grid, "output": output}

  if height is None: height = size
  if width is None: width = size
  if rows is None:
    while True:
      pixels = common.random_pixels(width, height)
      if pixels: break
    rows, cols = zip(*pixels)

  grid = common.grid(width * size, height * size)
  output = common.grid(width * size, height * size)
  for r, c in zip(rows, cols):
    grid[size * r + 1][size * c + 1] = common.gray()
    for rr in range(size):
      for cc in range(size):
        output[size * r + rr][size * c + cc] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2], cols=[0, 1, 2]),
      generate(rows=[0, 1, 2, 2], cols=[1, 1, 1, 2]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[2, 0, 2, 0]),
  ]
  return {"train": train, "test": test}
