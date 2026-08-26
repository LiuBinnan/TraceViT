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


def generate(row=None, col=None, colors=None, size=8, minisize=3,
             height=None, width=None, mini_h=None, mini_w=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the cutout
    col: a horizontal coordinate for the cutout
    colors: a list of colors to be used
    size: the width and height of one quarter of the grid
    minisize: the width and height of the cutout
    height: the height (rows) of one quarter of the grid; defaults to size
    width: the width (cols) of one quarter of the grid; defaults to size
    mini_h: the height (rows) of the cutout; defaults to minisize
    mini_w: the width (cols) of the cutout; defaults to minisize
    num_colors: how many distinct foreground colors fill the quarter (1-8);
      randomized when omitted
    density: fraction of the quarter's cells that are foreground rather than
      background (0-1); randomized when omitted
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if mini_h is None:
    mini_h = minisize
  if mini_w is None:
    mini_w = minisize
  if row is None:
    # TODO: Make sure we don't cut out the center.
    row = common.randint(0, height - mini_h)
    col = common.randint(0, width - mini_w)
    # Widen structural variation toward the re_arc band without touching the
    # rule: a background color plus a sampled number of foreground colors
    # (re_arc numcols) filling a sampled fraction of the quarter (re_arc nc).
    # The pattern stays in colors 1-9 so 0 remains exclusive to the cut hole,
    # which is exactly what the solver keys on.
    if num_colors is None:
      num_colors = common.randint(1, 8)
    if density is None:
      density = common.randint(1, height * width) / (height * width)
    bgc = common.random_color()
    # Cap at the colors available after excluding the background (guard against
    # an over-wide explicit num_colors overrunning the 9-color palette).
    num_colors = min(num_colors, 8)
    fg_colors = common.random_colors(num_colors, exclude=[bgc])
    num_fg = max(1, min(height * width, round(density * height * width)))
    cells = [(r, c) for r in range(height) for c in range(width)]
    fg_cells = set(common.sample(cells, num_fg))
    bitmap = common.grid(width, height)
    for r in range(height):
      for c in range(width):
        bitmap[r][c] = common.choice(fg_colors) if (r, c) in fg_cells else bgc
    colors = []
    for r in bitmap:
      colors.extend(r)

  output = common.grid(2 * width, 2 * height)
  for r in range(height):
    for c in range(width):
      color = colors[r * width + c]
      output[r][c] = output[2 * height - r - 1][2 * width - c - 1] = color
      output[r][2 * width - c - 1] = output[2 * height - r - 1][c] = color
  grid = common.deepcopy(output)
  for r in range(mini_h):
    for c in range(mini_w):
      grid[row + r][col + c] = common.black()
  output = [
      output[row + r][col:col + mini_w] for r in range(mini_h)
  ]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=4,
               colors=[2, 1, 3, 5, 1, 1, 1, 8, 1, 2, 5, 7, 1, 7, 8, 8, 3, 5, 4,
                       4, 1, 8, 2, 9, 5, 7, 4, 4, 8, 8, 9, 2, 1, 1, 1, 8, 4, 4,
                       1, 1, 1, 7, 8, 8, 4, 7, 1, 9, 1, 8, 2, 9, 1, 1, 1, 3, 8,
                       8, 9, 2, 1, 9, 3, 1]),
      generate(row=8, col=4,
               colors=[3, 3, 3, 1, 7, 7, 6, 6, 3, 3, 1, 3, 7, 7, 6, 1, 3, 1, 8,
                       8, 6, 6, 9, 7, 1, 3, 8, 5, 6, 1, 7, 9, 7, 7, 6, 6, 3, 3,
                       5, 1, 7, 7, 6, 1, 3, 3, 1, 1, 6, 6, 9, 7, 5, 1, 6, 1, 6,
                       1, 7, 9, 1, 1, 1, 4]),
      generate(row=7, col=10,
               colors=[9, 3, 5, 3, 3, 9, 5, 5, 3, 9, 3, 6, 9, 5, 5, 8, 5, 3, 3,
                       3, 5, 5, 6, 6, 3, 6, 3, 6, 5, 8, 6, 6, 3, 9, 5, 5, 5, 5,
                       2, 1, 9, 5, 5, 8, 5, 8, 1, 6, 5, 5, 6, 6, 2, 1, 9, 3, 5,
                       8, 6, 6, 1, 6, 3, 9]),
  ]
  test = [
      generate(row=5, col=1,
               colors=[4, 8, 9, 9, 6, 6, 5, 1, 8, 6, 9, 9, 6, 7, 1, 5, 9, 9, 5,
                       2, 5, 1, 5, 5, 9, 9, 2, 2, 1, 5, 5, 9, 6, 6, 5, 1, 1, 4,
                       5, 2, 6, 7, 1, 5, 4, 4, 2, 7, 5, 1, 5, 5, 5, 2, 9, 5, 1,
                       5, 5, 9, 2, 7, 5, 9]),
  ]
  return {"train": train, "test": test}
