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


def generate(width=None, height=None, static=None, colors=None,
             num_boxes=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    static: the color of the static
    colors: a list of colors to be used in the input grid
  """
  if colors is None:
    if height is None:
      height = common.randint(10, 30)
    if width is None:
      width = common.randint(10, 30)
    if static is None:
      static = common.random_color(exclude=[common.red(), common.yellow()])
    if density is None:
      density = common.randint(35, 65)
    density = density / 100 if density > 1 else density
    # First, create random static.
    pixels = common.random_pixels(width, height, density)
    grid = common.grid(width, height)
    for r, c in pixels:
      grid[r][c] = static
    # Second, create a few rectangles underneath.
    if num_boxes is None:
      num_boxes = common.randint(1, max(1, (width * height) // 30))
    num_boxes = min(5, num_boxes)
    rows, cols, wides, talls = [], [], [], []
    tries = 0
    while len(rows) < num_boxes and tries < 50 * num_boxes:
      tries += 1
      w = common.randint(2, min(7, width))
      t = common.randint(2, min(7, height))
      r, c = common.randint(0, height - t), common.randint(0, width - w)
      if common.overlaps(rows + [r], cols + [c], wides + [w], talls + [t], 2):
        continue
      candidate = [row[:] for row in grid]
      # Ensure every row and column has visible red, and at least one cell is
      # hidden by the static color.
      hidden_row = common.randint(r, r + t - 1)
      hidden_col = common.randint(c, c + w - 1)
      candidate[hidden_row][hidden_col] = static
      for row in range(r, r + t):
        col = common.randint(c, c + w - 1)
        if row == hidden_row and col == hidden_col:
          col = c if hidden_col != c else c + 1
        candidate[row][col] = 0
      for col in range(c, c + w):
        row = common.randint(r, r + t - 1)
        if row == hidden_row and col == hidden_col:
          row = r if hidden_row != r else r + 1
        candidate[row][col] = 0
      candidate[hidden_row][hidden_col] = static
      red_count, static_count, background_count = 0, 0, 0
      for row in range(height):
        for col in range(width):
          color = candidate[row][col]
          if r <= row < r + t and c <= col < c + w:
            color = common.yellow() if color else common.red()
          if color == common.red():
            red_count += 1
          elif color:
            static_count += 1
          else:
            background_count += 1
      if red_count >= min(static_count, background_count):
        continue
      rows.append(r)
      cols.append(c)
      wides.append(w)
      talls.append(t)
      for row in range(r, r + t):
        for col in range(c, c + w):
          candidate[row][col] = common.yellow() if candidate[row][col] else common.red()
      grid = candidate
    # Finally, flatten the colors into a list.
    colors = []
    for r in range(height):
      for c in range(width):
        colors.append(grid[r][c])

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      color = colors[r * width + c]
      grid[r][c] = color if color != common.yellow() else static
  output = [row[:] for row in grid]
  patterns, seen = [], set()
  for r in range(height):
    for c in range(width):
      if (r, c) in seen:
        continue
      if colors[r * width + c] not in [common.red(), common.yellow()]:
        continue
      component, queue = [], [(r, c)]
      seen.add((r, c))
      while queue:
        cr, cc = queue.pop()
        component.append((cr, cc))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
          nr, nc = cr + dr, cc + dc
          if nr < 0 or nr >= height or nc < 0 or nc >= width:
            continue
          if (nr, nc) in seen:
            continue
          if colors[nr * width + nc] not in [common.red(), common.yellow()]:
            continue
          seen.add((nr, nc))
          queue.append((nr, nc))
      if any(colors[rr * width + cc] == common.yellow() for rr, cc in component):
        patterns.append(component)

  def reveal_pattern(idx):
    if idx >= len(patterns):
      return
    for r, c in patterns[idx]:
      if colors[r * width + c] == common.yellow():
        output[r][c] = common.yellow()

  reveal_pattern(0)
  reveal_pattern(1)
  reveal_pattern(2)
  reveal_pattern(3)
  reveal_pattern(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=17, static=1,
               colors=[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,
                       1, 2, 4, 4, 4, 4, 4, 4, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1,
                       4, 2, 4, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 2,
                       4, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0,
                       1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 0, 4, 2, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 2, 4, 2, 4,
                       2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4,
                       0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 4, 2, 4, 2, 2, 0,
                       0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                       1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
                       0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                       1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
                       0, 1]),
      generate(width=16, height=15, static=8,
               colors=[8, 0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 8, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 8, 8, 8, 0,
                       8, 8, 8, 8, 8, 8, 0, 8, 0, 8, 0, 0, 8, 0, 8, 0, 0, 0, 0,
                       8, 0, 4, 4, 2, 8, 0, 0, 0, 2, 4, 2, 2, 2, 8, 0, 0, 0, 2,
                       4, 2, 8, 0, 8, 0, 2, 4, 2, 4, 4, 8, 0, 0, 0, 8, 0, 0, 8,
                       8, 8, 0, 0, 8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 0, 0, 0, 8, 0,
                       8, 0, 8, 0, 8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0, 0, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 4, 4, 2, 4, 8, 8,
                       0, 8, 0, 0, 0, 8, 8, 8, 8, 0, 2, 4, 4, 2, 8, 8, 0, 8, 0,
                       0, 8, 8, 0, 8, 0, 8, 0, 0, 0, 8, 8, 0, 0, 2, 4, 4, 0, 8,
                       8, 8, 8, 0, 0, 8, 8, 8, 8, 0, 0, 2, 4, 2, 0, 0, 0, 8, 0,
                       8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8, 0,
                       8, 0, 8, 0, 0, 0, 8, 8, 8, 8, 8, 8]),
      generate(width=14, height=15, static=3,
               colors=[3, 3, 0, 0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0,
                       3, 3, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 3,
                       0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 3, 0,
                       0, 0, 2, 2, 2, 2, 4, 0, 0, 0, 3, 0, 3, 0, 3, 3, 2, 2, 4,
                       4, 2, 0, 0, 0, 3, 3, 0, 0, 3, 0, 2, 2, 2, 4, 2, 0, 0, 3,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 0, 0, 0, 0, 3, 0, 0,
                       3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 3, 3, 3, 3, 4, 2, 0, 3, 3,
                       0, 0, 0, 3, 0, 3, 0, 0, 3, 2, 4, 0, 0, 0, 3, 3, 0, 0, 0,
                       3, 0, 0, 3, 3, 0, 3, 3, 0, 0, 3, 3, 0, 3, 0, 3, 0, 0, 3,
                       0, 3, 3, 0, 0, 3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 3, 0, 3, 0,
                       3, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 3, 3, 0, 3,
                       3]),
  ]
  test = [
      generate(width=18, height=17, static=9,
               colors=[0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9,
                       2, 4, 2, 2, 4, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 2,
                       2, 4, 4, 2, 0, 0, 9, 9, 9, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 9, 0,
                       0, 0, 9, 0, 9, 9, 0, 9, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0,
                       9, 2, 4, 2, 2, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                       2, 2, 2, 2, 9, 0, 9, 9, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0,
                       0, 9, 0, 9, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9,
                       9, 9, 9, 9, 0, 9, 0, 0, 0, 0, 9, 9, 0, 9, 0, 9, 0, 9, 9,
                       0, 0, 9, 9, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 4, 2, 9, 0,
                       0, 9, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 9, 2, 4, 9, 9, 0,
                       0, 0, 9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9, 0, 0, 9, 0,
                       0, 0, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 2, 2,
                       4, 2, 2, 4, 0, 0, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 2, 4, 2,
                       4, 4, 2, 9, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 0, 2, 2, 4, 2,
                       2, 4, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9,
                       9, 0]),
  ]
  return {"train": train, "test": test}
