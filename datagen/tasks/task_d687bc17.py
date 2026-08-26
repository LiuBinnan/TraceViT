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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             edgecolors=None, dot_count=None, noise_count=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    edgecolors: a list of digits representing the edge colors to be used
    dot_count: the number of candidate edge-colored dots to place
    noise_count: the number of irrelevant noise pixels to place
    num_colors: the total number of input/output colors to expose
  """
  if rows is None:
    width = common.randint(5, 30) if width is None else min(30, max(5, width))
    height = common.randint(5, 30) if height is None else min(30, max(5, height))
    edgecolors = common.random_colors(4)
    bitmap = common.grid(width, height)
    cands = [(r, c) for r in range(2, height - 2)
             for c in range(2, width - 2)]
    max_dots = min(len(cands), height + height + width + width)
    if dot_count is None:
      dot_count = common.randint(1, max(1, max_dots))
    dot_count = min(max(1, dot_count), max_dots)
    dot_pixels = common.sample(cands, dot_count)
    dot_pixels_by_color = {color: [] for color in edgecolors}
    for pixel in dot_pixels:
      dot_pixels_by_color[common.choice(edgecolors)].append(pixel)

    # Use one dot for each projected row/column, mirroring the re_arc coverage
    # guard that avoids a fully saturated projection lane.
    for idx, edgecolor in enumerate(edgecolors):
      pixels = dot_pixels_by_color[edgecolor]
      if idx in [0, 2]:
        coverage = sorted({col for _row, col in pixels})
        if len(coverage) == width - 4 and width > 5:
          coverage.remove(common.choice(coverage))
        for col in coverage:
          row = common.choice([r for r, c in pixels if c == col])
          bitmap[row][col] = edgecolor
      if idx in [1, 3]:
        coverage = sorted({row for row, _col in pixels})
        if len(coverage) == height - 4 and height > 5:
          coverage.remove(common.choice(coverage))
        for row in coverage:
          col = common.choice([c for r, c in pixels if r == row])
          bitmap[row][col] = edgecolor

    noise_cands = [(r, c) for r, c in cands if not bitmap[r][c]]
    area_cap = ((height * width) - 2 * height - 2 * (width - 2)) // 2
    max_noise = min(len(noise_cands), max(0, area_cap - dot_count - 1))
    max_total_colors = min(10, 5 + max_noise)
    if num_colors is None:
      num_colors = common.randint(5, max_total_colors)
    num_colors = min(max(5, num_colors), max_total_colors)
    noise_palette_size = num_colors - 5
    if noise_palette_size:
      noise_palette = common.random_colors(noise_palette_size,
                                           exclude=edgecolors)
      if noise_count is None:
        noise_count = common.randint(noise_palette_size, max_noise)
      noise_count = min(max(noise_palette_size, noise_count), max_noise)
      noise_pixels = common.sample(noise_cands, noise_count)
      for idx, (r, c) in enumerate(noise_pixels):
        bitmap[r][c] = noise_palette[idx % len(noise_palette)]
    # Convert the bitmap back to a list of rows and columns.
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid, output = common.grids(width, height)
  for c in range(1, width - 1):
    output[0][c] = grid[0][c] = edgecolors[0]
  for row, col, color in zip(rows, cols, colors):
    if color == edgecolors[0]:
      grid[row][col] = color
      output[1][col] = color
  for r in range(1, height - 1):
    output[r][width - 1] = grid[r][width - 1] = edgecolors[1]
  for row, col, color in zip(rows, cols, colors):
    if color == edgecolors[1]:
      grid[row][col] = color
      output[row][width - 2] = color
  for c in range(1, width - 1):
    output[height - 1][c] = grid[height - 1][c] = edgecolors[2]
  for row, col, color in zip(rows, cols, colors):
    if color == edgecolors[2]:
      grid[row][col] = color
      output[height - 2][col] = color
  for r in range(1, height - 1):
    output[r][0] = grid[r][0] = edgecolors[3]
  for row, col, color in zip(rows, cols, colors):
    if color == edgecolors[3]:
      grid[row][col] = color
      output[row][1] = color
  for row, col, color in zip(rows, cols, colors):
    if color not in edgecolors:
      grid[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=10, rows=[2, 3, 4, 5, 6, 7, 7],
               cols=[10, 3, 7, 3, 5, 9, 11], colors=[3, 2, 7, 3, 8, 4, 2],
               edgecolors=[4, 3, 8, 2]),
      generate(width=12, height=12, rows=[2, 3, 4, 6, 8, 9, 9],
               cols=[9, 7, 4, 8, 3, 5, 8], colors=[7, 2, 3, 4, 8, 1, 7],
               edgecolors=[1, 4, 7, 2]),
      generate(width=11, height=14, rows=[2, 3, 4, 7, 9, 10],
               cols=[2, 8, 4, 3, 6, 2], colors=[2, 6, 8, 4, 8, 8],
               edgecolors=[6, 8, 3, 4]),
  ]
  test = [
      generate(width=17, height=14,
               rows=[2, 2, 3, 3, 5, 5, 5, 7, 9, 9, 9, 10, 10],
               cols=[7, 12, 3, 14, 6, 10, 13, 4, 5, 8, 14, 3, 11],
               colors=[8, 1, 2, 3, 1, 7, 8, 2, 6, 4, 4, 8, 1],
               edgecolors=[4, 2, 8, 1]),
  ]
  return {"train": train, "test": test}
