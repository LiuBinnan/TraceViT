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
             num_dots=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    num_dots: how many seed pixels to place (one per distinct row)
    num_colors: how many distinct colors the seed pixels may draw from
  """
  if width is None:
    width, height = common.randint(3, 30), common.randint(3, 30)
    if num_dots is None:
      num_dots = common.randint(1, height)
    if num_colors is None:
      num_colors = common.randint(1, 8)
    palette = common.random_colors(num_colors, exclude=[common.gray()])
    rows = common.sample(range(height), num_dots)
    cols = [common.randint(0, width // 2) for _ in range(num_dots)]
    colors = [common.sample(palette, 1)[0] for _ in range(num_dots)]

  grid = common.grid(width, height)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
  output = [row[:] for row in grid]
  seeds = list(zip(rows, cols, colors))

  def extend_wave(wave_idx):
    for seed_idx in range(wave_idx, len(seeds), 4):
      row, col, color = seeds[seed_idx]
      for c in range(col, width):
        output[row][c] = color if c % 2 == col % 2 else common.gray()

  extend_wave(0)
  extend_wave(1)
  extend_wave(2)
  extend_wave(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=10, rows=[2, 5], cols=[2, 3], colors=[2, 6]),
      generate(width=12, height=10, rows=[1, 4, 5], cols=[2, 1, 6],
               colors=[2, 3, 6]),
      generate(width=8, height=7, rows=[3], cols=[3], colors=[8]),
  ]
  test = [
      generate(width=8, height=9, rows=[1, 2, 4, 6], cols=[3, 2, 4, 3],
               colors=[3, 4, 8, 2]),
  ]
  return {"train": train, "test": test}
