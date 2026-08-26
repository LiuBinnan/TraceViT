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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             brows=None, bcols=None, num_sprites=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the sprites
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    num_sprites: the requested number of sprites to place
  """
  if (rows is None or cols is None or idxs is None or
      brows is None or bcols is None):
    if width is None:
      width = common.randint(10, 30)
    if height is None:
      height = common.randint(10, 30)
    if num_sprites is None:
      num_sprites = common.randint(1, min(30, (width * height) // 9))
    num_sprites = min(30, max(1, num_sprites))

    rows, cols, idxs = [], [], []
    brows, bcols = [], []
    available = {(r, c) for r in range(height) for c in range(width)}
    trials, maxtrials = 0, num_sprites * 5
    while trials < maxtrials and len(brows) < num_sprites:
      sprite_height = common.randint(1, 5)
      sprite_width = common.randint(1, 5)
      sprite_area = sprite_height * sprite_width
      delta = common.randint(0, sprite_area // 2)
      sprite_size = common.choice([delta + 1, sprite_area - delta])
      sprite_size = min(max(1, sprite_size), sprite_area)
      pixels = common.continuous_creature(
          sprite_size, sprite_width, sprite_height)
      brow = common.randint(0, height - sprite_height)
      bcol = common.randint(0, width - sprite_width)
      placed = {(brow + r, bcol + c) for r, c in pixels}
      if placed.issubset(available):
        idx = len(brows)
        brows.append(brow)
        bcols.append(bcol)
        rows.extend([p[0] for p in pixels])
        cols.extend([p[1] for p in pixels])
        idxs.extend([idx] * len(pixels))
        for r, c in placed:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              available.discard((r + dr, c + dc))
      trials += 1

  grid, output = common.grid(width, height), common.grid(len(brows), len(brows))
  for r, c, i in zip(rows, cols, idxs):
    grid[brows[i] + r][bcols[i] + c] = common.cyan()
  for i in range(len(brows)):
    output[i][i] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=16,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 2,
                     0, 0, 1, 1],
               cols=[1, 2, 1, 2, 0, 1, 2, 1, 1, 2, 0, 1, 2, 2, 2, 3, 0, 1, 2, 2,
                     0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3],
               brows=[1, 6, 10, 12], bcols=[1, 4, 1, 7]),
      generate(width=12, height=12,
               rows=[0, 1, 1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1],
               cols=[2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 0, 2, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 3, 8], bcols=[1, 5, 3]),
      generate(width=12, height=8,
               rows=[0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[0, 1, 0, 1, 2, 1, 2, 0, 0, 1, 0],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
               brows=[2, 3],
               bcols=[2, 8]),
  ]
  test = [
      generate(width=12, height=15,
               rows=[0, 1, 1, 2, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 1,
                     1, 0, 0],
               cols=[1, 0, 1, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 1, 2, 2, 0, 1, 0, 1,
                     2, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3,
                     3, 4, 4],
               brows=[1, 2, 9, 9, 13], bcols=[8, 3, 1, 8, 6]),
  ]
  return {"train": train, "test": test}
