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


def generate(row=None, length=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: Row of the line.
    length: Length of the line.
    size: Height and width of the square grid.
  """

  if row is None:
    if size is None:
      size = common.randint(14, 28)
    length = common.randint(1, min(7, (size - 1) // 2))
    row = common.randint(0, size - 1 - length * 2)
  elif size is None:
    size = 16

  grid, output = common.grids(size, size, 7)
  for i in range(length):
    grid[size - 1 - row - i][row + i] = 2
  for i in range(length):
    output[size - 1 - row - i - length][row + i + length] = 2
  output[size - 1 - row - 2 * length][row + 2 * length] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, length=2),
      generate(row=0, length=1),
      generate(row=3, length=3),
  ]
  test = [
      generate(row=6, length=4),
  ]
  return {"train": train, "test": test}
