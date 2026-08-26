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


def generate(colors=None, cols=None, gravity=None, size=12, height=None, width=None,
             count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a pair of digits representing two different colors
    cols: a list of horizontal coordinates where centers should be placed
    gravity: which side of the grid is the "bottom" (0: top, 1: left, ...)
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size, keeping the grid square)
    width: the number of columns (defaults to size, keeping the grid square)
    count: number of plus/cross objects to place
    num_colors: number of foreground colors to sample when colors is omitted
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if gravity is None:
    gravity = common.randint(0, 3)
  if colors is None:
    if num_colors is None:
      num_colors = common.randint(2, 7)
    num_colors = max(2, min(num_colors, 9))
    colors = common.random_colors(num_colors)

  max_count = max(1, (height // 5) * (width // 5))
  if cols is not None:
    positions = [(2 + 6 * idx, col) for idx, col in enumerate(cols)]
  else:
    if count is None:
      count = common.randint(1, max_count)
    count = max(1, min(count, max_count))
    candidates = [(r, c) for r in range(2, height - 2, 5)
                  for c in range(2, width - 2, 5)]
    positions = common.shuffle(candidates)[:count]

  raw_grid = common.grid(width, height)
  pairs = []
  for idx, (r, c) in enumerate(positions):
    color_a = colors[(2 * idx) % len(colors)]
    color_b = colors[(2 * idx + 1) % len(colors)]
    pairs.append((color_a, color_b))
    raw_grid[r][c] = color_a
    for [dr, dc] in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      raw_grid[r + dr][c + dc] = color_b
  raw_output = [row[:] for row in raw_grid]
  output = common.apply_gravity([row[:] for row in raw_output], gravity)

  for (r, c), (_, color_b) in zip(positions, pairs):
    for [dr, dc] in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      raw_output[r + 2 * dr][c + 2 * dc] = color_b
  output = common.apply_gravity([row[:] for row in raw_output], gravity)

  for (r, c), (color_a, _) in zip(positions, pairs):
    for [dr, dc] in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
      raw_output[r + dr][c + dc] = raw_output[r + 2 * dr][c + 2 * dc] = color_a
  output = common.apply_gravity([row[:] for row in raw_output], gravity)
  grid = common.apply_gravity(raw_grid, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 7], cols=[3, 7], gravity=1),
      generate(colors=[6, 8], cols=[8, 3], gravity=2),
  ]
  test = [
      generate(colors=[4, 3], cols=[7, 2], gravity=1),
  ]
  return {"train": train, "test": test}
