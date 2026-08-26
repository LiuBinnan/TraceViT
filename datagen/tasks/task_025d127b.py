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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None, count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of colors to be used for pixels
    count: the number of objects to attempt to place
    num_colors: the number of foreground colors to sample
  """
  if rows is None:
    if width is None: width = common.randint(5, 30)
    if height is None: height = common.randint(5, 30)
    if count is None: count = common.randint(1, max(1, width * height // 20))
    if num_colors is None: num_colors = common.randint(1, 9)
    palette = common.random_colors(num_colors)
    rows, cols, wides, talls, colors = [], [], [], [], []
    occupied = set()
    tries = 0
    while len(rows) < count and tries < 5 * count:
      tries += 1
      tall = common.randint(3, 6)
      top_wide = common.randint(3, 6)
      wide = top_wide + tall - 2
      if tall > height or wide > width: continue
      row = common.randint(0, height - tall)
      col = common.randint(0, width - wide)
      full = set()
      for c in range(wide - tall + 2):
        full.add((row, col + c))
        full.add((row + tall - 1, col + c + tall - 2))
        full.add((row, col + c + 1))
      for r in range(1, tall - 1):
        full.add((row + r, col + r - 1))
        full.add((row + r, col + r + wide - tall + 1))
        full.add((row + r, col + r))
        full.add((row + r, min(col + r + wide - tall + 2, col + wide - 1)))
      if any(pixel in occupied for pixel in full): continue
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
      colors.append(common.choice(palette))
      for r, c in full:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < height and 0 <= cc < width:
              occupied.add((rr, cc))

  grid = common.grid(width, height)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    # Horizontal stuff.
    for c in range(wide - tall + 2):
      grid[row][col + c] = color
      grid[row + tall - 1][col + c + tall - 2] = color
    # Diagonal stuff
    for r in range(1, tall - 1):
      grid[row + r][col + r - 1] = color
      grid[row + r][col + r + wide - tall + 1] = color
  output = common.grid(width, height)

  def keep_base_edges():
    """Copies the unchanged bottom edge of each leaning outline."""
    for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
      for c in range(wide - tall + 2):
        output[row + tall - 1][col + c + tall - 2] = color

  def shift_top_edges():
    """Moves each top edge one cell to the right."""
    for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
      for c in range(wide - tall + 2):
        output[row][col + c + 1] = color

  def shift_side_edges():
    """Moves each slanted side one cell to the right."""
    for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
      for r in range(1, tall - 1):
        output[row + r][col + r] = color
        output[row + r][min(col + r + wide - tall + 2, col + wide - 1)] = color

  keep_base_edges()
  shift_top_edges()
  shift_side_edges()
  return {"input": grid, "output": output}



def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=14, rows=[1, 7], cols=[1, 2], wides=[6, 4],
               talls=[5, 3], colors=[6, 2]),
      generate(width=9, height=8, rows=[1], cols=[1], wides=[8], talls=[5],
               colors=[8]),
  ]
  test = [
      generate(width=10, height=10, rows=[1], cols=[1], wides=[9], talls=[5],
               colors=[4]),
  ]
  return {"train": train, "test": test}
