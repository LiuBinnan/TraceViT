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


def generate(vals=None, offset=None, size=9, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: a list of bar heights
    offset: the amount to shift bars horizontally
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if offset is None:
    offset = common.randint(0, 1)
    num = common.randint(4, 4 if offset == 1 else 5)
    vals = common.sample(range(1, height + 1), num)

  grid, output = common.grids(width, height)
  for idx, val in enumerate(vals):
    for c in range(val):
      grid[height - 1 - c][2 * idx + offset] = common.gray()

  def color_bar(target, color):
    for idx, val in enumerate(vals):
      if val != target:
        continue
      for c in range(val):
        output[height - 1 - c][2 * idx + offset] = color

  color_bar(min(vals), common.red())
  color_bar(max(vals), common.blue())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[6, 8, 4, 7, 3], offset=0),
      generate(vals=[7, 2, 9, 6], offset=0),
  ]
  test = [
      generate(vals=[1, 7, 5, 8], offset=1),
  ]
  return {"train": train, "test": test}
