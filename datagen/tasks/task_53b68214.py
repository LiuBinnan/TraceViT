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


def generate(height=None, rows=None, cols=None, offset=None, color=None,
             diag=None, width=10, gh=None, colors=None, num_colors=None,
             obj_height=None, obj_width=None, ncells=None, step=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the vertical offset of the pattern
    color: a digit representing a color to be used
    diag: whether the pattern should repeat diagonally
    width: the width of the input grid (= the output grid's column extent)
    gh: the output grid's row extent (and the vertical-tiling repeat count);
      defaults to width so the original square output is reproduced exactly
    colors: optional per-cell colors for the repeated pattern
    num_colors: the number of foreground colors to use in random patterns
    obj_height: the repeated pattern's bounding-box height
    obj_width: the repeated pattern's bounding-box width
    ncells: the number of cells in the repeated pattern
    step: optional horizontal drift per vertical repetition
  """
  # gw = output/input column extent; gh = output row extent (= tiling count).
  gw = width
  if gh is None:
    gh = 10  # rule: output row extent is fixed at 10 (re_arc generator+verifier)
  if height is None:
    height = common.randint(2, max(2, min(6, gh - 1)))
    max_obj_height = max(1, height // 2)
    max_obj_width = max(1, gw // 2 - 1)
    if obj_height is None:
      obj_height = common.randint(1, max_obj_height)
    if obj_width is None:
      obj_width = common.randint(1, max_obj_width)
    obj_height = min(max(1, obj_height), max_obj_height)
    obj_width = min(max(1, obj_width), max_obj_width)
    area = obj_height * obj_width
    if ncells is None:
      ncells = common.randint(1, area)
    ncells = min(max(1, ncells), area)
    if num_colors is None:
      num_colors = common.randint(1, min(9, ncells))
    num_colors = min(max(1, num_colors), 9, ncells)
    palette = common.random_colors(num_colors)
    cells = [(r, c) for r in range(obj_height) for c in range(obj_width)]
    cells = common.sample(cells, ncells)
    rows, cols, colors = [], [], []
    for idx, (row, col) in enumerate(cells):
      rows.append(row)
      cols.append(col)
      colors.append(palette[idx] if idx < num_colors else common.choice(palette))
    offset, color = common.randint(0, gw // 2), colors[0]
    diag = 0
    if step is None:
      step = common.randint(0, obj_width // 2 + 1)

  if colors is None:
    colors = [color] * len(rows)
  grid, output = common.grid(gw, height), common.grid(gw, gh)
  wide, tall = max(cols) + 1, max(rows) + 1
  for dr in range(gh):  # vertical tiling count = output row extent
    horizontal_step = step if step is not None else (wide - 1) * diag
    for row, col, cell_color in zip(rows, cols, colors):
      r = dr * tall + row
      c = dr * horizontal_step + col + offset
      common.draw(grid, r, c, cell_color)
      common.draw(output, r, c, cell_color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=6, rows=[0, 0, 0, 1], cols=[0, 1, 2, 2], offset=0,
               color=1, diag=1),
      generate(height=5, rows=[0], cols=[0], offset=2, color=3, diag=0),
      generate(height=8, rows=[0, 1, 2, 2], cols=[1, 1, 0, 2], offset=0,
               color=2, diag=0),
  ]
  test = [
      generate(height=8, rows=[0, 1], cols=[1, 0], offset=3, color=6, diag=0),
      generate(height=5, rows=[0, 0, 0, 1, 1], cols=[0, 1, 2, 0, 2], offset=1,
               color=8, diag=0),
  ]
  return {"train": train, "test": test}
