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


def _create_linegrid(bitmap, spacing, linecolor, row_spacing=None,
                     col_spacing=None):
  """Creates a line grid with optionally independent row/column spacing."""
  if row_spacing is None:
    row_spacing = spacing
  if col_spacing is None:
    col_spacing = spacing
  actual_height = len(bitmap) * (row_spacing + 1) - 1
  actual_width = len(bitmap[0]) * (col_spacing + 1) - 1
  ingrid = common.grid(actual_width, actual_height)
  for r in range(actual_height):
    for c in range(actual_width):
      if (r + 1) % (row_spacing + 1) == 0:
        ingrid[r][c] = linecolor
      if (c + 1) % (col_spacing + 1) == 0:
        ingrid[r][c] = linecolor
  for r, row in enumerate(bitmap):
    for c, color in enumerate(row):
      for dr in range(row_spacing):
        for dc in range(col_spacing):
          ingrid[r * (row_spacing + 1) + dr][
              c * (col_spacing + 1) + dc] = color
  return ingrid


def _sample_pattern_key(pixel_count):
  offsets = [(-1, 0), (0, 1), (1, 0), (0, -1),
             (-1, 1), (1, 1), (1, -1), (-1, -1)]
  selected = []
  while len(selected) < pixel_count:
    candidates = []
    for offset in offsets:
      if offset in selected:
        continue
      attached = False
      for chosen in selected:
        dist = abs(offset[0] - chosen[0]) + abs(offset[1] - chosen[1])
        if dist == 1:
          attached = True
      if not selected and abs(offset[0]) + abs(offset[1]) == 1:
        attached = True
      if attached:
        candidates.append(offset)
    selected.append(common.choice(candidates))
  key = 0
  for offset in selected:
    key |= 1 << offsets.index(offset)
  return key


def generate(size=None, rows=None, cols=None, colors=None, spacing=None,
             linecolor=None, height=None, width=None, count=None,
             row_spacing=None, col_spacing=None, num_colors=None,
             pixel_count=None, pattern_key=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the bitmap
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of colors to be used for the middle / edges / corners
    spacing: how much spacing to leave in between the lines
    linecolor: the color of the lines
    height: the height (rows) of the bitmap; defaults to size
    width: the width (cols) of the bitmap; defaults to size
    count: the number of marked cells in the bitmap
    row_spacing: how much vertical spacing to leave inside each cell
    col_spacing: how much horizontal spacing to leave inside each cell
    num_colors: the number of colors used by the copied motif
    pixel_count: the number of motif pixels around the exemplar
    pattern_key: bitmask selecting motif offsets around the exemplar
  """
  if size is None:
    size = common.randint(5, 10)
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    while True:
      # The selected checkpoints consume up to the original four extra draws.
      # Keep the sampled count under that cap even when count is overridden.
      max_count = min(4, (min(height, width) - 1) // 2)
      if count is None:
        count = common.randint(2, max(2, max_count))
      count = max(2, min(max_count, count))
      if pixel_count is None:
        pixel_count = common.randint(1, 8)
      pixel_count = max(1, min(8, pixel_count))
      if pattern_key is None:
        pattern_key = _sample_pattern_key(pixel_count)
      offsets = [(-1, 0), (0, 1), (1, 0), (0, -1),
                 (-1, 1), (1, 1), (1, -1), (-1, -1)]
      selected = [offset for bit, offset in enumerate(offsets)
                  if pattern_key & (1 << bit)]
      candidates = common.shuffle(common.all_pixels(width, height))
      pixels, occupied = [], set()
      for row, col in candidates:
        shape = {(row, col)}
        fits = True
        for dr, dc in selected:
          rr, cc = row + dr, col + dc
          if rr < 0 or rr >= height or cc < 0 or cc >= width:
            fits = False
          shape.add((rr, cc))
        if not fits or shape & occupied:
          continue
        touches = False
        for rr, cc in shape:
          for nr, nc in [(rr - 1, cc), (rr + 1, cc),
                         (rr, cc - 1), (rr, cc + 1)]:
            if (nr, nc) in occupied:
              touches = True
        if touches:
          continue
        if not pixels and (row in [0, height - 1] or col in [0, width - 1]):
          continue
        pixels.append((row, col))
        occupied |= shape
        if len(pixels) == count:
          break
      if len(pixels) != count:
        pattern_key = None
        pixel_count = None
        continue
      rows, cols = zip(*pixels)
      break
    linecolor = common.random_color()
    if row_spacing is None:
      row_spacing = common.randint(1, max(1, (31 - height) // height))
    if col_spacing is None:
      col_spacing = common.randint(1, max(1, (31 - width) // width))
    if num_colors is None:
      num_colors = common.randint(1, 7)
    num_colors = max(1, min(7, num_colors))
    center = common.random_color(exclude=[linecolor])
    ext = []
    for _ in range(num_colors):
      ext.append(common.random_color(exclude=[linecolor, center] + ext))
    colors = [center] + ext

  bitmap = common.grid(width, height)
  for row, col in zip(rows, cols):
    common.draw(bitmap, row, col, colors[0])

  def draw_pattern(idx):
    if idx >= len(rows):
      return
    row, col = rows[idx], cols[idx]
    if pattern_key is not None:
      offsets = [(-1, 0), (0, 1), (1, 0), (0, -1),
                 (-1, 1), (1, 1), (1, -1), (-1, -1)]
      selected = [offset for bit, offset in enumerate(offsets)
                  if pattern_key & (1 << bit)]
      for pos, (dr, dc) in enumerate(selected):
        color = colors[1 + (pos % (len(colors) - 1))]
        common.draw(bitmap, row + dr, col + dc, color)
      return
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
      common.draw(bitmap, row + dr, col + dc, colors[1])
    if len(colors) < 3: return
    for dr, dc in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
      common.draw(bitmap, row + dr, col + dc, colors[2])

  draw_pattern(0)
  grid = _create_linegrid(bitmap, spacing, linecolor, row_spacing, col_spacing)
  output = grid
  draw_pattern(1)
  output = _create_linegrid(bitmap, spacing, linecolor, row_spacing, col_spacing)
  draw_pattern(2)
  output = _create_linegrid(bitmap, spacing, linecolor, row_spacing, col_spacing)
  draw_pattern(3)
  output = _create_linegrid(bitmap, spacing, linecolor, row_spacing, col_spacing)
  draw_pattern(4)
  output = _create_linegrid(bitmap, spacing, linecolor, row_spacing, col_spacing)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[1, 4], cols=[1, 3], colors=[6, 3], spacing=4,
               linecolor=8),
      generate(size=7, rows=[2, 0, 5], cols=[2, 6, 3], colors=[4, 6], spacing=3,
               linecolor=3),
      generate(size=7, rows=[4, 0, 1], cols=[4, 6, 1], colors=[2, 4, 4],
               spacing=3, linecolor=8),
  ]
  test = [
      generate(size=10, rows=[3, 1, 7, 8], cols=[3, 7, 5, 0], colors=[6, 3, 8],
               spacing=2, linecolor=4),
  ]
  return {"train": train, "test": test}
