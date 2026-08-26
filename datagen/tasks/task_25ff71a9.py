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


def generate(rows=None, cols=None, color=None, size=3, height=None, width=None,
             count=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing the color of a live cell
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    count: the number of foreground cells in the shifted shape
    density: approximate foreground density percentage
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    source_height = max(1, height - 1)
    max_count = min(width * source_height, max(1, (height * width) // 2 - 1))
    if count is None:
      if density is None:
        count = common.randint(1, max_count)
      else:
        count = max(1, (height * width * density) // 100)
    count = min(max(1, count), max_count)
    pixels = common.all_pixels(width, source_height)
    pixels = common.sample(pixels, count)
    rows, cols = zip(*pixels)
    color = common.randint(1, 2)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r + 1][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0], cols=[0, 1, 2], color=1),
      generate(rows=[1, 1, 1], cols=[0, 1, 2], color=1),
      generate(rows=[0, 1, 1], cols=[1, 0, 1], color=1),
      generate(rows=[0, 0, 1], cols=[1, 2, 2], color=2),
  ]
  test = [
      generate(rows=[0, 1], cols=[0, 0], color=2),
      generate(rows=[1], cols=[1], color=1),
  ]
  return {"train": train, "test": test}
