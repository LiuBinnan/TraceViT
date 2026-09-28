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


def generate(size=None, brows=None, bcols=None, angles=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The row of each box.
    bcols: The column of each box.
    angles: The angles of each box.
    colors: The colors of each box.
  """

  if size is None:
    size = 4 * common.randint(2, 6)
    num_boxes = common.randint(max(3, size * size // 32), size * size // 16)
    attempts = 0
    while True:
      brows = [common.randint(0, size - 2) for _ in range(num_boxes)]
      bcols = [common.randint(0, size - 2) for _ in range(num_boxes)]
      if not common.overlaps(brows, bcols, [2] * num_boxes, [2] * num_boxes, 1):
        break
      attempts += 1
      if attempts >= 32:
        # A shuffled 3-spaced lattice guarantees enough non-overlapping slots
        # for the area-scaled count while avoiding an unbounded dense-packing
        # rejection loop. Random offsets keep boxes away from a fixed origin.
        row_offset = common.randint(0, 2)
        col_offset = common.randint(0, 2)
        positions = common.shuffle([
            (row, col)
            for row in range(row_offset, size - 1, 3)
            for col in range(col_offset, size - 1, 3)
        ])
        brows = [row for row, _ in positions[:num_boxes]]
        bcols = [col for _, col in positions[:num_boxes]]
        break
    angles = [common.randint(0, 3) for _ in range(num_boxes)]
    colors = [2 if common.randint(0, 1) else 5 for _ in range(num_boxes)]

  grid = common.grid(size, size, common.orange())
  for target in [5, 2]:
    for brow, bcol, angle, color in zip(brows, bcols, angles, colors):
      if color != target: continue
      row, col, hue = brow, bcol, color
      if angle != 0: common.draw(grid, row, col, hue)
      if angle != 1: common.draw(grid, row, col + 1, hue)
      if angle != 2: common.draw(grid, row + 1, col, hue)
      if angle != 3: common.draw(grid, row + 1, col + 1, hue)
  output = common.deepcopy(grid)

  def draw_box(canvas, row, col, angle, hue):
    """Draws an L-shaped box with the specified missing corner."""
    if angle != 0: common.draw(canvas, row, col, hue)
    if angle != 1: common.draw(canvas, row, col + 1, hue)
    if angle != 2: common.draw(canvas, row + 1, col, hue)
    if angle != 3: common.draw(canvas, row + 1, col + 1, hue)

  def extend_color(target):
    """Extends every box of one color in its color-specific direction."""
    hue = common.yellow() if target == common.gray() else common.green()
    cdir = 1 if target == common.gray() else -1
    for brow, bcol, angle, color in zip(brows, bcols, angles, colors):
      if color != target: continue
      draw_box(output, brow, bcol, angle, color)
      row, col = brow, bcol
      if angle == 0: row, col = row - cdir, col - cdir
      if angle == 1: row, col = row - cdir, col + cdir
      if angle == 2: row, col = row + cdir, col - cdir
      if angle == 3: row, col = row + cdir, col + cdir
      draw_box(output, row, col, angle, hue)
    if target == common.gray():
      for brow, bcol, angle, color in zip(brows, bcols, angles, colors):
        if color == common.red():
          draw_box(output, brow, bcol, angle, color)

  extend_color(common.gray())
  extend_color(common.red())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, brows=[1, 2, 6], bcols=[4, 1, 4], angles=[1, 1, 0],
               colors=[2, 5, 2]),
      generate(size=8, brows=[1, 1, 5, 5], bcols=[1, 5, 1, 5],
               angles=[1, 2, 2, 1], colors=[5, 5, 2, 2]),
  ]
  test = [
      generate(size=16,
               brows=[1, 2, 2, 3, 5, 6, 6, 8, 9, 9, 10, 11, 12, 13, 13, 14],
               bcols=[1, 8, 11, 5, 12, 3, 6, 11, 5, 9, 2, 13, 9, 2, 5, 12],
               angles=[1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1],
               colors=[5, 2, 5, 5, 2, 5, 5, 2, 2, 2, 5, 2, 5, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
