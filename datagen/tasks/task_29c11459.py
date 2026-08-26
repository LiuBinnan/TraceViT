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


def generate(rows=None, left_colors=None, right_colors=None, width=11,
             height=5, num_rows=None, num_colors=None, background_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where lines sholud be placed
    left_colors: which colors to use for the left side
    right_colors: which colors to use for the right side
    width: the width of the grid
    height: the height of the grid
    num_rows: how many rows contain endpoint clues
    num_colors: size of the reusable foreground palette
    background_color: the background color
  """
  if rows is None:
    if background_color is None:
      background_color = common.choice(
          [color for color in range(10) if color != common.gray()])
    colors = [
        color for color in range(10)
        if color not in [background_color, common.gray()]
    ]
    if num_colors is None:
      num_colors = common.randint(2, min(8, len(colors)))
    num_colors = min(num_colors, len(colors))
    colors = common.sample(colors, num_colors)
    if num_rows is None:
      num_rows = common.randint(1, height)
    num_rows = min(num_rows, height)
    rows = common.sample(range(height), num_rows)
    left_colors, right_colors = [], []
    left_forbid, right_forbid = None, None
    for _ in range(num_rows):
      left_options = [color for color in colors if color != left_forbid]
      right_options = [color for color in colors if color != right_forbid]
      left_color = common.choice(left_options)
      right_color = common.choice(right_options)
      left_colors.append(left_color)
      right_colors.append(right_color)
      left_forbid, right_forbid = left_color, right_color

  grid, output = common.grids(width, height, background_color or 0)
  for r, left_color, right_color in zip(rows, left_colors, right_colors):
    grid[r][0], grid[r][-1] = left_color, right_color
  for r, left_color in zip(rows, left_colors):
    for c in range(width // 2):
      output[r][c] = left_color
  for r, right_color in zip(rows, right_colors):
    for c in range(width // 2):
      output[r][width - 1 - c] = right_color
  for r in rows:
    output[r][width // 2] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1], left_colors=[1], right_colors=[2]),
      generate(rows=[3], left_colors=[3], right_colors=[7]),
  ]
  test = [
      generate(rows=[1, 4], left_colors=[4, 6], right_colors=[8, 9]),
  ]
  return {"train": train, "test": test}
