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


def generate(rows=None, cols=None, idx=None, color=None, size=3,
             height=None, width=None, ncolors=None, colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idx: the index into the pixel that should be the input grid location
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    height: the height of the mini-grid, sampled 2..5 when omitted
    width: the width of the mini-grid, sampled 2..5 when omitted
    ncolors: the number of foreground colors, sampled 1..9 when omitted
    colors: per-pixel foreground colors
    density: optional foreground-cell fraction for the mini-grid
  """
  if rows is None:
    if height is None:
      height = common.randint(2, 5)
    if width is None:
      width = common.randint(2, 5)
    cells = common.all_pixels(width, height)
    area = width * height
    if density is None:
      midpoint = area // 2
      num_cells = midpoint + common.choice([-1, 1]) * common.randint(0, midpoint)
    else:
      num_cells = round(density * area)
    num_cells = max(0, min(10, area, num_cells))
    chosen = []
    for row in range(height):
      chosen.append((row, common.randint(0, width - 1)))
    for col in range(width):
      if col not in {cc for _, cc in chosen}:
        chosen.append((common.randint(0, height - 1), col))
    chosen = list(set(chosen))
    while len(chosen) < max(num_cells, max(height, width)):
      options = [cell for cell in cells if cell not in chosen]
      chosen.append(common.choice(options))
    chosen = common.shuffle(chosen)
    rows, cols = zip(*chosen)
    idx = common.randint(0, len(rows) - 1)
    if ncolors is None:
      ncolors = common.randint(1, min(9, len(rows)))
    ncolors = max(1, min(ncolors, 9, len(rows)))
    palette = common.random_colors(ncolors)
    colors = [palette[i % ncolors] for i in range(len(rows))]
    colors = common.shuffle(colors)
    color = colors[0]

  grid = common.grid((width or size) * (width or size),
                     (height or size) * (height or size))
  for row, col, pixel_color in zip(
      rows, cols, colors if colors is not None else [color] * len(rows)):
    grid[rows[idx] * (height or size) + row][
        cols[idx] * (width or size) + col] = pixel_color
  output = [row[:] for row in grid]
  block_positions = [
      (row, col) for row, col in zip(rows, cols)
      if (row, col) != (rows[idx], cols[idx])
  ]

  def reveal_block(block_idx):
    if block_idx >= len(block_positions):
      return
    row, col = block_positions[block_idx]
    for r, c, pixel_color in zip(
        rows, cols, colors if colors is not None else [color] * len(rows)):
      output[row * (height or size) + r][
          col * (width or size) + c] = pixel_color

  reveal_block(0)
  reveal_block(1)
  reveal_block(2)
  reveal_block(3)
  reveal_block(4)
  reveal_block(5)
  reveal_block(6)
  reveal_block(7)
  reveal_block(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 2, 0], idx=0, color=8),
      generate(rows=[0, 1, 1, 2], cols=[2, 1, 2, 0], idx=1, color=7),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 1], idx=0, color=6),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2], cols=[0, 0, 1, 1, 2], idx=1, color=2),
  ]
  return {"train": train, "test": test}
