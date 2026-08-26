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
             num_boxes=None, palette_size=None, bg_color=None, markers=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if rows is None or cols is None or colors is None:
    if width is None:
      width = common.randint(10, 30)
    if height is None:
      height = common.randint(10, 30)
    if num_boxes is None:
      num_boxes = common.randint(2, max(2, (width * height) // 16))
    num_boxes = max(2, min(num_boxes, max(2, (width * height) // 16), 18))
    if bg_color is None:
      bg_color = common.choice([color for color in range(10)
                                if color != common.cyan()])
    if bg_color == common.cyan():
      bg_color = common.maroon()
    object_colors = [color for color in range(10)
                     if color not in [bg_color, common.cyan()]]
    if palette_size is None:
      palette_size = common.randint(1, len(object_colors))
    palette_size = max(1, min(palette_size, len(object_colors)))
    object_colors = common.sample(object_colors, palette_size)
    hidden_color = common.choice(object_colors)
    # Choose some nonoverlapping box locations.
    while True:
      wides, talls, brows, bcols = [], [], [], []
      for _ in range(40 * num_boxes):
        wide, tall = common.randint(3, 6), common.randint(3, 6)
        if wide > width or tall > height:
          continue
        brow = common.randint(0, height - tall)
        bcol = common.randint(0, width - wide)
        test_rows = brows + [brow]
        test_cols = bcols + [bcol]
        test_wides = wides + [wide]
        test_talls = talls + [tall]
        if common.overlaps(test_rows, test_cols, test_wides, test_talls, 2):
          continue
        brows, bcols = test_rows, test_cols
        wides, talls = test_wides, test_talls
        if len(brows) >= num_boxes:
          break
      if len(brows) >= 2:
        break
    num_boxes = len(brows)
    # Draw the boxes (subtracting pixels from open ones) and adding "barnacles".
    grid, _ = common.grids(width, height, bg_color)
    while True:
      closeds = [common.randint(0, 1) for _ in range(num_boxes)]
      while sum(closeds) > 10:
        closeds[common.choice([idx for idx, closed in enumerate(closeds)
                               if closed])] = 0
      if len(set(closeds)) > 1: break
    all_barnacles = []
    barnacle_colors = {}
    open_color_idx = 0
    for idx in range(num_boxes):
      brow, bcol, wide, tall = brows[idx], bcols[idx], wides[idx], talls[idx]
      closed = closeds[idx]
      if closed:
        input_color = hidden_color
      else:
        input_color = object_colors[open_color_idx % len(object_colors)]
        open_color_idx += 1
      color, perim = common.cyan() if closed else input_color, []
      for r in range(brow, brow + tall):
        for c in range(bcol, bcol + wide):
          h, v = r in [brow, brow + tall - 1], c in [bcol, bcol + wide - 1]
          if not h and not v: continue  # Anything inside the box.
          grid[r][c] = color  # Any part of the perimeter.
          if h != v: perim.append((r, c))  # Excludes edge pixels.
      # Draw little things around the edges.
      barnacles = []
      barnacles.append((brow - 1, bcol))
      barnacles.append((brow, bcol - 1))
      barnacles.append((brow - 1, bcol + wide - 1))
      barnacles.append((brow, bcol + wide))
      barnacles.append((brow + tall - 1, bcol + wide))
      barnacles.append((brow + tall, bcol + wide - 1))
      barnacles.append((brow + tall, bcol))
      barnacles.append((brow + tall - 1, bcol - 1))
      for barnacle in barnacles:
        if common.randint(0, 4): continue
        all_barnacles.append(barnacle)
        barnacle_colors[barnacle] = color if closed else input_color
      if closed: continue
      pixel = common.choice(perim)
      grid[pixel[0]][pixel[1]] = bg_color
    all_barnacles = common.remove_neighbors(all_barnacles)
    for barnacle in all_barnacles:
      if common.get_pixel(grid, barnacle[0], barnacle[1]) == bg_color:
        common.draw(grid, barnacle[0], barnacle[1], barnacle_colors[barnacle])
    input_grid = common.grid(width, height, bg_color)
    for r in range(height):
      for c in range(width):
        input_grid[r][c] = hidden_color if grid[r][c] == common.cyan() else grid[r][c]

    hole_cells = set()
    seen = set()
    for r in range(height):
      for c in range(width):
        if (r, c) in seen or input_grid[r][c] != bg_color:
          continue
        component = []
        stack = [(r, c)]
        seen.add((r, c))
        borders = False
        while stack:
          sr, sc = stack.pop()
          component.append((sr, sc))
          if sr in [0, height - 1] or sc in [0, width - 1]:
            borders = True
          for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = sr + dr, sc + dc
            if nr < 0 or nr >= height or nc < 0 or nc >= width:
              continue
            if (nr, nc) in seen or input_grid[nr][nc] != bg_color:
              continue
            seen.add((nr, nc))
            stack.append((nr, nc))
        if not borders:
          hole_cells.update(component)

    reveal_cells = set()
    seen = set()
    for r in range(height):
      for c in range(width):
        if (r, c) in seen or input_grid[r][c] == bg_color:
          continue
        color = input_grid[r][c]
        component = []
        stack = [(r, c)]
        seen.add((r, c))
        touches_hole = False
        while stack:
          sr, sc = stack.pop()
          component.append((sr, sc))
          for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = sr + dr, sc + dc
            if (nr, nc) in hole_cells:
              touches_hole = True
            if nr < 0 or nr >= height or nc < 0 or nc >= width:
              continue
            if ((nr, nc) in seen or input_grid[nr][nc] != color):
              continue
            seen.add((nr, nc))
            stack.append((nr, nc))
        if touches_hole:
          reveal_cells.update(component)

    rows, cols, colors, markers = [], [], [], []
    for r in range(height):
      for c in range(width):
        if input_grid[r][c] == bg_color: continue
        rows.append(r)
        cols.append(c)
        colors.append(input_grid[r][c])
        markers.append((r, c) in reveal_cells)
  else:
    bg_color = common.maroon()
    hidden_color = common.blue()

  grid = common.grid(width, height, bg_color)
  reveal_marks = markers
  if reveal_marks is None:
    reveal_marks = [color == common.cyan() for color in colors]
  for r, c, color, reveal in zip(rows, cols, colors, reveal_marks):
    grid[r][c] = color if not reveal else (
        hidden_color if markers is None else color)
  output = [row[:] for row in grid]
  cyan_cells = [
      (r, c) for r, c, reveal in zip(rows, cols, reveal_marks)
      if reveal
  ]
  components = []
  remaining = set(cyan_cells)
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
      output[r][c] = common.cyan()

  reveal_component(0)
  reveal_component(1)
  reveal_component(2)
  reveal_component(3)
  reveal_component(4)
  reveal_component(5)
  reveal_component(6)
  reveal_component(7)
  reveal_component(8)
  reveal_component(9)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=9,
               cols=[1, 2, 3, 7, 1, 3, 7, 1, 3, 6, 7, 8, 9, 1, 2, 3, 7, 7],
               rows=[2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6],
               colors=[8, 8, 8, 1, 8, 8, 1, 8, 8, 1, 1, 1, 1, 8, 8, 8, 1, 1]),
      generate(width=11, height=12,
               cols=[1, 2, 3, 4, 5, 8, 1, 5, 8, 10, 1, 2, 3, 4, 5, 8, 9, 10, 3,
                     2, 3, 4, 5, 6, 3, 5, 3, 4, 5, 8, 9, 10, 8, 10, 0, 1, 8, 9,
                     10],
               rows=[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 6, 7,
                     7, 7, 7, 7, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 11, 11, 11, 11,
                     11],
               colors=[8, 8, 8, 8, 8, 1, 8, 8, 1, 1, 8, 8, 8, 8, 8, 1, 1, 1, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 8, 8,
                       8]),
      generate(width=13, height=12,
               cols=[5, 8, 2, 7, 8, 9, 10, 1, 2, 3, 4, 8, 1, 4, 8, 1, 2, 3, 4,
                     8, 9, 10, 4, 4, 1, 7, 8, 9, 0, 1, 2, 9, 1, 6, 8, 9, 0, 1,
                     6, 7, 8],
               rows=[0, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5,
                     5, 5, 6, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11,
                     11, 11, 11],
               colors=[1, 1, 8, 1, 1, 1, 1, 8, 8, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8,
                       1, 1, 1, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1]),
      generate(width=15, height=14,
               cols=[1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 2, 6, 11, 14, 2, 3, 4, 6,
                     10, 11, 12, 14, 4, 5, 6, 14, 4, 8, 9, 10, 8, 10, 11, 8, 9,
                     10, 0, 1, 2, 3, 0, 3, 7, 9, 0, 1, 2, 3, 7, 8, 9, 10, 11, 0,
                     9, 5, 4, 5, 12, 13],
               rows=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3,
                     3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8,
                     9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 12,
                     13, 13, 13, 13],
               colors=[8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 8, 8, 1, 1, 8, 8, 8, 8, 1,
                       1, 1, 1, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 1, 1, 8, 8, 8, 8, 1, 1, 1, 1, 1, 8, 1, 1, 1,
                       1, 1, 1]),
  ]
  test = [
      generate(width=15, height=16,
               cols=[0, 1, 11, 3, 4, 5, 6, 7, 11, 4, 7, 11, 4, 7, 11, 4, 5, 6,
                     7, 11, 14, 7, 11, 12, 13, 14, 0, 1, 2, 3, 7, 11, 14, 0, 3,
                     14, 0, 3, 13, 14, 0, 1, 3, 4, 5, 6, 7, 8, 12, 13, 3, 8, 13,
                     3, 8, 13, 3, 4, 5, 6, 7, 8, 9, 13],
               rows=[0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5,
                     5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9,
                     10, 10, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 14, 14,
                     14, 15, 15, 15, 15, 15, 15, 15, 15],
               colors=[1, 1, 1, 8, 8, 8, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8,
                       1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 1, 1, 8, 8, 1, 8, 8, 1, 8,
                       8, 8, 8, 8, 8, 8, 1]),
  ]
  return {"train": train, "test": test}
