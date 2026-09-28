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


def generate(rows=None, cols=None, angles=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the lines.
    cols: The columns of the lines.
    angles: The angles of the lines.
    colors: The colors of the lines.
    gsize: The side length of the square input grid.
  """

  def draw_input():
    side = gsize if gsize is not None else 16
    grid = common.grid(side, side, 7)
    for row, col, angle, color in zip(rows, cols, angles, colors):
      r, c, is_horiz = row, col, row == side - 1
      while r < side:
        # First, check that there are no other lines below.
        if not is_horiz:
          for rr in range(r, side):
            if grid[rr][c] != 7: return None
        # Second, draw the next pixel, and adjust its position.
        common.draw(grid, r, c, color)
        r, c = (r + 1) if not is_horiz else r, c + angle
        if c < 0 or c >= side: break
        if is_horiz and (c < 1 or c >= side - 1): break
    return grid

  def draw_summary_bar(canvas, index, color):
    row = index + 5 - len(rows)
    for col in range(3):
      canvas[row][col] = color

  if rows is None:
    if gsize is None:
      gsize = common.randint(14, 26)
    num_diags = common.randint(3, 4)
    extra_line = common.randint(0, 1)
    while True:
      rows = sorted(common.sample(list(range(1, gsize - 3)), num_diags))
      cols = [common.randint(3, gsize - 3) for _ in range(num_diags)]
      angles = [2 * common.randint(0, 1) - 1 for _ in range(num_diags)]
      if extra_line:
        rows.append(gsize - 1)
        cols.append(common.randint(3 * gsize // 8, 5 * gsize // 8))
        angles.append(2 * common.randint(0, 1) - 1)
      colors = common.sample([1, 2, 3, 4, 5, 6, 8, 9], len(rows))
      grid = draw_input()
      if grid: break

  grid = draw_input()
  output = common.grid(3, 5, 7)
  split = max(1, len(colors) // 2)
  for i, color in enumerate(colors[:split]):
    draw_summary_bar(output, i, color)
  for i, color in enumerate(colors[split:], start=split):
    draw_summary_bar(output, i, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[5, 10, 12, 15], cols=[5, 6, 6, 10], angles=[1, 1, -1, -1],
               colors=[3, 9, 1, 4]),
      generate(rows=[3, 8, 11], cols=[6, 8, 7], angles=[1, -1, 1],
               colors=[1, 8, 2]),
      generate(rows=[2, 8, 11, 12, 15], cols=[3, 5, 6, 6, 15],
               angles=[1, 1, -1, 1, -1], colors=[4, 9, 1, 3, 8]),
  ]
  test = [
      generate(rows=[6, 10, 11, 15], cols=[10, 8, 6, 3], angles=[-1, 1, 1, 1],
               colors=[5, 1, 4, 3]),
  ]
  return {"train": train, "test": test}
