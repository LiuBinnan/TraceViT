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


def generate(lengths=None, width=None, height=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: the lengths of the columns
    width: number of columns in the grid; randomized when omitted
    height: number of rows in the grid; randomized when omitted
    num_colors: how many distinct bar colors to draw from; randomized when
      omitted
  """
  if lengths is None:
    if width is None:
      width = common.randint(6, 30)
    if height is None:
      height = common.randint(6, 30)
    max_bars = max(1, (width - 2) // 2)
    num_bars = common.randint(1, max_bars)
    options = list(range(1, width - 1))
    columns = []
    while options and len(columns) < num_bars:
      col = common.sample(options, 1)[0]
      columns.append(col)
      for adjacent in (col - 1, col, col + 1):
        if adjacent in options:
          options.remove(adjacent)
    columns.sort()
    lengths = [common.randint(2, height - 1) for _ in columns]
    if num_colors is None:
      num_colors = common.randint(1, 8)
    palette = common.random_colors(num_colors, exclude=[common.cyan()])
    bar_colors = [palette[common.randint(0, len(palette) - 1)] for _ in columns]
  else:
    width, height = 2 * len(lengths) + 1, max(lengths) + 1
    columns = [2 * idx + 1 for idx in range(len(lengths))]
    bar_colors = [common.red() for _ in lengths]
  grid = common.grid(width, height)
  output = common.grid(width, height)
  for idx in range(min(1, len(lengths))):
    length = lengths[idx]
    for i in range(length):
      r, c = height - i - 1, columns[idx]
      grid[r][c] = bar_colors[idx]
      output[r][c] = common.cyan() if i < length // 2 else bar_colors[idx]
  for idx in range(1, min(2, len(lengths))):
    length = lengths[idx]
    for i in range(length):
      r, c = height - i - 1, columns[idx]
      grid[r][c] = bar_colors[idx]
      output[r][c] = common.cyan() if i < length // 2 else bar_colors[idx]
  for idx in range(2, min(3, len(lengths))):
    length = lengths[idx]
    for i in range(length):
      r, c = height - i - 1, columns[idx]
      grid[r][c] = bar_colors[idx]
      output[r][c] = common.cyan() if i < length // 2 else bar_colors[idx]
  for idx in range(3, len(lengths)):
    length = lengths[idx]
    for i in range(length):
      r, c = height - i - 1, columns[idx]
      grid[r][c] = bar_colors[idx]
      output[r][c] = common.cyan() if i < length // 2 else bar_colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[6, 5, 4, 3]),
      generate(lengths=[7, 5, 3, 6]),
      generate(lengths=[7, 3, 4, 8]),
  ]
  test = [
      generate(lengths=[10, 9, 2, 5]),
  ]
  return {"train": train, "test": test}
