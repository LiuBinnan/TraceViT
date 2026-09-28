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


def generate(colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    gsize: The width and height of the square grid.
  """

  if colors is None:
    if gsize is None:
      gsize = common.randint(10, 16)
    # Choose the colors along the side.
    height = common.randint(gsize - 3, gsize - 2)
    row = start = common.randint(1, gsize - 1 - height)
    subset = common.random_colors(common.randint(2, 4), exclude=[5])
    segment_max = 4 if gsize == 10 else height - len(subset) + 1
    while True:
      segments = [common.randint(1, segment_max) for _ in subset]
      if sum(segments) == height: break
    # Draw the side.
    grid = common.grid(gsize, gsize)
    for color, segment in zip(subset, segments):
      for _ in range(segment):
        grid[row][0] = color
        row += 1
    # Draw the grey shape.
    width = common.randint(3, gsize // 2)
    while True:
      if common.randint(0, 1):
        length = common.randint(2, width)
        pos = common.randint(0, width - length)
        row = common.randint(0, height - 1)
        for col in range(pos, pos + length):
          grid[start + row][3 + col] = 5
      else:
        length = common.randint(2, height)
        pos = common.randint(0, height - length)
        col = common.randint(0, width - 1)
        for row in range(pos, pos + length):
          grid[start + row][3 + col] = 5
      # Check if every row has grey.
      good = True
      for row in range(start, start + height):
        see_grey = False
        for col in range(gsize):
          if grid[row][col] == 5: see_grey = True
        if not see_grey: good = False
      if not good: continue
      # Check if it's connected.
      pixels = []
      for row in range(gsize):
        for col in range(gsize):
          if grid[row][col] == 5: pixels.append((row, col))
      if common.connected(pixels): break
    colors = common.flatten(grid)
  elif gsize is None:
    gsize = 10

  # Rebuild the input grid from the flattened colors (the side bar plus the grey
  # shape).
  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color

  # Solve forward: the output starts as the input, then the grey shape is
  # recolored one bar segment at a time -- each left-edge color floods across
  # the shape cells sharing its rows.
  output = common.deepcopy(grid)
  bar_colors = []
  for r in range(gsize):
    c = grid[r][0]
    if c and (not bar_colors or bar_colors[-1] != c):
      bar_colors.append(c)

  def reveal_color(k):
    """Floods bar color k across every non-background cell in its rows.

    A no-op when k is past the segment count, so the unrolled calls below cover
    the hard maximum of 4 side colors (a subset of size 2..4).
    """
    nonlocal output
    if k >= len(bar_colors):
      return
    bar_color = bar_colors[k]
    for row in range(gsize):
      if grid[row][0] != bar_color:
        continue
      for col in range(gsize):
        if output[row][col]:
          output[row][col] = bar_color

  reveal_color(0)
  reveal_color(1)
  reveal_color(2)
  reveal_color(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       9, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       9, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       6, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       6, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       6, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       8, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       8, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       2, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 0, 5, 5, 0, 5, 0, 0,
                       2, 0, 0, 5, 5, 5, 5, 5, 0, 0,
                       3, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       3, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       3, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       7, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
