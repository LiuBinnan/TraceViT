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


def generate(colors=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    size: The even height and width of the square grid.
  """

  if colors is None:
    if size is None:
      size = 2 * common.randint(2, 4)
    colors = [6] * (size * size)
    for _ in range(size * size // 2 - 1):
      colors[common.randint(0, size * size - 1)] = common.choice(
          [0, 1, 3, 4, 5, 6, 7, 8, 9])
    colors[common.randint(0, size * size - 1)] = 2
  elif size is None:
    size = 4

  grid, output = common.grids(size, size, 6)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color

  def reveal_marker():
    """Copies the lone red locator pixel onto the blank canvas."""
    for i, color in enumerate(colors):
      if color == common.red():
        output[i // size][i % size] = common.red()

  def fill_quadrant():
    """Expands the red pixel to fill the quadrant it lands in."""
    for i, color in enumerate(colors):
      if color != common.red(): continue
      row, col = i // size, i % size
      half = size // 2
      r, c = 0 if row < half else half, 0 if col < half else half
      for out_row in range(r, r + half):
        for out_col in range(c, c + half):
          output[out_row][out_col] = common.red()

  reveal_marker()
  fill_quadrant()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 6, 6, 6, 6, 9, 6, 1, 4, 6, 6, 2, 6, 6, 5, 6]),
      generate(colors=[5, 6, 0, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 4]),
      generate(colors=[6, 9, 0, 0, 9, 6, 1, 6, 6, 6, 6, 1, 8, 6, 6, 2]),
  ]
  test = [
      generate(colors=[2, 6, 8, 1, 6, 6, 6, 6, 4, 6, 9, 9, 0, 5, 6, 6]),
  ]
  return {"train": train, "test": test}
