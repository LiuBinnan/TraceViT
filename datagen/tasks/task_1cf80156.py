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


def generate(height=None, rows=None, cols=None, color=None, width=12,
             grid_width=None, shape_height=None, shape_width=None,
             num_pixels=None, hole_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the grid
    grid_width: the width of the grid for random generations
    shape_height: the height of the sampled shape bounds
    shape_width: the width of the sampled shape bounds
    num_pixels: the number of pixels in the sampled shape
    hole_count: the number of isolated interior holes in dense sampled shapes
  """
  if height is None:
    dense_shape = hole_count is not None or (
        num_pixels is None and common.randint(0, 3) == 0)
    if dense_shape:
      height = common.randint(6, 20)
      width = common.randint(6, 20) if grid_width is None else grid_width
    else:
      height = common.randint(3, 30)
      width = common.randint(3, 30) if grid_width is None else grid_width
    max_shape_height = max(1, min(15, height - 1))
    max_shape_width = max(1, min(15, width - 1))
    if dense_shape and shape_height is None:
      shape_height = max_shape_height
    elif shape_height is None:
      shape_height = common.randint(1, max_shape_height)
    else:
      shape_height = max(1, min(shape_height, max_shape_height))
    if dense_shape and shape_width is None:
      shape_width = max_shape_width
    elif shape_width is None:
      shape_width = common.randint(1, max_shape_width)
    else:
      shape_width = max(1, min(shape_width, max_shape_width))
    area = shape_height * shape_width
    if dense_shape and shape_height >= 3 and shape_width >= 3:
      candidates = [(r, c) for r in range(1, shape_height - 1)
                    for c in range(1, shape_width - 1) if (r + c) % 2 == 0]
      max_holes = min(7, len(candidates))
      if hole_count is None:
        hole_count = common.randint(0, max_holes)
      else:
        hole_count = max(0, min(hole_count, max_holes))
      holes = []
      for _ in range(hole_count):
        idx = common.randint(0, len(candidates) - 1)
        holes.append(candidates.pop(idx))
      pixels = [(r, c) for r in range(shape_height)
                for c in range(shape_width) if (r, c) not in holes]
    else:
      if num_pixels is None:
        mid = area // 2
        dev = common.randint(0, mid)
        num_pixels = common.choice((dev + 1, area - dev))
      num_pixels = max(1, min(num_pixels, area))
      corners = ((0, 0), (0, shape_width - 1), (shape_height - 1, 0),
                 (shape_height - 1, shape_width - 1))
      pixels = [common.choice(corners)]
      frontier = []
      while len(pixels) < num_pixels:
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          r, c = pixels[-1][0] + dr, pixels[-1][1] + dc
          if r < 0 or r >= shape_height or c < 0 or c >= shape_width: continue
          if (r, c) in pixels or (r, c) in frontier: continue
          frontier.append((r, c))
        if not frontier: break
        idx = common.randint(0, len(frontier) - 1)
        pixels.append(frontier.pop(idx))
    min_shape_row = min(r for r, _ in pixels)
    min_shape_col = min(c for _, c in pixels)
    pixels = [(r - min_shape_row, c - min_shape_col) for r, c in pixels]
    placement_height = max(r for r, _ in pixels) + 1
    placement_width = max(c for _, c in pixels) + 1
    row = common.randint(0, height - placement_height)
    col = common.randint(0, width - placement_width)
    rows, cols = zip(*[(r + row, c + col) for r, c in pixels])
    color = common.random_color()

  min_row, max_row = min(rows), max(rows)
  min_col, max_col = min(cols), max(cols)
  grid = common.grid(width, height)
  output = common.grid(max_col - min_col + 1, max_row - min_row + 1)
  for r, c in zip(rows, cols):
    output[r - min_row][c - min_col] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=10, rows=[2, 2, 2, 3, 4, 4, 4, 5, 5],
               cols=[4, 5, 6, 5, 3, 4, 5, 3, 5], color=2),
      generate(height=11, rows=[1, 2, 2, 3, 4, 4, 4, 5],
               cols=[2, 2, 3, 3, 2, 3, 4, 4], color=1),
      generate(height=12, rows=[3, 3, 4, 4, 4, 4, 5, 5],
               cols=[4, 6, 3, 4, 5, 6, 6, 7], color=8),
  ]
  test = [
      generate(height=12, rows=[4, 4, 4, 4, 5, 6, 6, 7, 7, 7, 7],
               cols=[4, 5, 6, 7, 4, 2, 4, 2, 3, 4, 5], color=6),
  ]
  return {"train": train, "test": test}
