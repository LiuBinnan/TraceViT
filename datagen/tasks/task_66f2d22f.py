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


def generate(top=None, bottom=None, width=None, height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    if width is None:
      width = common.randint(4, 9)
    if height is None:
      height = common.randint(3, 7)
    while True:
      top = [common.randint(0, 1) for _ in range(width * height)]
      bottom = [common.randint(0, 1) for _ in range(width * height)]
      nor_count = sum(not a and not b for a, b in zip(top, bottom))
      if 0 < nor_count < width * height:
        break
  else:
    if width is None:
      width = 7
    if height is None:
      height = 4

  grid = common.grid(2 * width, height)
  output = common.grid(width, height)
  for i, occupied in enumerate(top):
    grid[i // width][i % width] = 3 if occupied else 0
  for i, occupied in enumerate(bottom):
    grid[i // width][width + i % width] = 2 if occupied else 0
  for i, occupied in enumerate(top):
    if occupied:
      output[i // width][i % width] = 3
  for i, occupied in enumerate(bottom):
    if occupied:
      output[i // width][i % width] = 2
  for i, (top_occupied, bottom_occupied) in enumerate(zip(top, bottom)):
    if top_occupied and bottom_occupied:
      output[i // width][i % width] = 5
  output = [[5 if not top[row * width + col] and
             not bottom[row * width + col] else 0
             for col in range(width)] for row in range(height)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
               bottom=[1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]),
      generate(top=[1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
               bottom=[1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1]),
      generate(top=[0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
               bottom=[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0]),
      generate(top=[0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               bottom=[1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1]),
  ]
  test = [
      generate(top=[1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1],
               bottom=[0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1]),
  ]
  return {"train": train, "test": test}
