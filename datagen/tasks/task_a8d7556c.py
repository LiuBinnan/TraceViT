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


def generate(colors=None, size=18, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size

  def draw(grid, output, stripes=[0, 1]):
    legal = True
    for r in range(height):
      for c in range(width):
        output[r][c] = grid[r][c] = colors[r * width + c]
    def is_empty(r, c):
      if output[r][c] or output[r][c + 1]: return False
      if output[r + 1][c] or output[r + 1][c + 1]: return False
      return True
    def paint(paintlist):
      for (r, c) in paintlist:
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          output[r + dr][c + dc] = common.red()
    for stripe in stripes:
      topaint = []
      if stripe == 0:  # First, paint all downstripes
        for r in range(height - 1):
          for c in range(width - 1):
            if not is_empty(r, c): continue
            # Cells on one side can't both be empty
            if c > 0 and output[r][c - 1] + output[r + 1][c - 1] == 0:
              legal = False
              continue
            if c < width - 2 and output[r][c + 2] + output[r + 1][c + 2] == 0:
              legal = False
              continue
            topaint.append((r, c))
      if stripe == 1:  # Second, paint all sidestripes
        for r in range(height - 1):
          for c in range(width - 1):
            if not is_empty(r, c): continue
            # Cells on one side can't both be empty
            if r > 0 and output[r - 1][c] + output[r - 1][c + 1] == 0:
              legal = False
              continue
            if r < height - 2 and output[r + 2][c] + output[r + 2][c + 1] == 0:
              legal = False
              continue
            topaint.append((r, c))
      paint(topaint)
    return legal

  if colors is None:
    while True:
      # Create some static
      pixels = common.random_pixels(width, height, 0.8)
      grid = common.grid(width, height)
      for (r, c) in pixels:
        grid[r][c] = common.gray()
      # Add some holes
      for _ in range(common.randint(4, 6)):
        r, c = common.randint(0, height - 2), common.randint(0, width - 2)
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          grid[r + dr][c + dc] = common.black()
      # Extract the colors
      colors = []
      for r in range(height):
        for c in range(width):
          colors.append(grid[r][c])
      grid, output1 = common.grids(width, height)
      if not draw(grid, output1, [0, 1]): continue
      grid, output2 = common.grids(width, height)
      if not draw(grid, output2, [1, 0]): continue
      if output1 == output2: break  # Avoid ambigous problems.

  grid = common.grid(width, height)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
  output = [row[:] for row in grid]

  def is_empty(r, c):
    if output[r][c] or output[r][c + 1]:
      return False
    if output[r + 1][c] or output[r + 1][c + 1]:
      return False
    return True

  def paint(paintlist):
    for r, c in paintlist:
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        output[r + dr][c + dc] = common.red()

  def downstripe_cells():
    topaint = []
    for r in range(height - 1):
      for c in range(width - 1):
        if not is_empty(r, c):
          continue
        if c > 0 and output[r][c - 1] + output[r + 1][c - 1] == 0:
          continue
        if c < width - 2 and output[r][c + 2] + output[r + 1][c + 2] == 0:
          continue
        topaint.append((r, c))
    return topaint

  def paint_downstripes(part_idx):
    cells = downstripe_cells()
    cutoff = height // 2
    if part_idx == 0:
      paint([(r, c) for r, c in cells if r < cutoff])
    else:
      paint([(r, c) for r, c in cells if r >= cutoff])

  side_cells = []

  def collect_sidestripes():
    nonlocal side_cells
    topaint = []
    for r in range(height - 1):
      for c in range(width - 1):
        if not is_empty(r, c):
          continue
        if r > 0 and output[r - 1][c] + output[r - 1][c + 1] == 0:
          continue
        if r < height - 2 and output[r + 2][c] + output[r + 2][c + 1] == 0:
          continue
        topaint.append((r, c))
    side_cells = topaint

  def paint_sidestripes(part_idx):
    cutoff = width // 2
    if part_idx == 0:
      paint([(r, c) for r, c in side_cells if c < cutoff])
    else:
      paint([(r, c) for r, c in side_cells if c >= cutoff])

  paint_downstripes(0)
  paint_downstripes(1)
  collect_sidestripes()
  paint_sidestripes(0)
  paint_sidestripes(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5,
                       5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5,
                       5, 0, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5,
                       0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0,
                       0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0,
                       5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0, 5, 0,
                       5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5,
                       5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5,
                       5, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0,
                       5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0,
                       5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 0, 5,
                       5]),
      generate(colors=[5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 5,
                       5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0,
                       5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 0, 0, 5,
                       0, 5, 5, 5, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5,
                       0, 0, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5,
                       5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5,
                       0, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 0,
                       5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0,
                       0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5,
                       0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5,
                       0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 0, 5, 5,
                       5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0,
                       0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5,
                       5]),
      generate(colors=[0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0,
                       5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5,
                       0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5,
                       5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5,
                       5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5,
                       5, 0, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5,
                       0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5,
                       5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5,
                       0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5,
                       5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 0,
                       5, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5,
                       5, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 0, 0,
                       5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 5,
                       0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5,
                       0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0,
                       0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 5,
                       5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5,
                       0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5,
                       5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 5, 5, 5,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5,
                       5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0,
                       5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5,
                       0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5,
                       5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 5, 5, 5, 0,
                       5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5,
                       5, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 5, 0,
                       0]),
  ]
  return {"train": train, "test": test}
