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


def generate(rows=None, cols=None, color=None, size=5, minisize=3,
             height=None, width=None, num_cells=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) input grid
    minisize: the width and height of the (square) output grid
    height: the height of the input grid
    width: the width of the input grid
    num_cells: the number of distractor cells to place
    num_colors: the number of distractor colors to sample
  """
  if rows is None:
    height = common.randint(2, 30) if height is None else height
    width = common.randint(2, 30) if width is None else width
    color = common.choice([1, 2, 3]) if color is None else color
    distractor_colors = [0, 4, 5, 6, 7, 8, 9]
    if num_colors is None:
      num_colors = common.randint(1, len(distractor_colors))
    num_colors = max(1, min(num_colors, len(distractor_colors)))
    distractor_colors = common.sample(distractor_colors, num_colors)
    max_cells = width * height - 1
    if num_cells is None:
      num_cells = common.randint(0, max_cells)
    num_cells = max(0, min(num_cells, max_cells))
    pixels = common.sample(common.all_pixels(width, height), num_cells)
    grid = common.grid(width, height, color)
    for r, c in pixels:
      grid[r][c] = common.choice(distractor_colors)
  else:
    grid = common.grid(size, size)
    for r, c in zip(rows, cols):
      grid[r][c] = color
  output = [row[:] for row in grid]
  output = common.grid(minisize, minisize)
  output[0][0] = color if color in [2] else common.black()
  output[0][1] = color if color in [1, 2] else common.black()
  output[0][2] = color if color in [2, 3] else common.black()
  output[1][0] = color if color in [1] else common.black()
  output[1][1] = color if color in [1, 2] else common.black()
  output[1][2] = color if color in [1, 3] else common.black()
  output[2][0] = color if color in [3] else common.black()
  output[2][1] = color
  output[2][2] = color if color in [3] else common.black()
  output = common.grid(minisize, minisize)
  output[0][0] = common.gray() if color in [2] else common.black()
  output[0][1] = common.gray() if color in [1, 2] else common.black()
  output[0][2] = common.gray() if color in [2, 3] else common.black()
  output[1][0] = common.gray() if color in [1] else common.black()
  output[1][1] = common.gray() if color in [1, 2] else common.black()
  output[1][2] = common.gray() if color in [1, 3] else common.black()
  output[2][0] = common.gray() if color in [3] else common.black()
  output[2][1] = common.gray()
  output[2][2] = common.gray() if color in [3] else common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 2, 3, 3, 4, 4],
               cols=[0, 1, 4, 0, 3, 3, 4, 2, 3], color=2),
      generate(rows=[1, 1, 1, 2, 2, 2, 3, 3, 4],
               cols=[2, 3, 4, 1, 3, 4, 1, 3, 4], color=1),
      generate(rows=[0, 1, 1, 2, 2, 3, 3, 4, 4, 4],
               cols=[0, 3, 4, 1, 2, 1, 3, 0, 2, 3], color=3),
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4],
               cols=[0, 2, 0, 3, 4, 0, 1, 3, 1, 3, 0, 4], color=1),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
               cols=[0, 2, 4, 0, 4, 0, 1, 0, 3, 4, 0, 1, 2, 4], color=2),
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4],
               cols=[1, 3, 1, 2, 3, 1, 2, 4, 0, 1, 2, 2, 4], color=2),
      generate(rows=[0, 0, 1, 1, 2, 3, 4, 4, 4],
               cols=[1, 3, 0, 1, 1, 2, 0, 1, 2], color=3),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 1, 1, 2, 3, 3, 4],
               cols=[0, 1, 2, 3, 2, 4, 1, 1, 4, 2], color=1),
      generate(rows=[0, 0, 0, 1, 2, 3, 3, 4],
               cols=[1, 3, 4, 2, 0, 2, 4, 4], color=3),
  ]
  return {"train": train, "test": test}
