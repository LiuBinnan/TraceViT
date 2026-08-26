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


def generate(rows=None, cols=None, idxs=None, colors=None, size=30,
             width=None, height=None, object_width=None, object_height=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of digits representing colors to be used (0th is special!)
    size: the width and height of the (square) grid
    width: the width of the generated input grid
    height: the height of the generated input grid
    object_width: width of the sampled connected object's bounding box
    object_height: height of the sampled connected object's bounding box
    num_colors: total non-background colors, including the object color
    density: number of distractor cells before clipping to feasible cells
  """
  if rows is None:
    # First, create the pixels for our little celestial object (color idx is 0).
    rows, cols, idxs = [], [], []
    if width is None:
      width = common.randint(10, 30)
    if height is None:
      height = common.randint(10, 30)
    if object_width is None:
      object_width = common.randint(3, min(8, width // 2))
    object_width = max(1, min(object_width, width))
    if object_height is None:
      object_height = common.randint(3, min(8, height // 2))
    object_height = max(1, min(object_height, height))
    num_cells = common.randint(max(object_width, object_height),
                               object_width * object_height)
    seed = (common.randint(0, object_height - 1),
            common.randint(0, object_width - 1))
    pixels, frontier = [seed], []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      nr, nc = seed[0] + dr, seed[1] + dc
      if 0 <= nr < object_height and 0 <= nc < object_width:
        frontier.append((nr, nc))
    while len(pixels) < num_cells and frontier:
      pixel = frontier.pop(common.randint(0, len(frontier) - 1))
      if pixel in pixels: continue
      pixels.append(pixel)
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = pixel[0] + dr, pixel[1] + dc
        if nr < 0 or nr >= object_height or nc < 0 or nc >= object_width:
          continue
        if (nr, nc) in pixels or (nr, nc) in frontier: continue
        frontier.append((nr, nc))
    min_obj_row = min(r for r, _ in pixels)
    min_obj_col = min(c for _, c in pixels)
    pixels = [(r - min_obj_row, c - min_obj_col) for r, c in pixels]
    object_height = max(r for r, _ in pixels) + 1
    object_width = max(c for _, c in pixels) + 1
    row = common.randint(0, height - object_height)
    col = common.randint(0, width - object_width)
    for r, c in pixels:
      rows.append(row + r)
      cols.append(col + c)
      idxs.append(0)
    if num_colors is None:
      num_colors = common.randint(2, 9)
    num_colors = max(1, min(num_colors, 9))
    colors = common.random_colors(num_colors)
    # Then, create all the other pixels in the background (but don't clobber!).
    blocked = set()
    for r in range(row, row + object_height):
      for c in range(col, col + object_width):
        blocked.add((r, c))
    available = [(r, c) for r in range(height) for c in range(width)
                 if (r, c) not in blocked]
    max_noise = max(0, min(len(available), len(available) // 4))
    if density is None:
      density = common.randint(0, max_noise)
    num_noise = max(0, min(density, max_noise))
    if len(colors) == 1:
      num_noise = 0
    if len(colors) > 1 and num_noise > 0:
      num_noise = max(num_noise, min(len(colors) - 1, max_noise))
    for idx, (r, c) in enumerate(common.sample(available, num_noise)):
      rows.append(r)
      cols.append(c)
      if idx < len(colors) - 1:
        idxs.append(idx + 1)
      else:
        idxs.append(common.randint(1, len(colors) - 1))

  min_col = min(col for col, idx in zip(cols, idxs) if idx == 0)
  max_col = max(col for col, idx in zip(cols, idxs) if idx == 0)
  min_row = min(row for row, idx in zip(rows, idxs) if idx == 0)
  max_row = max(row for row, idx in zip(rows, idxs) if idx == 0)
  if width is None:
    width = size
  if height is None:
    height = size
  grid, _ = common.grids(width, height)
  output = common.grid(max_col - min_col + 1, max_row - min_row + 1)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = colors[idx]
    if r < min_row or r > max_row or c < min_col or c > max_col: continue
    output[r - min_row][c - min_col] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6,
                     7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 11, 11,
                     11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13,
                     13, 14, 14, 14, 14, 14, 15, 15, 16, 16, 16, 16, 17, 17, 18,
                     18, 18, 19, 19, 19, 19, 19, 19, 20, 20, 20, 21, 22, 22, 23,
                     23, 23, 23, 23, 24, 24, 25, 25, 26, 26, 26, 26, 27, 27, 27,
                     28, 28, 28, 28, 29, 29],
               cols=[0, 5, 22, 15, 10, 26, 8, 15, 22, 3, 4, 8, 12, 13, 15, 19,
                     18, 29, 4, 7, 4, 24, 2, 4, 11, 15, 17, 18, 19, 21, 27, 0,
                     9, 17, 18, 21, 0, 2, 5, 13, 14, 17, 18, 19, 25, 28, 17, 19,
                     22, 15, 17, 18, 19, 27, 3, 7, 11, 18, 19, 0, 28, 8, 12, 22,
                     29, 19, 21, 1, 7, 25, 4, 13, 15, 20, 22, 29, 1, 16, 23, 4,
                     23, 24, 0, 12, 21, 24, 29, 7, 15, 20, 22, 13, 24, 26, 29,
                     7, 8, 25, 13, 17, 21, 25, 6, 10],
               idxs=[1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1,
                     2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 0, 0, 1, 2, 2, 1, 1,
                     1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2,
                     1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1,
                     1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2,
                     2, 2, 2, 1],
               colors=[3, 1, 5]),
      generate(rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9,
                     9, 10, 10, 10, 10, 11, 11, 11, 12, 12, 13, 14, 17, 17, 18,
                     19, 19, 20, 20, 21, 23, 23, 25, 25, 26, 27, 27, 27, 28],
               cols=[10, 11, 23, 6, 0, 7, 10, 0, 2, 7, 27, 13, 2, 7, 7, 20, 27,
                     20, 7, 12, 23, 11, 12, 13, 22, 3, 12, 13, 6, 29, 29, 8, 19,
                     25, 28, 1, 16, 8, 28, 19, 2, 6, 4, 14, 6, 17, 18, 21, 27],
               idxs=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                     1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1],
               colors=[4, 2]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3,
                     3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6,
                     7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 10, 10, 11, 11, 11, 11, 11,
                     11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14,
                     14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 17,
                     17, 18, 18, 18, 19, 19, 19, 19, 19, 19, 20, 20, 21, 21, 21,
                     22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24,
                     24, 24, 25, 25, 25, 25, 25, 25, 25, 26, 26, 26, 27, 27, 27,
                     27, 27, 27, 28, 28, 29, 29, 29, 29, 29],
               cols=[2, 4, 6, 19, 21, 2, 3, 17, 20, 27, 28, 0, 19, 20, 21, 22,
                     23, 2, 9, 12, 16, 20, 23, 29, 0, 16, 23, 24, 26, 29, 17,
                     29, 1, 3, 8, 9, 22, 26, 27, 29, 3, 4, 18, 19, 22, 11, 16,
                     18, 22, 25, 5, 20, 1, 2, 5, 10, 11, 17, 3, 6, 10, 12, 20,
                     21, 22, 2, 10, 19, 20, 22, 26, 8, 19, 20, 22, 3, 12, 17,
                     20, 21, 22, 24, 25, 0, 13, 15, 10, 11, 4, 9, 17, 2, 8, 17,
                     18, 22, 29, 17, 19, 8, 17, 25, 6, 12, 14, 29, 10, 14, 16,
                     18, 21, 26, 6, 8, 11, 12, 13, 17, 25, 1, 12, 16, 20, 23,
                     25, 27, 2, 5, 7, 5, 14, 17, 19, 20, 22, 16, 21, 2, 7, 17,
                     21, 29],
               idxs=[1, 2, 3, 2, 3, 3, 2, 3, 3, 1, 1, 1, 3, 3, 3, 1, 2, 3, 3, 1,
                     3, 2, 2, 3, 1, 2, 1, 3, 3, 2, 3, 3, 3, 1, 1, 1, 3, 3, 3, 2,
                     1, 3, 2, 1, 3, 1, 3, 2, 3, 2, 1, 3, 1, 3, 2, 3, 2, 3, 1, 1,
                     2, 2, 0, 0, 0, 1, 3, 0, 0, 0, 1, 1, 0, 0, 0, 2, 1, 2, 0, 0,
                     0, 3, 2, 1, 2, 3, 1, 1, 3, 2, 3, 3, 2, 3, 2, 2, 2, 1, 2, 2,
                     1, 1, 3, 2, 1, 2, 1, 2, 2, 1, 2, 3, 3, 3, 1, 1, 1, 3, 1, 3,
                     3, 3, 1, 3, 2, 2, 1, 2, 1, 2, 1, 3, 2, 1, 1, 2, 2, 3, 3, 2,
                     2, 2],
               colors=[2, 1, 3, 8]),
  ]
  return {"train": train, "test": test}
