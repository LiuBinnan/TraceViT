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


def generate(width=None, height=None, colors=None, num_colors=None,
             blank_weight=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
    num_colors: The number of nonzero colors available to random instances.
    blank_weight: The relative sampling weight of black logical cells.
  """

  if width is None:
    width, height = common.randint(1, 4), common.randint(1, 4)
    if num_colors is None:
      num_colors = common.randint(3, 6)
    if blank_weight is None:
      blank_weight = 1
    subset = common.random_colors(num_colors)
    while True:
      colors = common.choices(subset + [0] * blank_weight, width * height)
      good = True
      # Let's avoid a square where they're all the same color.
      for row in range(1, height):
        for col in range(1, width):
          if colors[row * width + col] != colors[row * width + col - 1]:
            continue
          if colors[row * width + col] != colors[(row - 1) * width + col]:
            continue
          if colors[row * width + col] != colors[(row - 1) * width + col - 1]:
            continue
          good = False
      # Let's also make sure no row or column is blank.
      for row in range(height):
        if sum([colors[row * width + col] for col in range(width)]) == 0:
          good = False
      for col in range(width):
        if sum([colors[row * width + col] for row in range(height)]) == 0:
          good = False
      if good: break

  wide, tall = (24 - 2 * width) // width, (24 - 2 * height) // height
  grid = common.grid(2 * width + 1, 2 * height + 1)
  # First, draw the squares themselves.
  for row in range(height):
    for col in range(width):
      color = colors[row * width + col]
      grid[2 * row + 1][2 * col + 1] = color
  output = common.grid(26, 26)
  taken = common.grid(width, height)

  def draw_square_row(row):
    """Draws one row of expanded colored squares."""
    if row >= height:
      return
    for col in range(width):
      color = colors[row * width + col]
      r, c = (2 + tall) * row + 2, (2 + wide) * col + 2
      common.rect(output, wide, tall, r, c, color)

  def connect_horizontal_row(row):
    """Draws same-color horizontal bridges for one input row."""
    if row >= height:
      return
    for col in range(1, width):
      color = colors[row * width + col]
      if color != colors[row * width + col - 1]: continue
      taken[row][col] = taken[row][col - 1] = 1
      r, c = (2 + tall) * row + 2, (2 + wide) * col
      common.rect(output, 2, tall, r, c, color)

  def connect_vertical_column(col):
    """Draws same-color vertical bridges for one input column."""
    if col >= width:
      return
    for row in range(1, height):
      color = colors[row * width + col]
      if color != colors[(row - 1) * width + col]: continue
      if taken[row][col] or taken[row - 1][col]: continue
      r, c = (2 + tall) * row, (2 + wide) * col + 2
      common.rect(output, wide, 2, r, c, color)

  draw_square_row(0)
  draw_square_row(1)
  draw_square_row(2)
  draw_square_row(3)
  connect_horizontal_row(0)
  connect_horizontal_row(1)
  connect_horizontal_row(2)
  connect_horizontal_row(3)
  connect_vertical_column(0)
  connect_vertical_column(1)
  connect_vertical_column(2)
  connect_vertical_column(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=4, colors=[4, 4, 6, 0, 8, 8, 8, 4]),
      generate(width=3, height=2, colors=[8, 6, 3, 8, 4, 4]),
      generate(width=4, height=4,
               colors=[4, 8, 8, 8, 4, 4, 6, 8, 8, 3, 8, 8, 0, 8, 0, 8]),
      generate(width=1, height=2, colors=[6, 4]),
  ]
  test = [
      generate(width=3, height=3, colors=[6, 3, 4, 8, 1, 7, 8, 7, 7]),
  ]
  return {"train": train, "test": test}
