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
             height=None, width=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    count: how many gray sprites to place (defaults to a randomized value; the
      original task used 4-6, this generator scales the upper bound with the
      grid's smaller dimension so larger grids carry more sprites to fill)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    # Scale the sprite ceiling with the grid's smaller dimension; empirically
    # ~0.7 * min(height, width) sprites pack quickly with a 1-cell margin
    # across the supported 5..30 size range. Default 10x10 -> up to 7 (the
    # original capped at 6). `count`, when given, requests that many sprites.
    floor = 4
    ceiling = max(floor, int(0.7 * min(height, width)))
    num_sprites = count if count is not None else common.randint(floor, ceiling)
    # First, choose sprite dimensions & positions. If a target count cannot be
    # packed quickly, back it off by one rather than spinning forever (this
    # also keeps tiny grids, where even the original could stall, terminating).
    attempts = 0
    while True:
      wides = [common.randint(2, 3) for _ in range(num_sprites)]
      talls = [common.randint(1, 2) for _ in range(num_sprites)]
      if not common.randint(0, 3): wides[0], talls[0] = 1, 4  # Rare tetris "I".
      for i in range(num_sprites):  # Flip the orientation of a few.
        if common.randint(0, 1): wides[i], talls[i] = talls[i], wides[i]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
      attempts += 1
      if attempts >= 400 and num_sprites > floor:
        num_sprites, attempts = num_sprites - 1, 0
    # Second, choose sprite contents, removing cells from their bounding boxes.
    rows, cols, idxs = [], [], []
    for i in range(num_sprites):
      wide, tall, exclude = wides[i], talls[i], []
      if wide == 2 and tall == 2 and common.randint(0, 1):
        exclude.append(common.choice([(0, 0), (0, 1), (1, 0), (1, 1)]))
      if wide == 2 and tall == 3:
        exclude.extend(common.sample([(0, 0), (0, 1), (2, 0), (2, 1)], 2))
      if wide == 3 and tall == 2:
        exclude.extend(common.sample([(0, 0), (0, 2), (1, 0), (1, 2)], 2))
      for r in range(tall):
        for c in range(wide):
          if (r, c) in exclude: continue
          rows.append(r)
          cols.append(c)
          idxs.append(i)

  grid, output = common.grids(width, height)
  for row, col, idx in zip(rows, cols, idxs):
    count = len([i for i in idxs if i == idx])
    grid[brows[idx] + row][bcols[idx] + col] = common.gray()

  counts = {idx: len([i for i in idxs if i == idx]) for idx in set(idxs)}
  active_colors = sorted(set(5 - count for count in counts.values()))

  def color_group(color_idx):
    if color_idx >= len(active_colors):
      return
    target = active_colors[color_idx]
    for row, col, idx in zip(rows, cols, idxs):
      if 5 - counts[idx] == target:
        output[brows[idx] + row][bcols[idx] + col] = target

  color_group(0)
  color_group(1)
  color_group(2)
  color_group(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 1, 0, 1, 1],
               cols=[0, 1, 0, 1, 0, 1, 1, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5],
               brows=[1, 2, 5, 6, 7, 8], bcols=[7, 1, 9, 5, 1, 3]),
      generate(rows=[0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
               cols=[0, 1, 2, 0, 0, 0, 1, 0, 1, 0, 1, 2, 0, 1, 0, 1],
               idxs=[0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4],
               brows=[2, 2, 5, 7, 8], bcols=[1, 7, 3, 6, 1]),
      generate(rows=[0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 2],
               cols=[0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
               idxs=[0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3],
               brows=[1, 1, 5, 6], bcols=[2, 6, 4, 0]),
  ]
  test = [
      generate(rows=[0, 1, 2, 3, 0, 0, 1, 1, 0, 0, 1, 0, 1, 2, 0, 0, 0, 1],
               cols=[0, 0, 0, 0, 1, 2, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5],
               brows=[0, 2, 2, 6, 7, 7], bcols=[9, 1, 5, 0, 3, 7]),
  ]
  return {"train": train, "test": test}
