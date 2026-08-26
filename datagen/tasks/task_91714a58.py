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


def generate(width=None, height=None, row=None, col=None, colors=None, size=16,
             gridh=None, gridw=None, bg_color=None, density=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the box
    height: the height of the box
    row: the row of the box
    col: the column of the box
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    gridh: the height (rows) of the grid; defaults to size
    gridw: the width (cols) of the grid; defaults to size
    bg_color: the background color for generated examples
    density: noise density as a percentage of grid area
    num_colors: total number of colors to include in generated examples
  """
  if gridh is None: gridh = size
  if gridw is None: gridw = size
  if width is None:
    if bg_color is None: bg_color = common.randint(0, 9)
    if num_colors is None: num_colors = common.randint(2, 10)
    num_colors = max(2, min(10, num_colors))
    palette = [bg_color]
    palette.extend(common.sample([c for c in range(10) if c != bg_color],
                                 num_colors - 1))
    color = common.choice([c for c in palette if c != bg_color])
    noise_colors = [c for c in palette if c not in [bg_color, color]]
    if not noise_colors: noise_colors = [bg_color]
    if density is None:
      density = common.randint(1, 50)
    noise_count = max(1, (gridw * gridh * density) // 100)
    noise_count = min(gridw * gridh, noise_count)
    while True:
      width, height = common.randint(2, 8), common.randint(2, 8)
      if width * height >= 9 and width * height <= 16: break
    row = common.randint(1, gridh - height - 1)
    col = common.randint(1, gridw - width - 1)
    while True:
      pixels = common.sample(common.all_pixels(gridw, gridh), noise_count)
      bitmap = common.grid(gridw, gridh, bg_color)
      for r, c in pixels:
        neighbor_colors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          neighbor_colors.append(common.get_pixel(bitmap, r + dr, c + dc))
        choices = [c for c in noise_colors if c not in neighbor_colors]
        if choices:
          bitmap[r][c] = common.choice(choices)
      # Make sure no two neighbors are the same color as our box.
      same_color_neighbors = False
      for r in range(gridh):
        for c in range(gridw):
          if bitmap[r][c] != color: continue
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if common.get_pixel(bitmap, r + dr, c + dc) == color:
              same_color_neighbors = True
      if same_color_neighbors: continue
      # Now draw the box.
      for r in range(row, row + height):
        for c in range(col, col + width):
          bitmap[r][c] = color
      colors = []
      for r in bitmap:
        colors.extend(r)
      # Make sure no random pixels accidentally extend the box.
      all_alike = True
      for r in range(row, row + height):
        if colors[r * gridw + col - 1] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for r in range(row, row + height):
        if colors[r * gridw + col + width] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for c in range(col, col + width):
        if colors[(row - 1) * gridw + c] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for c in range(col, col + width):
        if colors[(row + height) * gridw + c] != color: all_alike = False
      if all_alike: continue
      break
  elif bg_color is None:
    bg_color = 0

  grid, output = common.grids(gridw, gridh, bg_color)
  for r in range(gridh):
    for c in range(gridw):
      grid[r][c] = colors[r * gridw + c]
      if r < row or r >= row + height or c < col or c >= col + width: continue
      output[r][c] = grid[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=4, row=3, col=3,
               colors=[0, 0, 0, 0, 1, 1, 4, 0, 2, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0,
                       3, 5, 0, 0, 0, 9, 9, 8, 0, 4, 0, 5, 8, 1, 0, 8, 2, 8, 0,
                       0, 6, 0, 8, 5, 0, 0, 0, 8, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 1, 9, 5, 0,
                       0, 2, 0, 4, 0, 4, 0, 2, 2, 2, 0, 2, 0, 0, 7, 0, 0, 0, 0,
                       0, 3, 0, 6, 2, 2, 2, 0, 0, 0, 3, 5, 0, 7, 0, 0, 0, 7, 0,
                       4, 6, 0, 0, 4, 7, 7, 3, 0, 2, 0, 0, 7, 1, 0, 7, 0, 0, 0,
                       0, 0, 9, 7, 7, 0, 0, 0, 8, 5, 2, 1, 5, 6, 4, 9, 3, 0, 3,
                       0, 0, 0, 0, 0, 9, 4, 6, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 2,
                       0, 1, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 4, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0, 2, 0, 0, 0, 0, 0,
                       3, 0, 0, 7, 0, 2, 0, 7, 9, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       7, 0, 0, 0, 0, 0, 0, 0, 6, 5, 3, 0, 1, 0, 0, 9, 0, 0, 0,
                       2, 0, 0, 0, 1, 0, 0, 9, 0]),
      generate(width=7, height=2, row=11, col=2,
               colors=[0, 0, 7, 0, 0, 6, 0, 6, 0, 0, 0, 7, 3, 0, 0, 0, 0, 0, 3,
                       0, 0, 1, 0, 0, 8, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 9,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 8, 2, 2, 0, 2, 9, 0, 0, 0, 0,
                       1, 0, 2, 0, 0, 0, 0, 0, 5, 2, 0, 0, 7, 0, 6, 0, 0, 0, 3,
                       0, 0, 1, 0, 4, 4, 0, 3, 9, 0, 0, 0, 0, 7, 0, 2, 0, 0, 0,
                       0, 8, 0, 0, 0, 0, 6, 0, 0, 0, 8, 0, 0, 3, 0, 0, 0, 0, 9,
                       0, 0, 0, 4, 8, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 9, 5, 0,
                       0, 0, 0, 4, 6, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       3, 1, 0, 8, 0, 5, 9, 4, 0, 9, 3, 9, 0, 3, 0, 0, 5, 6, 7,
                       0, 5, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 7,
                       0, 0, 0, 4, 6, 6, 6, 6, 6, 6, 6, 0, 0, 4, 4, 6, 0, 2, 0,
                       5, 0, 0, 0, 0, 4, 5, 3, 0, 8, 0, 0, 0, 6, 9, 0, 0, 9, 7,
                       5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 1, 0, 8, 0, 0, 0, 0, 0,
                       1, 0, 3, 0, 0, 3, 8, 7, 0]),
      generate(width=3, height=3, row=2, col=8,
               colors=[3, 0, 0, 0, 0, 0, 6, 2, 0, 0, 0, 5, 0, 0, 0, 3, 0, 7, 0,
                       0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 8,
                       8, 0, 7, 7, 7, 0, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 7,
                       7, 7, 0, 2, 0, 5, 0, 0, 8, 0, 0, 9, 6, 1, 7, 7, 7, 7, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 6, 0, 6, 0, 0, 3, 3, 0, 0,
                       0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 8, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 6, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0, 0, 3,
                       0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 5,
                       0, 0, 4, 0, 0, 1, 7, 0, 3, 0, 0, 7, 5, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 7, 2, 0, 0, 5, 0, 0, 1, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 7, 9,
                       0, 0, 0, 5, 0, 2, 0, 3, 0]),
  ]
  test = [
      generate(width=6, height=2, row=10, col=5,
               colors=[0, 0, 1, 7, 3, 0, 0, 0, 0, 0, 1, 2, 0, 4, 7, 0, 0, 0, 0,
                       3, 0, 0, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8, 0, 1,
                       0, 0, 1, 0, 0, 0, 7, 0, 4, 8, 0, 3, 8, 0, 0, 0, 3, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 8, 0, 0, 3, 8,
                       0, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 5, 0, 7, 0, 0,
                       0, 0, 0, 0, 0, 9, 0, 0, 2, 7, 0, 7, 0, 0, 9, 4, 0, 2, 1,
                       0, 0, 0, 0, 0, 7, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 5, 0, 8, 9, 4, 0, 5, 5, 5, 5, 5, 5,
                       3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 5, 5, 5, 5, 5, 0, 1, 4,
                       0, 0, 9, 5, 2, 0, 0, 5, 1, 3, 0, 0, 6, 2, 0, 0, 1, 5, 0,
                       7, 0, 0, 0, 0, 1, 6, 0, 7, 0, 3, 0, 6, 0, 0, 0, 0, 9, 0,
                       0, 3, 7, 7, 0, 6, 0, 0, 8, 0, 0, 0, 5, 0, 0, 0, 0, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 9]),
  ]
  return {"train": train, "test": test}
