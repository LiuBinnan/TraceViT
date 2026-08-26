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


def generate(colors=None, rows=None, cols=None, size=3, height=None, width=None,
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_colors: the number of colors to place in the input
    density: controls how many non-majority cells are placed
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    area = width * height
    max_colors = min(10, area - 1)
    if num_colors is None:
      num_colors = common.randint(2, max_colors)
    num_colors = min(max(2, num_colors), max_colors)
    colors = common.sample(range(0, 10), num_colors)
    least_majority = area // num_colors + 1
    max_majority = area - num_colors + 1
    max_minority = area - least_majority
    min_minority = num_colors - 1
    if density is None:
      minority_count = common.randint(min_minority, max_minority)
    else:
      density = min(max(0, density), 100)
      minority_count = min_minority + (
          density * (max_minority - min_minority)) // 100
    majority_count = area - minority_count
    counts = [1 for _ in range(num_colors - 1)]
    for _ in range(minority_count - len(counts)):
      candidates = [
          idx for idx, count in enumerate(counts)
          if count < majority_count - 1
      ]
      if not candidates:
        break
      counts[common.choice(candidates)] += 1
    majority_count = area - sum(counts)
    pixels = common.shuffle(common.all_pixels(width, height))
    rows, cols = zip(*pixels)
    placements = [colors[0]] * majority_count
    for color, count in zip(colors[1:], counts):
      placements.extend([color] * count)
    placements = common.shuffle(placements)
    grid = common.grid(width, height, 0)
    for (row, col), color in zip(pixels, placements):
      grid[row][col] = color
  else:
    grid = common.grid(width, height, 0)
    grid[rows[0]][cols[0]] = colors[0]
    grid[rows[1]][cols[1]] = colors[0]
    grid[rows[2]][cols[2]] = colors[0]
    grid[rows[3]][cols[3]] = colors[1]
    grid[rows[4]][cols[4]] = colors[1]
    grid[rows[5]][cols[5]] = colors[2]
    grid[rows[6]][cols[6]] = colors[3]
    grid[rows[7]][cols[7]] = colors[4]
    grid[rows[8]][cols[8]] = colors[5]
  output = [row[:] for row in grid]
  output = common.grid(width, height)
  for r, c in [(r, c) for r in range(height) for c in range(width)
               if grid[r][c] == colors[0]]:
    output[r][c] = colors[0]
  output = common.grid(width, height, colors[0])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 3, 0, 8, 6, 6],
               rows=[0, 0, 1, 1, 2, 2, 0, 1, 2],
               cols=[0, 1, 1, 2, 1, 2, 2, 0, 0]),
      generate(colors=[9, 1, 4, 6, 8, 8],
               rows=[0, 2, 2, 1, 1, 2, 0, 0, 1],
               cols=[2, 0, 2, 0, 2, 1, 0, 1, 1]),
      generate(colors=[6, 4, 1, 9, 8, 8],
               rows=[0, 1, 2, 0, 1, 1, 0, 2, 2],
               cols=[1, 0, 2, 0, 1, 2, 2, 0, 1]),
  ]
  test = [
      generate(colors=[8, 6, 0, 3, 4, 9],
               rows=[0, 0, 2, 0, 1, 2, 2, 1, 1],
               cols=[0, 1, 0, 2, 1, 2, 1, 0, 2]),
  ]
  return {"train": train, "test": test}
