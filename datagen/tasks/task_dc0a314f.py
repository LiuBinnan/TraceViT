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


def generate(row=None, col=None, colors=None, size=8, minisize=5,
             miniheight=None, miniwidth=None, num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the cutout
    col: a horizontal coordinate for the cutout
    colors: a list of colors to be used
    size: the width and height of one quarter of the grid
    minisize: the height and width of the (square) cutout fallback
    miniheight: the height of the cutout (defaults to minisize)
    miniwidth: the width of the cutout (defaults to minisize)
    num_colors: how many foreground colors the symmetric pattern uses
    density: percent (1-100) of quarter cells painted with a foreground color
  """
  if miniheight is None and row is not None:
    miniheight = minisize
  if miniwidth is None and row is not None:
    miniwidth = minisize
  if row is None:
    # Widen the quarter side like the reference re_arc generator (a square
    # quarter, side 3..15) so the full 2*size grid ranges 6x6..30x30 rather
    # than a fixed 16x16 -- this alone spreads the density / object-count /
    # output-size variation. The puzzle rule (a symmetric grid with a green
    # cutout to reconstruct) is unchanged.
    size = common.randint(3, 15)
    # Independent cutout height/width, coupled to `size` so the hole always
    # stays inside the top-left quarter and is recoverable from symmetry.
    if miniheight is None:
      miniheight = common.randint(1, size)
    else:
      miniheight = min(miniheight, size)
    if miniwidth is None:
      miniwidth = common.randint(1, size)
    else:
      miniwidth = min(miniwidth, size)
    # TODO: Make sure we don't cut out the center.
    row = common.randint(0, size - miniheight)
    col = common.randint(0, size - miniwidth)
    # Paint a symmetric quarter over a solid background: a background color,
    # a bounded foreground palette (num_colors) and a fill density -- mirroring
    # re_arc's (bgc, numcols, nc) sampling. Fewer colors / lower density widen
    # the #colors, object-count and density axes; every cell still satisfies
    # bitmap[i][j] == bitmap[j][i] so the quarter stays diagonally symmetric.
    bgc = common.random_color(exclude=[common.green()])
    if num_colors is None:
      num_colors = common.randint(1, 7)
    else:
      num_colors = min(num_colors, 7)
    palette = common.random_colors(num_colors, exclude=[common.green(), bgc])
    if density is None:
      density = common.randint(1, 100)
    bitmap = common.grid(size, size, bgc)
    for j in range(size):
      for i in range(j + 1):
        if common.randint(1, 100) <= density:
          color = common.sample(palette, 1)[0]
          bitmap[i][j] = bitmap[j][i] = color
    colors = []
    for r in bitmap:
      colors.extend(r)

  output = common.grid(2 * size, 2 * size, common.green())
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      output[r][c] = output[2 * size - r - 1][2 * size - c - 1] = color
      output[r][2 * size - c - 1] = output[2 * size - r - 1][c] = color
  grid = common.deepcopy(output)
  for r in range(miniheight):
    for c in range(miniwidth):
      grid[row + r][col + c] = common.green()
  output = [
      output[row + r][col:col + miniwidth] for r in range(miniheight)
  ]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=9,
               colors=[2, 1, 2, 2, 6, 5, 5, 6, 1, 6, 6, 1, 5, 6, 5, 2, 2, 6, 1,
                       6, 5, 5, 5, 2, 2, 1, 6, 6, 6, 2, 2, 2, 6, 5, 5, 6, 5, 8,
                       5, 7, 5, 6, 5, 2, 8, 8, 5, 8, 5, 5, 5, 2, 5, 5, 5, 8, 6,
                       2, 2, 2, 7, 8, 8, 8]),
      generate(row=0, col=3,
               colors=[8, 9, 9, 8, 7, 7, 2, 2, 9, 8, 9, 9, 7, 1, 7, 2, 9, 9, 8,
                       2, 2, 7, 2, 7, 8, 9, 2, 9, 2, 2, 7, 1, 7, 7, 2, 2, 2, 7,
                       8, 7, 7, 1, 7, 2, 7, 2, 7, 7, 2, 7, 2, 7, 8, 7, 2, 8, 2,
                       2, 7, 1, 7, 7, 8, 2]),
      generate(row=0, col=7,
               colors=[2, 2, 5, 2, 9, 9, 9, 5, 2, 5, 4, 4, 9, 5, 2, 9, 5, 4, 5,
                       4, 9, 2, 5, 5, 2, 4, 4, 4, 5, 9, 5, 2, 9, 9, 9, 5, 9, 6,
                       9, 9, 9, 5, 2, 9, 6, 6, 9, 9, 9, 2, 5, 5, 9, 9, 7, 9, 5,
                       9, 5, 2, 9, 9, 9, 6]),
  ]
  test = [
      generate(row=4, col=8,
               colors=[5, 5, 2, 5, 2, 5, 5, 5, 5, 2, 2, 5, 5, 5, 2, 2, 2, 2, 5,
                       8, 5, 2, 2, 5, 5, 5, 8, 5, 5, 2, 5, 5, 2, 5, 5, 5, 4, 6,
                       6, 9, 5, 5, 2, 2, 6, 6, 9, 9, 5, 2, 2, 5, 6, 9, 6, 9, 5,
                       2, 5, 5, 9, 9, 9, 9]),
  ]
  return {"train": train, "test": test}
