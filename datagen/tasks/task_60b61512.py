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


def generate(sprites=None, rows=None, cols=None, xpose=None, size=9,
             minisize=3, height=None, width=None, count=None, num_colors=None,
             offsets=None, sprite_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    sprites: a list of sprite indices for the pixels
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    xpose: whether to transpose the grid (it's an inverted transpose)
    size: the width and height of the (square) grid
    minisize: the width and height of the sprites
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: how many sprites to scatter (defaults to an area-scaled random count)
    num_colors: how many distinct foreground colors to draw from (1-8, random)
    offsets: maps each sprite index to its (row, col) top-left placement
    sprite_colors: maps each sprite index to its foreground color
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    # re_arc mirrors an area-scaled sprite count and 1-8 foreground colors;
    # sprites are scattered non-overlapping and non-adjacent (a one-cell moat
    # around each minisize box) so no two share a color-merged bounding box.
    if count is None:
      count = common.randint(1, max(1, (width * height) // 20))
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = min(num_colors, 8)
    palette = common.random_colors(num_colors, exclude=[common.orange()])
    sprites, rows, cols = [], [], []
    offsets, sprite_colors = {}, {}
    blocked = set()
    placed, trials, maxtrials = 0, 0, 4 * count
    while placed < count and trials <= maxtrials:
      trials += 1
      while True:
        sprite_rows, sprite_cols = common.conway_sprite()
        if common.diagonally_connected(list(zip(sprite_rows, sprite_cols))):
          break
      roff = common.randint(0, height - minisize)
      coff = common.randint(0, width - minisize)
      box = {(roff + r, coff + c)
             for r in range(minisize) for c in range(minisize)}
      if box & blocked:
        continue
      sprites.extend([placed] * len(sprite_rows))
      rows.extend(sprite_rows)
      cols.extend(sprite_cols)
      offsets[placed] = (roff, coff)
      sprite_colors[placed] = palette[placed % num_colors]
      blocked |= {(roff + r, coff + c)
                  for r in range(-1, minisize + 1)
                  for c in range(-1, minisize + 1)}
      placed += 1
    xpose = common.randint(0, 1)

  raw_grid = common.grid(width, height)
  for sprite, row, col in zip(sprites, rows, cols):
    roff, coff = offsets[sprite] if offsets else (4 if sprite else 1,
                                                  5 if sprite else 0)
    color = sprite_colors[sprite] if sprite_colors else common.yellow()
    raw_grid[row + roff][col + coff] = color
  raw_output = [row[:] for row in raw_grid]
  def orient(thegrid):
    return common.transpose_inverted(thegrid) if xpose else thegrid

  output = orient(raw_output)

  def fill_group(which):
    nonlocal output
    distinct = []
    for sprite in sprites:
      if sprite not in distinct:
        distinct.append(sprite)
    half = (len(distinct) + 1) // 2
    group = distinct[:half] if which == 0 else distinct[half:]
    for sprite in group:
      roff, coff = offsets[sprite] if offsets else (4 if sprite else 1,
                                                    5 if sprite else 0)
      color = sprite_colors[sprite] if sprite_colors else common.yellow()
      for row in range(minisize):
        for col in range(minisize):
          r, c = row + roff, col + coff
          raw_output[r][c] = color if raw_output[r][c] else common.orange()
    output = orient(raw_output)

  fill_group(0)
  fill_group(1)
  grid = orient(raw_grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(sprites=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               rows=[0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 2, 2, 0, 1, 1, 2, 0, 2],
               xpose=0),
      generate(sprites=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 1, 2],
               cols=[0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 1],
               xpose=0),
  ]
  test = [
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1],
               rows=[0, 1, 1, 2, 2, 0, 1, 2, 2],
               cols=[1, 0, 1, 1, 2, 2, 1, 0, 1],
               xpose=1),
  ]
  return {"train": train, "test": test}
