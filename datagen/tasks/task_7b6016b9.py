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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, lowerrows=None, lowercols=None, upperrows=None,
             uppercols=None, color=None, flip=None, xpose=None, count=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    lowerrows: a list of lower vertical coordinates for lines
    lowercols: a list of lower horizontal coordinates for lines
    upperrows: a list of upper vertical coordinates for lines
    uppercols: a list of upper horizontal coordinates for lines
    color: the color of the lines
    flip: whether to flip the grids
    xpose: whether to transpose the grids
    count: rough number of boundary segments to place
    density: rough number of extra line pixels to attempt
  """

  def draw(grid, output):
    legal = True
    # Draw and fill boxes.
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          output[r][c] = grid[r][c] = color
      for r  in range(row + 1, row + tall - 1):
        for c in range(col + 1, col + wide - 1):
          grid[r][c] = common.black()
          output[r][c] = common.red()
    # Draw lines using -2 so we can detect intersection.
    for lrow, lcol, urow, ucol in zip(lowerrows, lowercols, upperrows,
                                      uppercols):
      dr, dc = (0 if lrow == urow else 1), (0 if lcol == ucol else 1)
      r, c = lrow, lcol
      if common.get_pixel(grid, r - dr, c - dc) == -2: legal = False
      while True:
        # Check for intersection.
        if common.get_pixel(grid, r, c) == -2: legal = False
        if common.get_pixel(grid, r + dr, c + dc) == -2: legal = False
        if grid[r][c] == 0: output[r][c] = grid[r][c] = -2
        if r == urow and c == ucol: break
        r, c = r + dr, c + dc
    # Redraw lines using the correct color.
    for r in range(height):
      for c in range(width):
        if grid[r][c] == -2: grid[r][c] = color
        if output[r][c] == -2: output[r][c] = color
    return legal

  if width is None:
    while True:  # Keep trying this until we get a grid with no intersections.
      width = common.randint(5, 30)
      height = common.randint(5, 30)
      this_count = count
      if this_count is None:
        this_count = common.randint(4, min(height, width))
      this_density = density
      if this_density is None:
        this_density = common.randint(0, (width * height) // 4)
      rows, cols, wides, talls = [], [], [], []

      def separated(row, col, wide, tall):
        for r, c, w, t in zip(rows, cols, wides, talls):
          if row <= r + t and r <= row + tall and col <= c + w and c <= col + wide:
            return False
        return True

      max_boxes = max(1, min(7, this_count, (width * height) // 35))
      target_boxes = common.randint(1, max_boxes)
      for _ in range(160):
        if len(rows) >= target_boxes: break
        wide = common.randint(3, max(3, min(width, width // 2 + 1)))
        tall = common.randint(3, max(3, min(height, height // 2 + 1)))
        row = common.randint(0, height - tall)
        col = common.randint(0, width - wide)
        if not separated(row, col, wide, tall): continue
        rows.append(row)
        cols.append(col)
        wides.append(wide)
        talls.append(tall)
      if len(rows) == 0: continue

      # Add non-intersecting loose line segments; boxes still define the fills.
      lowerrows, lowercols, upperrows, uppercols = [], [], [], []
      line_pixels = set()
      box_pixels = sum(2 * w + 2 * t - 4 for w, t in zip(wides, talls))
      max_line_pixels = max(0, (width * height) // 2 - box_pixels - 1)
      line_target = min(30, max(0, this_count + this_density // max(1, min(width, height))))
      for _ in range(6 * line_target):
        if len(lowerrows) >= line_target: break
        horizontal = common.randint(0, 1)
        if horizontal:
          span = common.randint(1, width)
          row = common.randint(0, height - 1)
          col = common.randint(0, width - span)
          cells = [(row, c) for c in range(col, col + span)]
          guard = cells + [(row, col - 1), (row, col + span)]
          lrow, urow = row, row
          lcol, ucol = col, col + span - 1
        else:
          span = common.randint(1, height)
          row = common.randint(0, height - span)
          col = common.randint(0, width - 1)
          cells = [(r, col) for r in range(row, row + span)]
          guard = cells + [(row - 1, col), (row + span, col)]
          lrow, urow = row, row + span - 1
          lcol, ucol = col, col
        if any(cell in line_pixels for cell in guard): continue
        if len(line_pixels) + len(cells) > max_line_pixels: continue
        line_pixels.update(cells)
        lowerrows.append(lrow)
        lowercols.append(lcol)
        upperrows.append(urow)
        uppercols.append(ucol)
      grid = common.grid(width, height)
      output = common.grid(width, height, common.green())
      if not draw(grid, output): continue
      colored = sum(1 for row in grid for cell in row if cell != common.black())
      if 2 * colored >= width * height: continue
      border = grid[0] + grid[-1]
      if height > 2:
        border += [grid[r][0] for r in range(1, height - 1)]
        border += [grid[r][-1] for r in range(1, height - 1)]
      border_colored = sum(1 for cell in border if cell != common.black())
      if 2 * border_colored >= len(border): continue
      break
    color = common.random_color(
        exclude=[common.black(), common.red(), common.green()])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  def coords(r, c):
    if flip: r = height - 1 - r
    if xpose: r, c = c, r
    return r, c

  final_width, final_height = (height, width) if xpose else (width, height)
  grid = common.grid(final_width, final_height)
  output = common.grid(final_width, final_height)

  def paint(target, r, c, value):
    r, c = coords(r, c)
    target[r][c] = value

  def pixel(target, r, c):
    r, c = coords(r, c)
    return target[r][c]

  # Draw the visible box borders.
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        if r in [row, row + tall - 1] or c in [col, col + wide - 1]:
          paint(grid, r, c, color)
          paint(output, r, c, color)
  # Draw the visible lines.
  for lrow, lcol, urow, ucol in zip(lowerrows, lowercols, upperrows,
                                    uppercols):
    dr, dc = (0 if lrow == urow else 1), (0 if lcol == ucol else 1)
    r, c = lrow, lcol
    while True:
      if pixel(grid, r, c) == common.black():
        paint(grid, r, c, color)
        paint(output, r, c, color)
      if r == urow and c == ucol: break
      r, c = r + dr, c + dc
  # Fill enclosed background components, preserving boundary pixels.
  seen = set()
  exterior = []
  for sr in range(final_height):
    for sc in range(final_width):
      if output[sr][sc] != common.black() or (sr, sc) in seen: continue
      seen.add((sr, sc))
      queue = [(sr, sc)]
      cells = []
      borders = False
      while queue:
        r, c = queue.pop()
        cells.append((r, c))
        borders = borders or r in [0, final_height - 1] or c in [0, final_width - 1]
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
          if nr < 0 or nr >= final_height or nc < 0 or nc >= final_width:
            continue
          if output[nr][nc] != common.black() or (nr, nc) in seen: continue
          seen.add((nr, nc))
          queue.append((nr, nc))
      if borders:
        exterior.extend(cells)
      else:
        for r, c in cells:
          output[r][c] = common.red()
  # Fill the remaining, border-connected background.
  for r, c in exterior:
    output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=23, height=23, rows=[4, 8, 15], cols=[6, 6, 13],
               wides=[5, 11, 4], talls=[5, 8, 5],
               lowerrows=[4, 8, 15, 19, 3, 0, 16, 1, 5],
               lowercols=[3, 3, 0, 12, 6, 10, 13, 16, 20],
               upperrows=[4, 8, 15, 19, 19, 10, 21, 21, 11],
               uppercols=[12, 21, 17, 20, 6, 10, 13, 16, 20], color=8, flip=0,
               xpose=0),
      generate(width=25, height=22, rows=[3, 3], cols=[4, 10], wides=[7, 7],
               talls=[10, 5],
               lowerrows=[3, 7, 12, 16, 1, 3, 1],
               lowercols=[0, 8, 1, 14, 4, 10, 16],
               upperrows=[3, 7, 12, 16, 18, 19, 19],
               uppercols=[24, 19, 12, 20, 4, 10, 16], color=1, flip=0, xpose=0),
      generate(width=21, height=24, rows=[5, 15, 15], cols=[4, 4, 13],
               wides=[10, 4, 6], talls=[11, 5, 4],
               lowerrows=[5, 8, 15, 18, 19, 1, 13, 2, 13],
               lowercols=[1, 9, 2, 12, 1, 4, 7, 13, 18],
               upperrows=[5, 8, 15, 18, 19, 22, 22, 22, 21],
               uppercols=[16, 17, 18, 20, 9, 4, 7, 13, 18], color=4, flip=0,
               xpose=0),
  ]
  test = [
      generate(width=25, height=22, rows=[4, 4], cols=[5, 16], wides=[12, 7],
               talls=[11, 6],
               lowerrows=[4, 9, 14, 17, 18, 1, 2, 1, 2],
               lowercols=[2, 10, 3, 12, 3, 5, 11, 16, 22],
               upperrows=[4, 9, 14, 17, 18, 21, 11, 19, 12],
               uppercols=[23, 23, 19, 20, 7, 5, 11, 16, 22], color=7, flip=0,
               xpose=0),
  ]
  return {"train": train, "test": test}
