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


def generate(brow=None, bcol=None, colors=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brow: The row of the box.
    bcol: The column of the box.
    colors: The colors of the pixels.
    size: The side length of the selected quadrant.
  """

  if brow is None:
    if size is None:
      size = common.randint(3, 6)
    brow, bcol = common.randint(0, size), common.randint(0, size)
    subset = common.random_colors(common.randint(3, 6))
    while True:
      rows, cols = common.conway_sprite(size, size, 10)
      pixels = sorted(set(zip(rows, cols)))
      if common.diagonally_connected(pixels): break
    colors = [0] * (size * size)
    for row, col in pixels:
      colors[row * size + col] = colors[col * size + row] = common.choice(subset)

  size = 4 if size is None else size
  grid = common.grid(3 * size, 3 * size)
  for i, color in enumerate(colors):
    row, col = i // size, i % size
    grid[brow + row][bcol + col] = color
    grid[brow + row][bcol + 2 * size - 1 - col] = color
    grid[brow + 2 * size - 1 - row][bcol + col] = color
    grid[brow + 2 * size - 1 - row][bcol + 2 * size - 1 - col] = color

  output = common.grid(size, size)
  for i, color in enumerate(colors[:size * size // 2]):
    output[i // size][i % size] = color

  for i, color in enumerate(colors[size * size // 2:],
                            start=size * size // 2):
    output[i // size][i % size] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brow=2, bcol=2,
               colors=[0, 0, 0, 2, 0, 5, 5, 2, 0, 5, 3, 3, 2, 2, 3, 1]),
      generate(brow=0, bcol=0,
               colors=[0, 0, 0, 2, 0, 0, 2, 2, 0, 2, 3, 1, 2, 2, 1, 0]),
      generate(brow=4, bcol=4,
               colors=[0, 7, 7, 0, 7, 2, 2, 3, 7, 2, 8, 8, 0, 3, 8, 0]),
  ]
  test = [
      generate(brow=0, bcol=2,
               colors=[1, 0, 0, 5, 0, 5, 3, 8, 0, 3, 2, 8, 5, 8, 8, 6]),
  ]
  return {"train": train, "test": test}
