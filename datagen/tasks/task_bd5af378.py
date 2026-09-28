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


def generate(width=None, height=None, colors=None, flip=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the boxes.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
  """

  if width is None:
    height, width = common.randint(5, 28), common.randint(5, 28)
    colors = common.random_colors(2, exclude=[8])
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(width, height)
  common.rect(grid, width, height, 0, 0, colors[0])
  common.rect(grid, width - 1, height - 1, 1, 1, colors[1])
  output = common.grid(width, height)

  def swap_frames():
    """Swaps the two roles: block color becomes the frame, frame color the block."""
    common.rect(output, width, height, 0, 0, colors[1])
    common.rect(output, width - 1, height - 1, 1, 1, colors[0])

  def carve_core():
    """Carves an azure core inside the nested rectangles."""
    common.rect(output, width - 2, height - 2, 2, 2, common.cyan())

  def draw_diagonal():
    """Caps the corner with azure and shoots a colors[1] ray down the diagonal."""
    output[0][0] = common.cyan()
    output[1][1] = common.cyan()
    for i in range(2, min(width, height)):
      output[i][i] = colors[1]

  swap_frames()
  carve_core()
  draw_diagonal()
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=5, colors=[7, 9], flip=True, flop=True),
      generate(width=8, height=5, colors=[3, 6], flip=True, flop=False),
      generate(width=6, height=8, colors=[5, 1], flip=True, flop=True),
      generate(width=10, height=10, colors=[1, 6], flip=False, flop=False),
  ]
  test = [
      generate(width=8, height=10, colors=[7, 3], flip=True, flop=False),
  ]
  return {"train": train, "test": test}
