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


def generate(size=None, left=None, width=None, height=None, red=None, cyan=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    left: The leftmost column of the box.
    width: The width of the box.
    height: The height of the box.
    red: The column of the red pixel.
    cyan: The column of the cyan pixel.
    flop: Whether to flop the grid.
  """

  if size is None:
    size = common.randint(5, 28)
    width = common.randint(3, size - 1)
    height = common.randint(2, size - 2)
    left = common.randint(0, size - width - 1)
    while True:
      red, cyan = common.randint(0, width - 1), common.randint(0, width - 1)
      if red + 1 < cyan: break
    flop = common.randint(0, 1)

  # Input: a gray box at the bottom, with a red and a cyan pixel sitting just
  # above its top edge (red to the left of cyan). Orient it up front so every
  # output frame below is built directly in the final orientation.
  grid = common.grid(size, size, 7)
  common.rect(grid, width, height, size - height, left, 5)
  grid[size - height - 1][left + red] = 2
  grid[size - height - 1][left + cyan] = 8
  if flop: grid = common.flop(grid)

  # Output: the same box (finalized in orientation), then the two markers move
  # to their solved positions - the red slides along the top to the cyan's
  # column, and the cyan drops to the bottom-right corner just past the box.
  output = common.grid(size, size, 7)
  common.rect(output, width, height, size - height, left, 5)
  if flop: output = common.flop(output)

  def put(r, c, v):
    output[r][size - 1 - c if flop else c] = v

  def slide_red_to_cyan():
    """Moves the red pixel along the top edge to the cyan pixel's column."""
    put(size - height - 1, left + cyan, 2)

  def drop_cyan_off_box():
    """Sends the cyan pixel to the bottom-right corner beside the box."""
    put(size - 1, left + width, 8)

  slide_red_to_cyan()
  drop_cyan_off_box()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, left=0, width=6, height=4, red=0, cyan=4, flop=False),
      generate(size=7, left=2, width=3, height=5, red=0, cyan=2, flop=False),
      generate(size=11, left=3, width=6, height=9, red=1, cyan=4, flop=True),
  ]
  test = [
      generate(size=19, left=1, width=17, height=9, red=2, cyan=7, flop=True),
  ]
  return {"train": train, "test": test}
