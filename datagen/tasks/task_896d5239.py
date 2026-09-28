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


def generate(width=None, height=None, brows=None, bcols=None, angles=None,
             lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    brows: The row indices of the sprite points.
    bcols: The column indices of the sprite points.
    angles: The angles of the sprites.
    lengths: The lengths of the sprites.
    colors: The colors of the input grid.
  """

  def draw():
    talls, wides, rows, cols = [], [], [], []
    for brow, bcol, angle, length in zip(brows, bcols, angles, lengths):
      talls.append(length if angle in [0, 2] else (2 * length - 1))
      wides.append(length if angle in [1, 3] else (2 * length - 1))
      rows.append(brow)
      cols.append(bcol)
      if angle == 0:
        rows[-1] -= length - 1
        cols[-1] -= length - 1
      if angle == 1:
        rows[-1] -= length - 1
      if angle == 2:
        cols[-1] -= length - 1
      if angle == 3:
        rows[-1] -= length - 1
        cols[-1] -= length - 1
    if common.overlaps(rows, cols, wides, talls, 2): return None, None
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    for brow, bcol, angle, length in zip(brows, bcols, angles, lengths):
      left, right = False, False
      for i in range(length):
        good = False
        for j in range(-i, i + 1):
          if angle == 0: r, c = -i, j
          elif angle == 1: r, c = j, i
          elif angle == 2: r, c = i, j
          else: r, c = j, -i
          if common.get_pixel(output, r + brow, c + bcol) == 3:
            if j < 0: left = True
            if j > 0: right = True
            good = True
          else:
            common.draw(output, r + brow, c + bcol, 8)
        if i in [0, length - 1] and not good: return None, None
      if not left or not right: return None, None
    return grid, output

  if brows is None:
    if width is None: width = common.randint(10, 26)
    if height is None: height = common.randint(10, 26)
    num_sprites = 1
    if width * height >= 150: num_sprites = 2
    if width * height >= 200: num_sprites = 3
    if width * height >= 250: num_sprites = 4
    num_sprites = min(4, num_sprites)
    for _ in range(200):
      angles = common.randints(0, 3, num_sprites)
      lengths = common.randints(3, 5, num_sprites)
      brows, bcols = [], []
      for angle, length in zip(angles, lengths):
        if angle == 0:
          brows.append(common.randint(length - 1, height - 1))
          bcols.append(common.randint(length - 1, width - length))
        elif angle == 1:
          brows.append(common.randint(length - 1, height - length))
          bcols.append(common.randint(0, width - length))
        elif angle == 2:
          brows.append(common.randint(0, height - length))
          bcols.append(common.randint(length - 1, width - length))
        else:
          brows.append(common.randint(length - 1, height - length))
          bcols.append(common.randint(length - 1, width - 1))
      grid = common.grid(width, height)
      for row in range(height):
        for col in range(width):
          grid[row][col] = common.randint(0, 1)
      for brow, bcol, angle, length in zip(brows, bcols, angles, lengths):
        for i in range(length):
          for j in [-i, i]:
            if angle == 0:
              r, c = -i, j
            elif angle == 1:
              r, c = j, i
            elif angle == 2:
              r, c = i, j
            else:
              r, c = j, -i
            if common.randint(0, 4): common.draw(grid, r + brow, c + bcol, 3)
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break
    else:
      # Pack short fans into two rows or columns, then make their partial
      # outlines constructively valid. This bounds the rejection tail while
      # preserving the same fan-completion rule.
      lengths = [3] * num_sprites
      if width >= 12:
        boxes = [(0, 0), (0, 7), (5, 0), (5, 7)]
        angles, brows, bcols = [], [], []
        for row, col in boxes[:num_sprites]:
          angle = common.choice([0, 2])
          angles.append(angle)
          brows.append(row + 2 if angle == 0 else row)
          bcols.append(col + 2)
      else:
        boxes = [(0, 0), (7, 0), (0, 5), (7, 5)]
        angles, brows, bcols = [], [], []
        for row, col in boxes[:num_sprites]:
          angle = common.choice([1, 3])
          angles.append(angle)
          brows.append(row + 2)
          bcols.append(col if angle == 1 else col + 2)
      grid = common.grid(width, height)
      for row in range(height):
        for col in range(width):
          grid[row][col] = common.randint(0, 1)
      for brow, bcol, angle, length in zip(brows, bcols, angles, lengths):
        for i in range(length):
          for j in [-i, i]:
            if angle == 0:
              r, c = -i, j
            elif angle == 1:
              r, c = j, i
            elif angle == 2:
              r, c = i, j
            else:
              r, c = j, -i
            common.draw(grid, r + brow, c + bcol, 3)
        for i in range(1, length):
          for j in [-i, i]:
            critical = i == 1 or (i == length - 1 and j < 0)
            if not critical and common.randint(0, 4) == 0:
              if angle == 0:
                r, c = -i, j
              elif angle == 1:
                r, c = j, i
              elif angle == 2:
                r, c = i, j
              else:
                r, c = j, -i
              common.draw(grid, r + brow, c + bcol, common.randint(0, 1))
      colors = common.flatten(grid)
      grid, _ = draw()

  # Input first: the random 0/1 field carrying the partial green fan outlines.
  # (draw()/validate() branch on literal color ints, so the forward fills below
  # keep the same literals: azure 8 fills the fan, green 3 outline is preserved.)
  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  output = common.deepcopy(grid)

  def fill_fan(k):
    """Fills sprite k's triangular fan with azure, keeping its green outline."""
    if k >= len(brows): return
    brow, bcol, angle, length = brows[k], bcols[k], angles[k], lengths[k]
    for i in range(length):
      for j in range(-i, i + 1):
        if angle == 0: r, c = -i, j
        elif angle == 1: r, c = j, i
        elif angle == 2: r, c = i, j
        else: r, c = j, -i
        if common.get_pixel(output, r + brow, c + bcol) != 3:
          common.draw(output, r + brow, c + bcol, 8)

  fill_fan(0)
  fill_fan(1)
  fill_fan(2)
  fill_fan(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=15, brows=[5, 12], bcols=[3, 4], angles=[1, 2],
               lengths=[4, 3],
               colors=[1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0,
                       1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1,
                       1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 1, 1,
                       1, 0, 0, 1, 0, 3, 0, 1, 1, 1, 1, 1,
                       1, 1, 1, 0, 3, 1, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 3, 1, 1, 1, 1, 0, 1, 0, 0,
                       0, 1, 0, 0, 3, 1, 0, 0, 1, 0, 0, 1,
                       1, 1, 1, 1, 1, 3, 0, 0, 1, 0, 0, 1,
                       0, 0, 1, 0, 0, 1, 3, 0, 1, 0, 1, 1,
                       1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0,
                       1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0,
                       1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0,
                       0, 1, 0, 0, 3, 1, 1, 0, 0, 0, 0, 1,
                       0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
                       0, 1, 3, 0, 0, 0, 3, 0, 0, 1, 1, 1]),
      generate(width=12, height=13, brows=[2, 8], bcols=[4, 5], angles=[2, 2],
               lengths=[3, 4],
               colors=[0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1,
                       1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1,
                       1, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 1, 3, 1, 3, 0, 0, 0, 0, 0, 0,
                       1, 0, 3, 1, 1, 1, 3, 0, 1, 0, 1, 0,
                       1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0,
                       1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
                       0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 3, 0, 3, 0, 1, 0, 1, 0,
                       0, 0, 0, 3, 1, 0, 1, 1, 0, 0, 1, 0,
                       1, 0, 3, 1, 0, 1, 0, 0, 1, 0, 0, 1,
                       0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1]),
      generate(width=16, height=15, brows=[2, 10, 11], bcols=[5, 14, 5],
               angles=[2, 0, 1], lengths=[3, 3, 4],
               colors=[1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 0, 0, 3, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0,
                       0, 0, 0, 0, 3, 1, 3, 0, 1, 1, 0, 0, 1, 1, 1, 0,
                       0, 1, 0, 3, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1,
                       0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1,
                       1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 1, 1, 3, 0, 0, 0, 3, 1, 1, 0,
                       0, 1, 0, 1, 1, 0, 1, 3, 1, 1, 1, 0, 0, 3, 1, 3,
                       1, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0,
                       0, 0, 1, 0, 1, 3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                       1, 1, 0, 1, 1, 1, 3, 0, 0, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
                       0, 1, 1, 1, 0, 0, 1, 1, 3, 1, 0, 1, 0, 1, 1, 1]),
  ]
  test = [
      generate(width=18, height=15, brows=[1, 5, 11, 12], bcols=[3, 15, 3, 6],
               angles=[2, 0, 3, 1], lengths=[3, 3, 3, 4],
               colors=[0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                       1, 0, 1, 3, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0,
                       0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0,
                       0, 3, 0, 1, 0, 3, 1, 0, 1, 1, 0, 1, 0, 3, 1, 0, 0, 3,
                       0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 3, 0, 3, 0,
                       0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 3, 1, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0,
                       1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0,
                       1, 3, 0, 0, 1, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 3, 0, 0, 0, 1, 1, 3, 0, 1, 1, 0, 1, 0, 0, 1, 0,
                       0, 0, 0, 3, 0, 1, 1, 3, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0,
                       0, 0, 3, 1, 1, 0, 3, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0,
                       0, 1, 1, 0, 0, 1, 1, 3, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0,
                       1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1]),
  ]
  return {"train": train, "test": test}
