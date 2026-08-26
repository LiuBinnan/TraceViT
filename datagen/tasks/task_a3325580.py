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
             colors=None, size=10, height=None, width=None, num_objs=None,
             num_max=None, max_count=None, bg_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size for examples)
    width: the number of columns of the grid (defaults to size for examples)
    num_objs: the total number of colored objects
    num_max: the number of maximum-size objects
    max_count: the number of cells in each maximum-size object
    bg_color: the background color
  """
  if rows is None:
    if height is None:
      height = common.randint(10, 30)
    if width is None:
      width = common.randint(10, 30)
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  if rows is None:
    if num_objs is None:
      num_objs = common.randint(1, 9)
    num_objs = min(9, max(1, num_objs))
    if num_max is None:
      num_max = common.randint(1, num_objs)
    num_max = min(num_objs, max(1, num_max))
    if max_count is None:
      max_count = common.randint(1, 30)
    max_count = min(30, max(1, max_count))
    if max_count == 1:
      num_objs = num_max

    def sample_pixels(count):
      max_wide = min(6, width)
      max_tall = min(6, height)
      count = min(count, max_wide * max_tall)
      for _ in range(100):
        wide = common.randint(1, max_wide)
        tall = common.randint(1, max_tall)
        if wide * tall >= count:
          return common.continuous_creature(count, wide, tall)
      wide = max_wide
      tall = min(max_tall, max(1, (count + wide - 1) // wide))
      return common.continuous_creature(count, wide, tall)

    def place(pixels, blocked, forbidden_lefts=None):
      tall = max([p[0] for p in pixels]) + 1
      wide = max([p[1] for p in pixels]) + 1
      candidates = [
          (r, c)
          for r in range(height - tall + 1)
          for c in range(width - wide + 1)
      ]
      for brow, bcol in common.shuffle(candidates):
        if forbidden_lefts is not None and bcol in forbidden_lefts:
          continue
        placed = set((brow + row, bcol + col) for row, col in pixels)
        if placed & blocked:
          continue
        halo = set(placed)
        for row, col in placed:
          for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
              halo.add((nr, nc))
        return brow, bcol, halo
      return None

    fallback_bands = [
        (num_objs, max_count),
        (min(num_objs, 6), max_count),
        (min(num_objs, 4), max_count),
        (min(num_objs, 3), min(max_count, 20)),
        (min(num_objs, 2), max_count),
        (1, max_count),
    ]
    success = False
    for total_objs, top_count in fallback_bands:
      total_max = min(num_max, total_objs)
      counts = [top_count] * total_max
      if max_count > 1:
        counts.extend([
            common.randint(1, top_count - 1)
            for _ in range(total_objs - total_max)
        ])
      for _ in range(20):
        rows, cols, idxs, brows, bcols = [], [], [], [], []
        blocked = set()
        used_max_lefts = set()
        success = True
        for idx, count in enumerate(counts):
          pixels = sample_pixels(count)
          placed = place(
              pixels, blocked, used_max_lefts if idx < total_max else None)
          if placed is None:
            success = False
            break
          brow, bcol, halo = placed
          brows.append(brow)
          bcols.append(bcol)
          rows.extend([p[0] for p in pixels])
          cols.extend([p[1] for p in pixels])
          idxs.extend([idx] * len(pixels))
          blocked.update(halo)
          if idx < total_max:
            used_max_lefts.add(bcol)
        if success:
          break
      if success:
        break
    if bg_color is None:
      bg_color = common.choice(list(range(10)))
    colors = common.sample([c for c in range(10) if c != bg_color], len(brows))

  idxs_to_counts = {x: idxs.count(x) for x in idxs}
  count = max(idxs_to_counts.values())
  max_idxs = [(c, i) for i, c in enumerate(bcols) if idxs_to_counts[i] == count]
  max_idxs.sort()  # We need them ordered by column value.
  grid = common.grid(width, height, bg_color if bg_color is not None else 0)
  output = common.grid(len(max_idxs), count)
  for row, col, idx in zip(rows, cols, idxs):
    grid[brows[idx] + row][bcols[idx] + col] = colors[idx]
  for c in range(len(max_idxs)):
    idx = max_idxs[c][1]
    for r in range(count):
      output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 0, 1, 2, 2, 3, 0, 0, 1, 2, 2, 0, 0, 0, 1, 2],
               cols=[1, 2, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 2, 2, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
               brows=[7, 2, 3, 1], bcols=[0, 2, 5, 7], colors=[3, 4, 6, 8]),
      generate(rows=[0, 1, 1, 2, 2, 3, 4, 4, 5, 0, 1, 2, 2, 2, 3, 0, 0, 0, 1, 1,
                     2, 3, 3, 4],
               cols=[1, 1, 2, 0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 2, 0, 1, 2, 0, 2,
                     2, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               brows=[3, 3, 0], bcols=[0, 4, 7], colors=[9, 6, 4]),
      generate(rows=[0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 2, 0, 1, 2, 3],
               cols=[0, 1, 2, 2, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0],
               idxs=[0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3],
               brows=[1, 5, 1, 0], bcols=[0, 3, 5, 9], colors=[7, 3, 2, 1]),
      generate(rows=[0, 1, 2, 0, 0, 0, 1], cols=[0, 0, 0, 0, 1, 0, 0],
               idxs=[0, 0, 0, 1, 1, 2, 2], brows=[3, 8, 4], bcols=[2, 4, 6],
               colors=[8, 4, 6]),
      generate(rows=[0, 1, 1, 0, 0, 1], cols=[0, 0, 1, 0, 1, 1],
               idxs=[0, 0, 0, 1, 1, 1], brows=[4, 2], bcols=[1, 5],
               colors=[2, 3]),
      generate(rows=[0, 1, 2, 0, 0, 1, 0, 0, 0],
               cols=[0, 0, 0, 0, 1, 0, 0, 1, 2],
               idxs=[0, 0, 0, 1, 1, 1, 2, 2, 2], brows=[2, 5, 3],
               bcols=[1, 3, 7], colors=[1, 4, 8]),
  ]
  test = [
      generate(rows=[0, 1, 2, 0, 1, 1, 2, 0, 0, 1, 2, 0, 0, 0, 1, 1, 1],
               cols=[0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2],
               idxs=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4],
               brows=[6, 1, 7, 5, 0],
               bcols=[0, 1, 3, 5, 7],
               colors=[8, 5, 2, 9, 1]),
  ]
  return {"train": train, "test": test}
