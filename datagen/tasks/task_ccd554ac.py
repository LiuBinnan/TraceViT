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


def generate(size=None, colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    colors: A list of colors to use.
    density: Removal-attempt multiplier for the randomized input sprite.
  """

  if size is None:
    size = common.randint(2, 5)
    fgcolor = common.random_color()
    if density is None:
      density = 2
    pixels = common.diagonally_connected_sprite(size, size, density * size)
    colors = [0] * (size * size)
    for row in range(size):
      for col in range(size):
        colors[row * size + col] = fgcolor if (row, col) in pixels else 0
    colors = "".join(str(c) for c in colors)

  # Input: the size x size pattern. Output: that pattern tiled size times in
  # each direction, revealed one horizontal band of copies at a time.
  grid = common.grid(size, size)
  output = common.grid(size * size, size * size)
  for row in range(size):
    for col in range(size):
      grid[row][col] = int(colors[row * size + col])

  def tile_row(k):
    """Stamps the k-th horizontal band: the input tiled across the width."""
    if k >= size:
      return
    for row in range(size):
      for col in range(size):
        for c in range(size):
          output[k * size + row][c * size + col] = grid[row][col]

  tile_row(0)
  tile_row(1)
  tile_row(2)
  tile_row(3)
  tile_row(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, colors="008888800"),
      generate(size=2, colors="1011"),
      generate(size=2, colors="0330"),
      generate(size=4, colors="0020202002022220"),
      generate(size=3, colors="202020222"),
      generate(size=4, colors="0700777707000707"),
  ]
  test = [
      generate(size=5, colors="0880088888088008888808808"),
  ]
  return {"train": train, "test": test}
