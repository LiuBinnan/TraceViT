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


def generate(rows=None, cols=None, idxs=None, size=3, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    size: the width and height of the (square) grid
    height: the number of rows in each panel (defaults to size)
    width: the number of columns in each panel (defaults to size)
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    while True:
      rows, cols, idxs = [], [], []
      for idx in range(2):
        pixels = common.random_pixels(width, height)
        rows.extend([p[0] for p in pixels])
        cols.extend([p[1] for p in pixels])
        idxs.extend([idx] * len(pixels))
      if len(set(rows)) == height and len(set(cols)) == width: break

  grid, output = common.grid(width, 2 * height), common.grid(width, height)
  for r, c, idx in zip(rows, cols, idxs):
    grid[height + r if idx else r][c] = common.blue() if idx else common.maroon()
  for r, c, idx in zip(rows, cols, idxs):
    if idx == 0:
      output[r][c] = common.maroon()
  for r, c, idx in zip(rows, cols, idxs):
    if idx == 1:
      output[r][c] = common.blue()
  output = common.grid(width, height)
  for r in range(height):
    for c in range(width):
      if grid[r][c] > 0 or grid[height + r][c] > 0: continue
      output[r][c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 0, 1, 2, 2, 2],
               cols=[1, 2, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2, 0, 0, 1, 2],
               cols=[0, 2, 1, 2, 2, 0, 2, 0, 0],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1]),
      generate(rows=[0, 1, 1, 2, 1, 2],
               cols=[1, 0, 2, 0, 2, 0],
               idxs=[0, 0, 0, 0, 1, 1]),
      generate(rows=[0, 1, 1, 1, 2, 0, 1, 1, 2],
               cols=[2, 0, 1, 2, 1, 0, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1]),
      generate(rows=[0, 1, 1, 2, 2, 1, 1, 1, 2, 2],
               cols=[1, 1, 2, 1, 2, 0, 1, 2, 0, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2, 2, 0, 0, 1, 2],
               cols=[0, 2, 2, 0, 2, 1, 2, 1, 0],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
