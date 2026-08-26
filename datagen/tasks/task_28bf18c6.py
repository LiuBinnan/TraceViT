# Copyright 2025 Google LLC
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


def generate(rows=None, cols=None, row=None, col=None, color=None, size=8,
             minisize=3, height=None, width=None, sprite_height=None,
             sprite_width=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical coordinate where the sprite should be placed
    col: a horizontal coordinate where the sprite should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the sprite
    height: the height of the grid
    width: the width of the grid
    sprite_height: the height of the sprite sampling box
    sprite_width: the width of the sprite sampling box
    density: the number of extra connected sprite cells after the seed cell
  """
  if rows is None:
    if height is None: height = common.randint(3, 30)
    if width is None: width = common.randint(3, 30)
    if sprite_height is None:
      sprite_height = common.randint(1, min(14, height - 1))
    else:
      sprite_height = max(1, min(sprite_height, min(14, height - 1)))
    if sprite_width is None:
      sprite_width = common.randint(1, min(14, width - 1))
    else:
      sprite_width = max(1, min(sprite_width, min(14, width - 1)))
    max_density = sprite_height * sprite_width - 1
    if density is None:
      midpoint = (sprite_height * sprite_width) // 2
      dev = common.randint(0, midpoint)
      density = common.choice([dev, sprite_height * sprite_width - dev])
    density = max(0, min(max_density, density))
    pixels = common.continuous_creature(density + 1, sprite_width,
                                        sprite_height)
    rows, cols = zip(*pixels)
    rows, cols = list(rows), list(cols)
    color = common.random_color()

  if height is None: height = size
  if width is None: width = size
  sprite_height = max(rows) + 1
  sprite_width = max(cols) + 1
  if row is None: row = common.randint(0, height - sprite_height - 1)
  if col is None: col = common.randint(0, width - sprite_width - 1)
  if color is None: color = common.random_color()

  grid = common.grid(width, height)
  output = common.grid(2 * sprite_width, sprite_height)
  for r, c in zip(rows, cols):
    grid[row + r][col + c] = color
    output[r][c + sprite_width] = output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2, 2], cols=[0, 1, 1, 0, 1, 2], row=1, col=1,
               color=8),
      generate(rows=[0, 1, 1, 1, 2, 2], cols=[1, 0, 1, 2, 0, 1], row=5, col=2,
               color=2),
      generate(rows=[0, 0, 1, 2], cols=[1, 2, 0, 1], row=1, col=4,
               color=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2], cols=[2, 0, 1, 2, 0], row=4, col=1,
               color=3),
  ]
  return {"train": train, "test": test}
