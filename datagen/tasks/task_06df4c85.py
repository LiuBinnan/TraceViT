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


def generate(size=None, rows=None, cols=None, colors=None, linecolor=None,
             height=None, width=None, spacing=None, num_lines=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used for the cells
    linecolor: a digit representing a color to be used for the gridlines
    height: number of grid rows (defaults to size when omitted)
    width: number of grid columns (defaults to size when omitted)
    spacing: lattice cell size (defaults to 2, the original rendering); varying
      it independently of the cell counts widens the distinct output sizes
    num_lines: how many extra colored line-objects to attempt placing; widens
      the per-example color count, object count and foreground density
  """

  # Helper functions.
  def connect_bitmap(thebitmap, therows, thecols, thecolors):
    for j in range(len(thecolors)):
      for i in range(j):
        if thecolors[i] != thecolors[j]: continue
        if therows[i] == therows[j]:
          min_col = min(thecols[i], thecols[j])
          max_col = max(thecols[i], thecols[j])
          for col in range(min_col, max_col):
            bitmap[rows[i]][col] = thecolors[i]
        if thecols[i] == thecols[j]:
          min_row = min(therows[i], therows[j])
          max_row = max(therows[i], therows[j])
          for row in range(min_row, max_row):
            thebitmap[row][cols[i]] = thecolors[i]

  def horiz_free(thebitmap, therow, thecols):
    for thecol in range(thecols[0], thecols[1] + 1):
      if thebitmap[therow][thecol] > 0: return False
    return True

  def vert_free(thebitmap, thecol, therows):
    for therow in range(therows[0], therows[1] + 1):
      if thebitmap[therow][thecol] > 0: return False
    return True

  def matches_up(therows, thecols, thecolors, therow, thecol, thecolor):
    for r, c, color in zip(therows, thecols, thecolors):
      if color != thecolor: continue
      if r == therow or c == thecol: return True
    return False

  if size is None:
    size = common.randint(6, 10)
    if height is None: height = size
    if width is None: width = size
    # Vary the lattice cell size independently of the cell counts (re_arc
    # samples oh/ow in 1..4).  Cap the cell counts so the rendered linegrid
    # (cells * (spacing + 1) - 1) always stays within 30x30.
    if spacing is None:
      spacing = common.randint(1, 4)
    maxcells = 31 // (spacing + 1)
    height = max(5, min(height, maxcells))
    width = max(5, min(width, maxcells))
    linecolor = common.random_color()
    # First, decide where the "L" should live
    boxw = common.randint(3, width - 2)
    boxh = common.randint(3, height - 2)
    col_gap = common.randint(1, width - boxw - 1)
    row_gap = common.randint(1, height - boxh - 1)
    pixels = [[row_gap, col_gap], [row_gap + boxh - 1, col_gap + boxw - 1],
              [row_gap, col_gap + boxw - 1], [row_gap + boxh - 1, col_gap]]
    pixels = common.sample(pixels, 3)
    rows, cols = [list(p) for p in zip(*pixels)]
    el_color = common.random_color(exclude=[linecolor])
    colors = [el_color] * len(pixels)
    # Second, mark those cells in the bitmap and connect them
    bitmap = common.grid(width, height)
    for row, col, color in zip(rows, cols, colors):
      bitmap[row][col] = color
    connect_bitmap(bitmap, rows, cols, colors)
    # Third, try to add a couple lines, with different colors.  re_arc scales
    # the number of colored objects with the grid area (its ncols reaches 8);
    # mirror that so color/object/density variation widens toward its band.
    if num_lines is None:
      num_lines = common.randint(1, min(7, max(1, (height * width) // 12)))
    excluded = [linecolor, el_color]
    for _ in range(num_lines):
      if len(excluded) >= 9:  # never exhaust the 9 non-background colors
        break
      newrows, newcols = [], []
      if common.randint(0, 1) == 0:  # horiz
        row, col = common.randint(0, height - 1), common.sample(range(width), 2)
        col.sort()
        if not horiz_free(bitmap, row, col): continue
        newrows.extend([row] * 2)
        newcols.extend(col)
      else:  # vert
        row, col = common.sample(range(height), 2), common.randint(0, width - 1)
        row.sort()
        if not vert_free(bitmap, col, row): continue
        newrows.extend(row)
        newcols.extend([col] * 2)
      newcolor = common.random_color(exclude=excluded)
      newcolors = [newcolor] * 2
      excluded.append(newcolor)
      for row, col, color in zip(newrows, newcols, newcolors):
        bitmap[row][col] = color
      rows.extend(newrows)
      cols.extend(newcols)
      colors.extend(newcolors)
      connect_bitmap(bitmap, rows, cols, colors)
    # Fourth, add a random dot. Can't fall on a line or match up with same color
    while True:
      row, col = common.randint(0, height - 1), common.randint(0, width - 1)
      if bitmap[row][col] > 0: continue  # already filled
      color = common.random_color(exclude=[linecolor])
      if matches_up(rows, cols, colors, row, col, color): continue
      rows.append(row)
      cols.append(col)
      colors.append(color)
      break

  if height is None: height = size
  if width is None: width = size
  bitmap = common.grid(width, height)
  for row, col, color in zip(rows, cols, colors):
    bitmap[row][col] = color
  grid = common.create_linegrid(bitmap, spacing or 2, linecolor)
  output = common.create_linegrid(bitmap, spacing or 2, linecolor)

  def connect_matching_rows():
    nonlocal output
    for j in range(len(colors)):
      for i in range(j):
        if colors[i] != colors[j] or rows[i] != rows[j]:
          continue
        min_col = min(cols[i], cols[j])
        max_col = max(cols[i], cols[j])
        for col in range(min_col, max_col):
          bitmap[rows[i]][col] = colors[i]
    output = common.create_linegrid(bitmap, spacing or 2, linecolor)

  def connect_matching_cols():
    nonlocal output
    for j in range(len(colors)):
      for i in range(j):
        if colors[i] != colors[j] or cols[i] != cols[j]:
          continue
        min_row = min(rows[i], rows[j])
        max_row = max(rows[i], rows[j])
        for row in range(min_row, max_row):
          bitmap[row][cols[i]] = colors[i]
    output = common.create_linegrid(bitmap, spacing or 2, linecolor)

  connect_matching_rows()
  connect_matching_cols()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, rows=[1, 1, 2, 3, 4, 4], cols=[1, 5, 3, 5, 1, 3],
               colors=[2, 2, 1, 2, 3, 3], linecolor=8),
      generate(size=8, rows=[1, 1, 3, 3, 4, 5, 6, 6],
               cols=[1, 4, 3, 7, 6, 1, 6, 3], colors=[2, 4, 9, 9, 8, 2, 8, 8],
               linecolor=1),
      generate(size=8, rows=[1, 1, 3, 3, 6, 6], cols=[1, 5, 3, 6, 1, 5],
               colors=[3, 2, 2, 2, 3, 3], linecolor=4),
  ]
  test = [
      generate(size=9, rows=[1, 1, 3, 4, 6, 6], cols=[2, 5, 7, 2, 1, 5],
               colors=[8, 2, 3, 8, 2, 2], linecolor=4),
  ]
  return {"train": train, "test": test}
