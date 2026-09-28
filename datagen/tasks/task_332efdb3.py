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


def generate(size=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The width and height of the square grid fallback.
    height: The number of rows, defaulting to size.
    width: The number of columns, defaulting to size.
  """

  if size is None:
    size = 2 * common.randint(1, 14) + 1
  if height is None:
    height = size
  if width is None:
    width = size

  grid, output = common.grids(width, height)

  def paint_even_rows():
    for row in range(0, height, 2):
      for col in range(width):
        output[row][col] = common.blue()

  def paint_even_cols():
    for row in range(height):
      for col in range(0, width, 2):
        output[row][col] = common.blue()

  paint_even_rows()
  paint_even_cols()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5),
      generate(size=7),
      generate(size=9),
  ]
  test = [
      generate(size=11),
  ]
  return {"train": train, "test": test}
