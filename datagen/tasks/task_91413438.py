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


def generate(rows=None, cols=None, color=None, size=3, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    # The output tiles the input across a voids x voids arrangement, where
    # voids = height*width - len(rows); the result is (height*voids) x
    # (width*voids). Pick the pixel count so that (a) both output extents stay
    # <= 30 and (b) the len(rows) copies fit the voids x voids grid
    # (len(rows) <= voids*voids), exactly mirroring the original square rule.
    cells = height * width
    maxdim = max(height, width)
    choices = []
    for voids in range(1, cells):
      if maxdim * voids > 30:
        continue
      npix = cells - voids
      if 1 <= npix <= voids * voids:
        choices.append(npix)
    num_pixels = choices[common.randint(0, len(choices) - 1)]
    pixels = common.sample(common.all_pixels(width, height), num_pixels)
    rows, cols = zip(*pixels)
    color = common.random_color()

  voids = height * width - len(rows)
  mega_height, mega_width = height * voids, width * voids
  grid, output = common.grid(width, height), common.grid(mega_width, mega_height)
  for r, c in zip(rows, cols):
    grid[r][c] = color
  for i in range(len(rows)):
    row, col = i // voids, i % voids
    for r, c in zip(rows, cols):
      output[row * height + r][col * width + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 1, 1, 2, 2], color=6),
      generate(rows=[0, 1, 1, 2], cols=[1, 1, 2, 0], color=4),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 2, 0, 2, 1, 2], color=3),
      generate(rows=[0, 0, 1], cols=[0, 2, 1], color=2),
  ]
  test = [
      generate(rows=[0, 1], cols=[2, 1], color=8),
  ]
  return {"train": train, "test": test}
