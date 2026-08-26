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


def generate(
    width=None,
    height=None,
    spriterow=None,
    spritecol=None,
    brow=None,
    bcol=None,
    rows=None,
    cols=None,
    colors=None,
    output_height=None,
    output_width=None,
    sprite_removals=None,
    background_color=None,
    sprite_color=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    spriterow: the row of the sprite in the input grid
    spritecol: the column of the sprite in the input grid
    brow: the row of the box
    bcol: the column of the box
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    output_height: the height of the output box
    output_width: the width of the output box
    sprite_removals: how many attempts are made to remove sprite cells
    background_color: the color of the background
    sprite_color: the color of the input sprite
  """
  if width is None:
    if output_height is None:
      if height is None:
        height = common.randint(12, 30)
      output_height = common.randint(4, max(4, height // 2 - 2))
    elif height is None:
      height = common.randint(max(12, 2 * output_height + 4), 30)
    if output_width is None:
      if width is None:
        width = common.randint(12, 30)
      output_width = common.randint(4, max(4, width // 2 - 2))
    elif width is None:
      width = common.randint(max(12, 2 * output_width + 4), 30)
    sh, sw = output_height - 2, output_width - 2
    if background_color is None:
      background_color = common.randint(0, 9)
    if sprite_color is None:
      sprite_color = common.randint(0, 9)
      while sprite_color == background_color:
        sprite_color = common.randint(0, 9)
    if sprite_color == background_color:
      sprite_color = (sprite_color + 1) % 10
    colors = common.random_colors(4, exclude=[background_color, sprite_color])
    max_removals = max(1, (sw * sh) // 2)
    if sprite_removals is None:
      sprite_removals = common.randint(1, max_removals)
    sprite_removals = min(sprite_removals, max_removals)
    rows, cols = common.conway_sprite(sw, sh, sprite_removals)
    while True:
      spriterow = common.randint(0, height - sh)
      spritecol = common.randint(0, width - sw)
      brow = common.randint(0, height - sh - 2)
      bcol = common.randint(0, width - sw - 2)
      if abs(brow - spriterow) >= sh + 2: break
      if abs(bcol - spritecol) >= sw + 2: break

  sh = max(rows) + 1  # sprite height (row extent)
  sw = max(cols) + 1  # sprite width (col extent)
  if background_color is None:
    background_color = common.black()
  if sprite_color is None:
    sprite_color = common.cyan()
  grid = common.grid(width, height, background_color)
  output = common.grid(sw + 2, sh + 2, background_color)
  for r, c in zip(rows, cols):
    output[r + 1][c + 1] = grid[spriterow + r][spritecol + c] = sprite_color
  ph = sh + 1  # Shorthand (row extent of the box)
  pw = sw + 1  # Shorthand (col extent of the box)
  for i in range(1, pw):
    output[0][i] = grid[brow][bcol + i] = colors[0]
    output[ph][i] = grid[brow + ph][bcol + i] = colors[2]
  for i in range(1, ph):
    output[i][pw] = grid[brow + i][bcol + pw] = colors[1]
    output[i][0] = grid[brow + i][bcol] = colors[3]
  for r in range(sh):
    for c in range(sw):
      if output[r + 1][c + 1] == background_color:
        continue
      # Manhattan distance from this sprite cell to each box wall; the
      # strictly-nearest wall recolors the cell, ties stay cyan.
      dists = [r + 1, sw - c, sh - r, c + 1]  # top, right, bottom, left
      nearest = min(dists)
      color = sprite_color
      if dists.count(nearest) == 1:
        color = colors[dists.index(nearest)]
      output[r + 1][c + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=15, spriterow=1, spritecol=1, brow=7, bcol=6,
               rows=[0, 0, 1, 1, 2, 2, 2, 2, 3, 3],
               cols=[0, 3, 1, 3, 0, 1, 2, 3, 1, 3], colors=[4, 1, 3, 2]),
      generate(width=16, height=14, spriterow=2, spritecol=8, brow=6, bcol=1,
               rows=[0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2], colors=[3, 4, 2, 6]),
      generate(width=15, height=15, spriterow=9, spritecol=6, brow=1, bcol=2,
               rows=[0, 0, 0, 1, 1, 2, 2, 3, 3, 3],
               cols=[0, 1, 3, 1, 2, 1, 3, 0, 1, 3], colors=[7, 6, 1, 4]),
  ]
  test = [
      generate(width=16, height=16, spriterow=9, spritecol=2, brow=0, bcol=5,
               rows=[0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4],
               cols=[0, 1, 3, 4, 0, 2, 3, 1, 2, 3, 4, 2, 0, 1, 3, 4],
               colors=[1, 4, 3, 2]),
  ]
  return {"train": train, "test": test}
