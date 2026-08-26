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


def _legacy_cells(row, col, halfsize):
  pairs = [(row, col), (row, -col), (-row, col), (-row, -col)]
  if not row:  # For row zero, we also replicate elsewhere.
    pairs += [(col, row), (col, -row), (-col, row), (-col, -row)]
  return pairs, {(halfsize + dr, halfsize + dc) for dr, dc in pairs}


def _border(width, height):
  cells = set()
  for c in range(width):
    cells.add((0, c))
    cells.add((height - 1, c))
  for r in range(height):
    cells.add((r, 0))
    cells.add((r, width - 1))
  return cells


def _corners(width, height):
  return {(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)}


def _normalize(cells):
  min_r = min(r for r, _ in cells)
  min_c = min(c for _, c in cells)
  return {(r - min_r, c - min_c) for r, c in cells}


def _shape(cells):
  return (max(r for r, _ in cells) - min(r for r, _ in cells) + 1,
          max(c for _, c in cells) - min(c for _, c in cells) + 1)


def _place(grid, cells, color):
  for r, c in cells:
    grid[r][c] = color


def _fits(grid, cells, row, col, bgcolor):
  height, width = len(grid), len(grid[0])
  for r, c in cells:
    rr, cc = row + r, col + c
    if rr < 0 or rr >= height or cc < 0 or cc >= width:
      return False
    if grid[rr][cc] != bgcolor:
      return False
  return True


def generate(width=None, height=None, halfsize=None, bgcolor=None, rows=None,
             cols=None, colors=None, brows=None, bcols=None, out_width=None,
             out_height=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    halfsize: half the size of the target square
    bgcolor: the color of the background
    rows: a list of vertical coordinates of the target square perimeter
    cols: a list of horizontal coordinates of the target square perimeter
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates of the broken border centers
    bcols: a list of horizontal coordinates of the broken border centers
    out_width: the width of the reconstructed output rectangle
    out_height: the height of the reconstructed output rectangle
    num_colors: the number of non-background colors to sample
  """

  if width is None:
    if out_width is None:
      out_width = common.randint(3, 10)
    if out_height is None:
      out_height = common.randint(3, 10)
    if bgcolor is None:
      bgcolor = common.randint(0, 9)
    if num_colors is None:
      num_colors = common.randint(1, 9)
    width = common.randint(2 * out_width, 30)
    height = common.randint(2 * out_height, 30)
    palette = [c for c in range(10) if c != bgcolor]
    colors = common.sample(palette, min(num_colors, len(palette)))
    ring = _border(out_width, out_height)
    corner_cells = _corners(out_width, out_height)
    remaining = ring - corner_cells
    side_left = {(r, 0) for r in range(out_height)}
    side_right = {(r, out_width - 1) for r in range(out_height)}
    side_top = {(0, c) for c in range(out_width)}
    side_bottom = {(out_height - 1, c) for c in range(out_width)}
    valid_pairs = ((side_left, side_top), (side_left, side_bottom),
                   (side_right, side_top), (side_right, side_bottom))
    while True:
      grid = common.grid(width, height, bgcolor)
      pieces = []
      row = common.randint(0, height - out_height)
      col = common.randint(0, width - out_width)
      _place(grid, {(row + r, col + c) for r, c in corner_cells}, colors[0])
      pieces.append((corner_cells, colors[0]))
      for color in colors[1:]:
        if len(remaining) < 3:
          break
        max_piece = max(3, min(len(remaining), len(ring) // len(colors)))
        placed = False
        for _ in range(30):
          cells = set(common.sample(list(remaining),
                                    common.randint(3, max_piece)))
          if not any(cells & side1 and cells & side2
                     for side1, side2 in valid_pairs):
            continue
          norm = _normalize(cells)
          shape_h, shape_w = _shape(norm)
          if shape_h > height or shape_w > width:
            continue
          candidates = []
          for rr in range(height - shape_h + 1):
            for cc in range(width - shape_w + 1):
              if _fits(grid, norm, rr, cc, bgcolor):
                candidates.append((rr, cc))
          if not candidates:
            continue
          rr, cc = common.choice(candidates)
          _place(grid, {(rr + r, cc + c) for r, c in norm}, color)
          pieces.append((cells, color))
          remaining -= cells
          placed = True
          break
        if not placed:
          continue
      if pieces:
        break
  else:
    out_width = out_height = 2 * halfsize + 1
    grid = common.grid(width, height, bgcolor)
    pieces = []
    for row, col, color, brow, bcol in zip(rows, cols, colors, brows, bcols):
      pairs, cells = _legacy_cells(row, col, halfsize)
      for dr, dc in pairs:
        grid[brow + dr][bcol + dc] = color
      pieces.append((cells, color))

  output = common.grid(out_width, out_height, bgcolor)
  for cells, color in pieces:
    _place(output, cells, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, halfsize=2, bgcolor=3, rows=[0, 1, 2, 2],
               cols=[2, 2, 2, 1], colors=[1, 8, 2, 4], brows=[4, 9, 8, 2],
               bcols=[4, 2, 8, 8]),
      generate(width=8, height=10, halfsize=1, bgcolor=1, rows=[0, 1],
               cols=[1, 1], colors=[3, 8], brows=[6, 2], bcols=[4, 2]),
      generate(width=14, height=12, halfsize=2, bgcolor=4, rows=[0, 2], 
               cols=[2, 2], colors=[7, 1], brows=[7, 3], bcols=[9, 4]),
  ]
  test = [
      generate(width=19, height=18, halfsize=3, bgcolor=8, rows=[0, 1, 3, 3],
               cols=[3, 3, 3, 1], colors=[1, 2, 3, 6], brows=[5, 7, 12, 13],
               bcols=[6, 14, 6, 15]),
  ]
  return {"train": train, "test": test}
