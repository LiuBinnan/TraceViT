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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    offset=None,
    color=None,
    flip=None,
    num_colors=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the offset of the pattern
    color: a digit representing a color to be used
    flip: whether to flip the pattern
    num_colors: the number of foreground colors to use
  """
  sampled = rows is None
  if rows is None:
    if width is None:
      width = common.randint(4, 30)
    if height is None:
      height = common.randint(8, 30)
    motif_height = common.randint(2, max(2, height // 3))
    motif_width = common.randint(2, width)
    max_cells = max(2, (motif_height * motif_width * 2) // 3)
    num_cells = common.randint(2, max_cells)
    cells = common.shuffle(common.all_pixels(motif_width, motif_height))[:num_cells]
    min_row = min(row for row, _ in cells)
    min_col = min(col for _, col in cells)
    rows = [row - min_row for row, _ in cells]
    cols = [col - min_col for _, col in cells]
    motif_height = max(rows) + 1
    if num_colors is None:
      num_colors = common.randint(1, min(9, len(rows)))
    num_colors = min(num_colors, len(rows))
    palette = common.random_colors(num_colors)
    color = common.shuffle(
        palette + [common.choice(palette) for _ in range(len(rows) - num_colors)])
    offset = common.randint(0, height - motif_height)
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  wide = max(cols) + 1
  tall = motif_height if sampled else 3
  colors = color if isinstance(color, list) else [color for _ in rows]
  for i in range(0, width, wide):
    for row, col, cell_color in zip(rows, cols, colors):
      r = offset + (row if not flip or i % 2 == 0 else tall - 1 - row)
      c = col + i
      common.draw(grid, r, c, cell_color)
      common.draw(output, r, c, cell_color)
  upper_offsets = [j for j in range(-((offset // tall) + 1) * tall, 0, tall)]
  lower_offsets = [j for j in range(tall, height, tall)]

  def reveal_offsets(offsets):
    for j in offsets:
      for i in range(0, width, wide):
        for row, col, cell_color in zip(rows, cols, colors):
          r = offset + (row if not flip or i % 2 == 0 else tall - 1 - row) + j
          c = col + i
          common.draw(output, r, c, cell_color)

  def reveal_upper_repeats():
    reveal_offsets(upper_offsets)

  def reveal_lower_repeats():
    reveal_offsets(lower_offsets)

  reveal_upper_repeats()
  reveal_lower_repeats()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=15, rows=[0, 1, 1, 1], cols=[2, 0, 1, 2],
               offset=4, color=8, flip=1),
      generate(width=12, height=10, rows=[0, 1, 1, 2], cols=[0, 0, 1, 0],
               offset=3, color=2, flip=0),
  ]
  test = [
      generate(width=13, height=14, rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 2],
               offset=3, color=1, flip=0),
  ]
  return {"train": train, "test": test}
