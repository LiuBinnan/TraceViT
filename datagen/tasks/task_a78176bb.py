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


def _structure_cells(diag, rows, cols, width, height):
  """Returns the input/output cells touched by one diagonal-hint structure."""
  input_cells, output_cells = set(), set()
  for r in range(height):
    for c in range(width):
      mydiag = r - c
      if mydiag == diag:
        input_cells.add((r, c))
        output_cells.add((r, c))
      for row, col in zip(rows, cols):
        linediag = row - col
        if diag < mydiag and mydiag <= linediag and r <= row and c >= col:
          input_cells.add((r, c))
        if diag > mydiag and mydiag >= linediag and r >= row and c <= col:
          input_cells.add((r, c))
        if linediag < diag and linediag == mydiag + 2:
          output_cells.add((r, c))
        if linediag > diag and linediag == mydiag - 2:
          output_cells.add((r, c))
  return input_cells, output_cells


def _neighbors(cells, width, height):
  out = set(cells)
  for r, c in cells:
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
          out.add((nr, nc))
  return out


def _structure_candidates(width, height):
  candidates = []
  for diag in range(-(width - 4), height - 4):
    for row in range(1, height - 1):
      for col in range(1, width - 1):
        compact = 2 <= abs(row - col - diag) <= 5
        if not compact:
          continue
        if row - col < diag - 1 and col < (width - diag) and row >= diag:
          candidates.append((diag, row, col))
        if row - col > diag + 1 and col >= -diag and row < (height + diag):
          candidates.append((diag, row, col))
  return candidates


def _sample_structure(width, height, candidates=None):
  if candidates is None:
    candidates = _structure_candidates(width, height)
  diag, row, col = common.choice(candidates)
  return diag, [row], [col]


def generate(diag=None, rows=None, cols=None, color=None, size=10,
             height=None, width=None, line_count=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    diag: a diagonal to be drawn
    rows: a list of rows for the gray corners
    cols: a list of columns for the gray corners
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    line_count: number of diagonal-hint structures to sample
    num_colors: number of distinct structure colors to use
  """
  if height is None: height = size
  if width is None: width = size
  specs = []
  if diag is None:
    max_lines = max(1, (height + width) // 8)
    if line_count is None:
      line_count = common.randint(1, max_lines)
    line_count = max(1, min(line_count, max_lines))
    if num_colors is None:
      num_colors = common.randint(1, min(6, line_count, 8))
    num_colors = max(1, min(num_colors, line_count, 8))
    palette = common.random_colors(num_colors, exclude=[common.gray()])
    candidates = _structure_candidates(width, height)
    occupied_input = set()
    occupied_output = set()
    tries = 0
    while len(specs) < line_count and tries < 40 * line_count:
      tries += 1
      sdiag, srows, scols = _sample_structure(width, height, candidates)
      incells, outcells = _structure_cells(sdiag, srows, scols, width, height)
      if (incells & occupied_input) or (incells & occupied_output):
        continue
      if outcells & occupied_output:
        continue
      specs.append((sdiag, srows, scols, palette[len(specs) % num_colors]))
      occupied_input |= _neighbors(incells, width, height)
      occupied_output |= outcells
    if not specs:
      diag, rows, cols = _sample_structure(width, height)
      color = palette[0]
      specs.append((diag, rows, cols, color))
  else:
    specs.append((diag, rows, cols, color))

  grid, output = common.grids(width, height)
  for diag, rows, cols, color in specs:
    for r in range(height):
      for c in range(width):
        mydiag = r - c
        if mydiag == diag: output[r][c] = grid[r][c] = color
        for row, col in zip(rows, cols):
          linediag = row - col
          if diag < mydiag and mydiag <= linediag and r <= row and c >= col:
            grid[r][c] = common.gray()
          if diag > mydiag and mydiag >= linediag and r >= row and c <= col:
            grid[r][c] = common.gray()
          if linediag < diag and linediag == mydiag + 2: output[r][c] = color
          if linediag > diag and linediag == mydiag - 2: output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(diag=0, rows=[3], cols=[5], color=7),
      generate(diag=-5, rows=[4], cols=[5], color=9),
      generate(diag=1, rows=[3, 7], cols=[4, 3], color=2),
  ]
  test = [
      generate(diag=-1, rows=[1, 8], cols=[4, 4], color=1),
  ]
  return {"train": train, "test": test}
