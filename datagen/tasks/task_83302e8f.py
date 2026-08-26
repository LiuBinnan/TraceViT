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


def _create_linegrid(bitmap, row_spacing, col_spacing, linecolor):
  """Creates a line grid with independent row and column cell sizes."""
  actual_height = len(bitmap) * (row_spacing + 1) - 1
  actual_width = len(bitmap[0]) * (col_spacing + 1) - 1
  ingrid = common.grid(actual_width, actual_height)
  for r in range(actual_height):
    for c in range(actual_width):
      if (r + 1) % (row_spacing + 1) == 0:
        ingrid[r][c] = linecolor
      if (c + 1) % (col_spacing + 1) == 0:
        ingrid[r][c] = linecolor
  for r, row in enumerate(bitmap):
    for c, color in enumerate(row):
      for dr in range(row_spacing):
        for dc in range(col_spacing):
          ingrid[r * (row_spacing + 1) + dr][
              c * (col_spacing + 1) + dc] = color
  return ingrid


def _line_candidates(gh, gw, row_spacing, col_spacing):
  """Returns line segments and intersections that may be broken."""
  candidates = []
  for r in range(row_spacing, gh * (row_spacing + 1) - 1,
                 row_spacing + 1):
    for j in range(gw):
      start = j * (col_spacing + 1)
      candidates.append([(r, start + dc) for dc in range(col_spacing)])
  for c in range(col_spacing, gw * (col_spacing + 1) - 1,
                 col_spacing + 1):
    for i in range(gh):
      start = i * (row_spacing + 1)
      candidates.append([(start + dr, c) for dr in range(row_spacing)])
  for r in range(row_spacing, gh * (row_spacing + 1) - 1,
                 row_spacing + 1):
    for c in range(col_spacing, gw * (col_spacing + 1) - 1,
                   col_spacing + 1):
      candidates.append([(r, c)])
  return candidates


def _components(ingrid, color):
  """Returns 4-connected components of a color."""
  height, width = len(ingrid), len(ingrid[0])
  seen = set()
  components = []
  for row in range(height):
    for col in range(width):
      if ingrid[row][col] != color or (row, col) in seen:
        continue
      component, queue = [], [(row, col)]
      seen.add((row, col))
      while queue:
        r, c = queue.pop()
        component.append((r, c))
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
          if nr < 0 or nr >= height or nc < 0 or nc >= width:
            continue
          if ingrid[nr][nc] != color or (nr, nc) in seen:
            continue
          seen.add((nr, nc))
          queue.append((nr, nc))
      components.append(component)
  return components


def generate(size=None, minisize=None, color=None, rows=None, cols=None,
             height=None, width=None, row_spacing=None, col_spacing=None,
             break_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the number of large cells
    minisize: the number of pixels within a large cell
    color: a digit representing a color to be used
    rows: a list of vertical coordinates where black pixels should be placed
    cols: a list of horizontal coordinates where black pixels should be placed
    height: the number of large cell rows (defaults to size; row extent)
    width: the number of large cell columns (defaults to size; col extent)
    row_spacing: the height of each large cell
    col_spacing: the width of each large cell
    break_count: the number of line segments or intersections to break
  """
  if size is None:
    if row_spacing is None:
      row_spacing = common.randint(2, 5)
    if col_spacing is None:
      col_spacing = common.randint(2, 5)
    if height is None:
      height = common.randint(3, 30 // (row_spacing + 1))
    if width is None:
      width = common.randint(3, 30 // (col_spacing + 1))
    gh, gw = height, width
    candidates = _line_candidates(gh, gw, row_spacing, col_spacing)
    max_breaks = len(candidates) // 2
    if break_count is None:
      break_count = common.randint(0, max_breaks)
    break_count = max(0, min(break_count, max_breaks))
    breakobjs = common.sample(candidates, break_count)
    pixels = [common.choice(obj) for obj in breakobjs]
    rows, cols = zip(*pixels) if pixels else ([], [])
    color = common.random_color(exclude=[common.yellow(), common.green()])
    use_object_rule = True
  else:
    gh = size if height is None else height
    gw = size if width is None else width
    row_spacing = minisize if row_spacing is None else row_spacing
    col_spacing = minisize if col_spacing is None else col_spacing
    use_object_rule = False

  grid = common.grid(gw, gh, common.black())
  output = common.grid(gw, gh, common.green())
  if use_object_rule:
    grid = _create_linegrid(grid, row_spacing, col_spacing, color)
  if not use_object_rule:
    for r, c in zip(rows, cols):
      if r % (minisize + 1) != minisize:
        output[r // (minisize + 1)][c // (minisize + 1)] = common.yellow()
        output[r // (minisize + 1)][c // (minisize + 1) + 1] = common.yellow()
      if c % (minisize + 1) != minisize:
        output[r // (minisize + 1)][c // (minisize + 1)] = common.yellow()
        output[r // (minisize + 1) + 1][c // (minisize + 1)] = common.yellow()
  if not use_object_rule:
    grid = common.create_linegrid(grid, minisize, color)
    output = common.create_linegrid(output, minisize, color)
  for r, c in zip(rows, cols):
    grid[r][c] = common.black()
    if not use_object_rule:
      output[r][c] = common.yellow()
  if use_object_rule:
    output = [row[:] for row in grid]
  if use_object_rule:
    for component in _components(grid, common.black()):
      if len(component) == row_spacing * col_spacing:
        for r, c in component:
          output[r][c] = common.green()
  if use_object_rule:
    for r, row in enumerate(output):
      for c, value in enumerate(row):
        if value == common.black():
          output[r][c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, minisize=4, color=8,
               rows=[4, 7, 8, 9, 9, 10, 12, 13, 14, 14, 17],
               cols=[17, 4, 19, 8, 13, 14, 4, 9, 20, 23, 9]),
      generate(size=5, minisize=5, color=1,
               rows=[6, 7, 8, 10, 11, 11, 13, 13, 14, 17, 17, 17, 23],
               cols=[11, 5, 5, 17, 8, 24, 5, 11, 17, 14, 20, 25, 0]),
      generate(size=4, minisize=4, color=9,
               rows=[2, 2, 3, 4, 6, 9, 14, 15, 17],
               cols=[4, 9, 4, 7, 4, 10, 18, 14, 4]),
  ]
  test = [
      generate(size=7, minisize=3, color=5,
               rows=[2, 3, 3, 3, 4, 5, 5, 7, 9, 11, 11, 11, 11, 12, 12, 12, 13,
                     15, 15, 18, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 25, 26,
                     26],
               cols=[7, 6, 7, 26, 3, 11, 15, 13, 7, 5, 6, 10, 12, 3, 11, 19, 3,
                     2, 21, 11, 22, 15, 19, 15, 23, 11, 23, 5, 18, 11, 3, 7,
                     15]),
  ]
  return {"train": train, "test": test}
