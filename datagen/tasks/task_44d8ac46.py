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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None,
             size=12, height=None, width=None, count=None, num_colors=None,
             bg_color=None, frame_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of digits representing box colors (black / red)
    size: the width and height of the (square) grid
    height: the number of grid rows (defaults to size)
    width: the number of grid columns (defaults to size)
    count: the number of primary boxes to place
    num_colors: the number of non-red frame colors to sample
    bg_color: the grid background color
    frame_colors: a list of digits representing box frame colors
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if bg_color is None:
      bg_options = [color for color in common.internal_colors if color != common.red()]
      bg_color = common.choice(bg_options)
    frame_options = [
        color for color in common.internal_colors
        if color not in [common.red(), bg_color]]
    if num_colors is None:
      num_colors = common.randint(1, min(6, len(frame_options)))
    frame_palette = common.sample(frame_options, min(num_colors, len(frame_options)))
    num_boxes = common.randint(1, 10) if count is None else count
    # First, choose nonoverlapping positions.
    rows, cols, wides, talls = [], [], [], []
    max_trials, trials = 4 * num_boxes, 0
    while len(rows) < num_boxes and trials <= max_trials:
      trials += 1
      wide = common.randint(5, min(7, width))
      tall = common.randint(5, min(7, height))
      candidates = []
      for row in range(height - tall + 1):
        for col in range(width - wide + 1):
          if not common.overlaps(rows + [row], cols + [col],
                                 wides + [wide], talls + [tall], 1):
            candidates.append((row, col))
      if not candidates:
        continue
      row, col = common.choice(candidates)
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
    # Then, decide whether to manipulate the boxes, and settle on colors.
    num_boxes = len(rows)
    if num_boxes:
      dim = min(wides[0], talls[0])
      wides[0], talls[0] = dim, dim
    colors = [bg_color] * num_boxes
    frame_colors = [common.choice(frame_palette) for _ in range(num_boxes)]
    for i in range(num_boxes):
      wide, tall = wides[i], talls[i]
      if i == 0:
        colors[i] = common.red()
        continue
      # Plain square holes become red; rectangular holes remain background.
      if wide == tall:
        colors[i] = common.red()

  grid = common.grid(width, height, common.black() if bg_color is None else bg_color)
  base = common.grid(width, height, common.black() if bg_color is None else bg_color)
  output = common.grid(width, height, common.black() if bg_color is None else bg_color)
  for idx, (row, col, wide, tall, color) in enumerate(zip(rows, cols, wides, talls, colors)):
    frame_color = common.gray() if frame_colors is None else frame_colors[idx]
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        base[r][c] = grid[r][c] = frame_color
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        grid[r][c] = common.black() if bg_color is None else bg_color
        base[r][c] = common.black() if bg_color is None else bg_color

  def fill_area(target, idx):
    row, col, wide, tall, color = rows[idx], cols[idx], wides[idx], talls[idx], colors[idx]
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        frame_values = [common.gray()] if frame_colors is None else frame_colors
        if target[r][c] not in frame_values:
          target[r][c] = color

  active_boxes, probe = [], [row[:] for row in base]
  for idx in range(len(rows)):
    before = [row[:] for row in probe]
    fill_area(probe, idx)
    if probe != before:
      active_boxes.append(idx)

  started = False

  def fill_box(idx):
    nonlocal output, started
    if not started:
      output = [row[:] for row in base]
      started = True
    if not active_boxes:
      return
    if idx >= len(active_boxes):
      return
    fill_area(output, active_boxes[idx])

  fill_box(0)
  fill_box(1)
  fill_box(2)
  fill_box(3)
  fill_box(4)
  fill_box(5)
  fill_box(6)
  fill_box(7)
  fill_box(8)
  fill_box(9)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 4, 4, 8, 9], cols=[1, 7, 9, 2, 2],
               wides=[4, 4, 2, 4, 3], talls=[4, 4, 2, 4, 3],
               colors=[2, 0, 0, 0, 2]),
      generate(rows=[1, 1, 3, 7, 8], cols=[1, 2, 6, 0, 0],
               wides=[4, 3, 6, 5, 4], talls=[4, 3, 6, 5, 4],
               colors=[0, 2, 2, 0, 2]),
      generate(rows=[1, 3, 8], cols=[1, 7, 3], wides=[5, 4, 6], talls=[6, 4, 4],
               colors=[0, 2, 0]),
      generate(rows=[1, 3, 6, 6], cols=[1, 1, 3, 6], wides=[4, 4, 5, 2],
               talls=[4, 2, 5, 3], colors=[0, 0, 0, 0]),
  ]
  test = [
      generate(rows=[1, 1, 1, 8], cols=[0, 7, 7, 2], wides=[5, 4, 2, 6],
               talls=[5, 5, 2, 4], colors=[2, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
