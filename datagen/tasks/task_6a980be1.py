# Copyright 2026 Google LLC
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


def generate(width=None, height=None, length=None, spacing=None, col=None,
             color=None, offset=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the red boxes.
    spacing: The spacing between the red boxes.
    col: The column where the leftmost green line lies.
    color: The color of the input bofder.
    offset: The row where the red boxes start.
    xpose: Whether to transpose the grids.
  """

  if width is None:
    width, height = common.randint(12, 26), common.randint(12, 28)
    length = common.randint(1, 5)
    spacing = common.randint(2, 4)
    col = common.randint(2, width - length - 3)
    color = common.random_color(exclude=[2, 3])
    offset = common.randint(1, 2)
    xpose = common.randint(0, 1)

  def orient(ingrid):
    return common.transpose(ingrid) if xpose else ingrid

  def paint_color_bands(ingrid):
    for row in range(offset, height, length + spacing):
      for r in range(row, row + length):
        for c in range(width):
          common.draw(ingrid, r, c, color)

  def paint_green_stripes(ingrid):
    for row in range(height):
      ingrid[row][col] = 3
      ingrid[row][col + length + 1] = 3

  def paint_red_boxes(ingrid):
    for row in range(offset, height, length + spacing):
      for r in range(row, row + length):
        for c in range(col + 1, col + 1 + length):
          common.draw(ingrid, r, c, 2)

  grid = common.grid(width, height)
  paint_green_stripes(grid)
  paint_red_boxes(grid)
  common.hollow_rect(grid, width, height, 0, 0, color)
  grid = orient(grid)

  canonical_output = common.grid(width, height)
  paint_color_bands(canonical_output)
  output = orient(canonical_output)
  paint_green_stripes(canonical_output)
  output = orient(canonical_output)
  paint_red_boxes(canonical_output)
  output = orient(canonical_output)
  return {"input": grid, "output": output}

def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=18, length=3, spacing=3, col=6, color=8,
               offset=1, xpose=False),
      generate(width=14, height=18, length=2, spacing=2, col=4, color=4,
               offset=1, xpose=True),
      generate(width=15, height=19, length=1, spacing=2, col=4, color=6,
               offset=2, xpose=False),
  ]
  test = [
      generate(width=19, height=19, length=4, spacing=2, col=6, color=1,
               offset=1, xpose=True),
  ]
  return {"train": train, "test": test}
