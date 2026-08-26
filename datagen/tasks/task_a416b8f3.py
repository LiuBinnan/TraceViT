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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             colors=None, num_colors=None, bg_color=None, palette_id=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of digits representing colors to be used
    num_colors: the number of foreground colors to sample
    bg_color: the background color
    palette_id: a bit mask selecting foreground colors
  """
  if width is None:
    width = common.randint(1, 15)
  if height is None:
    height = common.randint(1, 30)
  if rows is None or cols is None or idxs is None or colors is None:
    if bg_color is None:
      bg_color = common.randint(0, 9)
    cells = [(r, c) for r in range(height) for c in range(width)]
    max_colors = min(9, width * height)
    if palette_id is None and num_colors is None:
      num_colors = common.randint(0, max_colors)
    if palette_id is None:
      num_colors = max(0, min(num_colors, max_colors))
      colors = common.sample(
          [color for color in range(10) if color != bg_color], num_colors)
    else:
      colors = [
          color for color in range(10)
          if color != bg_color and palette_id & (1 << color)
      ]
      if num_colors is None:
        num_colors = len(colors)
      num_colors = max(0, min(num_colors, max_colors, len(colors)))
      colors = colors[:num_colors]
    rows, cols, idxs = [], [], []
    for idx in range(num_colors):
      count = common.randint(1, max(1, len(cells) // num_colors))
      pixels = common.sample(cells, count)
      for r, c in pixels:
        rows.append(r)
        cols.append(c)
        idxs.append(idx)
      cells = [cell for cell in cells if cell not in pixels]

  if bg_color is None:
    bg_color = 0
  grid, _ = common.grids(width, height, bg_color)
  output = common.grid(2 * width, height, bg_color)
  for r, c, idx in zip(rows, cols, idxs):
    output[r][width + c] = output[r][c] = grid[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 1, 1, 1], cols=[1, 0, 1, 2],
               idxs=[0, 0, 0, 1], colors=[5, 2]),
      generate(width=3, height=4, rows=[0, 1, 1, 2, 2, 2, 3],
               cols=[0, 0, 1, 0, 1, 2, 1], idxs=[0, 1, 0, 1, 2, 3, 2],
               colors=[3, 2, 1, 8]),
      generate(width=4, height=4,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3],
               cols=[0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 2],
               idxs=[0, 1, 2, 1, 0, 2, 0, 1, 3, 3, 4], colors=[5, 2, 3, 8, 6]),
  ]
  test = [
      generate(width=4, height=5, rows=[0, 1, 1, 2, 2, 3, 3, 3, 4],
               cols=[0, 0, 1, 1, 2, 0, 1, 2, 3],
               idxs=[0, 0, 1, 1, 2, 2, 2, 3, 3], colors=[4, 5, 6, 1]),
  ]
  return {"train": train, "test": test}
