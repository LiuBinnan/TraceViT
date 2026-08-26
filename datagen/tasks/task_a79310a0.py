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


def generate(size=None, rows=None, cols=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if size is None:
    size = common.randint(3, 7)
    if height is None:
      height = common.randint(2, 30)
    if width is None:
      width = common.randint(2, 30)
    sprite_h = common.randint(height // 2, (height + 1) // 2)
    sprite_w = common.randint(width // 2, (width + 1) // 2)
    row = common.randint(0, height - sprite_h - 1)
    col = common.randint(0, width - sprite_w)
    while True:
      pixels = common.random_pixels(sprite_w, sprite_h, 0.5)
      if not pixels: continue
      rows, cols = zip(*pixels)
      rows, cols = [r + row for r in rows], [c + col for c in cols]
      break
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c] = common.cyan()
  for r, c in zip(rows, cols):
    output[r + 1][c] = common.cyan()
  for r, c in zip(rows, cols):
    output[r + 1][c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0, 0, 1, 1], cols=[0, 1, 0, 1]),
      generate(size=3, rows=[0], cols=[1]),
      generate(size=5, rows=[1, 1, 1], cols=[1, 2, 3]),
  ]
  test = [
      generate(size=5, rows=[0, 1, 1, 2], cols=[2, 1, 2, 2]),
  ]
  return {"train": train, "test": test}
