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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             dot_count=None, bar_count=None, bar_color=None, dot_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    dot_count: the number of singleton pixels to place
    bar_count: the number of two-pixel bars to place
    bar_color: the color of the two-pixel bars
    dot_color: the color of the singleton pixels
  """
  if rows is None or cols is None or colors is None:
    if width is None:
      width = common.randint(4, 30)
    if height is None:
      height = common.randint(4, 30)
    area = width * height
    max_dots = max(0, area // 5)
    if dot_count is None:
      dot_count = common.randint(0, max_dots)
    else:
      dot_count = max(0, min(dot_count, max_dots))
    max_bars = min(8, max(1, area // 12))
    if bar_count is None:
      bar_count = common.randint(1, max_bars)
    else:
      bar_count = max(1, min(bar_count, max_bars))
    if bar_color is None:
      bar_color = common.random_color(exclude=[common.green()])
    if dot_color is None:
      dot_color = bar_color
      if dot_count and common.randint(0, 1):
        dot_color = common.random_color(exclude=[common.green(), bar_color])
    bitmap = common.grid(width, height)
    red_cells, green_cells = set(), set()

    bar_candidates = []
    for r in range(height):
      for c in range(width):
        if c + 1 < width:
          bar_candidates.append((r, c, 0))
        if r + 1 < height:
          bar_candidates.append((r, c, 1))
    bar_candidates = common.shuffle(bar_candidates)
    placed_bars = 0
    for r1, c1, vert in bar_candidates:
      if placed_bars >= bar_count:
        break
      r2, c2 = r1 + vert, c1 + 1 - vert
      bar_red = [(r1, c1), (r2, c2)]
      if any((r, c) in red_cells for r, c in bar_red):
        continue
      bar_green = set()
      for r, c in [(r1, c1), (r2, c2)]:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < height and 0 <= cc < width:
              bar_green.add((rr, cc))
      if (bar_green & green_cells) or (bar_green & red_cells):
        continue
      for r, c in bar_green:
        bitmap[r][c] = common.green()
      for r, c in bar_red:
        bitmap[r][c] = bar_color
      green_cells.update(bar_green - set(bar_red))
      red_cells.update(bar_red)
      placed_bars += 1

    dot_candidates = []
    for r in range(height):
      for c in range(width):
        if bitmap[r][c]:
          continue
        dot_candidates.append((r, c))
    dot_candidates = common.shuffle(dot_candidates)
    placed_dots = 0
    for r, c in dot_candidates:
      if placed_dots >= dot_count:
        break
      neighbors_red = False
      for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        if (r + dr, c + dc) in red_cells:
          neighbors_red = True
      if neighbors_red:
        continue
      bitmap[r][c] = dot_color
      red_cells.add((r, c))
      placed_dots += 1
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid = common.grid(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color if color != common.green() else common.black()
  output = [row[:] for row in grid]
  green_cells = [
      (r, c) for r, c, color in zip(rows, cols, colors)
      if color == common.green()
  ]
  components = []
  remaining = set(green_cells)
  while remaining:
    start = remaining.pop()
    component = [start]
    stack = [start]
    while stack:
      r, c = stack.pop()
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          neighbor = (r + dr, c + dc)
          if neighbor not in remaining:
            continue
          remaining.remove(neighbor)
          stack.append(neighbor)
          component.append(neighbor)
    components.append(component)
  components.sort()

  def reveal_component(component_idx):
    if component_idx >= len(components):
      return
    for r, c in components[component_idx]:
      output[r][c] = common.green()

  reveal_component(0)
  reveal_component(1)
  reveal_component(2)
  reveal_component(3)
  reveal_component(4)
  reveal_component(5)
  reveal_component(6)
  reveal_component(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=15,
               rows=[1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 8, 11, 11, 12,
                     14, 14],
               cols=[6, 7, 8, 2, 6, 7, 8, 6, 7, 8, 6, 7, 8, 13, 17, 4, 8, 0, 0,
                     17],
               colors=[3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2,
                       2]),
      generate(width=16, height=15,
               rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3,
                     3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 7, 12, 13, 14, 14],
               cols=[7, 8, 9, 10, 12, 13, 14, 0, 7, 8, 9, 10, 12, 13, 14, 12,
                     13, 14, 8, 14, 15, 2, 10, 13, 14, 15, 14, 15, 10, 14, 15,
                     1, 1, 14, 2, 10],
               colors=[3, 2, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2,
                       3, 3, 2, 2, 2, 3, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2]),
  ]
  test = [
      generate(width=16, height=17,
               rows=[0, 1, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6,
                     6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9,
                     10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12,
                     12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14,
                     14, 14, 14, 14, 14, 15, 16],
               cols=[15, 4, 7, 8, 9, 10, 13, 15, 7, 8, 9, 10, 7, 8, 9, 10, 12,
                     1, 2, 3, 4, 1, 2, 3, 4, 13, 14, 15, 1, 2, 3, 4, 13, 14, 15,
                     6, 13, 14, 15, 0, 7, 8, 9, 10, 13, 14, 15, 8, 9, 10, 11, 2,
                     4, 5, 6, 7, 8, 9, 10, 1, 5, 6, 7, 8, 9, 10, 11, 13, 3, 5,
                     6, 7, 8, 15, 7, 8],
               colors=[2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                       3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 2,
                       3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 2, 3, 3, 3, 3,
                       2, 3, 2, 3, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2,
                       2]),
  ]
  return {"train": train, "test": test}
