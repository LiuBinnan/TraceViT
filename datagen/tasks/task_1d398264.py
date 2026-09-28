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


def generate(size=None, colors=None, brow=None, bcol=None, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
    brow: The row of the box.
    bcol: The column of the box.
    height: The height of the grid, or size for a square grid.
    width: The width of the grid, or size for a square grid.
  """

  if size is None:
    if height is None and width is None:
      size = common.randint(10, 28)
      height, width = size, size
    else:
      if height is None:
        height = common.randint(10, 28)
      if width is None:
        width = common.randint(10, 28)
    center = common.random_color()
    colors = [common.random_color(exclude=[center])
              for _ in range(height * width)]
    colors[4] = center
    brow = common.randint(1, height - 4)
    bcol = common.randint(1, width - 4)
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid = common.grid(width, height)
  for row in [-1, 0, 1]:
    for col in [-1, 0, 1]:
      r, c = brow + row + 1, bcol + col + 1
      color = colors[(row + 1) * 3 + col + 1]
      grid[r][c] = color
  output = common.deepcopy(grid)
  rays = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
          (1, 0), (1, 1)]

  def extend_ray(index):
    """Extends one non-center seed color along its compass ray."""
    row, col = rays[index]
    r, c = brow + row + 1, bcol + col + 1
    color = colors[(row + 1) * 3 + col + 1]
    r, c = r + row, c + col
    while r >= 0 and c >= 0 and r < height and c < width:
      output[r][c] = color
      r, c = r + row, c + col

  extend_ray(0)
  extend_ray(1)
  extend_ray(2)
  extend_ray(3)
  extend_ray(4)
  extend_ray(5)
  extend_ray(6)
  extend_ray(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, colors=[6, 2, 2, 4, 5, 4, 6, 8, 8], brow=6, bcol=15),
      generate(size=10, colors=[3, 1, 2, 2, 6, 2, 2, 7, 7], brow=2, bcol=3),
      generate(size=15, colors=[2, 5, 7, 2, 8, 7, 3, 3, 3], brow=1, bcol=2),
  ]
  test = [
      generate(size=16, colors=[4, 2, 5, 2, 9, 5, 4, 1, 1], brow=2, bcol=3),
      generate(size=12, colors=[6, 1, 1, 6, 7, 1, 3, 3, 1], brow=2, bcol=3),
  ]
  return {"train": train, "test": test}
