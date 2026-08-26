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


def generate(rows=None, cols=None, size=3, height=None, width=None,
             num_colors=None, pixel_colors=None):
  """Returns input and output grids according to the given parameters.

  The transformation is unchanged: the output is the input grid concatenated
  with its own left-right mirror (hconcat(input, vmirror(input))).

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid, used by the explicit path
    height: number of rows in the random input grid (decoupled from width)
    width: number of columns in the random input grid (output is 2 * width wide)
    num_colors: how many distinct non-background colors to scatter
    pixel_colors: per-pixel colors parallel to rows/cols
  """
  if rows is None:
    # Sample height and width independently so the mirrored output varies in
    # both axes (re_arc: h in 1..30, w in 1..15 keeps the 2 * width output
    # within the 30-cell cap).
    if height is None:
      height = common.randint(1, 30)
    if width is None:
      width = common.randint(1, 15)
    # Number of distinct colors, area-scaled like re_arc (0..min(9, h * w)).
    if num_colors is None:
      num_colors = common.randint(0, min(9, height * width))
    rows, cols, pixel_colors = [], [], []
    inds = [(r, c) for r in range(height) for c in range(width)]
    for color in common.random_colors(num_colors):
      num = common.randint(1, max(1, len(inds) // max(1, num_colors)))
      chosen = common.sample(inds, num)
      chosen_set = set(chosen)
      for r, c in chosen:
        rows.append(r)
        cols.append(c)
        pixel_colors.append(color)
      inds = [ind for ind in inds if ind not in chosen_set]
  else:
    height = width = size
    if pixel_colors is None:
      pixel_colors = [common.orange()] * len(rows)

  grid, output = common.grid(width, height), common.grid(2 * width, height)
  for r, c, color in zip(rows, cols, pixel_colors):
    output[r][2 * width - 1 - c] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2, 2], cols=[1, 2, 1, 2]),
      generate(rows=[1, 1], cols=[1, 2]),
      generate(rows=[1], cols=[0]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 1, 2]),
  ]
  return {"train": train, "test": test}
