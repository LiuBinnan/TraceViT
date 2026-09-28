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


def generate(colors=None, tile_h=None, tile_w=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the input pixels.
    tile_h: The height of the input tile.
    tile_w: The width of the input tile.
  """

  if colors is None:
    if tile_h is None:
      tile_h = common.randint(2, 15)
    if tile_w is None:
      tile_w = common.randint(2, 15)
    raw_colors = common.random_colors(3)
    colors = [
        raw_colors[common.randint(0, 2)] for _ in range(tile_h * tile_w)
    ]
  else:
    tile_h = 3 if tile_h is None else tile_h
    tile_w = 4 if tile_w is None else tile_w

  grid = common.grid(tile_w, tile_h)
  for r in range(tile_h):
    for c in range(tile_w):
      grid[r][c] = colors[r * tile_w + c]

  output = common.grid(2 * tile_w, 2 * tile_h)

  def place_source_tile():
    for r in range(tile_h):
      for c in range(tile_w):
        output[r + tile_h][c + tile_w] = grid[r][c]

  def reflect_tile_left():
    for r in range(tile_h):
      for c in range(tile_w):
        output[r + tile_h][tile_w - 1 - c] = output[r + tile_h][
            c + tile_w
        ]

  def reflect_bottom_up():
    for r in range(tile_h):
      for c in range(2 * tile_w):
        output[tile_h - 1 - r][c] = output[r + tile_h][c]

  place_source_tile()
  reflect_tile_left()
  reflect_bottom_up()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 9, 9, 9, 5, 5, 5, 5, 7, 5, 7]),
      generate(colors=[6, 2, 4, 2, 2, 2, 6, 6, 6, 4, 2, 4]),
      generate(colors=[3, 3, 5, 5, 5, 8, 5, 8, 8, 8, 5, 8]),
  ]
  test = [
      generate(colors=[8, 5, 7, 8, 7, 7, 8, 8, 5, 5, 8, 5]),
  ]
  return {"train": train, "test": test}
