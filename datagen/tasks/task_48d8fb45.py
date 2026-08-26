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


def generate(sprites=None, rows=None, cols=None, minirows=None, minicols=None,
             color=None, size=10, minisize=3, gh=None, gw=None,
             minisizeh=None, minisizew=None, count=None, num_colors=None,
             sprite_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    sprites: a list of digits representing sprite indices
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    minirows: a list of vertical coordinates where sprites should be placed
    minicols: a list of horizontal coordinates where sprites should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the (square) grid for sprites
    gh: the height (row extent) of the input grid; defaults to size
    gw: the width (col extent) of the input grid; defaults to size
    minisizeh: the height of each sprite's bounding box; defaults to minisize
    minisizew: the width of each sprite's bounding box; defaults to minisize
    count: how many sprites to scatter; defaults to an area-scaled random count
    num_colors: how many foreground colors to draw from; defaults to 1-8
    sprite_colors: maps each sprite index to its foreground color
  """
  if minisizeh is None: minisizeh = minisize
  if minisizew is None: minisizew = minisize
  if rows is None:
    if gh is None: gh = common.randint(10, 30)
    if gw is None: gw = common.randint(10, 30)
    gh = max(gh, minisizeh * 3 + 2)
    gw = max(gw, minisizew * 3 + 2)
    if count is None:
      count = common.randint(2, max(2, (gh * gw) // 15))
    count = max(1, count)
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = max(1, min(num_colors, 8))
    palette = common.random_colors(num_colors, exclude=[common.gray()])
    minirows, minicols = [], []
    trials, maxtrials = 0, 4 * count
    while len(minirows) < count and trials < maxtrials:
      trials += 1
      row = common.randint(1, gh - minisizeh)
      col = common.randint(0, gw - minisizew)
      overlaps = False
      for r, c in zip(minirows, minicols):
        overlaps = overlaps or (abs(r - row) < minisizeh + 2 and
                                abs(c - col) <= minisizew + 1)
      if overlaps: continue
      minirows.append(row)
      minicols.append(col)
    sprites, rows, cols = [], [], []
    for sprite in range(len(minirows)):
      while True:
        sprite_rows, sprite_cols = common.conway_sprite(
            width=minisizew, height=minisizeh)
        sprite_rows, sprite_cols = sprite_rows + [0], sprite_cols + [1]
        if _diagonally_connected(list(zip(sprite_rows, sprite_cols))):
          break
      rows, cols = rows + sprite_rows, cols + sprite_cols
      sprites.extend([sprite] * len(sprite_rows))
    color = palette[0]
    sprite_colors = {
        sprite: palette[sprite % num_colors] for sprite in range(len(minirows))
    }

  if gh is None: gh = size
  if gw is None: gw = size
  grid = common.grid(gw, gh)
  grid[minirows[0] - 1][minicols[0] + 1] = common.gray()
  for sprite, r, c in zip(sprites, rows, cols):
    mr, mc = minirows[sprite], minicols[sprite]
    grid[mr + r][mc + c] = sprite_colors[sprite] if sprite_colors else color
  output = [row[:] for row in grid]
  output = common.grid(gw, gh)
  output[minirows[0] - 1][minicols[0] + 1] = common.gray()
  for sprite, r, c in zip(sprites, rows, cols):
    if sprite != 0:
      continue
    mr, mc = minirows[sprite], minicols[sprite]
    output[mr + r][mc + c] = sprite_colors[sprite] if sprite_colors else color
  sprite0_rows = [r for sprite, r in zip(sprites, rows) if sprite == 0]
  sprite0_cols = [c for sprite, c in zip(sprites, cols) if sprite == 0]
  oh = max(sprite0_rows) - min(sprite0_rows) + 1
  ow = max(sprite0_cols) - min(sprite0_cols) + 1
  r0, c0 = min(sprite0_rows), min(sprite0_cols)
  output = common.grid(ow, oh)
  for sprite, r, c in zip(sprites, rows, cols):
    if sprite != 0:
      continue
    output[r - r0][c - c0] = sprite_colors[sprite] if sprite_colors else color
  return {"input": grid, "output": output}


def _diagonally_connected(pixels):
  """Fast 8-neighbor connectivity check for larger sampled sprites."""
  remaining = set(pixels)
  if not remaining:
    return False
  queue = [next(iter(remaining))]
  remaining.remove(queue[0])
  while queue:
    row, col = queue.pop()
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        neighbor = (row + dr, col + dc)
        if neighbor in remaining:
          remaining.remove(neighbor)
          queue.append(neighbor)
  return not remaining


def validate():
  """Validates the generator."""
  train = [
      generate(sprites=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
               rows=[0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2, 1, 2, 0, 1, 1, 1, 2, 0, 1, 2, 1, 2],
               minirows=[3, 1, 7], minicols=[2, 7, 5], color=1),
      generate(sprites=[0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 1, 1, 0, 2, 1, 2],
               minirows=[2, 3], minicols=[6, 1], color=4),
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 1, 1, 2, 0, 0, 1, 1, 2],
               cols=[1, 2, 0, 1, 1, 1, 2, 0, 2, 1],
               minirows=[5, 2], minicols=[6, 1], color=2),
  ]
  test = [
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
               rows=[0, 1, 1, 2, 2, 0, 1, 1, 2, 0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 2],
               minirows=[1, 4, 6], minicols=[5, 1, 5], color=3),
  ]
  return {"train": train, "test": test}
