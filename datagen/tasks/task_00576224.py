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


def generate(colors=None, size=2):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    size: The height and width of the input tile.
  """

  if size is None or colors is None:
    size = common.randint(2, 10) if size is None else size
    colors = ([common.random_color() for _ in range(size * size)]
              if colors is None else colors)

  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  output = common.grid(3 * size, 3 * size)

  def fill_band(row):
    for i, color in enumerate(colors):
      for col in range(3):
        r = row * size + i // size
        c = col * size + ((size - 1 - i % size)
                          if row % 2 else (i % size))
        output[r][c] = color

  fill_band(0)
  fill_band(1)
  fill_band(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 9, 4, 3]),
      generate(colors=[8, 6, 6, 4]),
  ]
  test = [
      generate(colors=[3, 2, 7, 8]),
  ]
  return {"train": train, "test": test}
