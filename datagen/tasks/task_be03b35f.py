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


def generate(colors=None, cvalue=1, tsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    cvalue: The color used for active cells in the binary tile.
    tsize: The side length of the hidden binary tile. Defaults to 2 for the
      official examples; randomized instances use 2 through 4.
  """

  if colors is None or cvalue is None or cvalue == 2:
    # Preserve blue (1) as the validation default, but let
    # randomized instances relabel the tile bits without colliding with the
    # load-bearing red mask.
    if cvalue is None or cvalue == 2:
      cvalue = common.random_color(exclude=[2])
    if tsize is None:
      tsize = common.randint(2, 4) if colors is None else 2
    if colors is None:
      if tsize == 2:
        while True:
          colors = [common.randint(0, 1) for _ in range(4)]
          if sum(colors) > 0 and sum(colors) < 4: break
      else:
        while True:
          colors = [common.randint(0, 1) for _ in range(tsize * tsize)]
          if sum(colors) > 0 and sum(colors) < tsize * tsize: break
  elif tsize is None:
    tsize = 2

  if tsize == 2:
    grid = common.grid(5, 5)
  else:
    grid = common.grid(2 * tsize + 1, 2 * tsize + 1)
    for r in range(tsize):
      for c in range(tsize):
        value = cvalue if colors[r * tsize + c] else 0
        grid[c][tsize - 1 - r] = value
        grid[tsize - 1 - r][2 * tsize - c] = value
        grid[2 * tsize - c][r] = value
    common.rect(grid, tsize, tsize, tsize + 1, tsize + 1, 2)
  if tsize == 2:
    grid[0][1] = grid[1][4] = grid[4][0] = cvalue if colors[0] else 0
  if tsize == 2:
    grid[1][1] = grid[1][3] = grid[3][0] = cvalue if colors[1] else 0
  if tsize == 2:
    grid[0][0] = grid[0][4] = grid[4][1] = cvalue if colors[2] else 0
  if tsize == 2:
    grid[1][0] = grid[0][3] = grid[3][1] = cvalue if colors[3] else 0
  if tsize == 2:
    common.rect(grid, 2, 2, 3, 3, 2)
  output = common.grid(tsize, tsize)

  def lift_tile():
    """Lifts the top-left visible quadrant, a rotated copy of the hidden tile."""
    for r in range(tsize):
      for c in range(tsize):
        output[r][c] = grid[r][c]

  def rotate_upright():
    """Turns the lifted tile a quarter-turn to match the masked corner's orientation."""
    upright = common.flip(common.transpose(output))
    for r in range(tsize):
      for c in range(tsize):
        output[r][c] = upright[r][c]

  lift_tile()
  rotate_upright()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 1, 1, 1]),
      generate(colors=[1, 0, 1, 1]),
      generate(colors=[1, 0, 1, 0]),
  ]
  test = [
      generate(colors=[1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
