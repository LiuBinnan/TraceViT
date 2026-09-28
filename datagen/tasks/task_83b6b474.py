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


def generate(outsize=None, insize=None, border=None, brows=None, bcols=None,
             colors=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    outsize: The size of the output grid.
    insize: The size of the input grid.
    border: The colors on the border.
    brows: The rows of the stamps.
    bcols: The columns of the stamps.
    colors: The colors of the stamps.
    bgcolor: The color of the background.
  """

  def check_legal():
    side = outsize - 1
    # Map colors to their positions in the output grid.
    rows, cols = {}, {}
    for i, color in enumerate(border):
      row, col = 0, 0
      if i >= 0 and i < side: row, col = 0, i
      if i >= side and i < 2 * side: row, col = i - side, outsize - 1
      if i >= 2 * side and i < 3 * side: row, col = outsize - 1, 3 * side - i
      if i >= 3 * side and i < 4 * side: row, col = 4 * side - i, 0
      rows.setdefault(color, []).append(row)
      cols.setdefault(color, []).append(col)
    # Check that at least two corners are preserved, and at most one of the
    # other three types of stamp.
    corner_colors = []
    vert_colors = []
    horiz_colors = []
    dot_colors = []
    for color in colors:
      if len(set(rows[color])) > 1 and len(set(cols[color])) > 1:
        corner_colors.append(color)
      if len(set(rows[color])) > 1 and len(set(cols[color])) == 1:
        vert_colors.append(color)
      if len(set(rows[color])) == 1 and len(set(cols[color])) > 1:
        horiz_colors.append(color)
      if len(set(rows[color])) == 1 and len(set(cols[color])) == 1:
        dot_colors.append(color)
    if len(corner_colors) < 2: return False
    if len(vert_colors) >= 2: return False
    if len(horiz_colors) >= 2: return False
    if len(dot_colors) >= 2: return False
    # Prevent the case where a dot lines up with a vert / horiz segment.
    for dot in dot_colors:
      for vert in vert_colors:
        if cols[dot][0] == cols[vert][0]: return False
      for horiz in horiz_colors:
        if rows[dot][0] == rows[horiz][0]: return False
    # As far as I know, the above checks are sufficient (but I may be wrong!)
    return True

  def sub_draw(thegrid, row_offset=0, col_offset=0, thecolor=-1):
    side = outsize - 1
    for i, color in enumerate(border):
      if thecolor != -1 and color != thecolor: continue
      row, col = 0, 0
      if i >= 0 and i < side: row, col = 0, i
      if i >= side and i < 2 * side: row, col = i - side, outsize - 1
      if i >= 2 * side and i < 3 * side: row, col = outsize - 1, 3 * side - i
      if i >= 3 * side and i < 4 * side: row, col = 4 * side - i, 0
      if row_offset + row < 0 or row_offset + row >= insize: return False
      if col_offset + col < 0 or col_offset + col >= insize: return False
      if thegrid[row_offset + row][col_offset + col] != bgcolor: return False
      thegrid[row_offset + row][col_offset + col] = color
    return True

  def draw():
    grid = common.grid(insize, insize, bgcolor)
    output = common.grid(outsize, outsize, bgcolor)
    sub_draw(output)
    for brow, bcol, color in zip(brows, bcols, colors):
      if not sub_draw(grid, brow, bcol, color): return None, None
    return grid, output

  if insize is None:
    base = common.randint(2, 4)
    outsize = 2 * base
    insize = 2 * (base + common.randint(1, base * (base + 1) // 2))
    # Six segments cannot satisfy check_legal() on the 4x4 frame, so retain
    # the original upper bound there and widen the larger frames only.
    segments = common.randint(4, 5 if outsize == 4 else 6)
    bgcolor = common.random_color()
    colors = common.random_colors(segments, exclude=[bgcolor])
    border_length = 4 * (outsize - 1)
    # First, find a border with a "deterministic" rearrangement.
    for _ in range(500):
      lengths = [common.randint(1, outsize + 1) for _ in range(segments)]
      if sum(lengths) != border_length: continue
      border = [-1] * border_length
      offset = common.randint(0, border_length - 1)
      for color, length in zip(colors, lengths):
        for _ in range(length):
          border[offset] = color
          offset = (offset + 1) % border_length
      if check_legal(): break
    else:
      # Exhaust the bounded compositions and offsets as a guaranteed finite
      # fallback.  Every yielded length is positive and at most outsize + 1,
      # exactly matching the random proposal space above.
      def length_compositions(total, count, prefix=()):
        if count == 0:
          if total == 0: yield prefix
          return
        lo = max(1, total - (count - 1) * (outsize + 1))
        hi = min(outsize + 1, total - (count - 1))
        for length in range(lo, hi + 1):
          yield from length_compositions(
              total - length, count - 1, prefix + (length,))

      found_border = False
      for lengths in length_compositions(border_length, segments):
        for offset in range(border_length):
          border = [-1] * border_length
          next_offset = offset
          for color, length in zip(colors, lengths):
            for _ in range(length):
              border[next_offset] = color
              next_offset = (next_offset + 1) % border_length
          if check_legal():
            found_border = True
            break
        if found_border: break
      if not found_border:
        raise RuntimeError("no legal border composition")
    # Second, find a positioning within the input grid that is contained and
    # non-overlapping.
    for _ in range(500):
      brows = [common.randint(-outsize, insize) for _ in range(segments)]
      bcols = [common.randint(-outsize, insize) for _ in range(segments)]
      grid, _ = draw()
      if grid: break
    else:
      # Build every contained translation of every fragment, then place the
      # most constrained fragments first with a small finite backtracking
      # search.  This preserves the same translated-piece geometry as draw().
      piece_pixels = {color: [] for color in colors}
      side = outsize - 1
      for i, color in enumerate(border):
        row, col = 0, 0
        if i >= 0 and i < side: row, col = 0, i
        if i >= side and i < 2 * side: row, col = i - side, outsize - 1
        if i >= 2 * side and i < 3 * side:
          row, col = outsize - 1, 3 * side - i
        if i >= 3 * side and i < 4 * side: row, col = 4 * side - i, 0
        piece_pixels[color].append((row, col))

      candidates = []
      for color in colors:
        pixels = piece_pixels[color]
        min_row = min(row for row, _ in pixels)
        max_row = max(row for row, _ in pixels)
        min_col = min(col for _, col in pixels)
        max_col = max(col for _, col in pixels)
        placements = []
        for brow in range(-min_row, insize - max_row):
          for bcol in range(-min_col, insize - max_col):
            placed = tuple((brow + row, bcol + col) for row, col in pixels)
            placements.append((brow, bcol, placed))
        candidates.append(placements)

      order = sorted(range(segments),
                     key=lambda i: (len(candidates[i]),
                                    -len(piece_pixels[colors[i]])))
      chosen = [None] * segments
      occupied = set()

      def place_remaining(pos):
        if pos == len(order): return True
        idx = order[pos]
        for brow, bcol, placed in candidates[idx]:
          if any(pixel in occupied for pixel in placed): continue
          chosen[idx] = (brow, bcol)
          occupied.update(placed)
          if place_remaining(pos + 1): return True
          occupied.difference_update(placed)
          chosen[idx] = None
        return False

      if not place_remaining(0):
        raise RuntimeError("no non-overlapping fragment placement")
      brows = [chosen[i][0] for i in range(segments)]
      bcols = [chosen[i][1] for i in range(segments)]

  grid, _ = draw()
  output = common.grid(outsize, outsize, bgcolor)

  def place_piece(i):
    """Sets one scattered color's segment onto its slot in the frame."""
    if i >= len(colors): return
    sub_draw(output, 0, 0, colors[i])

  place_piece(0)
  place_piece(1)
  place_piece(2)
  place_piece(3)
  place_piece(4)
  for i in range(5, len(colors)):
    place_piece(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(outsize=4, insize=6, border=[2, 2, 2, 2, 4, 1, 1, 1, 8, 8, 8, 8],
               brows=[1, 2, 2, 0], bcols=[2, -3, 1, 1], colors=[2, 4, 1, 8],
               bgcolor=9),
      generate(outsize=6, insize=16,
               border=[6, 6, 8, 8, 8, 8, 1, 1, 1, 9, 9, 9, 9, 9, 4, 4, 4, 4, 4, 6],
               brows=[8, 4, 0, 5, 9], bcols=[2, 4, 8, 8, 4],
               colors=[6, 8, 1, 9, 4], bgcolor=2),
  ]
  test = [
      generate(outsize=6, insize=8,
               border=[8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 4, 4],
               brows=[0, 1, 1, 3], bcols=[2, -4, 3, 5], colors=[8, 9, 1, 4],
               bgcolor=6),
  ]
  return {"train": train, "test": test}
