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


def generate(size=None, minisize=None, colors=None, row=None, col=None,
             bitesize=None, height=None, width=None, biteh=None, bitew=None,
             pattern_height=None, pattern_width=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    minisize: the width and height of the pattern
    colors: a list of colors to be used
    row: the vertical coordinate where the bite should be placed
    col: the horizontal coordinate where the bite should be placed
    bitesize: the width and height of the bite
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    biteh: the number of rows in the bite
    bitew: the number of columns in the bite
    pattern_height: the number of rows in the repeating pattern
    pattern_width: the number of columns in the repeating pattern
    num_colors: the number of foreground colors used by the pattern
  """
  if size is None:
    if height is None: height = common.randint(4, 30)
    if width is None: width = common.randint(4, 30)
    if pattern_height is None:
      pattern_height = common.randint(2, min(10, height // 2))
    if pattern_width is None:
      pattern_width = common.randint(2, min(10, width // 2))
    if minisize is None: minisize = pattern_height
    if num_colors is None: num_colors = common.randint(1, 9)
    if colors is None:
      color_list = common.random_colors(num_colors)
      colors = [color_list[common.randint(0, num_colors - 1)]
                for _ in range(pattern_height * pattern_width)]
    if biteh is None:
      biteh = common.randint(1, height - pattern_height - 1)
    if bitew is None:
      bitew = common.randint(1, width - pattern_width - 1)
    valid_rows = [r for r in range(height - biteh + 1)
                  if r >= pattern_height
                  or height - (r + biteh) >= pattern_height]
    valid_cols = [c for c in range(width - bitew + 1)
                  if c >= pattern_width
                  or width - (c + bitew) >= pattern_width]
    row = common.choice(valid_rows)
    col = common.choice(valid_cols)
  if height is None: height = size
  if width is None: width = size
  if pattern_height is None: pattern_height = minisize
  if pattern_width is None: pattern_width = minisize
  if biteh is None: biteh = bitesize
  if bitew is None: bitew = bitesize

  grid, full_grid = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      mr, mc = r % pattern_height, c % pattern_width
      color = colors[(mr * pattern_width + mc) % len(colors)]
      grid[r][c] = color
      full_grid[r][c] = color
  output = [list(grid_row) for grid_row in full_grid]
  for r in range(biteh):
    for c in range(bitew):
      grid[r + row][c + col] = common.black()
  output = [grid_row[col:col + bitew]
            for grid_row in output[row:row + biteh]]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, minisize=2, colors=[2, 1, 1, 1], row=3, col=0,
               bitesize=2),
      generate(size=4, minisize=2, colors=[8, 6, 6, 8], row=0, col=2,
               bitesize=1),
      generate(size=7, minisize=3, colors=[2, 2, 5, 2, 2, 5, 5, 5, 5], row=5,
               col=5, bitesize=2),
  ]
  test = [
      generate(size=7, minisize=3, colors=[8, 1, 8, 1, 8, 8, 8, 8, 1], row=0,
               col=4, bitesize=3),
  ]
  return {"train": train, "test": test}
