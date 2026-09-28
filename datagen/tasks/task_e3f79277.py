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


def generate(length=None, color=None, flip=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the lines.
    color: The color of the lines.
    flip: Whether to flip the grids.
    flop: Whether to flop the grids.
  """

  if length is None:
    length = common.randint(2, 6)
    color = common.random_color(exclude=[7])
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(6, 6, 7)
  for i in range(length):
    grid[0][i] = grid[i][0] = color
  if flip: grid = common.flip(grid)
  if flop: grid = common.flop(grid)

  # The input is an L-shaped corner: two perpendicular arms of `length` meeting
  # at one vertex. The answer scales the corner up - both arms grow to double
  # length - and then a diagonal joins their far tips, closing the corner into
  # a right triangle. Build the answer directly in the input's flip/flop
  # orientation (via put) so every frame already matches the final grid.
  output = common.grid(16, 16, 7)

  def put(r, c):
    fr = 15 - r if flip else r
    fc = 15 - c if flop else c
    output[fr][fc] = color

  def draw_top_arm():
    """Grow the horizontal arm to double length."""
    for i in range(2 * length):
      put(0, i)

  def draw_left_arm():
    """Grow the vertical arm to double length."""
    for i in range(2 * length):
      put(i, 0)

  def close_triangle():
    """Join the two arm tips with a diagonal, closing the triangle."""
    for i in range(2 * length):
      put(i, 2 * length - 1 - i)

  draw_top_arm()
  draw_left_arm()
  close_triangle()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, color=5, flip=1, flop=1),
      generate(length=3, color=9, flip=1, flop=0),
  ]
  test = [
      generate(length=4, color=8, flip=0, flop=1),
  ]
  return {"train": train, "test": test}
