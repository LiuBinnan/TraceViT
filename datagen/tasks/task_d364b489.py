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


def generate(rows=None, cols=None, size=10, height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: the maximum number of pixels to place
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if count is None: count = common.randint(1, max(1, (width * height) // 5))
    candidates = common.sample(common.all_pixels(width, height), width * height)
    available = set(candidates)
    kept = []
    for p in candidates:
      if len(kept) >= count: break
      if p not in available: continue
      kept.append(p)
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          available.discard((p[0] + dr, p[1] + dc))
      for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        available.discard((p[0] + dr, p[1] + dc))
    rows, cols = [p[0] for p in kept], [p[1] for p in kept]

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = 1
    if r > 0:
      output[r - 1][c] = common.red()
    if r < height - 1:
      output[r + 1][c] = common.cyan()
    if c > 0:
      output[r][c - 1] = common.orange()
    if c < width - 1:
      output[r][c + 1] = common.pink()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3, 5, 7, 9], cols=[6, 9, 3, 7, 1]),
      generate(rows=[0, 2, 3, 5, 8, 9], cols=[5, 0, 9, 5, 2, 9]),
  ]
  test = [
      generate(rows=[0, 0, 2, 3, 6, 6, 9], cols=[1, 9, 7, 3, 7, 0, 4]),
  ]
  return {"train": train, "test": test}
