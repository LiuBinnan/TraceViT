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


def generate(colors=None, width=None, height=None, row=None, col=None,
             wide=None, tall=None, size=17, gh=None, gw=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of colors to be used for pixels
    width: the width of the repeating color tile
    height: the height of the repeating color tile
    row: the row of the sky blue rectangle
    col: the column of the sky blue rectangle
    wide: the width of the sky blue rectangle
    tall: the height of the sky blue rectangle
    size: the width and height of the (square) grid
    gh: the height (rows) of the grid; defaults to size
    gw: the width (cols) of the grid; defaults to size
  """
  if gh is None: gh = size
  if gw is None: gw = size

  def draw(grid, output):
    for r in range(gh):
      for c in range(gw):
        output[r][c] = grid[r][c] = colors[(r % height) * width + c % width]
    for r in range(tall):
      for c in range(wide):
        if grid[row + r][col + c] != common.blue():
          grid[row + r][col + c] = common.cyan()
        if output[row + r][col + c] == common.blue():
          output[row + r][col + c] = common.green()
        else:
          output[row + r][col + c] = common.cyan()
    # Check that each row / column of the rectangle is visible.
    for r in range(tall):
      visible = False
      for c in range(wide):
        if grid[row + r][col + c] == common.cyan(): visible = True
      if not visible: return False
    for c in range(wide):
      visible = False
      for r in range(tall):
        if grid[row + r][col + c] == common.cyan(): visible = True
      if not visible: return False
    return True

  if colors is None:
    if common.randint(0, 3) == 0:  # totally randomize the whole grid
      width, height = gw, gh
    else:
      width, height = common.randint(2, 4), common.randint(2, 4)
    while True:
      pixels, area = common.all_pixels(width, height), width * height
      pixels = common.sample(pixels, common.randint(area // 4, area // 2))
      grid, colors = common.grid(width, height), []
      for (r, c) in pixels:
        grid[r][c] = common.blue()
      for r in range(height):
        for c in range(width):
          colors.append(grid[r][c])
      wide, tall = common.randint(2, 10), common.randint(2, 10)
      row, col = common.randint(0, gh - tall), common.randint(0, gw - wide)
      grid, output = common.grids(gw, gh)
      if draw(grid, output) and output != grid: break

  grid, output = common.grids(gw, gh)
  for r in range(gh):
    for c in range(gw):
      output[r][c] = grid[r][c] = colors[(r % height) * width + c % width]
  for r in range(tall):
    for c in range(wide):
      if grid[row + r][col + c] != common.blue():
        grid[row + r][col + c] = common.cyan()
      output[row + r][col + c] = grid[row + r][col + c]

  active_rows = []
  for row_idx in range(tall):
    r = row + row_idx
    if any(colors[(r % height) * width + c % width] == common.blue()
           for c in range(col, col + wide)):
      active_rows.append(row_idx)

  def reveal_band(band_idx):
    if 2 * band_idx >= len(active_rows):
      return
    for row_idx in active_rows[2 * band_idx:2 * band_idx + 2]:
      r = row + row_idx
      for c in range(col, col + wide):
        if colors[(r % height) * width + c % width] == common.blue():
          output[r][c] = common.green()

  reveal_band(0)
  reveal_band(1)
  reveal_band(2)
  reveal_band(3)
  reveal_band(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
               width=4, height=4, row=2, col=5, wide=5, tall=5),
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1,
                       0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                       1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0,
                       0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1,
                       1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                       1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                       0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                       0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1,
                       0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1,
                       0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                       0, 0, 1, 1],
               width=17, height=17, row=7, col=1, wide=8, tall=3),
      generate(colors=[0, 1, 0, 1, 0, 1], width=3, height=2, row=3, col=4,
               wide=5, tall=5),
  ]
  test = [
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 1], width=3, height=3, row=11,
               col=7, wide=6, tall=4),
  ]
  return {"train": train, "test": test}
