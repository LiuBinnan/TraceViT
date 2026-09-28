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


def generate(size=None, pair=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the box.
    pair: The pair of colors.
    colors: The colors of the grid.
    gsize: The height and width of the grid.
  """

  if size is None:
    if gsize is None:
      gsize = common.randint(8, 16)
    size = 2 * common.randint(3, (gsize - 2) // 2)
    pair = common.random_colors(2, exclude=[5])
    colors = []
    for _ in range(gsize * gsize):
      color = common.randint(0, 2)
      colors.append(0 if color == 0 else pair[color - 1])
    box_top = common.randint(1, gsize - size - 1)
    box_left = common.randint(1, gsize - size - 1)
  else:
    if gsize is None:
      gsize = 10
    box_top = (gsize - size) // 2
    box_left = (gsize - size) // 2

  # Input: a two-color speckled field framed by a gray box.
  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color
  top, bottom, left, right = box_top, box_top + size, box_left, box_left + size
  for i in range(size):
    grid[top][left + i] = common.gray()
    grid[bottom - 1][left + i] = common.gray()
    grid[top + i][left] = common.gray()
    grid[top + i][right - 1] = common.gray()

  # Output is solved forward: swap the two colors inside the box.
  output = common.deepcopy(grid)

  def recolor_inside(src, dst):
    """Recolors box-interior cells that were `src` in the input to `dst`."""
    for r in range(top, bottom):
      for c in range(left, right):
        if grid[r][c] == src:
          output[r][c] = dst

  recolor_inside(pair[0], pair[1])
  recolor_inside(pair[1], pair[0])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, pair=[6, 8], colors=[0, 0, 8, 6, 0, 6, 0, 8, 0, 8,
                                            8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 0, 0, 8, 8, 6, 6, 0, 0, 8,
                                            6, 0, 6, 6, 6, 8, 0, 6, 0, 8,
                                            0, 0, 6, 6, 8, 6, 0, 6, 0, 8,
                                            6, 0, 8, 8, 8, 6, 8, 0, 0, 8,
                                            6, 0, 6, 8, 6, 8, 6, 8, 0, 8,
                                            0, 0, 6, 0, 6, 8, 8, 8, 0, 8,
                                            8, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                                            8, 8, 8, 0, 8, 8, 6, 0, 6, 6]),
      generate(size=6, pair=[4, 9], colors=[9, 4, 0, 0, 4, 9, 0, 0, 9, 9,
                                            4, 9, 9, 4, 9, 9, 0, 0, 9, 0,
                                            0, 0, 0, 5, 5, 5, 5, 5, 0, 9,
                                            9, 4, 0, 9, 0, 9, 9, 5, 0, 4,
                                            4, 4, 0, 0, 0, 4, 0, 5, 4, 4,
                                            9, 4, 0, 4, 9, 0, 9, 5, 0, 0,
                                            0, 9, 0, 0, 4, 0, 0, 5, 0, 4,
                                            0, 4, 0, 5, 5, 5, 5, 5, 4, 4,
                                            9, 0, 9, 9, 4, 0, 9, 0, 0, 0,
                                            9, 9, 9, 0, 9, 4, 9, 9, 0, 0]),
      generate(size=8, pair=[2, 3], colors=[0, 0, 3, 3, 3, 3, 2, 0, 2, 0,
                                            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                            3, 0, 3, 2, 2, 2, 2, 0, 0, 2,
                                            0, 0, 0, 3, 0, 3, 2, 2, 0, 2,
                                            3, 0, 2, 0, 2, 3, 2, 2, 0, 3,
                                            3, 0, 3, 3, 0, 2, 3, 3, 0, 3,
                                            3, 0, 3, 3, 3, 0, 3, 2, 0, 2,
                                            0, 0, 3, 0, 3, 3, 3, 0, 0, 3,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                            2, 0, 3, 3, 3, 2, 3, 2, 3, 0]),
  ]
  test = [
      generate(size=8, pair=[1, 7], colors=[7, 0, 1, 1, 7, 0, 0, 7, 7, 7,
                                            1, 0, 0, 0, 0, 0, 0, 0, 0, 7,
                                            1, 0, 0, 0, 1, 0, 1, 7, 0, 7,
                                            0, 0, 7, 1, 7, 0, 1, 7, 0, 1,
                                            7, 0, 7, 7, 0, 1, 7, 1, 0, 1,
                                            7, 0, 0, 1, 7, 0, 7, 7, 0, 1,
                                            1, 0, 7, 7, 1, 1, 1, 1, 0, 0,
                                            0, 0, 1, 7, 7, 7, 7, 0, 0, 7,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 1, 7, 1, 0, 7, 0, 0, 7, 7]),
  ]
  return {"train": train, "test": test}
