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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None, size=10,
             height=None, width=None, num_sprites=None, num_colors=None,
             bg_color=None, sprite_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where the sprites should be placed
    bcols: a list of horizontal coordinates where the sprites should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_sprites: the number of sprites to attempt placing
    num_colors: the number of input foreground colors to use
    bg_color: the background color
    sprite_colors: the input foreground colors
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    if num_sprites is None:
      num_sprites = common.randint(1, max(1, (height * width) // 10))
    if bg_color is None:
      bg_options = [common.black()] * 4 + common.random_colors(
          7, exclude=[common.blue(), common.red()])
      bg_color = common.choice(bg_options)
    if num_colors is None:
      color_pool = common.random_colors(
          7, exclude=[common.blue(), common.red()])
      if bg_color in color_pool:
        color_pool.remove(bg_color)
      num_colors = common.randint(1, len(color_pool))
    if sprite_colors is None:
      sprite_colors = common.random_colors(
          num_colors, exclude=[bg_color, common.blue(), common.red()])
    # Choose connected sprites and place them without touching.
    rows, cols, idxs, brows, bcols = [], [], [], [], []
    blocked = set()
    trials, maxtrials = 0, 20 * num_sprites
    while len(brows) < num_sprites and trials <= maxtrials:
      wide = common.randint(2, 4)
      tall = 6 - wide
      count = common.randint(4, 8)
      count = count if common.randint(0, 2) else 6
      pixels = common.continuous_creature(count, wide, tall)
      max_row = height - max([p[0] for p in pixels]) - 1
      max_col = width - max([p[1] for p in pixels]) - 1
      brow = common.randint(0, max_row)
      bcol = common.randint(0, max_col)
      placed = set((brow + row, bcol + col) for row, col in pixels)
      if not placed & blocked:
        idx = len(brows)
        brows.append(brow)
        bcols.append(bcol)
        rows.extend([p[0] for p in pixels])
        cols.extend([p[1] for p in pixels])
        idxs.extend([idx] * len(pixels))
        blocked.update(placed)
        for row, col in placed:
          for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
              blocked.add((nr, nc))
      trials += 1

  grid, output = common.grids(
      width, height, bg_color if bg_color is not None else common.black())
  for row, col, idx in zip(rows, cols, idxs):
    color = (sprite_colors[idx % len(sprite_colors)]
             if sprite_colors else common.gray())
    grid[row + brows[idx]][col + bcols[idx]] = color
  sprite_ids = sorted(set(idxs))
  for target in sprite_ids[:1]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[1:2]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[2:3]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[3:4]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[4:5]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[5:6]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[6:7]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  for target in sprite_ids[7:]:
    for row, col, idx in zip(rows, cols, idxs):
      if idx != target: continue
      sprite_size = len([i for i in idxs if i == idx])
      color = common.red() if sprite_size == 6 else common.blue()
      output[row + brows[idx]][col + bcols[idx]] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1],
               cols=[0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               brows=[2, 5, 7], bcols=[2, 5, 1]),
      generate(rows=[0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
                     1, 2, 2, 0, 0, 1, 1],
               cols=[2, 0, 1, 2, 2, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 0, 0, 0, 1, 0,
                     1, 0, 1, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4,
                     4, 4, 4, 5, 5, 5, 5],
               brows=[0, 1, 4, 4, 6, 7],
               bcols=[6, 0, 2, 8, 5, 1]),
      generate(rows=[0, 0, 0, 1, 1, 2, 3, 0, 0, 0, 1, 2, 3, 0, 0, 1, 1, 0, 0, 1,
                     1, 2, 2, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 2, 2],
               cols=[0, 1, 2, 1, 2, 2, 2, 0, 1, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1,
                     2, 1, 2, 0, 0, 0, 0, 1, 1, 0, 1, 2, 3, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3,
                     3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6],
               brows=[0, 0, 1, 4, 4, 5, 7],
               bcols=[0, 7, 4, 4, 9, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1,
                     0, 1, 2, 3, 0, 0, 0, 0, 0],
               cols=[1, 2, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 0, 1, 0, 1, 0, 1, 2, 3,
                     0, 0, 0, 0, 0, 1, 2, 3, 4],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3, 4, 4, 4, 4, 4],
               brows=[0, 0, 4, 4, 8],
               bcols=[0, 5, 1, 7, 1]),
  ]
  return {"train": train, "test": test}
