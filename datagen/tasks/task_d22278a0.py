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


def generate(size=None, rows=None, cols=None, colors=None, height=None,
             width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if size is None:
    if height is None: height = common.randint(6, 28)
    if width is None: width = common.randint(6, 28)
    corners = [(0, 0), (height - 1, 0), (0, width - 1), (height - 1, width - 1)]
    pixels = common.sample(corners, common.randint(2, 4))
    rows, cols = zip(*pixels)
    colors = common.random_colors(len(pixels))
  if height is None: height = size
  if width is None: width = size

  grid, output = common.grids(width, height)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color

  def reveal_seed_region(seed_idx):
    if seed_idx >= len(colors):
      return
    for r in range(height):
      for c in range(width):
        # Choose the (hopefully unique) minimal index.
        min_dist, min_idxs = height * width, []
        for idx, _ in enumerate(colors):
          row, col = rows[idx], cols[idx]
          dist = abs(row - r) +  abs(col - c)
          if min_dist > dist: min_dist, min_idxs = dist, []
          if min_dist == dist: min_idxs.append(idx)
        if len(min_idxs) > 1 or min_idxs[0] != seed_idx:
          continue
        if max(abs(rows[seed_idx] - r), abs(cols[seed_idx] - c)) % 2: continue
        output[r][c] = colors[seed_idx]

  reveal_seed_region(0)
  reveal_seed_region(1)
  reveal_seed_region(2)
  reveal_seed_region(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[0, 0], cols=[0, 9], colors=[1, 2]),
      generate(size=12, rows=[0, 11], cols=[11, 0], colors=[3, 8]),
      generate(size=13, rows=[0, 12], cols=[0, 0], colors=[2, 4]),
      generate(size=7, rows=[0, 0, 6], cols=[0, 6, 0], colors=[1, 2, 8]),
  ]
  test = [
      generate(size=17, rows=[0, 16, 16], cols=[0, 0, 16], colors=[4, 8, 1]),
  ]
  return {"train": train, "test": test}
