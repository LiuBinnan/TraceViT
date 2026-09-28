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


def generate(wide=None, flop=None, brow=None, bcols=None, colors=None,
             size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The inner width of the portal.
    flop: Whether to flop the output.
    brow: The starting row of the shape.
    bcols: The starting columns of the left and right portals.
    colors: The colors to use.
    size: The size of the grid.
  """

  if wide is None:
    wide = common.randint(1, 2 if size is None or size >= 9 else 1)
    if size is None: size = common.randint(7 + wide, 16)
    flop = common.randint(0, 1)
    brow = common.randint(1, size - 6)
    while True:
      bcols = [common.randint(0, size - 2 - wide) for _ in range(2)]
      if bcols[0] + wide + 2 < bcols[1]: break
    colors = [common.random_color(exclude=[4, 7])] * (wide * 3)
    if wide == 1:  # If we're thin, we can cut off the top and maybe the next.
      if common.randint(0, 1):
        colors[0] = 0
        if common.randint(0, 1):
          colors[1] = 0
    else:  # If we're fat, we could lose one of the bottom, and maybe both tops.
      if common.randint(0, 1): colors[common.randint(4, 5)] = 0
      if common.randint(0, 1): colors[0] = 0
      if common.randint(0, 1): colors[1] = 0

  # The solving story: the shape resting in the right portal's mouth is
  # swallowed by that portal and re-emerges from the left portal at the grid's
  # foot. We build the input, flop it up front so the final orientation is
  # fixed, then move the shape through the portals via an orientation-aware
  # column mapper (never re-flopping the output, which would desync the frames).
  size = 7 + wide if size is None else size
  grid = common.grid(size, size, 7)
  # Draw the left portal (top).
  grid[0][bcols[0]] = common.yellow()
  for i in range(wide): grid[0][bcols[0] + i + 1] = common.yellow()
  grid[0][bcols[0] + wide + 1] = common.yellow()
  grid[1][bcols[0]] = common.yellow()
  grid[1][bcols[0] + wide + 1] = common.yellow()
  # Draw the right portal (bottom).
  grid[size - 1][bcols[1]] = common.yellow()
  for i in range(wide): grid[size - 1][bcols[1] + i + 1] = common.yellow()
  grid[size - 1][bcols[1] + wide + 1] = common.yellow()
  grid[size - 2][bcols[1]] = common.yellow()
  grid[size - 2][bcols[1] + wide + 1] = common.yellow()
  # Draw the shape sitting in the right portal's mouth.
  for i, color in enumerate(colors):
    if not color: continue
    grid[brow + i // wide][bcols[1] + 1 + i % wide] = color
  if flop: grid = common.flop(grid)
  output = common.deepcopy(grid)

  def orient(col):
    return size - 1 - col if flop else col

  def enter_portal():
    """The right portal swallows the shape, clearing it from its mouth."""
    for i, color in enumerate(colors):
      if not color: continue
      output[brow + i // wide][orient(bcols[1] + 1 + i % wide)] = common.orange()

  def exit_portal():
    """The shape re-emerges from the left portal at the grid's foot."""
    for i, color in enumerate(colors):
      if not color: continue
      output[size - 3 + i // wide][orient(bcols[0] + 1 + i % wide)] = color

  enter_portal()
  exit_portal()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=2, flop=0, brow=3, bcols=[0, 5], colors=[0, 0, 1, 1, 1, 1]),
      generate(wide=1, flop=1, brow=1, bcols=[0, 5], colors=[2, 2, 2]),
      generate(wide=2, flop=1, brow=2, bcols=[0, 5], colors=[0, 8, 8, 8, 0, 8]),
  ]
  test = [
      generate(wide=1, flop=1, brow=2, bcols=[0, 4], colors=[0, 0, 3]),
  ]
  return {"train": train, "test": test}
