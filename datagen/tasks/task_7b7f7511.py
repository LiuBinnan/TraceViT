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


def _painted_cells(size, num_fg):
  """A length-`size` list of cell colors: one background plus `num_fg`
  foreground colors, each claiming a random count of the remaining cells
  (re_arc's fill shape, capped to the 1-9 palette this task uses)."""
  num_fg = min(8, max(1, num_fg))
  palette = common.random_colors(num_fg + 1)
  cells = [palette[0]] * size
  remaining = list(range(size))
  for color in palette[1:]:
    if not remaining:
      break
    count = min(len(remaining), common.randint(1, max(1, len(remaining) // num_fg)))
    chosen = common.sample(remaining, count)
    chosen_set = set(chosen)
    for index in chosen:
      cells[index] = color
    remaining = [index for index in remaining if index not in chosen_set]
  return cells


def _left_right_symmetric(cells, width, height):
  """Whether the width*height grid (row-major `cells`) has equal left and right
  halves under verify_7b7f7511's split (middle column dropped when odd)."""
  half = width // 2
  offset = half + width % 2
  for r in range(height):
    base = r * width
    for c in range(half):
      if cells[base + c] != cells[base + offset + c]:
        return False
  return True


def _break_symmetry(cells, width):
  """Recolor the first mirror-paired cells with two distinct colors so the grid
  is no longer left-right symmetric (a forced-asymmetry fallback)."""
  offset = width // 2 + width % 2
  two = common.random_colors(2)
  cells = list(cells)
  cells[0], cells[offset] = two[0], two[1]
  return cells


def generate(width=None, height=None, vert=None, colors=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the output grid
    height: the height of the output grid
    vert: whether to duplicate vertically
    colors: the colors of the pixels to be placed
    num_colors: how many foreground colors to scatter (background excluded)
  """
  if width is None:
    vert = common.randint(0, 1)
    # Size-decouple: independent height/width draws. The duplicated dimension
    # is doubled to build the input, so cap it at 15 (input stays <= 30); the
    # other dimension runs to 30 -- mirrors re_arc's (h in [2,30], w in [2,15]).
    if vert:
      width, height = common.randint(2, 30), common.randint(2, 15)
    else:
      width, height = common.randint(2, 15), common.randint(2, 30)
    size = width * height
    if num_colors is None:
      num_colors = common.randint(1, max(1, min(8, size - 1)))
    colors = _painted_cells(size, num_colors)
    # A vertical duplicate that is also left-right symmetric is ambiguous:
    # verify_7b7f7511 tests the horizontal split first and would mis-solve it.
    # Re-draw (then force-break) until the grid is left-right asymmetric.
    if vert:
      attempts = 0
      while _left_right_symmetric(colors, width, height) and attempts < 64:
        colors = _painted_cells(size, num_colors)
        attempts += 1
      if _left_right_symmetric(colors, width, height):
        colors = _break_symmetry(colors, width)

  grid = common.grid(width * (1 if vert else 2), height * (2 if vert else 1))
  output = common.grid(width, height)
  dr, dc = height if vert else 0, 0 if vert else width
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r + dr][c + dc] = grid[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=4, vert=0,
               colors=[1, 1, 3, 2, 1, 1, 3, 3, 3, 3, 1, 1, 2, 3, 1, 1]),
      generate(width=3, height=3, vert=0, colors=[4, 4, 4, 6, 4, 8, 6, 6, 8]),
      generate(width=2, height=3, vert=1, colors=[2, 3, 3, 2, 4, 4]),
  ]
  test = [
      generate(width=3, height=4, vert=1,
               colors=[5, 4, 5, 4, 5, 4, 6, 6, 4, 2, 6, 2]),
  ]
  return {"train": train, "test": test}
