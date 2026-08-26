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


def generate(rows=None, cols=None, size=3,
             height=None, width=None, noise_count=None, noise_ncolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where blue pixels should be placed
    cols: a list of horizontal coordinates where blue pixels should be placed
    size: the width and height of the (square) grid for the explicit path
    height: number of rows of the randomly generated input grid
    width: number of columns of the randomly generated input grid
    noise_count: how many distractor pixels to scatter on the background
    noise_ncolors: how many distinct colors the distractor pixels may use
  """
  if rows is None:
    if height is None:
      height = common.randint(3, 30)
    if width is None:
      width = common.randint(3, 30)
    count = common.randint(1, 4)
    cells = common.all_pixels(width, height)
    pixels = common.sample(cells, count)
    rows, cols = zip(*pixels)
    pixel_set = set(pixels)
    open_cells = [cell for cell in cells if cell not in pixel_set]
    max_noise = max(0, len(open_cells) // 2 - 1)
    if noise_count is None:
      noise_count = common.randint(0, max_noise)
    noise_count = max(0, min(noise_count, max_noise))
    if noise_ncolors is None:
      noise_ncolors = common.randint(1, 7)
    noise_ncolors = max(1, min(noise_ncolors, 7))
    palette = common.random_colors(
        noise_ncolors, exclude=[common.black(), common.blue(), common.red()])
    noise_cells = common.sample(open_cells, noise_count)
    noise = [(r, c, common.sample(palette, 1)[0]) for r, c in noise_cells]
    painted = [(r, c, common.blue()) for r, c in zip(rows, cols)] + noise
  else:
    height = width = size
    painted = [(r, c, common.blue()) for r, c in zip(rows, cols)]

  grid, output = common.grid(width, height), common.grid(3, 3)
  for r, c, color in painted:
    grid[r][c] = color

  positions = [(0, 0), (0, 1), (0, 2), (1, 1)]

  def mark_blue_count():
    for idx in range(min(len(rows), len(positions))):
      r, c = positions[idx]
      output[r][c] = common.blue()

  def recolor_count():
    for r, c in positions:
      if output[r][c] == common.blue():
        output[r][c] = common.red()

  mark_blue_count()
  recolor_count()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1], cols=[0]),
      generate(rows=[1, 0], cols=[0, 1]),
      generate(rows=[2, 0], cols=[0, 2]),
      generate(rows=[0, 1], cols=[1, 2]),
      generate(rows=[0], cols=[2]),
      generate(rows=[0, 0, 2], cols=[0, 1, 0]),
      generate(rows=[0, 1, 1], cols=[1, 0, 1]),
      generate(rows=[0, 0, 2, 2], cols=[0, 1, 0, 2]),
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 0]),
      generate(rows=[0, 1, 2, 2], cols=[0, 2, 1, 2]),
  ]
  test = [
      generate(rows=[0, 2], cols=[1, 1]),
      generate(rows=[0, 1, 1, 2], cols=[1, 1, 2, 0]),
  ]
  return {"train": train, "test": test}
