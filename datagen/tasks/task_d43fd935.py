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


def generate(rows=None, cols=None, colors=None, boxrow=None, boxcol=None,
             size=10, height=None, width=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    boxrow: the row where the box is placed
    boxcol: the column where the box is placed
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_colors: the number of non-green foreground colors to sample
    density: the number of sampled foreground pixels before line completion
  """

  if height is None: height = size
  if width is None: width = size

  def draw(grid, output):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      grid[boxrow + dr][boxcol + dc] = common.green()
      output[boxrow + dr][boxcol + dc] = common.green()
    for row, col, color in zip(rows, cols, colors):
      output[row][col] = grid[row][col] = color
      if row in [boxrow, boxrow + 1]:
        c, dc = col, -1 if col > boxcol else 1
        while output[row][c + dc] != common.green():
          output[row][c + dc], c = color, c + dc
      if col in [boxcol, boxcol + 1]:
        r, dr = row, -1 if row > boxrow else 1
        while output[r + dr][col] != common.green():
          output[r + dr][col], r = color, r + dr
    for dr in range(-1, 3):
      for dc in range(-1, 3):
        if grid[boxrow + dr][boxcol + dc] in [common.black(), common.green()]:
          continue
        return False
    return True

  if rows is None:
    while True:
      boxrow, boxcol = common.randint(2, height - 3), common.randint(2, width - 3)
      if num_colors is None:
        num_colors = common.randint(1, 8)
      num_colors = max(1, min(8, num_colors))
      color_list = common.random_colors(num_colors, exclude=[common.green()])
      protected = set()
      for row in range(boxrow - 1, boxrow + 3):
        for col in range(boxcol - 1, boxcol + 3):
          protected.add((row, col))
      candidates, noise_candidates = [], []
      line_by_side = {"up": [], "down": [], "left": [], "right": []}
      for row in range(height):
        for col in range(width):
          if (row, col) in protected:
            continue
          candidates.append((row, col))
          if row in [boxrow, boxrow + 1]:
            if col < boxcol:
              line_by_side["left"].append((row, col))
            elif col > boxcol + 1:
              line_by_side["right"].append((row, col))
          elif col in [boxcol, boxcol + 1]:
            if row < boxrow:
              line_by_side["up"].append((row, col))
            elif row > boxrow + 1:
              line_by_side["down"].append((row, col))
          else:
            noise_candidates.append((row, col))
      sides = [side for side, pixels in line_by_side.items() if pixels]
      if not sides:
        continue
      max_density = max(1, len(candidates) // 4)
      if density is None:
        count = common.randint(1, max_density)
      else:
        count = density
      count = max(num_colors, min(len(candidates), max(1, count)))
      count = min(len(noise_candidates) + min(4, len(sides)), count)
      line_count = common.randint(1, min(4, len(sides), count))
      pixels = [
          common.choice(line_by_side[side])
          for side in common.sample(sides, line_count)
      ]
      remaining = [pixel for pixel in noise_candidates if pixel not in pixels]
      pixels.extend(common.sample(remaining, min(len(remaining), count - line_count)))
      pixels = common.shuffle(pixels)
      rows, cols, colors = [], [], []
      for idx, (row, col) in enumerate(pixels):
        rows.append(row)
        cols.append(col)
        if idx < num_colors:
          colors.append(color_list[idx])
        else:
          colors.append(color_list[common.randint(0, num_colors - 1)])
      grid, output = common.grids(width, height)
      if draw(grid, output) and grid != output: break

  grid, output = common.grids(width, height)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    grid[boxrow + dr][boxcol + dc] = common.green()
    output[boxrow + dr][boxcol + dc] = common.green()
  for row, col, color in zip(rows, cols, colors):
    output[row][col] = grid[row][col] = color
  for row, col, color in zip(rows, cols, colors):
    if row not in [boxrow, boxrow + 1]: continue
    c, dc = col, -1 if col > boxcol else 1
    while output[row][c + dc] != common.green():
      output[row][c + dc], c = color, c + dc
  for row, col, color in zip(rows, cols, colors):
    if col not in [boxcol, boxcol + 1]: continue
    r, dr = row, -1 if row > boxrow else 1
    while output[r + dr][col] != common.green():
      output[r + dr][col], r = color, r + dr
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 3, 6, 7, 8, 9], cols=[0, 8, 8, 7, 6, 2, 4],
               colors=[1, 6, 1, 6, 6, 6, 1], boxrow=3, boxcol=2),
      generate(rows=[0, 0, 2, 2, 5, 6, 7, 8, 9, 9],
               cols=[1, 6, 3, 9, 1, 8, 3, 1, 5, 9],
               colors=[7, 8, 7, 8, 8, 8, 8, 7, 7, 7], boxrow=2, boxcol=5),
      generate(rows=[1, 2, 5, 9], cols=[4, 1, 9, 1], colors=[1, 1, 1, 1],
               boxrow=6, boxcol=4),
  ]
  test = [
      generate(rows=[0, 1, 2, 3, 4, 6, 8, 9, 9],
               cols=[3, 0, 7, 0, 7, 0, 7, 3, 5],
               colors=[2, 2, 2, 6, 6, 6, 2, 6, 6], boxrow=6, boxcol=2),
  ]
  return {"train": train, "test": test}
