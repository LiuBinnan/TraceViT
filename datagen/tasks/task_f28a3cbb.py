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


def generate(rows=None, cols=None, colors=None, pair=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
    pair: The pair of colors.
    gsize: The height and width of the square grid.
  """

  def draw():
    grid, output = common.grids(gsize, gsize, 6)
    common.rect(grid, 3, 3, 0, 0, pair[0])
    common.rect(output, 3, 3, 0, 0, pair[0])
    common.rect(grid, 3, 3, gsize - 3, gsize - 3, pair[1])
    common.rect(output, 3, 3, gsize - 3, gsize - 3, pair[1])
    for row, col, color in zip(rows, cols, colors):
      r, c = row, col
      if grid[r][c] != 6: return None, None
      grid[r][c] = color
      if color == pair[0] and r > 3: r, c = 3, min(c, 2)
      if color == pair[0] and c > 3: r, c = min(r, 2), 3
      if color == pair[1] and r < gsize - 4:
        r, c = gsize - 4, max(c, gsize - 3)
      if color == pair[1] and c < gsize - 4:
        r, c = max(r, gsize - 3), gsize - 4
      output[r][c] = color
    return grid, output

  if rows is None:
    if gsize is None:
      gsize = common.randint(9, 16)
    pair = common.random_colors(2, exclude=[6])
    while True:
      top_rows = common.sample([0, 1, 2], common.randint(1, 3))
      lef_cols = common.sample([0, 1, 2], common.randint(1, 3))
      rit_cols = common.sample(
          list(range(gsize - 3, gsize)), common.randint(1, 3))
      bot_rows = common.sample(
          list(range(gsize - 3, gsize)), common.randint(1, 3))
      top_cols = [common.randint(gsize // 2, gsize - 1) for _ in top_rows]
      lef_rows = [common.randint(gsize // 2, gsize - 1) for _ in lef_cols]
      rit_rows = [common.randint(0, gsize // 2) for _ in rit_cols]
      bot_cols = [common.randint(0, gsize // 2) for _ in bot_rows]
      rows = top_rows + lef_rows + rit_rows + bot_rows
      cols = top_cols + lef_cols + rit_cols + bot_cols
      colors = [pair[0]] * len(top_rows + lef_cols) + [pair[1]] * len(rit_cols + bot_rows)
      # Now, we sometimes (?) shift things a bit for some reason.
      for i in range(len(colors)):
        if common.randint(0, 1): continue
        if colors[i] == pair[0] and rows[i] == 2: rows[i] = 3
        if colors[i] == pair[0] and cols[i] == 2: cols[i] = 3
        if colors[i] == pair[1] and rows[i] == gsize - 3:
          rows[i] = gsize - 4
        if colors[i] == pair[1] and cols[i] == gsize - 3:
          cols[i] = gsize - 4
      grid, _ = draw()
      if grid: break
  elif gsize is None:
    gsize = 9

  # Build the input grid (two corner blocks plus the scattered specks).
  grid, _ = draw()

  # Build the output forward: each corner block is a magnet that pulls its
  # matching specks in until they hug the block's inner frame. One frame per
  # magnet/color, in solving order (top-left block first, then bottom-right).
  output = common.grid(gsize, gsize, 6)

  def gather(corner_row, corner_col, color):
    """Draws the block, then pulls its matching specks onto the block's frame."""
    common.rect(output, 3, 3, corner_row, corner_col, color)
    for row, col, c in zip(rows, cols, colors):
      if c != color: continue
      r, cc = row, col
      if color == pair[0] and r > 3: r, cc = 3, min(cc, 2)
      if color == pair[0] and cc > 3: r, cc = min(r, 2), 3
      if color == pair[1] and r < gsize - 4:
        r, cc = gsize - 4, max(cc, gsize - 3)
      if color == pair[1] and cc < gsize - 4:
        r, cc = max(r, gsize - 3), gsize - 4
      output[r][cc] = color

  gather(0, 0, pair[0])
  gather(gsize - 3, gsize - 3, pair[1])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 4, 5, 6, 7, 8], cols=[7, 8, 6, 7, 5, 2, 1, 0, 2, 3], colors=[9, 4, 4, 4, 9, 9, 9, 9, 4, 4], pair=[9, 4]),
      generate(rows=[0, 1, 3, 4, 4, 5, 7, 8], cols=[8, 8, 4, 1, 7, 4, 0, 2], colors=[2, 2, 2, 2, 5, 5, 5, 2], pair=[2, 5]),
  ]
  test = [
      generate(rows=[0, 1, 3, 3, 3, 5, 5, 7, 8], cols=[6, 4, 6, 7, 8, 1, 4, 1, 3], colors=[3, 3, 8, 8, 8, 3, 8, 8, 8], pair=[3, 8]),
  ]
  return {"train": train, "test": test}
