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


def generate(lines=None, brow=None, bcol=None, nrows=None, ncols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lines: The lines of the characters.
    brow: The row of the special.
    bcol: The column of the special.
    nrows: The number of glyph rows.
    ncols: The number of glyph columns.
  """

  def get_colors():
    rows = 4 if nrows is None else nrows
    cols = 6 if ncols is None else ncols
    target = lines[brow][bcol]
    colors = [[1 for _ in range(cols)] for _ in range(rows)]
    # First, mark all target cells.
    for row in range(rows):
      for col in range(cols):
        if lines[row][col] == target: colors[row][col] = 8
    # Second, scan rows for "in betweens" (ie, the target on the left or right).
    for row in range(rows):
      for col in range(1, cols - 1):
        is_left = sum([1 if lines[row][c] == target else 0 for c in range(col)])
        is_right = sum([1 if lines[row][c] == target else 0
                        for c in range(col + 1, cols)])
        if is_left and is_right:
          if colors[row][col] == 8: return None
          colors[row][col] = 7
    # Third, scan columns for "in betweens" (ie, the target above or below).
    for row in range(1, rows - 1):
      for col in range(cols):
        is_left = sum([1 if lines[r][col] == target else 0 for r in range(row)])
        is_right = sum([1 if lines[r][col] == target else 0
                        for r in range(row + 1, rows)])
        if is_left and is_right:
          if colors[row][col] == 8: return None
          colors[row][col] = 7
    return colors

  def draw():
    rows = 4 if nrows is None else nrows
    cols = 6 if ncols is None else ncols
    grid, output = common.grids(4 * cols + 1, 4 * rows + 1)
    colors = get_colors()
    if colors is None: return None, None  # Probably a target between 2 others.
    if 7 not in common.flatten(colors): return None, None  # No inbetwens.
    for row, line in enumerate(lines):
      for col, letter in enumerate(line):
        for dr, dc in common.letter_map()[letter]:
          r, c = 4 * row + 1 + dr, 4 * col + 1 + dc
          grid[r][c] = 8 if (row == brow and col == bcol) else 1
          output[r][c] = colors[row][col]
    return grid, output

  if lines is None:
    if nrows is None: nrows = 4
    if ncols is None: ncols = 6
    letters = common.sample(sorted(list(common.letter_map().keys())), 6)
    for _ in range(500):
      lines = []
      for _ in range(nrows):
        line = ""
        for _ in range(ncols):
          line += common.choice(letters)
        lines.append(line)
      brow = common.randint(0, nrows - 1)
      bcol = common.randint(0, ncols - 1)
      grid, _ = draw()
      if grid: break
    else:
      target, filler = letters[:2]
      lines = [filler * ncols for _ in range(nrows)]
      lines[0] = target + filler + target + filler * (ncols - 3)
      brow, bcol = 0, 0

  grid, _ = draw()
  output = common.deepcopy(grid)
  colors = get_colors()

  def reveal_targets():
    """Highlights every glyph sharing the marked cell's letter (cyan)."""
    rows = 4 if nrows is None else nrows
    cols = 6 if ncols is None else ncols
    for row in range(rows):
      for col in range(cols):
        if colors[row][col] != common.cyan(): continue
        for dr, dc in common.letter_map()[lines[row][col]]:
          output[4 * row + 1 + dr][4 * col + 1 + dc] = common.cyan()

  def reveal_betweens():
    """Highlights glyphs trapped between two matches in a row/column (orange)."""
    rows = 4 if nrows is None else nrows
    cols = 6 if ncols is None else ncols
    for row in range(rows):
      for col in range(cols):
        if colors[row][col] != common.orange(): continue
        for dr, dc in common.letter_map()[lines[row][col]]:
          output[4 * row + 1 + dr][4 * col + 1 + dc] = common.orange()

  reveal_targets()
  reveal_betweens()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lines=["H+@+IO", "@H.@H@", "+..+.I", "I+IH@+"], brow=0, bcol=3),
      generate(lines=["X+OXO+", "+XXO+X", "HO+XHO", "XHH+OX"], brow=0, bcol=2),
      generate(lines=["4+U/N+", "UY4UY/", "/N+4N+", "4/U+4Y"], brow=2, bcol=1),
  ]
  test = [
      generate(lines=["O?I.+?", "2IOIIO", "I+?.+.", "+?O+2?"], brow=0, bcol=1),
  ]
  return {"train": train, "test": test}
