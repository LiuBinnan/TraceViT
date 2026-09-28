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


def generate(top=None, bottom=None, width=4, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the left grid.
    bottom: Boolean values for the right grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    width = common.randint(3, 8)
    height = common.randint(4, 9)
    top = [common.randint(0, 1) for _ in range(width * height)]
    bottom = [common.randint(0, 1) for _ in range(width * height)]

  grid = common.grid(2 * width + 1, height)
  output = common.grid(width, height)

  for index in range(len(top)):
    if top[index]:
      grid[index // width][index % width] = 8

  for row in range(height):
    grid[row][width] = 4

  for index in range(len(bottom)):
    if bottom[index]:
      grid[index // width][width + 1 + index % width] = 5

  for index in range(len(top)):
    if top[index] and not bottom[index]:
      output[index // width][index % width] = 8
    if bottom[index] and not top[index]:
      output[index // width][index % width] = 5

  for row in range(height):
    for col in range(width):
      if output[row][col] in [5, 8]:
        output[row][col] = 2

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
               bottom=[0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1]),
      generate(top=[0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
               bottom=[1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]),
      generate(top=[0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
               bottom=[0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1]),
      generate(top=[1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1],
               bottom=[0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1]),
  ]
  test = [
      generate(top=[0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
               bottom=[1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
