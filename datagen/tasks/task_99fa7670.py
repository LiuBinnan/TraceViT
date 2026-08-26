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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             num=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    num: the number of row starts to sample
    num_colors: the number of foreground colors to sample
  """
  if width is None:
    width = common.randint(3, 30)
  if height is None:
    height = common.randint(3, 30)
  if rows is None or cols is None:
    max_num = max(1, height // 2)
    if num is None:
      num = common.randint(1, max_num)
    num = max(1, min(num, max_num))
    rows = sorted(common.sample(range(height), num))
    cols = []
    for idx, row in enumerate(rows):
      choices = list(range(width - 1))
      if idx and row == rows[idx - 1] + 1 and cols[-1] in choices:
        choices.remove(cols[-1])
      cols.append(common.choice(choices))
  if colors is None:
    if num_colors is None:
      num_colors = common.randint(1, 9)
    num_colors = max(1, min(num_colors, 9))
    palette = common.random_colors(num_colors)
    colors = [common.choice(palette) for _ in rows]

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    output[r][c] = color
  seeds = list(zip(rows, cols, colors))

  def extend_seed(seed_idx):
    if seed_idx >= len(seeds):
      return
    r, c, color = seeds[seed_idx]
    end = seeds[seed_idx + 1][0] if seed_idx + 1 < len(seeds) else height
    for col in range(c, width):
      output[r][col] = color
    for row in range(r, end):
      output[row][width - 1] = color

  extend_seed(0)
  extend_seed(1)
  extend_seed(2)
  extend_seed(3)
  extend_seed(4)
  extend_seed(5)
  extend_seed(6)
  extend_seed(7)
  extend_seed(8)
  extend_seed(9)
  extend_seed(10)
  extend_seed(11)
  extend_seed(12)
  extend_seed(13)
  extend_seed(14)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, rows=[1, 3], cols=[2, 1], colors=[2, 3]),
      generate(width=3, height=3, rows=[1], cols=[1], colors=[6]),
      generate(width=6, height=6, rows=[1, 4], cols=[1, 3], colors=[8, 5]),
      generate(width=5, height=7, rows=[1, 3, 5], cols=[2, 1, 2],
               colors=[8, 7, 6]),
  ]
  test = [
      generate(width=8, height=7, rows=[0, 2, 4], cols=[3, 2, 5],
               colors=[8, 7, 2]),
  ]
  return {"train": train, "test": test}
