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


def generate(width=None, height=None, linecols=None, linecolors=None,
             rows=None, cols=None, colors=None, xpose=None, linecount=None,
             rowcount=None, dotcount=None, noise_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    linecols: a list of horizontal coordinates where lines should be placed
    linecolors: a list of digits representing colors to be used for the lines
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used for the pixels
    xpose: whether to transpose the input grid
    linecount: number of colored guide lines to sample
    rowcount: number of rows that receive colored pixels
    dotcount: number of colored pixels per selected row
    noise_colors: number of irrelevant pixel colors to add
  """
  if width is None:
    width, height = common.randint(8, 30), common.randint(8, 30)
    # Choose re_arc-style line locations: up to width//5, spaced apart.
    max_lines = max(1, min(9, width // 5))
    if linecount is None:
      linecount = common.randint(1, max_lines)
    else:
      linecount = max(1, min(linecount, max_lines))
    locopts, linecols = list(range(width)), []
    for _ in range(linecount):
      if not locopts: break
      linecol = common.choice(locopts)
      linecols.append(linecol)
      locopts = [c for c in locopts if abs(c - linecol) > 2]
    linecols.sort()

    # Draw line colors and a variable pool of irrelevant pixel colors.
    max_noise_colors = 9 - len(linecols)
    if noise_colors is None:
      noise_colors = common.randint(0, max_noise_colors)
    else:
      noise_colors = max(0, min(noise_colors, max_noise_colors))
    color_pool = common.random_colors(len(linecols) + noise_colors)
    linecolors = color_pool[:len(linecols)]
    pixelcolors = color_pool

    # Choose colored pixels by rows and per-row dots, as in re_arc.
    rowcount = common.randint(1, height) if rowcount is None else rowcount
    rowcount = max(1, min(rowcount, height))
    dotcols = [c for c in range(width) if c not in linecols]
    max_dots = max(0, min(len(pixelcolors), (len(dotcols) // 2) - 1))
    rows, cols, colors = [], [], []
    if max_dots:
      chosen_rows = common.sample(list(range(height)), rowcount)
      for row in chosen_rows:
        ndots = common.randint(1, max_dots) if dotcount is None else dotcount
        ndots = max(1, min(ndots, max_dots))
        for col, color in zip(common.sample(dotcols, ndots),
                              common.sample(pixelcolors, ndots)):
          rows.append(row)
          cols.append(col)
          colors.append(color)
    xpose = common.randint(0, 1)

  raw_grid, raw_output = common.grids(width, height)
  output = common.transpose(raw_output) if xpose else raw_output
  for linecol, linecolor in zip(linecols[:1], linecolors[:1]):
    for r in range(height):
      raw_output[r][linecol] = raw_grid[r][linecol] = linecolor
    output = common.transpose(raw_output) if xpose else raw_output
  for linecol, linecolor in zip(linecols[1:], linecolors[1:]):
    for r in range(height):
      raw_output[r][linecol] = raw_grid[r][linecol] = linecolor
    output = common.transpose(raw_output) if xpose else raw_output
  for r, c, color in zip(rows, cols, colors):
    raw_grid[r][c] = color
    for linecol, linecolor in zip(linecols, linecolors):
      if color != linecolor: continue
      raw_output[r][linecol + (-1 if c < linecol else 1)] = color
    output = common.transpose(raw_output) if xpose else raw_output
  grid = common.transpose(raw_grid) if xpose else raw_grid
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=18, linecols=[3, 12], linecolors=[3, 4],
               rows=[3, 3, 7, 10, 11], cols=[1, 6, 9, 7, 16],
               colors=[4, 3, 4, 2, 3], xpose=0),
      generate(width=15, height=14, linecols=[3, 10], linecolors=[2, 1],
               rows=[2, 3, 6, 9, 10, 10], cols=[13, 0, 7, 1, 5, 13],
               colors=[1, 2, 2, 4, 1, 2], xpose=1),
      generate(width=15, height=16, linecols=[5], linecolors=[8],
               rows=[3, 3, 7, 11, 12], cols=[1, 12, 1, 8, 13],
               colors=[1, 8, 8, 8, 1], xpose=1),
  ]
  test = [
      generate(width=26, height=19, linecols=[4, 11, 20], linecolors=[2, 3, 4],
               rows=[2, 4, 5, 7, 9, 10, 11, 15, 15, 15, 17],
               cols=[16, 24, 9, 6, 13, 1, 17, 0, 8, 24, 22],
               colors=[2, 8, 8, 4, 3, 2, 8, 8, 3, 4, 3], xpose=0),
  ]
  return {"train": train, "test": test}
