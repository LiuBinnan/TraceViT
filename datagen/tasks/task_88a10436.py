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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    colors=None,
    tworows=None,
    twocols=None,
    obj_width=None,
    obj_height=None,
    num_colors=None,
    num_markers=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    tworows: a list of vertical coordinates where the two sprites should live
    twocols: a list of horizontal coordinates where the two sprites should live
    obj_width: the width of the sprite
    obj_height: the height of the sprite
    num_colors: the number of colors used in the sprite
    num_markers: the number of gray marker locations to copy the sprite to
  """
  if width is None:
    width, height = common.randint(8, 30), common.randint(8, 30)
    if obj_height is None:
      obj_height = 2 * common.randint(0, 2) + 1
    if obj_width is None:
      obj_width = 2 * common.randint(0, 2) + 1
    if obj_height == 1 and obj_width == 1:
      obj_width = common.choice([3, 5])
    center_r, center_c = obj_height // 2, obj_width // 2
    while True:
      tries = common.randint(0, obj_width * obj_height - max(obj_width, obj_height))
      rows, cols = common.conway_sprite(obj_width, obj_height, tries)
      if (center_r, center_c) not in zip(rows, cols): continue
      if common.connected(list(zip(rows, cols))): break
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = min(num_colors, len(rows))
    color_list = common.random_colors(num_colors, exclude=[0, common.gray()])
    colors = color_list[:]
    colors += [common.choice(color_list) for _ in range(len(rows) - num_colors)]
    colors = common.shuffle(colors)
    if num_markers is None:
      num_markers = common.randint(1, max(1, width * height // (2 * len(rows))))
    max_row = height - obj_height + center_r
    max_col = width - obj_width + center_c
    centers = []
    for row in range(center_r, max_row + 1):
      for col in range(center_c, max_col + 1):
        centers.append((row, col))
    centers = common.shuffle(centers)
    occupied = set()
    tworows, twocols = [], []
    for row, col in centers:
      placed = set()
      for r, c in zip(rows, cols):
        placed.add((row + r - center_r, col + c - center_c))
      blocked = set(occupied)
      for r, c in occupied:
        blocked.update([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
      if placed & blocked: continue
      tworows.append(row)
      twocols.append(col)
      occupied.update(placed)
      if len(tworows) >= num_markers + 1: break

  grid, output = common.grids(width, height)
  center_r = (max(rows) + min(rows)) // 2
  center_c = (max(cols) + min(cols)) // 2
  for idx in range(len(tworows)):
    if idx:
      grid[tworows[idx]][twocols[idx]] = common.gray()
    for r, c, color in zip(rows, cols, colors):
      output[tworows[idx] + r - center_r][twocols[idx] + c - center_c] = color
      if idx == 0:
        grid[tworows[idx] + r - center_r][twocols[idx] + c - center_c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, rows=[0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2], colors=[2, 2, 2, 1, 1, 3],
               tworows=[1, 5], twocols=[1, 5]),
      generate(width=7, height=8, rows=[0, 1, 1, 2, 2, 2],
               cols=[0, 0, 1, 0, 1, 2], colors=[6, 1, 1, 2, 2, 2],
               tworows=[1, 5], twocols=[5, 1]),
      generate(width=8, height=10, rows=[0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 1, 2, 0, 1, 2], colors=[2, 2, 3, 1, 3, 3, 1],
               tworows=[7, 2], twocols=[2, 4]),
  ]
  test = [
      generate(width=11, height=10, rows=[0, 0, 1, 1, 2, 2],
               cols=[1, 2, 0, 1, 1, 2], colors=[2, 2, 1, 1, 3, 3],
               tworows=[3, 8], twocols=[3, 6]),
  ]
  return {"train": train, "test": test}
