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


def generate(size=None, rows=None, cols=None, height=None, width=None,
             num_boxes=None, num_distractors=None, distractor_max=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    height: number of rows in the grid (widened synthesis path)
    width: number of columns in the grid (widened synthesis path)
    num_boxes: how many red 2x2 boxes to count (dice tally, capped at 5)
    num_distractors: how many non-red noise rectangles to scatter in
    distractor_max: maximum side length of a noise rectangle
  """
  if size is None:
    # Widened synthesis path: mirror re_arc's structural bands -- a larger
    # canvas, plus ignored non-red "noise" rectangles -- WITHOUT changing the
    # rule (only the red 2x2 boxes are counted into the dice tally).
    if height is None: height = common.randint(3, 30)
    if width is None: width = common.randint(3, 30)
    if num_boxes is None: num_boxes = common.randint(1, 5)
    num_boxes = min(5, num_boxes)  # the dice tally has exactly 5 cells
    if num_distractors is None:
      num_distractors = common.randint(0, 2 * num_boxes)
    if distractor_max is None: distractor_max = 3
    avail = set((r, c) for r in range(height) for c in range(width))
    boxes, red_cells = [], 0
    bh, bw = min(2, height), min(2, width)
    for _ in range(num_boxes):  # counted red boxes go down first
      for _ in range(10):
        r0 = common.randint(0, height - bh)
        c0 = common.randint(0, width - bw)
        cells = set((r0 + dr, c0 + dc) for dr in range(bh) for dc in range(bw))
        if cells <= avail:
          boxes.append((r0, c0, bh, bw, common.red()))
          red_cells += bh * bw
          for a, b in list(cells):
            for da, db in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
              cells.add((a + da, b + db))
          avail -= cells
          break
    if not boxes:  # degenerate tiny canvas: guarantee one counted box
      boxes = [(0, 0, bh, bw, common.red())]
      red_cells = bh * bw
    rows = [b[0] for b in boxes]
    cols = [b[1] for b in boxes]
    # Noise rectangles are ignored by the rule. Keep their total area under
    # half the non-red space so black stays the most common non-red color
    # (the color the transformation reads as background).
    budget = (height * width - red_cells) // 2
    dist_cells = 0
    for _ in range(num_distractors):
      dh = common.randint(1, min(distractor_max, height))
      dw = common.randint(1, min(distractor_max, width))
      color = common.random_color(
          exclude=[common.black(), common.blue(), common.red()])
      for _ in range(10):
        r0 = common.randint(0, height - dh)
        c0 = common.randint(0, width - dw)
        cells = set((r0 + dr, c0 + dc) for dr in range(dh) for dc in range(dw))
        if cells <= avail and dist_cells + dh * dw < budget:
          boxes.append((r0, c0, dh, dw, color))
          dist_cells += dh * dw
          for a, b in list(cells):
            for da, db in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
              cells.add((a + da, b + db))
          avail -= cells
          break
  else:
    height = width = size
    boxes = [(row, col, 2, 2, common.red()) for row, col in zip(rows, cols)]

  grid, output = common.grid(width, height), common.grid(3, 3)
  for r0, c0, bh, bw, color in boxes:
    for dr in range(bh):
      for dc in range(bw):
        grid[r0 + dr][c0 + dc] = color
  def mark_boxes():
    # Recolors every red box blue, in place.
    nonlocal output
    output = common.deepcopy(grid)
    for r in range(len(grid)):
      for c in range(len(grid[0])):
        if output[r][c] == common.red(): output[r][c] = common.blue()

  def count_box(idx):
    # Lights one tally cell for the idx-th counted box, dice-style.
    nonlocal output
    if idx >= len(rows): return
    if idx == 0: output = common.grid(3, 3)
    cells = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
    output[cells[idx][0]][cells[idx][1]] = common.blue()

  mark_boxes()
  count_box(0)
  count_box(1)
  count_box(2)
  count_box(3)
  count_box(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0], cols=[0]),
      generate(size=5, rows=[1, 3], cols=[1, 3]),
      generate(size=7, rows=[1, 2, 4], cols=[1, 4, 2]),
      generate(size=6, rows=[1, 4], cols=[1, 2]),
      generate(size=3, rows=[1], cols=[1]),
      generate(size=7, rows=[0, 2, 3, 5], cols=[4, 1, 4, 1]),
      generate(size=7, rows=[0, 1, 3, 4, 5], cols=[4, 1, 5, 0, 3]),
      generate(size=7, rows=[0, 0, 2, 3], cols=[2, 5, 0, 3]),
  ]
  test = [
      generate(size=6, rows=[0, 1, 3], cols=[3, 0, 2]),
      generate(size=7, rows=[1, 1, 3, 4], cols=[0, 3, 5, 2]),
      generate(size=7, rows=[0, 0, 2, 3, 5], cols=[0, 3, 5, 1, 4]),
  ]
  return {"train": train, "test": test}
