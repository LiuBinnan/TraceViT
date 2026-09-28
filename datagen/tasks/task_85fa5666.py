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


def generate(size=None, brows=None, bcols=None, colors=None, extra_rows=None,
             extra_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    extra_rows: The rows of the extra pixels (to handle an ambiguous case)
    extra_cols: The columns of the extra pixels (to handle an ambiguous case).
  """

  def draw():
    grid, output = common.grids(size, size)
    for brow, bcol in zip(brows, bcols):
      for r in range(2):
        for c in range(2):
          output[brow + r][bcol + c] = grid[brow + r][bcol + c] = 2
    for i, color in enumerate(colors):
      row, col = brows[i // 4] - 1, bcols[i // 4] - 1
      if i % 4 in [1, 3]: col += 3
      if i % 4 in [2, 3]: row += 3
      grid[row][col] = color
      row, col = brows[i // 4] - 1, bcols[i // 4] - 1
      if i % 4 in [0, 1]: col += 3
      if i % 4 in [1, 3]: row += 3
      output[row][col] = color
      rdir, cdir = -1, -1
      if i % 4 in [0, 1]: cdir = 1
      if i % 4 in [1, 3]: rdir = 1
      for _ in range(size):
        row, col = row + rdir, col + cdir
        if common.get_pixel(output, row, col) == 2: break
        if common.get_pixel(output, row, col) not in [-1, 0]: return None, None
        common.draw(output, row, col, color)
    if extra_rows:
      for row, col in zip(extra_rows, extra_cols):
        output[row][col] = 0
    return grid, output

  if brows is None:
    if size is None:
      size = common.randint(8, 22)
    num_boxes = min(4, size // 3)
    attempts = 0
    while True:
      attempts += 1
      brows = [common.randint(1, size - 3) for _ in range(num_boxes)]
      bcols = [common.randint(1, size - 3) for _ in range(num_boxes)]
      if not common.overlaps(brows, bcols, [4] * num_boxes,
                             [4] * num_boxes):
        colors = []
        for _ in range(num_boxes):
          colors.extend(common.shuffle([3, 6, 7, 8]))
        grid, _ = draw()
        if grid: break
      if attempts >= 256 and num_boxes > 1:
        num_boxes -= 1
        attempts = 0

  # Build the input grid: red 2x2 boxes, each ringed by a colored marker at its
  # four diagonal corners.
  grid = common.grid(size, size)
  for brow, bcol in zip(brows, bcols):
    for r in range(2):
      for c in range(2):
        grid[brow + r][bcol + c] = 2
  for i, color in enumerate(colors):
    row, col = brows[i // 4] - 1, bcols[i // 4] - 1
    if i % 4 in [1, 3]: col += 3
    if i % 4 in [2, 3]: row += 3
    grid[row][col] = color
  output = common.grid(size, size)

  def place_boxes():
    """Stamps every red anchor box; the diagonal beams break against these."""
    nonlocal output
    for brow, bcol in zip(brows, bcols):
      for r in range(2):
        for c in range(2):
          output[brow + r][bcol + c] = 2

  def fire_box_rays(b):
    """For box b, relocates each corner marker one step clockwise and fires a
    diagonal beam of its color outward to the grid edge."""
    nonlocal output
    if b >= len(brows): return
    for j in range(4):
      color = colors[4 * b + j]
      row, col = brows[b] - 1, bcols[b] - 1
      if j in [0, 1]: col += 3
      if j in [1, 3]: row += 3
      output[row][col] = color
      rdir, cdir = -1, -1
      if j in [0, 1]: cdir = 1
      if j in [1, 3]: rdir = 1
      for _ in range(size):
        row, col = row + rdir, col + cdir
        if common.get_pixel(output, row, col) == 2: break
        if common.get_pixel(output, row, col) not in [-1, 0]: break
        common.draw(output, row, col, color)

  place_boxes()
  fire_box_rays(0)
  fire_box_rays(1)
  fire_box_rays(2)
  fire_box_rays(3)
  if extra_rows:
    for row, col in zip(extra_rows, extra_cols):
      output[row][col] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, brows=[1, 3, 7], bcols=[7, 1, 7],
               colors=[6, 7, 8, 3, 8, 7, 6, 3, 6, 7, 3, 8]),
      generate(size=12, brows=[1, 5, 8], bcols=[7, 9, 2],
               colors=[8, 6, 3, 7, 6, 7, 3, 8, 8, 3, 7, 6], extra_rows=[8, 9],
               extra_cols=[1, 0]),
      generate(size=8, brows=[1, 5], bcols=[1, 4],
               colors=[3, 7, 6, 8, 6, 7, 8, 3]),
      generate(size=9, brows=[3], bcols=[3], colors=[3, 6, 8, 7]),
  ]
  test = [
      generate(size=8, brows=[1, 5], bcols=[3, 1],
               colors=[3, 8, 7, 6, 7, 6, 8, 3]),
  ]
  return {"train": train, "test": test}
