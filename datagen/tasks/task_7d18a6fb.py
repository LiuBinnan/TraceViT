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


def generate(width=None, height=None, brow=None, bcol=None, srows=None,
             scols=None, colors=None, values=None, num_sprites=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brow: The row of the blue box.
    bcol: The column of the blue box.
    srows: The rows of the sprites.
    scols: The columns of the sprites.
    colors: The colors of the sprites.
    values: The values of the sprites.
    num_sprites: The number of sprites, including the four template matches.
  """

  if width is None:
    requested_sprites = num_sprites
    while True:
      width, height = common.randint(12, 24), common.randint(12, 24)
      num_sprites = (common.randint(4, 8) if requested_sprites is None
                     else requested_sprites)
      if (num_sprites >= 6 and width <= 2 * num_sprites + 2 and
          height <= 2 * num_sprites + 2):
        continue
      break
    colors = common.random_colors(num_sprites, exclude=[1])
    brow = common.randint(0, 1) * (height - 7)
    bcol = common.randint(0, 1) * (width - 7)
    attempts = 0
    while True:
      srows = [common.randint(0, height - 3) for _ in range(num_sprites)]
      scols = [common.randint(0, width - 3) for _ in range(num_sprites)]
      if not common.overlaps([brow] + srows, [bcol] + scols,
                             [7] + [3] * num_sprites,
                             [7] + [3] * num_sprites, 1): break
      attempts += 1
      if attempts < 128: continue
      if num_sprites > 4:
        num_sprites, attempts = num_sprites - 1, 0
        colors = colors[:num_sprites]
        continue
      side_col = width - 3 if bcol == 0 else 0
      side_rows = [0, 4] if brow == 0 else [height - 3, height - 7]
      far_row = height - 3 if brow == 0 else 0
      far_cols = [0, 4] if bcol == 0 else [width - 3, width - 7]
      srows = side_rows + [far_row, far_row]
      scols = [side_col, side_col] + far_cols
      break
    values = []
    for _ in range(num_sprites):
      pixels = common.diagonally_connected_sprite()
      for r in range(3):
        for c in range(3):
          values.append(1 if (r, c) in pixels else 0)
    values = "".join(str(v) for v in values)

  grid = common.grid(width, height)
  common.rect(grid, 7, 7, brow, bcol, 1)
  for r in range(2):
    for c in range(2):
      grid[brow + 1 + r * 4][bcol + 1 + c * 4] = colors[r * 2 + c]
  for i, (srow, scol, color) in enumerate(zip(srows, scols, colors)):
    for row in range(3):
      for col in range(3):
        value = int(values[i * 9 + row * 3 + col])
        if value == 0: continue
        grid[srow + row][scol + col] = color * value

  output = common.deepcopy(grid)

  def erase_distractor_sprites():
    """Erases sprites whose colors do not appear in the blue template."""
    for i in range(4, len(srows)):
      for row in range(3):
        for col in range(3):
          value = int(values[i * 9 + row * 3 + col])
          if value == 0: continue
          output[srows[i] + row][scols[i] + col] = common.black()

  erase_distractor_sprites()
  output = common.grid(7, 7)

  def place_matching_sprite(i):
    """Places the sprite matching template marker i in its output quadrant."""
    for row in range(3):
      for col in range(3):
        value = int(values[i * 9 + row * 3 + col])
        if value == 0: continue
        output[4 * (i // 2) + row][4 * (i % 2) + col] = colors[i] * value

  place_matching_sprite(0)
  place_matching_sprite(1)
  place_matching_sprite(2)
  place_matching_sprite(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=17, brow=0, bcol=10, srows=[1, 13, 8, 9, 11],
               scols=[2, 2, 2, 12, 7], colors=[2, 4, 6, 3, 8],
               values="001111011010111011101010111110101010010111010"),
      generate(width=13, height=17, brow=10, bcol=0, srows=[2, 12, 6, 0],
               scols=[2, 9, 8, 7], colors=[4, 8, 3, 2],
               values="010111010010101010101110010110101010"),
      generate(width=17, height=18, brow=0, bcol=0, srows=[15, 2, 9, 10, 7, 13],
               scols=[1, 10, 8, 2, 13, 8], colors=[5, 4, 2, 3, 6, 8],
               values="010110001001010111010101111101011001010111010010111111"),
  ]
  test = [
      generate(width=17, height=16, brow=9, bcol=0, srows=[2, 10, 2, 4, 6],
               scols=[13, 10, 7, 1, 12], colors=[2, 3, 8, 6, 4],
               values="010110001111010111011111001011110011010101010"),
  ]
  return {"train": train, "test": test}
