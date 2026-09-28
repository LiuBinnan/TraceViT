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


def generate(spacing=None, start=None, size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    spacing: The spacing of the input pixels.
    start: The start of the input pixels.
    size: The height and width of the square grid.
  """

  if spacing is None:
    size = 15 if size is None else size
    spacing = common.randint(2, max(2, (size - 2) // 3))
    start = common.randint(0, 1)
  elif size is None:
    size = 15

  grid = common.grid(size, size)
  num = 0
  row = start
  while row < size:
    if num < 3:
      grid[row][row] = common.blue()
    row += spacing
    num += 1
  output = common.deepcopy(grid)

  def trace_progression():
    """Traces the whole inferred diagonal progression."""
    row = start
    while row < size:
      output[row][row] = common.red()
      row += spacing

  def restore_given_markers():
    """Restores the three visible terms of the progression."""
    row = start
    for _ in range(3):
      output[row][row] = common.blue()
      row += spacing

  trace_progression()
  restore_given_markers()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(spacing=4, start=0),
      generate(spacing=2, start=1),
  ]
  test = [
      generate(spacing=3, start=0),
  ]
  return {"train": train, "test": test}
