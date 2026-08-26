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


def generate(colors=None, size=3, height=None, width=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid (fallback for both axes)
    height: number of rows; defaults to size (square)
    width: number of columns; defaults to size (square)
    num_colors: number of foreground colors in the rectangular random grid
    density: foreground-cell percentage in the rectangular random grid
  """
  if height is None and width is None:
    # Original square behavior (preserves validate() byte-for-byte): the rule is
    # a 180-degree point reflection of the upper-left triangle of colored cells.
    if colors is None:
      colors = [common.randint(0, 9) for _ in range(6)]

    grid, output = common.grids(size, size)
    output[2][2] = grid[0][0] = colors[0]
    output[2][1] = grid[0][1] = colors[1]
    output[2][0] = grid[0][2] = colors[2]
    output[1][2] = grid[1][0] = colors[3]
    output[1][1] = grid[1][1] = colors[4]
    output[0][2] = grid[2][0] = colors[5]
    return {"input": grid, "output": output}

  # Rectangular case: independent height/width. The transformation rule is the
  # same 180-degree point reflection -- output[h-1-r][w-1-c] = grid[r][c] -- which
  # is well defined on any rectangle.
  if height is None:
    height = size
  if width is None:
    width = size

  area = width * height
  bgc = common.randint(0, 9)
  grid, output = common.grids(width, height, bgc)
  if num_colors is None:
    num_colors = common.randint(0, min(9, area))
  if density is None:
    density = common.randint(0, 100)

  num_colors = max(0, min(num_colors, 9, area))
  density = max(0, min(density, 100))
  foreground = int(round(area * density / 100))
  if num_colors == 0:
    foreground = 0
  elif foreground > 0:
    foreground = max(num_colors, min(area, foreground))
  else:
    num_colors = 0

  palette = [color for color in range(10) if color != bgc]
  colors = common.sample(palette, num_colors)
  pixels = common.shuffle(common.all_pixels(width, height))
  for idx, (r, c) in enumerate(pixels[:foreground]):
    color = colors[idx] if idx < num_colors else common.choice(colors)
    grid[r][c] = color
    output[height - 1 - r][width - 1 - c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 3, 8, 3, 7, 5]),
      generate(colors=[5, 5, 2, 1, 0, 0]),
  ]
  test = [
      generate(colors=[6, 3, 5, 6, 8, 4]),
  ]
  return {"train": train, "test": test}
