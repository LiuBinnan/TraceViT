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


def generate(rows=None, cols=None, wide=None, tall=None, brow=None, bcol=None,
             xpose=None, size=15, height=None, width=None, density=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wide: the width of the box
    tall: the height of the box
    brow: the vertical coordinate of the top of the box
    bcol: the horizontal coordinate of the left of the box
    xpose: whether to transpose the grids
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    density: target percentage of gray cells in the movable fragments
    count: target number of gray cells in the movable fragments
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    if xpose is None:
      xpose = 0
    logical_height = width if xpose else height
    logical_width = height if xpose else width

    def split_rows(box_height):
      top_rows = [r for r in range(box_height - 4) if r * 2 < box_height - 5]
      bottom_rows = [
          r for r in range(box_height - 4) if r * 2 > box_height - 5
      ]
      return top_rows, bottom_rows

    def brow_range(box_height):
      top_rows, bottom_rows = split_rows(box_height)
      if not top_rows or not bottom_rows:
        return None
      bottom_min_offset = -max(bottom_rows) + 1 + box_height + (
          box_height - 1) // 2
      if bottom_min_offset < box_height:
        return None
      min_brow = max(top_rows) + 2
      bottom_offset = -min(bottom_rows) + 1 + box_height + (
          box_height - 1) // 2
      max_brow = min(logical_height - box_height,
                     logical_height - 1 - bottom_offset)
      if min_brow > max_brow:
        return None
      return min_brow, max_brow

    valid_talls = []
    for box_height in range(8, logical_height + 1):
      if brow_range(box_height) is None:
        continue
      top_rows, bottom_rows = split_rows(box_height)
      row_span = max(max(top_rows) - min(top_rows),
                     max(bottom_rows) - min(bottom_rows))
      if logical_width >= row_span + 7:
        valid_talls.append(box_height)
    if tall is None:
      tall = common.randint(min(valid_talls), max(valid_talls))
    if brow is None:
      min_brow, max_brow = brow_range(tall)
      brow = common.randint(min_brow, max_brow)
    top_rows, bottom_rows = split_rows(tall)
    row_span = max(max(top_rows) - min(top_rows),
                   max(bottom_rows) - min(bottom_rows))
    if wide is None:
      wide_options = [
          box_width for box_width in range(row_span + 3, logical_width - 3)
          if box_width % 2 == 1
      ]
      wide = common.choice(wide_options)
    if bcol is None:
      bcol = common.randint(2, logical_width - wide - 2)

    inner_width = wide - 2
    top_area, bottom_area = len(top_rows) * inner_width, len(
        bottom_rows) * inner_width

    def sample_component_count(area):
      cells = common.randint(0, area // 2)
      cells = common.choice([cells, area - cells])
      return min(area, max(inner_width, cells))

    if density is None and count is None:
      top_count = sample_component_count(top_area)
      bottom_count = sample_component_count(bottom_area)
    else:
      if density is None:
        total_count = count
      else:
        total_count = round((top_area + bottom_area) * density / 100)
        if count is not None:
          total_count = min(total_count, count)
      total_count = min(top_area + bottom_area,
                        max(2 * inner_width, total_count))
      min_top = max(inner_width, total_count - bottom_area)
      max_top = min(top_area, total_count - inner_width)
      top_count = common.randint(min_top, max_top)
      bottom_count = total_count - top_count

    def component(row_values, cell_count):
      pixels = []
      row_count = len(row_values)
      period = max(1, 2 * row_count - 2)
      for col in range(inner_width):
        idx = col % period
        if idx >= row_count:
          idx = period - idx
        pixels.append((row_values[idx], col))
      while len(pixels) < cell_count:
        candidates = []
        for row, col in pixels:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              nr, nc = row + dr, col + dc
              if nr not in row_values or nc < 0 or nc >= inner_width:
                continue
              if (nr, nc) not in pixels and (nr, nc) not in candidates:
                candidates.append((nr, nc))
        if not candidates:
          break
        pixels.append(common.choice(candidates))
      return pixels

    pixels = component(top_rows, top_count) + component(
        bottom_rows, bottom_count)
    rows, cols = zip(*pixels)

  grid, output = common.grids(width, height)

  def coords(r, c):
    return (c, r) if xpose else (r, c)

  def set_cell(bitmap, r, c, color):
    r, c = coords(r, c)
    bitmap[r][c] = color

  def set_both(r, c, color):
    set_cell(grid, r, c, color)
    set_cell(output, r, c, color)

  def draw_grippers():
    for c in range(bcol, bcol + wide):
      set_both(brow, c, common.red())
      set_both(brow + tall - 1, c, common.red())
    for bitmap in [grid, output]:
      set_cell(bitmap, brow + 1, bcol, common.red())
      set_cell(bitmap, brow + 1, bcol + wide - 1, common.red())
      set_cell(bitmap, brow + tall - 2, bcol, common.red())
      set_cell(bitmap, brow + tall - 2, bcol + wide - 1, common.red())

  components = [
      [(r, c) for r, c in zip(rows, cols) if r * 2 < tall - 5],
      [(r, c) for r, c in zip(rows, cols) if r * 2 > tall - 5],
  ]
  for r, c in zip(rows, cols):
    if r < (tall - 1) // 2 - 1:
      set_cell(grid, brow - r - 2, bcol + c + 1, common.gray())
    else:
      set_cell(
          grid, brow - r + 1 + tall + (tall - 1) // 2, bcol + c + 1,
          common.gray())

  def reveal_component(component_idx):
    if component_idx >= len(components):
      return
    for r, c in components[component_idx]:
      set_cell(output, brow + r + 2, bcol + c + 1, common.gray())

  draw_grippers()
  reveal_component(0)
  reveal_component(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 4, 4, 4], cols=[1, 1, 0, 1, 2], wide=5, tall=9,
               brow=3, bcol=2, xpose=0),
      generate(rows=[0, 0, 1, 1, 3, 3, 4, 4, 4, 4],
               cols=[1, 2, 1, 2, 1, 2, 0, 1, 2, 3], wide=6, tall=9,
               brow=3, bcol=5, xpose=1),
      generate(rows=[0, 0, 0, 1, 2, 2, 3, 3], cols=[0, 1, 2, 1, 1, 2, 0, 1],
               wide=5, tall=8, brow=3, bcol=4, xpose=1),
  ]
  test = [
      generate(rows=[1, 1, 1, 0, 0, 0, 0, 4, 3, 3, 3, 3, 3],
               cols=[1, 2, 3, 0, 1, 3, 4, 2, 0, 1, 2, 3, 4],
               wide=7, tall=9, brow=3, bcol=3, xpose=0),
  ]
  return {"train": train, "test": test}
