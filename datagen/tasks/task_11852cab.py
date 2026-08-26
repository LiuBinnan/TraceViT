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


def generate(row=None, col=None, radius=None, keep=None, colors=None, size=10,
             height=None, width=None, count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the center of the board
    col: a horizontal coordinate for the center of the board
    radius: how far from the center is the blast
    keep: which cell to keep in the blast radius
    colors: a list of four digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: the number of blast patterns to place
    num_colors: the number of foreground colors to sample from
  """
  if height is None: height = size
  if width is None: width = size
  grid, output = common.grids(width, height)
  radius_1 = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
  radius_2 = [(-2, 0), (0, 2), (2, 0), (0, -2)]
  radius_3 = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
  rings = [radius_1, radius_2, radius_3]
  placements = []
  if row is None:
    if count is None:
      count = common.randint(1, max(1, (width * height) // 36))
    if num_colors is None:
      num_colors = common.randint(1, 9)
    num_colors = max(1, min(9, num_colors))
    palette = common.random_colors(num_colors)
    occupied = set()
    tries = 0
    max_tries = 10 * count
    while len(placements) < count and tries < max_tries:
      tries += 1
      obj_row = common.randint(3, height - 4)
      obj_col = common.randint(3, width - 4)
      if any((r, c) in occupied
             for r in range(obj_row - 3, obj_row + 4)
             for c in range(obj_col - 3, obj_col + 4)):
        continue
      for r in range(obj_row - 3, obj_row + 4):
        for c in range(obj_col - 3, obj_col + 4):
          occupied.add((r, c))
      obj_colors = [common.choice(palette) for _ in range(4)]
      active_rings = sorted(common.sample([1, 2, 3], common.randint(1, 3)))
      placements.append((obj_row, obj_col, obj_colors, {}, active_rings))
    if placements:
      partial_obj = common.randint(0, len(placements) - 1)
      obj_row, obj_col, obj_colors, partials, active_rings = placements[partial_obj]
      partial = common.randint(1, 3)
      keep_count = common.choice([1, 3])
      keep_indices = common.sample(range(4), keep_count)
      assert 0 < len(keep_indices) < 4
      partials = {partial: keep_indices}
      placements[partial_obj] = (
          obj_row, obj_col, obj_colors, partials, [1, 2, 3])
  else:
    placements.append((row, col, colors, {radius: [keep]}, [1, 2, 3]))

  for obj_row, obj_col, obj_colors, partials, active_rings in placements:
    output[obj_row][obj_col] = grid[obj_row][obj_col] = obj_colors[0]
    for ring, offsets in enumerate(rings, start=1):
      if ring not in active_rings: continue
      for idx in range(len(offsets)):
        dr, dc = offsets[idx]
        if ring not in partials or idx in partials[ring]:
          grid[obj_row + dr][obj_col + dc] = obj_colors[ring]
        output[obj_row + dr][obj_col + dc] = obj_colors[ring]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4, radius=3, keep=0, colors=[3, 2, 8, 3]),
      generate(row=4, col=4, radius=3, keep=0, colors=[4, 4, 3, 2]),
      generate(row=3, col=5, radius=1, keep=0, colors=[1, 4, 8, 8]),
  ]
  test = [
      generate(row=4, col=3, radius=2, keep=0, colors=[1, 2, 4, 1]),
  ]
  return {"train": train, "test": test}
