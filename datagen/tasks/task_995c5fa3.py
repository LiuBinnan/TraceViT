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


def generate(colors=None, color_list=(2, 3, 4, 8), num=None,
             bg_color=None, fill_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: the colors to be used for the output grid
    color_list: the available list of colors for the output grid
    num: number of encoded squares (1-6); the output is a num x num grid
    bg_color: background/hole color of the input grid
    fill_colors: per-square fill color of the input squares
  """
  if num is None:
    num = len(colors) if colors is not None else common.randint(1, 6)
  num = max(1, min(6, num))
  if colors is None:
    colors = [color_list[common.randint(0, 3)] for _ in range(num)]
    if bg_color is None:
      bg_color = common.choice(range(10))
    if fill_colors is None:
      fill_colors = [common.choice([c for c in range(10)
                                    if c != bg_color and c != colors[k]])
                     for k in range(num)]
  if bg_color is None:
    bg_color = common.black()
  if fill_colors is None:
    fill_colors = [common.gray() for _ in range(num)]

  grid = common.grid(5 * num - 1, 4, bg_color)
  for idx in range(num):
    for r in range(4):
      for c in range(4):
        grid[r][idx * 5 + c] = fill_colors[idx]
  for idx in range(num):
    if colors[idx] == 8:
      grid[1][idx * 5 + 1] = grid[1][idx * 5 + 2] = bg_color
      grid[2][idx * 5 + 1] = grid[2][idx * 5 + 2] = bg_color
    elif colors[idx] == 3:
      grid[1][idx * 5] = grid[1][idx * 5 + 3] = bg_color
      grid[2][idx * 5] = grid[2][idx * 5 + 3] = bg_color
    elif colors[idx] == 4:
      grid[2][idx * 5 + 1] = grid[2][idx * 5 + 2] = bg_color
      grid[3][idx * 5 + 1] = grid[3][idx * 5 + 2] = bg_color
  output = common.deepcopy(grid)

  def color_square(idx):
    # Paints the idx-th square's fill cells with its code color.
    for r in range(4):
      for c in range(4):
        if output[r][idx * 5 + c] == fill_colors[idx]:
          output[r][idx * 5 + c] = colors[idx]

  def collapse_to_rows():
    # Each square becomes one row of the num x num output.
    nonlocal output
    output = common.grid(num, num)
    for r in range(num):
      for c in range(num):
        output[r][c] = colors[r]

  color_square(0)
  if num > 1:
    color_square(1)
  if num > 2:
    color_square(2)
  if num > 3:
    color_square(3)
  if num > 4:
    color_square(4)
  if num > 5:
    color_square(5)
  collapse_to_rows()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 8, 3]),
      generate(colors=[3, 4, 2]),
      generate(colors=[8, 2, 4]),
      generate(colors=[2, 4, 2]),
  ]
  test = [
      generate(colors=[4, 3, 8]),
  ]
  return {"train": train, "test": test}
