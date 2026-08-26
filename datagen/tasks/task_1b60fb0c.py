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


def generate(rows=None, cols=None, offset=None, size=10, height=None,
             width=None, count=None, block_size=None, shift=None,
             missing=None, variant=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: whether to offet some copies by a single pixel
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  random_branch = rows is None
  if random_branch:
    if variant is None:
      variant = common.randint(0, 7)
    if variant == 0:
      inobj, rempart = set(), set()
      for _ in range(100):
        pixels = common.continuous_creature(common.randint(6, 12), 4, 4)
        offset = common.randint(0, 1)
        red_part = set()
        blue_part = set()
        for r, c in pixels:
          red_part.add((4 + r, 4 - c + offset))
          blue_part.add((5 - r + offset, 5 + c))
          blue_part.add((4 - c + offset, 5 - r + offset))
          blue_part.add((5 + c, 4 + r))
        if not red_part - blue_part:
          inobj = blue_part
          break
      if not inobj:
        pixels = [(0, 0), (1, 0), (2, 0), (0, 1),
                  (1, 1), (2, 1), (0, 2), (3, 1)]
        offset = 1
        for r, c in pixels:
          inobj.add((5 - r + offset, 5 + c))
          inobj.add((4 - c + offset, 5 - r + offset))
          inobj.add((5 + c, 4 + r))
    else:
      max_block = min(height, width) // 2
      if block_size is None:
        block_size = common.randint(2, max_block)
      block_size = min(max(2, block_size), max_block)
      max_count = block_size * block_size - 1
      if count is None:
        count_low = common.randint(0, block_size * block_size // 2)
        count = [count_low, block_size * block_size - count_low][
            common.randint(0, 1)]
      count_cap = max(1, block_size * block_size // 2)
      count = min(max(1, count), count_cap, max_count)
      cells = [(r, c) for r in range(block_size) for c in range(block_size)]
      rows, cols = [], []
      for _ in range(count):
        idx = common.randint(0, len(cells) - 1)
        r, c = cells[idx]
        del cells[idx]
        rows.append(r)
        cols.append(c)
      if shift is None:
        shift = common.randint(0, block_size)
      shift = min(max(0, shift), block_size)
      if missing is None:
        missing = common.randint(0, 3)
      missing = min(max(0, missing), 3)
      loc_row = common.randint(0, height - 2 * block_size)
      loc_col = common.randint(0, width - 2 * block_size)
      parts = [set(), set(), set(), set()]
      for r, c in zip(rows, cols):
        parts[0].add((loc_row + r, loc_col + c + shift))
        parts[1].add((loc_row + c + shift,
                      loc_col + 2 * block_size - 1 - r))
        parts[2].add((loc_row + 2 * block_size - 1 - r,
                      loc_col + 2 * block_size - 1 - c - shift))
        parts[3].add((loc_row + 2 * block_size - 1 - c - shift,
                      loc_col + r))
      inobj = set()
      for idx, part in enumerate(parts):
        if idx != missing:
          inobj.update(part)
      rempart = parts[missing] - inobj

  grid, output = common.grids(width, height)
  if random_branch:
    for r, c in rempart:
      output[r][c] = common.red()
  if random_branch:
    for r, c in inobj:
      grid[r][c] = common.blue()
      output[r][c] = common.blue()
  if not random_branch:
    for r, c in zip(rows, cols):
      output[4 + r][4 - c + offset] = common.red()
  if not random_branch:
    for r, c in zip(rows, cols):
      for bitmap in [grid, output]:
        bitmap[5 - r + offset][5 + c] = common.blue()
        bitmap[4 - c + offset][5 - r + offset] = common.blue()
        bitmap[5 + c][4 + r] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2], cols=[0, 2, 3, 0, 1, 2, 3, 3],
               offset=0),
      generate(rows=[-1, -1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3],
               cols=[3, 4, 3, 4, 0, 1, 2, 3, 4, 3, 4, 3, 4], offset=1),
      generate(rows=[-1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3],
               cols=[4, 2, 4, 0, 1, 2, 3, 4, 2, 4, 4], offset=1),
  ]
  test = [
      generate(rows=[-1, 0, 0, 1, 1, 1, 1, 1, 2, 3, 0],
               cols=[3, 2, 3, 0, 1, 2, 3, 4, 3, 3, 0], offset=0),
  ]
  return {"train": train, "test": test}
