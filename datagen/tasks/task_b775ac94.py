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


def generate(size=None, rows=None, cols=None, idxs=None, brows=None, bcols=None,
             colors=None, shows=None, height=None, width=None,
             num_sprites=None, sprite_size=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates of the sprites
    bcols: a list of horizontal coordinates of the sprites
    colors: a list of digits representing the colors to be used
    shows: a list of angles that should be shown
  """

  def draw(grid, output):
    legal = True
    idx_grid = common.grid(width, height)
    for row, col, idx in zip(rows, cols, idxs):
      for angle in range(4):
        r, c, color = brows[idx], bcols[idx], colors[idx * 4 + angle]
        if not color: continue
        if angle == 0: r, c = r - row, c - col
        if angle == 1: r, c = r - row, c + col + 1
        if angle == 2: r, c = r + row + 1, c - col
        if angle == 3: r, c = r + row + 1, c + col + 1
        if output[r][c]: legal = False
        output[r][c] = color
        if shows[idx] == angle or (row == 0 and col == 0): grid[r][c] = color
        # Check that we're not adjacent to another sprite.
        idx_grid[r][c] = idx + 1
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(idx_grid, r + dr, c + dc) in [-1, 0, idx + 1]:
              continue
            legal = False
    return legal

  if size is None:
    if height is None: height = common.randint(12, 30)
    if width is None: width = common.randint(12, 30)
    if num_sprites is None:
      num_sprites = common.randint(1, max(1, (height * width) // 25))
    if num_colors is None:
      num_colors = common.randint(4, 9)
    palette = common.random_colors(num_colors)
    while True:
      # Allow diagonal connections in the creatures.
      rows, cols, idxs = [], [], []
      brows, bcols, colors, shows = [], [], [], []
      occupied = set()
      tries, max_tries = 0, max(100, 100 * num_sprites)
      while len(brows) < num_sprites and tries < max_tries:
        tries += 1
        idx = len(brows)
        size_i = sprite_size
        if size_i is None:
          size_i = common.randint(2, 12)
        pixels = common.continuous_creature(size_i, 5, 5)
        max_row = max(p[0] for p in pixels)
        max_col = max(p[1] for p in pixels)
        if height <= 2 * max_row + 1 or width <= 2 * max_col + 1:
          continue
        brow = common.randint(max_row, height - max_row - 2)
        bcol = common.randint(max_col, width - max_col - 2)
        sprite_colors = common.sample(palette, 4)
        show = common.randint(0, 3)
        angle = common.randint(0, 3)
        if not common.randint(0, 1) and show != angle:
          sprite_colors[angle] = 0
        cells = set()
        legal = True
        for row, col in pixels:
          for angle, color in enumerate(sprite_colors):
            if not color:
              continue
            r, c = brow, bcol
            if angle == 0: r, c = r - row, c - col
            if angle == 1: r, c = r - row, c + col + 1
            if angle == 2: r, c = r + row + 1, c - col
            if angle == 3: r, c = r + row + 1, c + col + 1
            if (r, c) in cells:
              legal = False
            cells.add((r, c))
        for r, c in cells:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if (r + dr, c + dc) in occupied:
                legal = False
        if legal:
          rows.extend([p[0] for p in pixels])
          cols.extend([p[1] for p in pixels])
          idxs.extend([idx] * len(pixels))
          brows.append(brow)
          bcols.append(bcol)
          colors.extend(sprite_colors)
          shows.append(show)
          occupied.update(cells)
      if brows:
        break
  else:
    if height is None: height = size
    if width is None: width = size

  grid = common.grid(width, height)
  all_pixels = []
  for row, col, idx in zip(rows, cols, idxs):
    for angle in range(4):
      r, c, color = brows[idx], bcols[idx], colors[idx * 4 + angle]
      if not color:
        continue
      if angle == 0:
        r, c = r - row, c - col
      if angle == 1:
        r, c = r - row, c + col + 1
      if angle == 2:
        r, c = r + row + 1, c - col
      if angle == 3:
        r, c = r + row + 1, c + col + 1
      all_pixels.append((idx, r, c, color))
      if shows[idx] == angle or (row == 0 and col == 0):
        grid[r][c] = color
  output = [row[:] for row in grid]

  def reveal_sprite(sprite_idx):
    for idx, r, c, color in all_pixels:
      if idx == sprite_idx:
        output[r][c] = color

  reveal_sprite(0)
  reveal_sprite(1)
  reveal_sprite(2)
  for sprite_idx in range(3, len(brows)):
    reveal_sprite(sprite_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=30,
               rows=[0, 0, 0, 1, 1, 1, 2, 3, 0, 0, 1, 2, 2, 0, 1, 1, 2],
               cols=[0, 1, 2, 0, 2, 3, 0, 1, 0, 1, 1, 0, 2, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[11, 9, 21], bcols=[6, 16, 13],
               colors=[3, 4, 1, 2, 2, 1, 7, 4, 8, 0, 2, 3],
               shows=[2, 2, 3]),
      generate(size=20,
               rows=[0, 0, 1, 1, 1, 1, 1, 2, 2],
               cols=[0, 1, 0, 1, 2, 3, 4, 1, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0],
               brows=[8], bcols=[7],
               colors=[2, 8, 4, 3],
               shows=[0]),
      generate(size=14,
               rows=[0, 1, 1, 1, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 0, 1, 2, 3, 1, 0, 1, 2, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               brows=[7, 3], bcols=[4, 9],
               colors=[0, 1, 2, 4, 8, 4, 0, 6],
               shows=[2, 0]),
  ]
  test = [
      generate(size=24,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 0, 0, 0, 1, 0, 1, 1, 1, 2],
               cols=[0, 1, 0, 2, 1, 2, 3, 2, 0, 1, 2, 1, 0, 0, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               brows=[6, 6, 16], bcols=[7, 17, 13],
               colors=[8, 2, 4, 3, 3, 2, 1, 8, 1, 0, 2, 4],
               shows=[0, 2, 2]),
  ]
  return {"train": train, "test": test}
