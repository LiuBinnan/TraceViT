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


def generate(size=None, colors=None, flip_middle=None, height=None, width=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: a list of digits representing the colors to be used
    flip_middle: whether to flip the middle figure
    height: the number of rows (defaults to size for square grids)
    width: the number of columns per panel (defaults to size for square grids)
    num_colors: number of non-background colors to use when randomized
  """
  if size is None:
    if height is None:
      height = common.randint(1, 30)
    if width is None:
      width = common.randint(1, 10)
    if colors is None:
      area = height * width
      if num_colors is None:
        num_colors = common.randint(1, min(9, area))
      num_colors = min(max(1, num_colors), 9, area)
      background = common.choice(range(10))
      color_list = common.sample([c for c in range(10) if c != background],
                                 num_colors)
      colors = [background for _ in range(area)]
      cells = list(range(area))
      for color in color_list:
        count = min(len(cells),
                    common.randint(1, max(1, len(cells) // num_colors)))
        selected = common.sample(cells, count)
        for idx in selected:
          colors[idx] = color
        cells = [idx for idx in cells if idx not in selected]
    if flip_middle is None:
      flip_middle = common.randint(0, 1)
  else:
    height = width = size

  grid, output = common.grid(3 * width, height, 0), common.grid(width, height, 0)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c + width * 2] = grid[r][c] = colors[r * width + c]
      grid[height - r - 1 if flip_middle else r][width + c] = (
          colors[r * width + c])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, colors=[4, 5, 1, 5, 5, 5, 1, 5, 4], flip_middle=1),
      generate(size=4, colors=[2, 0, 0, 1, 4, 2, 1, 4, 4, 1, 2, 4, 1, 0, 0, 2],
               flip_middle=0),
      generate(size=2, colors=[2, 1, 2, 3], flip_middle=0),
  ]
  test = [
      generate(size=5,
               colors=[0, 2, 0, 4, 4, 2, 2, 0, 4, 4, 0, 2, 2, 2, 0, 1, 1, 0, 2,
                       2, 1, 1, 0, 2, 0],
               flip_middle=0),
  ]
  return {"train": train, "test": test}
