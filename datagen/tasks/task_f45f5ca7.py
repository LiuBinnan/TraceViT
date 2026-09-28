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


def generate(colors=None, nrows=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    nrows: The number of rows to sample when colors is omitted.
  """

  if colors is None:
    if nrows is None:
      nrows = common.randint(8, 28)
    while True:
      colors = [common.choice([0, 2, 3, 4, 8]) for _ in range(nrows)]
      if len(set(colors)) == 5: break
  else:
    nrows = len(colors)

  grid = common.grid(10, nrows)
  offsets = [0, 0, 2, 4, 3, 0, 0, 0, 1, 0]
  for row, color in enumerate(colors):
    grid[row][0] = color

  output = common.grid(10, nrows)

  def slide_color(color):
    """Slides every column-0 cell of `color` right to its home column."""
    for row, cell in enumerate(colors):
      if cell == color:
        output[row][offsets[color]] = color

  slide_color(8)
  slide_color(2)
  slide_color(4)
  slide_color(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 8, 0, 3, 2, 4, 0, 8, 0, 3]),
      generate(colors=[3, 4, 2, 3, 0, 4, 8, 2, 0, 0]),
      generate(colors=[8, 3, 2, 4, 3, 8, 0, 3, 8, 0]),
  ]
  test = [
      generate(colors=[2, 4, 3, 2, 0, 8, 3, 0, 4, 2]),
  ]
  return {"train": train, "test": test}
