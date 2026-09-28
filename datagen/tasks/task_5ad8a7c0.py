# Copyright 2026 Google LLC
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


def generate(cols=None, nrows=None, half=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: The columns of the red pixels.
    nrows: The number of independently generated rows.
    half: Half the width of the horizontally symmetric grid.
  """

  if cols is None:
    if nrows is None:
      nrows = common.randint(3, 8)
    if half is None:
      half = common.randint(3, 5)
    while True:
      cols = [common.randint(-1, half - 1) for _ in range(nrows)]
      if max(cols) != -1: break
  else:
    if nrows is None:
      nrows = len(cols)
    if half is None:
      half = 3

  grid, output = common.grids(2 * half, nrows)
  target_col = max(cols)
  for r, col in enumerate(cols):
    if col == -1: continue
    grid[r][col] = grid[r][2 * half - 1 - col] = 2
  for r, col in enumerate(cols):
    if col != target_col: continue
    for c in range(col, half):
      output[r][c] = 2
  for r, col in enumerate(cols):
    if col != target_col: continue
    for c in range(col, half):
      output[r][2 * half - 1 - c] = 2
  for r, col in enumerate(cols):
    if col == -1 or col == target_col: continue
    output[r][col] = output[r][2 * half - 1 - col] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[0, -1, -1, 0]),
      generate(cols=[0, 1, 2, 1]),
      generate(cols=[-1, 1, 0, 1]),
      generate(cols=[2, 1, 0, 1]),
      generate(cols=[0, 1, 1, 0]),
  ]
  test = [
      generate(cols=[0, 1, -1, 0]),
  ]
  return {"train": train, "test": test}
