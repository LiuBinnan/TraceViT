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


def generate(row=None, col=None, dirs=None, color=None, size=9,
             height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the square should be placed
    col: a horizontal coordinate where the square should be placed
    dirs: a list of integers representing which directions to sprout
    color: the integer used to color the square & sprouts
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: the number of 2x2 squares to place
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if row is None:
    if count is None:
      count = common.randint(1, max(1, (height * width) // 24))
    color = common.random_color(exclude=[common.red()])
  else:
    count = 1

  def is_valid(r, c):
    return r >= 0 and r < height and c >= 0 and c < width

  grid = common.grid(width, height)
  deltas = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
  available = set(common.all_pixels(width, height))
  objects = []

  def object_cells(obj_row, obj_col):
    return {
        (obj_row, obj_col),
        (obj_row, obj_col + 1),
        (obj_row + 1, obj_col),
        (obj_row + 1, obj_col + 1),
    }

  def neighbors(cells):
    result = set()
    for r, c in cells:
      result.update([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
    return result

  def corner(obj_row, obj_col, delta_idx):
    dr, dc = deltas[delta_idx]
    return obj_row + (dr + 1) // 2, obj_col + (dc + 1) // 2

  if row is not None:
    objects.append((row, col, dirs))
  else:
    for _ in range(count):
      candidates = []
      for obj_row in range(height - 1):
        for obj_col in range(width - 1):
          cells = object_cells(obj_row, obj_col)
          if cells.issubset(available):
            candidates.append((obj_row, obj_col))
      if not candidates:
        break
      obj_row, obj_col = common.choice(candidates)
      num_dirs = common.randint(1, 3)
      obj_dirs = common.sample(range(4), num_dirs)
      objects.append((obj_row, obj_col, obj_dirs))
      cells = object_cells(obj_row, obj_col)
      available -= cells
      available -= neighbors(cells)

  for obj_row, obj_col, obj_dirs in objects:
    for delta_idx in range(len(deltas)):
      r, c = corner(obj_row, obj_col, delta_idx)
      grid[r][c] = common.red() if delta_idx in obj_dirs else color
  output = [row[:] for row in grid]
  active_dirs = []
  for obj_row, obj_col, obj_dirs in objects:
    for delta_idx in range(len(deltas)):
      if delta_idx in obj_dirs:
        active_dirs.append((obj_row, obj_col, delta_idx))

  def draw_active(active_idx):
    if active_idx >= len(active_dirs):
      return
    obj_row, obj_col, delta_idx = active_dirs[active_idx]
    dr, dc = deltas[delta_idx]
    r, c = corner(obj_row, obj_col, delta_idx)
    drew = True
    while drew:
      drew = False
      if is_valid(r, c): output[r][c], drew = color, True
      if is_valid(r + dr, c): output[r + dr][c], drew = color, True
      if is_valid(r, c + dc): output[r][c + dc], drew = color, True
      r, c = r + dr, c + dc

  draw_active(0)
  draw_active(1)
  for active_idx in range(2, len(active_dirs)):
    draw_active(active_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=4, col=2, dirs=[1], color=4),
      generate(row=1, col=2, dirs=[2], color=3),
      generate(row=3, col=3, dirs=[1, 3], color=6),
      generate(row=3, col=3, dirs=[0, 1, 3], color=7),
  ]
  test = [
      generate(row=2, col=5, dirs=[0, 1, 2], color=8),
  ]
  return {"train": train, "test": test}
