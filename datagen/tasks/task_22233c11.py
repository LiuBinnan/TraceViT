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


def _sample_boxes(width, height, count, num_colors, background):
  """Samples non-overlapping ARC 22233c11 motifs."""
  if count is None:
    count = common.randint(1, max(1, width * height // 10))
  if num_colors is None:
    num_colors = common.randint(1, 8)
  if background is None:
    background = common.choice([color for color in range(10) if color != 8])
  palette = [color for color in range(10) if color not in [background, 8]]
  palette = common.shuffle(common.sample(palette, min(num_colors, len(palette))))
  rows, cols, flips, magnifies, colors = [], [], [], [], []
  occupied = set()
  max_magnify = max(1, min(3, height // 4, width // 4))
  for _ in range(count):
    candidates = []
    for box_magnify in common.shuffle(list(range(1, max_magnify + 1))):
      for row in range(box_magnify, height - 3 * box_magnify + 1):
        for col in range(box_magnify, width - 3 * box_magnify + 1):
          box = set()
          for r in range(row - box_magnify, row + 3 * box_magnify):
            for c in range(col - box_magnify, col + 3 * box_magnify):
              box.add((r, c))
          margin = set(box)
          for r, c in box:
            for dr in [-1, 0, 1]:
              for dc in [-1, 0, 1]:
                margin.add((r + dr, c + dc))
          if occupied & margin:
            continue
          candidates.append((row, col, box_magnify, margin))
    if not candidates:
      break
    row, col, box_magnify, margin = common.choice(candidates)
    color = palette[len(rows) % len(palette)]
    rows.append(row)
    cols.append(col)
    flips.append(common.randint(0, 1))
    magnifies.append(box_magnify)
    colors.append(color)
    occupied |= margin
  return rows, cols, flips, magnifies, colors, background


def generate(rows=None, cols=None, flips=None, magnify=None, size=10,
             height=None, width=None, count=None, num_colors=None,
             background=None, magnifies=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flips: a list of 0 or 1 values (should the boxes be flipped?)
    magnify: how much the boxes should be enlarged
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: how many boxes should be attempted
    num_colors: how many box colors should be sampled
    background: the background color
    magnifies: a list of per-box magnification factors
    colors: a list of per-box colors
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    rows, cols, flips, magnifies, colors, background = _sample_boxes(
        width, height, count, num_colors, background)

  grid, output = common.grids(width, height, background if background is not None else 0)
  def draw_box(r, col, flip, box_magnify, color):
    for dr in range(box_magnify):
      for dc in range(box_magnify):
        c0 = col - box_magnify if flip else col + 2 * box_magnify
        c1 = col + box_magnify if flip else col
        c2 = col if flip else col + box_magnify
        c3 = col + 2 * box_magnify if flip else col - box_magnify
        common.draw(grid, r + dr, c1 + dc, color)
        common.draw(grid, r + dr + box_magnify, c2 + dc, color)
        common.draw(output, r + dr, c1 + dc, color)
        common.draw(output, r + dr + box_magnify, c2 + dc, color)
        common.draw(output, r + dr - box_magnify, c0 + dc, common.cyan())
        common.draw(output, r + dr + 2 * box_magnify, c3 + dc, common.cyan())

  boxes = list(zip(rows, cols, flips, magnifies or [magnify] * len(rows),
                   colors or [common.green()] * len(rows)))
  for r, col, flip, box_magnify, color in boxes[:1]:
    draw_box(r, col, flip, box_magnify, color)
  for r, col, flip, box_magnify, color in boxes[1:]:
    draw_box(r, col, flip, box_magnify, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 6], cols=[2, 6], flips=[0, 1], magnify=1),
      generate(rows=[3], cols=[1], flips=[1], magnify=2),
      generate(rows=[3], cols=[3], flips=[0], magnify=1),
  ]
  test = [
      generate(rows=[2], cols=[3], flips=[1], magnify=3),
  ]
  return {"train": train, "test": test}
