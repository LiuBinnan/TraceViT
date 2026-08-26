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


def generate(rows=None, cols=None, idxs=None, megarows=None, megacols=None,
             megaidxs=None, colors=None, size=14, height=None, width=None,
             spriteh=None, spritew=None, num_types=None, num_sprites=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of sprite indices
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where sprites should be placed
    megaidxs: a list of sprite indices for each sprite
    colors: a list of colors to be used for each sprite type
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    spriteh: the number of rows in each sprite / the output (defaults to 3)
    spritew: the number of columns in each sprite / the output (defaults to 3)
    num_types: the number of sprite types to generate
    num_sprites: the total number of sprite copies to place
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if spriteh is None:
    spriteh = 3
  if spritew is None:
    spritew = 3
  if rows is None:
    packed_rows = max(1, (height + 1) // (spriteh + 1))
    packed_cols = max(1, (width + 1) // (spritew + 1))
    sprite_capacity = packed_rows * packed_cols
    max_types = min(9, spriteh + spritew + 1, max(2, sprite_capacity - 1))
    if num_types is None:
      num_types = common.randint(2, max_types)
    num_types = max(2, min(num_types, max_types))
    min_sprites = num_types + 1
    max_sprites = min(sprite_capacity,
                      max(min_sprites, (height * width) // 16))
    if num_sprites is None:
      num_sprites = common.randint(min_sprites, max_sprites)
    num_sprites = max(min_sprites, min(num_sprites, max_sprites))
    # First chose the sprite types along with their colors.
    colors = common.random_colors(num_types)
    sprite_types = []
    while len(sprite_types) < len(colors):
      while True:
        rows, cols = common.conway_sprite(width=spritew, height=spriteh)
        if common.diagonally_connected(list(zip(rows, cols))): break
      sprite = list(zip(rows, cols))
      sprite.sort()
      if sprite not in sprite_types: sprite_types.append(sprite)
    rows, cols, idxs = [], [], []
    for idx, sprite in enumerate(sprite_types):
      rows.extend([s[0] for s in sprite])
      cols.extend([s[1] for s in sprite])
      idxs.extend([idx] * len(sprite))
    # Next, choose how many copies of each sprite type to place.  Type 0 stays
    # strictly most frequent, which is the object selected in the output.
    max_other = 0
    while max_other + (len(colors) - 1) * (max_other - 1) < num_sprites:
      max_other += 1
    num_sprites_per_type = [max_other] + [1] * (len(colors) - 1)
    remaining = num_sprites - sum(num_sprites_per_type)
    for idx in common.shuffle(list(range(1, len(colors)))):
      extra = min(remaining, max_other - 2)
      num_sprites_per_type[idx] += extra
      remaining -= extra
      if not remaining:
        break
    # Finally, pick non-overlapping locations for all the sprites.
    row_slack = height - (packed_rows * spriteh + packed_rows - 1)
    col_slack = width - (packed_cols * spritew + packed_cols - 1)
    row0 = common.randint(0, row_slack)
    col0 = common.randint(0, col_slack)
    candidates = []
    for prow in range(packed_rows):
      for pcol in range(packed_cols):
        candidates.append((row0 + prow * (spriteh + 1),
                           col0 + pcol * (spritew + 1)))
    candidates = common.shuffle(candidates)
    megarows, megacols, megaidxs = [], [], []
    for idx, num in enumerate(num_sprites_per_type):
      for _ in range(num):
        row, col = candidates.pop()
        megarows.append(row)
        megacols.append(col)
        megaidxs.append(idx)

  grid = common.grid(width, height)
  for megarow, megacol, megaidx in zip(megarows, megacols, megaidxs):
    for row, col, idx in zip(rows, cols, idxs):
      if idx != megaidx: continue
      grid[megarow + row][megacol + col] = colors[megaidx]
  output = [row[:] for row in grid]
  output = common.grid(width, height)
  for megarow, megacol, megaidx in zip(megarows, megacols, megaidxs):
    if megaidx:
      continue
    for row, col, idx in zip(rows, cols, idxs):
      if idx:
        continue
      output[megarow + row][megacol + col] = colors[megaidx]
  output = common.grid(spritew, spriteh)
  for row, col, idx in zip(rows, cols, idxs):
    if idx:
      continue
    output[row][col] = colors[0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2, 0, 0, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 0, 2, 0, 2, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[1, 2, 7, 7, 11], megacols=[2, 10, 3, 9, 1],
               megaidxs=[0, 0, 0, 1, 1], colors=[8, 2]),
      generate(rows=[0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 0, 0, 1, 2, 2],
               cols=[0, 1, 2, 0, 0, 2, 0, 1, 2, 1, 0, 2, 1, 0, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               megarows=[0, 1, 3, 5, 6, 8, 10, 11],
               megacols=[7, 2, 11, 6, 1, 9, 2, 11],
               megaidxs=[1, 0, 0, 2, 1, 0, 0, 1], colors=[4, 1, 2]),
      generate(rows=[0, 1, 1, 1, 2, 0, 0, 1, 1, 2],
               cols=[1, 0, 1, 2, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[2, 2, 8], megacols=[2, 9, 8], megaidxs=[0, 1, 0],
               colors=[8, 6]),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[1, 0, 1, 2, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               megarows=[2, 2, 7, 8, 11, 11], megacols=[3, 9, 6, 0, 4, 9],
               megaidxs=[1, 0, 2, 0, 0, 1], colors=[2, 3, 8]),
  ]
  return {"train": train, "test": test}
