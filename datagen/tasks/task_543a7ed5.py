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


def generate(rows=None, cols=None, widths=None, heights=None, colors=None,
             boxes=3, size=15, height=None, width=None, count=None,
             num_colors=None, bg_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    widths: a list of box widths
    heights: a list of box heights
    colors: a list of colors to be used
    boxes: the number of boxes to be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    count: the requested number of boxes sampled for random examples
    num_colors: the number of object colors sampled for random examples
    bg_color: the background color sampled for random examples
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    while True:
      if count is None:
        count = common.randint(1, max(1, (width * height) // 25))
      if bg_color is None:
        bg_color = common.sample([0, 1, 2, 5, 6, 7, 8, 9], 1)[0]
      if num_colors is None:
        num_colors = common.randint(1, 7)
      obj_colors = [color for color in [0, 1, 2, 5, 6, 7, 8, 9]
                    if color != bg_color]
      obj_colors = common.sample(obj_colors, min(num_colors, len(obj_colors)))
      rows, cols, widths, heights, colors = [], [], [], [], []
      newrows, newcols, newwidths, newheights = [], [], [], []
      trials, max_trials = 0, 12 * count
      while len(colors) < count and trials <= max_trials:
        trials += 1
        bw, bh = common.randint(2, 6), common.randint(2, 6)
        if height - bh - 1 < 1 or width - bw - 1 < 1: continue
        row = common.randint(1, height - bh - 1)
        col = common.randint(1, width - bw - 1)
        if common.overlaps(rows + [row], cols + [col],
                           widths + [bw], heights + [bh], 2):
          continue
        rows, cols = rows + [row], cols + [col]
        widths, heights = widths + [bw], heights + [bh]
        colors.append(obj_colors[common.randint(0, len(obj_colors) - 1)])
        if bw <= 2 or bh <= 2 or common.randint(1, 10) == 1: continue
        w, t = common.randint(1, bw - 2), common.randint(1, bh - 2)
        r = row + common.randint(1, bh - t - 1)
        c = col + common.randint(1, bw - w - 1)
        newrows, newcols = newrows + [r], newcols + [c]
        newwidths, newheights = newwidths + [w], newheights + [t]
      if not rows: continue
      rows, cols = rows + newrows, cols + newcols
      widths, heights = widths + newwidths, heights + newheights
      colors.extend([common.yellow()] * len(newrows))
      break

  grid, output = common.grids(
      width, height, common.cyan() if bg_color is None else bg_color)
  for row, col, bw, bh, color in zip(rows, cols, widths, heights, colors):
    for r in range(row, row + bh):
      for c in range(col, col + bw):
        grid[r][c] = (
            common.cyan() if color == common.yellow() and bg_color is None
            else bg_color if color == common.yellow() else color)
        output[r][c] = color
  for row, col, bw, bh, color in zip(rows, cols, widths, heights, colors):
    if color == common.yellow(): continue
    for r in range(row - 1, row + bh + 1):
      for c in range(col - 1, col + bw + 1):
        if r < row or r >= row + bh or c < col or c >= col + bw:
          output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [generate(rows=[2, 4, 10, 3], cols=[8, 3, 5, 9], widths=[4, 2, 4, 2],
                    heights=[5, 2, 4, 3], colors=[6, 6, 6, 4]),
           generate(rows=[1, 3, 8, 4, 9], cols=[8, 2, 8, 3, 9],
                    widths=[3, 4, 6, 1, 4], heights=[3, 4, 6, 2, 4],
                    colors=[6, 6, 6, 4, 4])]
  test = [generate(rows=[2, 3, 11, 4, 4, 12], cols=[9, 2, 4, 10, 3, 6],
                   widths=[3, 4, 7, 1, 2, 2], heights=[6, 4, 3, 3, 2, 1],
                   colors=[6, 6, 6, 4, 4, 4])]
  return {"train": train, "test": test}
