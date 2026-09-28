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
    width: Width of the output grid; randomized when masks are omitted.
    height: Height of the output grid; randomized when masks are omitted.
  """
  if top is None:
    if width is None:
      width = common.randint(3, 8)
    if height is None:
      height = common.randint(2, 6)
    while True:
      top = [common.randint(0, 1) for _ in range(width * height)]
      bottom = [common.randint(0, 1) for _ in range(width * height)]
      if (any(top[i] != bottom[i] for i in range(len(top))) and
          any(top[i] == bottom[i] for i in range(len(top)))):
        break
  else:
    if width is None:
      width = 5
    if height is None:
      height = 3

  grid = common.grid(width, 2 * height)
  output = common.grid(width, height)
  for i in range(len(top)):
    grid[i // width][i % width] = 9 if top[i] else 0
  for i in range(len(bottom)):
    grid[height + i // width][i % width] = 4 if bottom[i] else 0

  def reveal_exclusive_colors():
    """Keeps each layer's original color only where that layer is unique."""
    for i in range(len(top)):
      if top[i] and not bottom[i]:
        output[i // width][i % width] = 9
      if bottom[i] and not top[i]:
        output[i // width][i % width] = 4

  def unify_exclusive_regions():
    """Recolors both exclusive-color regions to the shared answer color."""
    for row in range(height):
      for col in range(width):
        if output[row][col] in [4, 9]:
          output[row][col] = common.pink()

  reveal_exclusive_colors()
  unify_exclusive_regions()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
               bottom=[0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1]),
      generate(top=[0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
               bottom=[1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1]),
      generate(top=[0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
               bottom=[0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0]),
      generate(top=[0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
               bottom=[1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0]),
      generate(top=[1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
               bottom=[1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]),
  ]
  test = [
      generate(top=[0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
               bottom=[1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]),
      generate(top=[1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
               bottom=[1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
