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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    colors: A list of colors to use.
  """

  if width is None or height is None or colors is None:
    if width is None:
      max_half_width = 4 if height is None else min(4, 30 // height)
      min_half_width = 2 if height == 2 else 1
      width = 2 * common.randint(min_half_width, max_half_width)
    if height is None:
      max_half_height = min(4, 30 // width)
      min_half_height = 2 if width == 2 else 1
      height = 2 * common.randint(min_half_height, max_half_height)
    if colors is None:
      colors = common.choices(list(range(10)), width * height)
      colors = "".join(str(c) for c in colors)

  size = width * height // 2

  # Input: the width x height grid of colors.
  grid = common.grid(width, height)
  for row in range(height):
    for col in range(width):
      grid[row][col] = int(colors[row * width + col])

  # Output: a size x size kaleidoscope. First roll the input into the two
  # central columns, then fan that strip outward into the four quadrants.
  output = common.grid(size, size)

  def fold_to_center():
    """Rolls each input cell into the output's two central columns."""
    for row in range(height):
      for col in range(width):
        color = grid[row][col]
        pair = (row // 2) * (width // 2) + col // 2
        if row % 2 == 0:
          r = size // 2 - 1 - pair
        else:
          r = size // 2 + pair
        c = size // 2 - 1 + col % 2
        output[r][c] = color

  def fan_quadrant(q):
    """Fans the central strip into quadrant q (0=TL, 1=TR, 2=BL, 3=BR)."""
    half = size // 2
    row_range = range(half) if q < 2 else range(half, size)
    col_range = range(half) if q % 2 == 0 else range(half, size)
    for row in row_range:
      for col in col_range:
        if q == 0:
          r, c = min(row, col), half - 1
        elif q == 1:
          r, c = min(row, size - 1 - col), half
        elif q == 2:
          r, c = size - 1 - min(size - 1 - row, col), half - 1
        else:
          r, c = size - 1 - min(size - 1 - row, size - 1 - col), half
        output[row][col] = output[r][c]

  fold_to_center()
  fan_quadrant(0)
  fan_quadrant(1)
  fan_quadrant(2)
  fan_quadrant(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=6, colors="139455289831401423653980"),
      generate(width=6, height=4, colors="911779207703287721539778"),
  ]
  test = [
      generate(width=4, height=4, colors="6975588701268743"),
  ]
  return {"train": train, "test": test}
