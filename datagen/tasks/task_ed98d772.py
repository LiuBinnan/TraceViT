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


def generate(colors=None, psize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    psize: The height and width of the input tile.
  """

  if colors is None:
    if psize is None:
      psize = common.randint(3, 12)
    hue = common.random_color()
    while True:
      colors = [hue * common.randint(0, 1) for _ in range(psize * psize)]
      if len(set(colors)) == 2: break
  elif psize is None:
    psize = 3

  # Input: the square tile. Build it first; the output is a 2p x 2p pinwheel of
  # the tile plus three rotated copies, one per quadrant.
  grid, output = common.grid(psize, psize), common.grid(2 * psize, 2 * psize)
  for row in range(psize):
    for col in range(psize):
      grid[row][col] = colors[row * psize + col]

  # Stage 1: stamp the tile itself into the top-left quadrant.
  def stamp_top_left():
    for row in range(psize):
      for col in range(psize):
        output[row][col] = colors[row * psize + col]

  # Stage 2: rotate it into the top-right quadrant.
  def stamp_top_right():
    for row in range(psize):
      for col in range(psize):
        output[psize - 1 - col][row + psize] = colors[row * psize + col]

  # Stage 3: rotate it into the bottom-right quadrant.
  def stamp_bottom_right():
    for row in range(psize):
      for col in range(psize):
        output[col + psize][2 * psize - 1 - row] = colors[row * psize + col]

  # Stage 4: rotate it into the bottom-left quadrant, completing the pinwheel.
  def stamp_bottom_left():
    for row in range(psize):
      for col in range(psize):
        output[2 * psize - 1 - row][psize - 1 - col] = colors[row * psize + col]

  stamp_top_left()
  stamp_top_right()
  stamp_bottom_right()
  stamp_bottom_left()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 0, 8, 8, 0, 0, 8, 0, 0]),
      generate(colors=[3, 0, 3, 0, 3, 3, 3, 3, 3]),
      generate(colors=[3, 3, 3, 0, 0, 3, 3, 0, 0]),
      generate(colors=[0, 7, 7, 0, 0, 0, 7, 7, 0]),
      generate(colors=[9, 9, 9, 0, 0, 0, 9, 9, 0]),
  ]
  test = [
      generate(colors=[6, 6, 0, 6, 6, 0, 0, 0, 6]),
  ]
  return {"train": train, "test": test}
