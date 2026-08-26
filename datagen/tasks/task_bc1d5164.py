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


def generate(rows=None, cols=None, color=None, width=7, height=5, size=3,
             oheight=None, owidth=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the grid
    height: the height of the grid
    size: the size of the (square) output grid
    oheight: the number of rows in the output grid (defaults to size)
    owidth: the number of columns in the output grid (defaults to size)
  """
  if oheight is None:
    oheight = size
  if owidth is None:
    owidth = size
  if rows is None:
    pixels = common.random_pixels(width, height)
    pixels = [p for p in pixels if not (oheight - 1 <= p[0] <= height - oheight or
                                        owidth - 1 <= p[1] <= width - owidth)]
    rows, cols = zip(*pixels)
    color = common.random_color()

  grid, output = common.grid(width, height), common.grid(owidth, oheight)
  for r, c in zip(rows, cols):
    grid[r][c] = color
  for r, c in zip(rows, cols):
    if r < oheight - 1 and c < owidth - 1:
      output[r][c] = color
  for r, c in zip(rows, cols):
    if r < oheight - 1 and c > width - owidth:
      mapped_r, mapped_c = r, c - (width - owidth)
      output[mapped_r][mapped_c] = color
  for r, c in zip(rows, cols):
    if r > height - oheight and c < owidth - 1:
      mapped_r, mapped_c = r - (height - oheight), c
      output[mapped_r][mapped_c] = color
  for r, c in zip(rows, cols):
    if r > height - oheight and c > width - owidth:
      mapped_r, mapped_c = r - (height - oheight), c - (width - owidth)
      output[mapped_r][mapped_c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 4, 4],
               cols=[1, 5, 0, 1, 5, 6, 0, 1, 5, 6, 1, 5], color=8),
      generate(rows=[0, 0, 0, 0, 1, 3, 3, 4, 4],
               cols=[0, 1, 5, 6, 6, 1, 5, 0, 6], color=2),
      generate(rows=[0, 0, 0, 1, 1, 4, 4],
               cols=[0, 1, 5, 5, 6, 0, 6], color=4),
      generate(rows=[0, 0, 4, 4, 4], cols=[0, 6, 0, 5, 6], color=4),
      generate(rows=[0, 0, 1, 1, 4], cols=[1, 5, 0, 6, 6], color=3),
  ]
  test = [
      generate(rows=[0, 0, 1, 4, 4], cols=[5, 6, 0, 1, 6], color=1),
  ]
  return {"train": train, "test": test}
