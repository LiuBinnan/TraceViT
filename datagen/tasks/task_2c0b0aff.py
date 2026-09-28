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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, colors=None, canvas_width=None, canvas_height=None,
             num_boxes=None, max_pluses=None, dust_count=None,
             max_rect_size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the output grid.
    tall: The height of the output grid.
    brow: The row of the desired box.
    bcol: The column of the desired box.
    colors: The colors of the pixels.
    canvas_width: The sampled width of a generated input grid.
    canvas_height: The sampled height of a generated input grid.
    num_boxes: The number of rectangles to compare.
    max_pluses: The largest marker count available to a rectangle.
    dust_count: The number of distractor pixels requested per rectangle.
    max_rect_size: The largest sampled rectangle dimension.
  """

  if width is None:
    if canvas_width is None:
      canvas_width = common.randint(18, 24)
    if canvas_height is None:
      canvas_height = common.randint(18, 24)
    if num_boxes is None:
      num_boxes = common.randint(3, 4)
    if max_pluses is None:
      max_pluses = 4
    if dust_count is None:
      dust_count = 7
    if max_rect_size is None:
      max_rect_size = 11
    width, height = canvas_width, canvas_height
    # Four comparison handlers are unrolled below, so never generate more.
    boxes = min(num_boxes, 4)
    counts = sorted(common.sample(list(range(1, max_pluses + 1)), boxes))

    # Construct separated placement slots instead of relying on an unbounded
    # whole-instance rejection loop.  Two boxes use broad strips; three or four
    # use a subset of four quadrants, with a one-cell black separator.
    if boxes == 2:
      if common.randint(0, 1):
        split = (width - 1) // 2
        slots = [(0, 0, height, split),
                 (0, split + 1, height, width - split - 1)]
      else:
        split = (height - 1) // 2
        slots = [(0, 0, split, width),
                 (split + 1, 0, height - split - 1, width)]
    else:
      row_split = (height - 1) // 2
      col_split = (width - 1) // 2
      slots = [
          (0, 0, row_split, col_split),
          (0, col_split + 1, row_split, width - col_split - 1),
          (row_split + 1, 0, height - row_split - 1, col_split),
          (row_split + 1, col_split + 1,
           height - row_split - 1, width - col_split - 1),
      ]
      if boxes < 4:
        slots = common.sample(slots, boxes)

    # Pair the highest counts with the roomiest slots.  The random shuffle
    # preserves positional variety when multiple slots have equal capacity.
    slots = common.sample(slots, len(slots))
    slots.sort(key=lambda slot: ((min(max_rect_size, slot[2]) // 3) *
                                 (min(max_rect_size, slot[3]) // 3)))
    wides, talls, brows, bcols = [], [], [], []
    for count, (srow, scol, sheight, swidth) in zip(counts, slots):
      shapes = [
          (w, t)
          for t in range(7, min(max_rect_size, sheight) + 1)
          for w in range(7, min(max_rect_size, swidth) + 1)
          if (t // 3) * (w // 3) >= count
      ]
      w, t = common.sample(shapes, 1)[0]
      wides.append(w)
      talls.append(t)
      brows.append(srow + common.randint(0, sheight - t))
      bcols.append(scol + common.randint(0, swidth - w))

    grid = common.grid(width, height)
    for w, t, brow, bcol in zip(wides, talls, brows, bcols):
      common.rect(grid, w, t, brow, bcol, 8)

    def patch_plus_count(patch):
      """Counts complete pluses while safely adding local distractors."""
      return sum(
          all(patch[row + dr][col + dc] == 3
              for dr, dc in ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)))
          for row in range(len(patch) - 2)
          for col in range(len(patch[0]) - 2))

    prows, pcols, plengths = [], [], []
    for count, w, t, brow, bcol in zip(counts, wides, talls, brows, bcols):
      row_offset = common.randint(0, t - 3 * (t // 3))
      col_offset = common.randint(0, w - 3 * (w // 3))
      marker_cells = [
          (row_offset + row, col_offset + col)
          for row in range(0, 3 * (t // 3), 3)
          for col in range(0, 3 * (w // 3), 3)
      ]
      markers = common.sample(marker_cells, count)
      for row, col in markers:
        prows.append(brow + row)
        pcols.append(bcol + col)
        plengths.append(3)

      patch = common.grid(w, t, 8)
      blocked = set()
      for row, col in markers:
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)):
          patch[row + dr][col + dc] = 3
        for dr in range(3):
          for dc in range(3):
            blocked.add((row + dr, col + dc))
      candidates = [(row, col) for row in range(t) for col in range(w)
                    if (row, col) not in blocked]
      candidates = common.sample(candidates, len(candidates))
      added = 0
      for row, col in candidates:
        if added >= dust_count:
          break
        patch[row][col] = 3
        if patch_plus_count(patch) != count:
          patch[row][col] = 8
          continue
        prows.append(brow + row)
        pcols.append(bcol + col)
        plengths.append(1)
        added += 1
    for prow, pcol, length in zip(prows, pcols, plengths):
      if length == 1:
        grid[prow][pcol] = 3
      else:
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
          grid[prow + dr][pcol + dc] = 3
    brow, bcol, wide, tall = brows[-1], bcols[-1], wides[-1], talls[-1]
    colors = common.flatten(grid)

  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color

  def find_rectangles():
    """Finds the non-background rectangular objects in reading order."""
    seen = set()
    rectangles = []
    for row in range(height):
      for col in range(width):
        if grid[row][col] == common.black() or (row, col) in seen:
          continue
        pending = [(row, col)]
        pixels = []
        seen.add((row, col))
        while pending:
          pixel = pending.pop()
          pixels.append(pixel)
          for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = (pixel[0] + dr, pixel[1] + dc)
            if not (0 <= neighbor[0] < height and
                    0 <= neighbor[1] < width):
              continue
            if (neighbor in seen or
                grid[neighbor[0]][neighbor[1]] == common.black()):
              continue
            seen.add(neighbor)
            pending.append(neighbor)
        top = min(pixel[0] for pixel in pixels)
        bottom = max(pixel[0] for pixel in pixels) + 1
        left = min(pixel[1] for pixel in pixels)
        right = max(pixel[1] for pixel in pixels) + 1
        rectangles.append((top, left, bottom - top, right - left))
    return rectangles

  def count_pluses(rectangle):
    """Counts complete green plus markers inside a rectangle."""
    top, left, rect_height, rect_width = rectangle
    plus = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
    count = 0
    for row in range(top, top + rect_height - 2):
      for col in range(left, left + rect_width - 2):
        if all(grid[row + dr][col + dc] == common.green()
               for dr, dc in plus):
          count += 1
    return count

  rectangles = find_rectangles()
  target = (brow, bcol, tall, wide)
  rectangles.sort(
      key=lambda rectangle: (rectangle == target, count_pluses(rectangle)))
  output = common.grid(wide, tall)

  def consider_rectangle(index):
    """Shows the next rectangle while comparing marker counts."""
    nonlocal output
    if index >= len(rectangles):
      return
    top, left, rect_height, rect_width = rectangles[index]
    output = [row[left:left + rect_width]
              for row in grid[top:top + rect_height]]

  consider_rectangle(0)
  consider_rectangle(1)
  consider_rectangle(2)
  consider_rectangle(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=24, wide=8, tall=8, brow=3, bcol=12,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 8, 8, 3, 8, 8, 3, 8, 8, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 8, 8, 8, 8, 0, 0, 8, 3, 3, 3, 8, 8, 3, 8, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 3, 8, 8, 8, 3, 0, 0, 8, 8, 3, 8, 8, 3, 3, 3, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 3, 8, 8, 3, 0, 0, 8, 8, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 3, 8, 8, 8, 8, 0, 0, 3, 8, 8, 8, 3, 8, 8, 3, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 8, 8, 8, 3, 3, 3, 8, 8, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 8, 8, 8, 8, 0, 0, 8, 3, 8, 8, 3, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 8, 8, 8, 8, 8, 8, 3, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=24, height=24, wide=9, tall=8, brow=12, bcol=1,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 8, 8, 3, 8, 8, 8, 3, 8, 0, 0, 3, 8, 8, 8, 3, 8, 8, 8, 3, 8, 0, 0,
                       0, 8, 8, 3, 3, 3, 8, 8, 8, 3, 0, 0, 8, 8, 3, 8, 8, 8, 8, 3, 3, 3, 0, 0,
                       0, 8, 8, 8, 3, 8, 8, 8, 8, 8, 0, 0, 8, 3, 3, 3, 8, 8, 8, 8, 3, 8, 0, 0,
                       0, 8, 3, 8, 8, 8, 8, 3, 8, 8, 0, 0, 8, 8, 3, 8, 3, 8, 3, 8, 8, 8, 0, 0,
                       0, 8, 8, 8, 3, 8, 3, 3, 3, 8, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 3, 3, 0, 0,
                       0, 3, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 8, 3, 8, 3, 8, 8, 3, 8, 8, 8, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 8, 3, 8, 0, 0, 8, 8, 8, 8, 8, 3, 3, 3, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 3, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 3, 3, 3, 8, 8, 3, 3, 3, 0, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 8, 3, 8, 0, 8, 8, 8, 3, 8, 8, 8, 8, 3, 3, 8, 0, 0,
                       0, 3, 8, 8, 8, 3, 8, 8, 8, 8, 0, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 0, 0,
                       0, 8, 3, 8, 8, 8, 8, 3, 8, 3, 0, 8, 8, 8, 3, 8, 8, 8, 3, 8, 8, 3, 0, 0,
                       0, 3, 3, 3, 8, 8, 3, 3, 3, 8, 0, 3, 8, 8, 8, 8, 8, 3, 3, 3, 8, 8, 0, 0,
                       0, 8, 3, 8, 8, 8, 8, 3, 8, 8, 0, 8, 8, 3, 8, 3, 8, 8, 3, 8, 8, 8, 0, 0,
                       0, 8, 8, 8, 8, 3, 8, 8, 8, 8, 0, 8, 3, 3, 3, 8, 8, 8, 8, 8, 3, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 8, 3, 3, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=20, height=22, wide=11, tall=8, brow=11, bcol=2,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 8, 3, 8, 0, 0, 0, 3, 8, 8, 3, 8, 8, 3, 8,
                       0, 0, 3, 3, 3, 8, 3, 3, 3, 0, 0, 0, 8, 8, 3, 8, 8, 3, 3, 3,
                       0, 0, 8, 3, 8, 8, 8, 3, 8, 0, 0, 0, 8, 3, 3, 3, 8, 8, 3, 8,
                       0, 0, 8, 8, 8, 3, 8, 8, 8, 0, 0, 0, 8, 8, 3, 8, 8, 8, 8, 8,
                       0, 0, 8, 3, 8, 8, 8, 8, 8, 0, 0, 0, 3, 8, 8, 8, 8, 3, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 3, 3, 3, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 3, 8, 8, 3, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 8, 8, 8, 8, 8, 3,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 3, 8, 8, 3, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 3, 8, 8, 8, 3, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 3, 8, 8, 8, 3, 3, 3, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 3, 3, 8, 8, 3, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 3, 3, 3, 8, 8, 3, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=23, height=23, wide=8, tall=7, brow=11, bcol=11,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 3, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 8, 8, 8, 3, 8, 0, 0, 0, 8, 8, 3, 3, 8, 8, 8, 0, 0, 0,
                       0, 0, 8, 3, 3, 3, 8, 3, 3, 3, 0, 0, 0, 3, 8, 8, 8, 8, 8, 3, 0, 0, 0,
                       0, 0, 8, 8, 3, 8, 8, 8, 3, 8, 0, 0, 0, 8, 8, 8, 3, 8, 8, 8, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 3, 8, 8, 8, 0, 0, 0, 8, 8, 3, 3, 3, 8, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 3, 8, 8, 8, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 8, 8, 8, 8, 8, 0, 0, 0,
                       0, 8, 3, 8, 8, 8, 8, 8, 3, 8, 0, 0, 0, 8, 8, 8, 8, 3, 8, 8, 0, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 3, 3, 3, 8, 3, 8, 3, 8, 0, 8, 3, 8, 8, 8, 8, 8, 3, 0, 0, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 8, 8, 8, 0, 3, 3, 3, 8, 8, 3, 8, 8, 0, 0, 0, 0,
                       0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 8, 3, 8, 8, 3, 3, 3, 8, 0, 0, 0, 0,
                       0, 8, 3, 8, 8, 8, 3, 8, 8, 8, 0, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 0, 0,
                       0, 8, 8, 8, 8, 3, 3, 3, 8, 8, 0, 8, 3, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0,
                       0, 8, 3, 8, 8, 8, 3, 8, 3, 8, 0, 3, 3, 3, 8, 8, 3, 3, 3, 0, 0, 0, 0,
                       0, 3, 8, 8, 8, 8, 8, 8, 8, 3, 0, 8, 3, 8, 8, 8, 8, 3, 8, 0, 0, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 3, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=23, height=22, wide=10, tall=8, brow=12, bcol=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 8, 3, 8, 8, 8, 3, 8, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 8, 3, 3, 3, 8, 8, 8, 3, 3, 3, 0, 0, 8, 8, 8, 8, 8, 8, 3, 3, 8, 8,
                       0, 8, 8, 3, 8, 8, 8, 8, 8, 3, 8, 0, 0, 3, 8, 8, 3, 8, 8, 8, 8, 8, 8,
                       0, 8, 3, 8, 8, 8, 3, 8, 3, 8, 8, 0, 0, 8, 8, 3, 3, 3, 8, 8, 8, 3, 8,
                       0, 8, 8, 8, 8, 3, 3, 3, 8, 8, 3, 0, 0, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8,
                       0, 3, 3, 8, 8, 8, 3, 8, 8, 8, 8, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 8, 8, 8, 8, 8, 8, 8, 8, 3, 8, 0, 0, 8, 8, 8, 3, 8, 8, 3, 8, 8, 8,
                       0, 3, 8, 8, 3, 8, 8, 8, 3, 8, 8, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 8, 8, 8, 8, 8, 8, 3, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       3, 8, 8, 8, 8, 8, 3, 8, 8, 8, 0, 0, 3, 3, 8, 8, 3, 8, 8, 8, 3, 8, 0,
                       8, 8, 3, 8, 8, 3, 3, 3, 8, 8, 0, 0, 8, 8, 8, 3, 3, 3, 8, 8, 8, 3, 0,
                       8, 3, 3, 3, 8, 8, 3, 8, 3, 8, 0, 0, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8, 0,
                       8, 8, 3, 8, 8, 8, 8, 3, 3, 3, 0, 0, 8, 3, 8, 8, 8, 8, 8, 3, 8, 8, 0,
                       8, 8, 8, 8, 3, 8, 8, 8, 3, 8, 0, 0, 3, 3, 3, 8, 8, 8, 3, 3, 3, 8, 0,
                       8, 3, 8, 3, 3, 3, 8, 8, 8, 8, 0, 0, 8, 3, 8, 3, 8, 8, 8, 3, 8, 8, 0,
                       3, 3, 3, 8, 3, 8, 8, 8, 8, 3, 0, 0, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 0,
                       8, 3, 8, 8, 8, 8, 8, 3, 8, 8, 0, 0, 8, 8, 8, 3, 8, 8, 8, 3, 8, 3, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
