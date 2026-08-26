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


def generate(col=None, color=None, size=10, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    col: a horizontal coordinate where the pixel should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if col is None:
    col = common.randint(0, width - 1)
    color = common.random_color(exclude=[common.gray()])

  grid = common.grid(width, height)
  row = height - 1
  grid[row][col] = color
  colored_segments, gray_connectors = [], []
  while col < width:
    d = -1 if row else 1
    segment = []
    segment.append((row, col, color))
    while row + d >= 0 and row + d < height:
      row += d
      segment.append((row, col, color))
    colored_segments.append(segment)
    col += 1
    if col >= width: break
    gray_connectors.append((row, col))
    col += 1
  output = [r[:] for r in grid]

  def draw_colored_path():
    for segment in colored_segments:
      for r, c, cell_color in segment:
        output[r][c] = cell_color

  def draw_gray_connectors():
    for r, c in gray_connectors:
      output[r][c] = common.gray()

  draw_colored_path()
  draw_gray_connectors()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(col=1, color=2),
      generate(col=5, color=3),
      generate(col=4, color=4),
  ]
  test = [
      generate(col=2, color=1),
  ]
  return {"train": train, "test": test}
