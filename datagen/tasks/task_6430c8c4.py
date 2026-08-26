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


def generate(rows=None, cols=None, idxs=None, size=4, gh=None, gw=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    size: the width and height of the (square) grid
    gh: the height (row extent) of each layer; defaults to size
    gw: the width (col extent) of each layer; defaults to size
  """
  if gh is None:
    gh = size
  if gw is None:
    gw = size
  if rows is None:
    rows, cols, idxs = [], [], []
    for idx in range(2):
      pixels = common.random_pixels(gw, gh)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))

  grid, output = common.grid(gw, 2 * gh + 1), common.grid(gw, gh)
  for c in range(gw):
    grid[gh][c] = common.yellow()
  for row, col, idx in zip(rows, cols, idxs):
    r, c = gh + row + 1 if idx else row, col
    grid[r][c] = common.red() if idx else common.orange()

  for row, col, idx in zip(rows, cols, idxs):
    if idx == 0:
      output[row][col] = common.orange()
  for row, col, idx in zip(rows, cols, idxs):
    if idx == 1:
      output[row][col] = (common.gray() if output[row][col] != common.black()
                          else common.red())
  for r in range(gh):
    for c in range(gw):
      output[r][c] = (common.black() if output[r][c] != common.black()
                      else common.green())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 1, 1, 2, 2, 2, 3, 3],
               cols=[0, 1, 3, 1, 2, 1, 2, 3, 1, 2, 1, 3, 0, 1, 2, 0, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 1, 1, 2, 2, 3],
               cols=[2, 3, 2, 3, 1, 2, 0, 1, 0, 2, 1, 3, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
      generate(rows=[0, 1, 1, 1, 2, 3, 3, 3, 0, 1, 1, 1, 2, 2, 3, 3],
               cols=[3, 1, 2, 3, 1, 1, 2, 3, 2, 1, 2, 3, 0, 1, 1, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 3, 3, 0, 0, 2, 2, 3, 3],
               cols=[0, 2, 2, 3, 0, 2, 3, 0, 1, 2, 3, 0, 3, 1, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 0, 0, 0, 2, 2, 2, 3],
               cols=[0, 1, 2, 3, 1, 2, 3, 0, 0, 2, 1, 2, 3, 0, 2, 3, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
