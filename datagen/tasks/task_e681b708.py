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


def generate(width=None, height=None, rows=None, cols=None, lefts=None,
             rights=None, tops=None, bottoms=None, colors=None, prows=None,
             pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    rows: The row indices of the horizontal dividing lines.
    cols: The column indices of the vertical dividing lines.
    lefts: The left column indices of the horizontal dividing lines.
    rights: The right column indices of the horizontal dividing lines.
    tops: The top row indices of the vertical dividing lines.
    bottoms: The bottom row indices of the vertical dividing lines.
    colors: The colors to use for the intersection points.
    prows: The row indices of the pixels.
    pcols: The column indices of the pixels.
  """

  def draw(debug=False):
    # Check that some line always connects to one side of the grid.
    if 0 not in lefts or 0 not in tops:
      if debug: print("No left or top.")
      return None, None, None, None
    if len(cols) + 1 not in rights or len(rows) + 1 not in bottoms:
      if debug: print("No right or bottom.")
      return None, None, None, None
    # Check that there's sufficient space between the lines.
    if common.overlaps_1d(rows, [2] * len(rows)):
      if debug: print("Rows too close.")
      return None, None, None, None
    if common.overlaps_1d(cols, [2] * len(cols)):
      if debug: print("Cols too close.")
      return None, None, None, None
    # Create the grids.
    grid, output = common.grids(width, height)
    rids, cids = common.grids(width, height)
    # Draw the horizontal dividing lines.
    for row, left, right in zip(rows, lefts, rights):
      left_col, right_col = 0, width - 1
      if left > 0: left_col = cols[left - 1]
      if right <= len(cols): right_col = cols[right - 1]
      for col in range(left_col, right_col + 1):
        rids[row][col] = output[row][col] = grid[row][col] = 1
    # Draw the vertical dividing lines.
    for col, top, bottom in zip(cols, tops, bottoms):
      top_row, bot_row = 0, height - 1
      if top > 0: top_row = rows[top - 1]
      if bottom <= len(rows): bot_row = rows[bottom - 1]
      for row in range(top_row, bot_row + 1):
        cids[row][col] = output[row][col] = grid[row][col] = 1
    # Check that the horizontal endpoints always connect to something.
    for row, left, right in zip(rows, lefts, rights):
      if left > 0 and not cids[row][cols[left - 1]]:
        if debug: print("Left endpoint doesn't connect.")
        return None, None, None, None
      if right <= len(cols) and not cids[row][cols[right - 1]]:
        if debug: print("Right endpoint doesn't connect.")
        return None, None, None, None
    # Check that the vertical endpoints always connect to something.
    for col, top, bottom in zip(cols, tops, bottoms):
      if top > 0 and not rids[rows[top - 1]][col]:
        if debug: print("Top endpoint doesn't connect.")
        return None, None, None, None
      if bottom <= len(rows) and not rids[rows[bottom - 1]][col]:
        if debug: print("Bottom endpoint doesn't connect.")
        return None, None, None, None
    # Draw the intersection colors.
    color_idx = 0
    for row in range(height):
      for col in range(width):
        if not rids[row][col] and row not in [0, height - 1]: continue
        if not cids[row][col] and col not in [0, width - 1]: continue
        if not rids[row][col] and not cids[row][col]: continue
        output[row][col] = grid[row][col] = colors[color_idx]
        color_idx += 1
    # Determine the colors of the pixels.
    pcolors = []
    for prow, pcol in zip(prows, pcols):
      left, right, bottom, top = pcol, pcol, prow, prow
      while bottom + 1 < height and grid[bottom][pcol] == 0:
        bottom += 1
      while top > 0 and grid[top][pcol] == 0:
        top -= 1
      while left > 0 and grid[prow][left] == 0:
        left -= 1
      while right + 1 < width and grid[prow][right] == 0:
        right += 1
      subset = []
      for row in range(top, bottom + 1):
        for col in range(left, right + 1):
          if top < row < bottom and left < col < right: continue
          if grid[row][col] not in [0, 1]: subset.append(grid[row][col])
          if row in [0, height - 1] or col in [0, width - 1]: continue
          if grid[row][col] == 0:
            if debug: print("Expected a line here.")
            return None, None, None, None  # We expected a line here.
      if not subset: return None, None, None, None
      counts = [subset.count(c) for c in subset]
      max_count = max(counts)
      subset = [c for c, count in zip(subset, counts) if count == max_count]
      subset = list(set(subset))
      if len(subset) != 1:
        if debug: print("Multiple maximum counts.")
        return None, None, None, None  # Multiple maximum counts.
      pcolors.append(subset[0])
    if len(set(pcolors)) < 2:
      if debug: print("Not enough colors.")
      return None, None, None, None
    # Draw the pixels.
    kept_prows, kept_pcols = [], []
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      if grid[prow][pcol] != 0: continue
      grid[prow][pcol] = 1
      output[prow][pcol] = pcolor
      kept_prows.append(prow)
      kept_pcols.append(pcol)
    pprows, ppcols = kept_prows, kept_pcols
    kept_prows, kept_pcols = [], []
    # Only keep pixels that don't touch anything on their edge.
    for prow, pcol in zip(pprows, ppcols):
      good = True
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r, c = prow + dr, pcol + dc
        if common.get_pixel(output, r, c) not in [-1, 0]: good = False
      if not good: continue
      kept_prows.append(prow)
      kept_pcols.append(pcol)
    return grid, output, kept_prows, kept_pcols

  if width is None:
    attempts = 0
    while True:
      attempts += 1
      base = common.randint(18, 28)
      width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
      num_rows, num_cols = common.randint(2, 3), common.randint(2, 3)
      options = [3] * 15 + [2] * 10 + [4] * 6 + [8] * 3 + [6]
      if attempts > 500:
        rows = [(i + 1) * height // (num_rows + 1)
                for i in range(num_rows)]
        cols = [(i + 1) * width // (num_cols + 1)
                for i in range(num_cols)]
        lefts, rights = [0] * num_rows, [num_cols + 1] * num_rows
        tops, bottoms = [0] * num_cols, [num_rows + 1] * num_cols
        row_bounds = [0] + rows + [height - 1]
        col_bounds = [0] + cols + [width - 1]
        safe_cells = []
        for ridx in range(num_rows + 1):
          for cidx in range(num_cols + 1):
            if (ridx in [0, num_rows] and
                cidx in [0, num_cols]):
              continue
            top, bottom = row_bounds[ridx], row_bounds[ridx + 1]
            left, right = col_bounds[cidx], col_bounds[cidx + 1]
            if bottom - top < 4 or right - left < 4: continue
            safe_cells.append((ridx, cidx, (top + bottom) // 2,
                               (left + right) // 2))
        sums = [ridx + cidx for ridx, cidx, _, _ in safe_cells]
        if len(set(sums)) < 2: continue
        threshold = (min(sums) + max(sums) + 3) // 2
        threshold = max(min(sums) + 2, min(max(sums) + 1, threshold))
        first_color = common.choices(options, 1)[0]
        other_options = [color for color in options if color != first_color]
        second_color = common.choices(other_options, 1)[0]
        colors = []
        for ridx in range(num_rows + 2):
          for cidx in range(num_cols + 2):
            if (ridx in [0, num_rows + 1] and
                cidx in [0, num_cols + 1]):
              continue
            colors.append(first_color if ridx + cidx < threshold
                          else second_color)
        prows = [prow for _, _, prow, _ in safe_cells]
        pcols = [pcol for _, _, _, pcol in safe_cells]
        grid, _, kept_prows, kept_pcols = draw()
        if grid:
          prows, pcols = kept_prows, kept_pcols
          break
        continue
      rows = sorted(common.sample(list(range(2, height - 3)), num_rows))
      cols = sorted(common.sample(list(range(2, width - 3)), num_cols))
      if common.overlaps_1d(rows, [4] * len(rows)): continue
      if common.overlaps_1d(cols, [4] * len(cols)): continue
      lefts, rights, tops, bottoms = [], [], [], []
      for _ in rows:
        length = common.randint(1, len(cols) + 1)
        left = common.randint(0, len(cols) + 1 - length)
        right = left + length
        lefts, rights = lefts + [left], rights + [right]
      lefts[common.randint(0, num_rows - 1)] = 0  # Add a left.
      rights[common.randint(0, num_rows - 1)] = len(cols) + 1  # Add a right.
      for _ in cols:
        length = common.randint(1, len(rows) + 1)
        top = common.randint(0, len(rows) + 1 - length)
        bottom = top + length
        tops, bottoms = tops + [top], bottoms + [bottom]
      tops[common.randint(0, num_cols - 1)] = 0  # Add a top.
      bottoms[common.randint(0, num_cols - 1)] = len(rows) + 1  # Add a bottom.
      num_colors = (num_rows + 2) * (num_cols + 2)
      colors = common.choices(options, num_colors)
      prows, pcols = [], []
      for row in range(height):
        for col in range(width):
          if common.randint(0, 9): continue
          prows.append(row)
          pcols.append(col)
      grid, candidate_output, kept_prows, kept_pcols = draw()
      if grid:
        kept_colors = {
            candidate_output[prow][pcol]
            for prow, pcol in zip(kept_prows, kept_pcols)
        }
        if len(kept_colors) >= 2:
          prows, pcols = kept_prows, kept_pcols
          break

        # If edge filtering removed every pixel of all but one target color,
        # retain a non-touching pair of differently colored candidates.
        layout = common.deepcopy(grid)
        candidates = []
        for prow, pcol in zip(prows, pcols):
          if (grid[prow][pcol] != common.blue() or
              candidate_output[prow][pcol] == common.blue()):
            continue
          candidates.append((prow, pcol, candidate_output[prow][pcol]))
          layout[prow][pcol] = common.black()
        safe = []
        for prow, pcol, pcolor in candidates:
          if all(common.get_pixel(layout, prow + dr, pcol + dc) in [-1, 0]
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]):
            safe.append((prow, pcol, pcolor))
        pair = None
        for i, first in enumerate(safe):
          for second in safe[i + 1:]:
            if first[2] == second[2]: continue
            if abs(first[0] - second[0]) + abs(first[1] - second[1]) == 1:
              continue
            pair = first, second
            break
          if pair: break
        if pair:
          selected = set(zip(kept_prows, kept_pcols))
          selected.add(pair[0][:2])
          selected.add(pair[1][:2])
          prows = [prow for prow, pcol, _ in candidates
                   if (prow, pcol) in selected]
          pcols = [pcol for prow, pcol, _ in candidates
                   if (prow, pcol) in selected]
          break

  grid, _, _, _ = draw()

  def find_pixel_targets():
    """Finds the dominant boundary color for every isolated blue pixel."""
    if not grid: return {}
    rids, cids = common.grids(width, height)
    for row, left, right in zip(rows, lefts, rights):
      left_col, right_col = 0, width - 1
      if left > 0: left_col = cols[left - 1]
      if right <= len(cols): right_col = cols[right - 1]
      for col in range(left_col, right_col + 1):
        rids[row][col] = common.blue()
    for col, top, bottom in zip(cols, tops, bottoms):
      top_row, bot_row = 0, height - 1
      if top > 0: top_row = rows[top - 1]
      if bottom <= len(rows): bot_row = rows[bottom - 1]
      for row in range(top_row, bot_row + 1):
        cids[row][col] = common.blue()

    layout = common.deepcopy(grid)
    pixel_positions = []
    for prow, pcol in zip(prows, pcols):
      if rids[prow][pcol] or cids[prow][pcol]: continue
      layout[prow][pcol] = common.black()
      pixel_positions.append((prow, pcol))

    targets = {}
    for prow, pcol in pixel_positions:
      left, right, bottom, top = pcol, pcol, prow, prow
      while (bottom + 1 < height and
             layout[bottom][pcol] == common.black()):
        bottom += 1
      while top > 0 and layout[top][pcol] == common.black():
        top -= 1
      while left > 0 and layout[prow][left] == common.black():
        left -= 1
      while (right + 1 < width and
             layout[prow][right] == common.black()):
        right += 1
      boundary_colors = []
      for row in range(top, bottom + 1):
        for col in range(left, right + 1):
          if top < row < bottom and left < col < right: continue
          color = layout[row][col]
          if color not in [common.black(), common.blue()]:
            boundary_colors.append(color)
      counts = [boundary_colors.count(color) for color in boundary_colors]
      max_count = max(counts)
      subset = [color for color, count in zip(boundary_colors, counts)
                if count == max_count]
      subset = list(set(subset))
      if len(subset) != 1: return {}
      targets[(prow, pcol)] = subset[0]
    return targets

  pixel_targets = find_pixel_targets()
  target_colors = sorted(set(pixel_targets.values()))
  output = common.deepcopy(grid) if grid else common.grid(1, 1)

  def reveal_color(index):
    """Recolors every pixel whose region has target color index."""
    if not grid: return
    if index >= len(target_colors): return
    color = target_colors[index]
    for (row, col), target in pixel_targets.items():
      if target == color:
        output[row][col] = color

  reveal_color(0)
  reveal_color(1)
  reveal_color(2)
  reveal_color(3)
  reveal_color(4)
  return {"input": grid, "output": output if grid else None}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=22, rows=[5, 13], cols=[7, 16], lefts=[0, 1],
               rights=[3, 3], tops=[0, 1], bottoms=[3, 3],
               colors=[2, 3, 2, 2, 3, 3, 8, 8, 3, 3],
               prows=[1, 1, 1, 3, 3, 3, 3, 8, 8, 8, 8, 9, 10, 10, 10, 10, 14, 15, 15, 16, 17, 17, 17, 19, 20, 20],
               pcols=[2, 12, 22, 2, 4, 10, 16, 10, 14, 20, 23, 1, 5, 13, 19, 22, 3, 10, 23, 19, 3, 12, 21, 1, 12, 20]),
      generate(width=23, height=27, rows=[3, 9, 16], cols=[10, 17],
               lefts=[0, 0, 0], rights=[3, 1, 3], tops=[0, 3], bottoms=[4, 4],
               colors=[2, 6, 2, 3, 8, 2, 3, 3, 3, 3, 2, 8],
               prows=[0, 0, 0, 0, 1, 1, 1, 1, 5, 5, 7, 7, 7, 7, 11, 11, 12, 12, 13, 14, 19, 19, 20, 20, 20, 20, 21, 22, 24, 24, 24, 25],
               pcols=[2, 5, 13, 19, 3, 7, 16, 21, 2, 5, 4, 8, 15, 19, 14, 18, 2, 6, 4, 7, 13, 19, 1, 6, 15, 21, 3, 12, 2, 14, 20, 22]),
      generate(width=22, height=20, rows=[7, 13], cols=[5, 14], lefts=[0, 2],
               rights=[3, 3], tops=[0, 1], bottoms=[3, 3],
               colors=[8, 8, 2, 3, 3, 3, 2, 2, 2],
               prows=[1, 1, 2, 2, 3, 3, 4, 9, 10, 10, 11, 12, 12, 15, 15, 15, 17, 17, 18, 18],
               pcols=[0, 9, 3, 18, 10, 15, 1, 19, 2, 8, 17, 1, 11, 3, 9, 18, 12, 20, 1, 17]),
  ]
  test = [
      generate(width=26, height=26, rows=[4, 12, 19, 21], cols=[7, 13, 18],
               lefts=[0, 1, 0, 3], rights=[4, 4, 1, 4], tops=[0, 1, 0],
               bottoms=[5, 2, 5],
               colors=[3, 8, 2, 2, 3, 3, 8, 4, 2, 4, 4, 3, 2, 3, 4, 3, 4],
               prows=[0, 0, 1, 1, 1, 2, 2, 2, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9, 9, 11, 14, 14, 14, 15, 15, 18, 18, 19, 20, 22, 22, 23, 24, 24, 24],
               pcols=[21, 25, 5, 10, 16, 2, 14, 23, 9, 15, 22, 2, 11, 16, 4, 24, 9, 15, 21, 1, 2, 4, 20, 12, 23, 20, 23, 10, 15, 0, 3, 13, 4, 22, 24]),
  ]
  return {"train": train, "test": test}
