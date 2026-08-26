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


def generate(size=None, colors=None, height=None, width=None, num_colors=None,
             special_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: a list of digits representing the colors to be used
    height: the number of rows (defaults to size for square grids)
    width: the number of columns (defaults to size for square grids)
    num_colors: the number of non-gray/cyan colors to use
    special_count: the number of gray/cyan cells to place
  """
  if size is None:
    if height is None: height = common.randint(2, 30)
    if width is None: width = common.randint(2, 30)
    area = height * width
    if num_colors is None: num_colors = common.randint(1, 8)
    if special_count is None:
      special_count = common.randint(0, area // 2)
    special_count = min(special_count, area // 2)
    if colors is None:
      neutral_pool = [common.black()]
      neutral_pool.extend(common.random_colors(7, exclude=[common.gray(), common.cyan()]))
      neutral_colors = common.sample(neutral_pool, min(num_colors, len(neutral_pool)))
      colors = [common.choice(neutral_colors) for _ in range(area)]
      special_idxs = common.sample(list(range(area)), special_count)
      split = common.randint(0, special_count)
      for idx in special_idxs[:split]:
        colors[idx] = common.cyan()
      for idx in special_idxs[split:]:
        colors[idx] = common.gray()
  else:
    if height is None: height = size
    if width is None: width = size

  grid, output = common.grids(width, height, 0)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c] = colors[r * width + c]

  def recolor_gray_to_cyan():
    for r in range(height):
      for c in range(width):
        if grid[r][c] == common.gray(): output[r][c] = common.cyan()

  def recolor_cyan_to_gray():
    for r in range(height):
      for c in range(width):
        if grid[r][c] == common.cyan(): output[r][c] = common.gray()

  recolor_gray_to_cyan()
  recolor_cyan_to_gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5,
               colors=[2, 7, 8, 8, 8, 5, 5, 6, 5, 4, 8, 5, 5, 5, 2, 8, 8, 4, 3,
                       6, 6, 5, 1, 9, 3]),
      generate(size=3, colors=[3, 5, 1, 4, 5, 8, 2, 4, 9]),
      generate(size=3, colors=[6, 5, 3, 5, 7, 5, 8, 8, 2]),
  ]
  test = [
      generate(size=4, colors=[8, 8, 4, 5, 3, 8, 7, 5, 3, 7, 1, 9, 6, 4, 8, 8]),
  ]
  return {"train": train, "test": test}
