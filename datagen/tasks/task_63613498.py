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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None,
             colors=None, bcolor=None, size=10, height=None, width=None,
             num_sprites=None, num_colors=None, max_cells=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    colors: a list of colors to be used for each sprite
    bcolor: a color to be used for the boxed sprite
    size: the size of the input and output grids
    height: the number of rows in the input and output grids
    width: the number of columns in the input and output grids
    num_sprites: the requested number of placed sprites
    num_colors: the size of the legal object-color palette
    max_cells: the largest connected sprite size in the 3x3 box
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    if num_sprites is None:
      num_sprites = common.randint(1, max(1, (width * height) // 20))
    if num_colors is None:
      num_colors = common.randint(1, 8)
    if max_cells is None:
      max_cells = common.randint(2, 9)
    num_sprites = max(1, num_sprites)
    num_colors = max(1, min(7, num_colors))
    max_cells = max(2, min(8, max_cells))

    brows, bcols = [], []
    for _ in range(num_sprites):
      candidates = []
      for row in range(height - 2):
        for col in range(width - 2):
          if row < 5 and col < 5:
            continue
          if common.overlaps(brows + [row], bcols + [col],
                             [3] * (len(brows) + 1),
                             [3] * (len(brows) + 1), spacing=1):
            continue
          candidates.append((row, col))
      if not candidates:
        break
      brow, bcol = candidates[common.randint(0, len(candidates) - 1)]
      brows.append(brow)
      bcols.append(bcol)
    num_sprites = len(brows)
    rows, cols, idxs = [], [], []
    creatures = []
    for idx in range(num_sprites):
      while True:
        cells = common.randint(2, max_cells)
        pixels = sorted(common.continuous_creature(cells))
        if not idx or pixels != creatures[0]:
          break
      creatures.append(pixels)
      xrows, xcols = zip(*pixels)
      rows.extend(xrows)
      cols.extend(xcols)
      idxs.extend([idx] * len(pixels))
    bcolor = common.random_color(exclude=[common.gray()])
    palette = common.random_colors(num_colors, exclude=[bcolor, common.gray()])
    colors = [palette[common.randint(0, len(palette) - 1)]
              for _ in range(num_sprites)]

  grid, output = common.grids(width, height)
  for i in range(4):
    output[i][3] = output[3][i] = grid[i][3] = grid[3][i] = common.gray()
  for row, col, idx in zip(rows, cols, idxs):
    r, c = brows[idx] + row, bcols[idx] + col
    grid[r][c] = colors[idx]
    if not idx:
      output[r][c] = colors[idx]
      output[row][col] = grid[row][col] = bcolor
  for row, col, idx in zip(rows, cols, idxs):
    if idx:
      continue
    r, c = brows[idx] + row, bcols[idx] + col
    output[r][c] = common.gray()
  for row, col, idx in zip(rows, cols, idxs):
    if not idx:
      continue
    r, c = brows[idx] + row, bcols[idx] + col
    output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 1, 1, 1, 1],
               cols=[0, 1, 1, 2, 2, 1, 0, 1, 2, 1, 0, 1, 2, 2, 1, 0, 1, 2, 3],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
               brows=[5, 0, 6, 8], bcols=[5, 6, 0, 3], colors=[6, 7, 7, 8],
               bcolor=1),
      generate(rows=[0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
               cols=[1, 0, 1, 0, 1, 0, 0, 1, 2, 0, 1, 0, 1],
               idxs=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3],
               brows=[7, 2, 5, 8], bcols=[7, 6, 2, 0], colors=[9, 4, 7, 8],
               bcolor=3),
      generate(rows=[0, 1, 1, 1, 0, 1, 1, 2, 0, 0, 0, 1],
               cols=[1, 0, 1, 2, 0, 0, 1, 0, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[0, 4, 7], bcols=[6, 6, 1], colors=[1, 3, 6], bcolor=4),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 0, 1, 1, 2, 0, 1, 2, 2, 0, 0, 0, 1, 0, 1, 2],
               cols=[0, 1, 2, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4],
               brows=[7, 0, 3, 6, 6], bcols=[4, 7, 5, 0, 8],
               colors=[7, 6, 3, 8, 4], bcolor=2),
  ]
  return {"train": train, "test": test}
