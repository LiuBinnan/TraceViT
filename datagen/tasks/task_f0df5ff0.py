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

  def draw():
    grid, output = common.grids(gsize, gsize)
    # First, draw blue squares.
    for i, color in enumerate(colors):
      if color == 1: common.rect(output, 3, 3, i // gsize - 1, i % gsize - 1, 1)
    # Second, draw confetti.
    for i, color in enumerate(colors):
      if color: output[i // gsize][i % gsize] = grid[i // gsize][i % gsize] = color
    # Third, make sure there are at least three pixels showing per square.
    for i, color in enumerate(colors):
      if color != 1: continue
      num_blue = 0
      for row in [-1, 0, 1]:
        for col in [-1, 0, 1]:
          if output[i // gsize + row][i % gsize + col] == 1: num_blue += 1
      if num_blue < 3: return None, None
    return grid, output

  if colors is None:
    if gsize is None:
      gsize = common.randint(12, 28)
    subset = common.choices(list(range(2, 10)), 6)
    max_boxes = min(10, max(3, gsize * gsize // 28))
    num_boxes = common.randint(2, max_boxes)
    while True:
      for _ in range(500):
        colors = [common.randint(0, 1) for _ in range(gsize * gsize)]
        colors = [common.choice(subset) if color else 0 for color in colors]
        brows = [common.randint(0, gsize - 3) for _ in range(num_boxes)]
        bcols = [common.randint(0, gsize - 3) for _ in range(num_boxes)]
        lengths = [3] * num_boxes
        if common.overlaps(brows, bcols, lengths, lengths): continue
        for brow, bcol in zip(brows, bcols):
          colors[(brow + 1) * gsize + bcol + 1] = 1
        grid, _ = draw()
        if grid: break
      else:
        num_boxes = common.randint(2, max_boxes)
        continue
      break
  elif gsize is None:
    gsize = 15

  # Lay down the confetti input, then complete each hidden 3x3 blue square.
  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    if color: grid[i // gsize][i % gsize] = color
  output = common.deepcopy(grid)
  centers = [(i // gsize, i % gsize) for i, color in enumerate(colors) if color == 1]

  def reveal_square(j):
    """Completes blue square j: paints the black cells of its 3x3 footprint."""
    if j >= len(centers): return
    row, col = centers[j]
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        r, c = row + dr, col + dc
        if 0 <= r < gsize and 0 <= c < gsize and output[r][c] == 0:
          output[r][c] = 1

  reveal_square(0)
  reveal_square(1)
  reveal_square(2)
  reveal_square(3)
  reveal_square(4)
  reveal_square(5)
  reveal_square(6)
  reveal_square(7)
  for j in range(8, len(centers)):
    reveal_square(j)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 6, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 4,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 6, 0, 4, 0, 0,
                       6, 3, 0, 1, 0, 4, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 4, 0, 6, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0,
                       6, 0, 3, 0, 0, 0, 0, 0, 0, 3, 2, 2, 0, 0, 4,
                       4, 2, 0, 2, 0, 2, 0, 0, 0, 0, 6, 0, 0, 6, 0,
                       0, 0, 0, 0, 2, 6, 0, 6, 0, 0, 4, 0, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 4, 0, 0, 0, 4, 6, 0, 0, 0,
                       0, 0, 0, 6, 0, 6, 0, 0, 3, 3, 4, 0, 6, 6, 0,
                       4, 6, 0, 3, 1, 3, 0, 0, 4, 0, 0, 2, 6, 0, 0,
                       0, 0, 3, 2, 0, 4, 0, 6, 0, 0, 4, 3, 6, 0, 0,
                       0, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 3, 0, 3, 0, 0, 2, 2, 0,
                       6, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 4, 3,
                       0, 0, 0, 0, 0, 3, 4, 0, 0, 2, 0, 0, 0, 0, 0]),
      generate(colors=[3, 0, 0, 0, 0, 0, 0, 9, 2, 3, 0, 2, 3, 3, 0,
                       2, 2, 2, 3, 0, 0, 3, 5, 7, 0, 0, 0, 2, 7, 0,
                       0, 3, 2, 2, 0, 0, 0, 7, 0, 5, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 9, 0, 0, 2, 9, 2,
                       8, 0, 0, 3, 0, 0, 1, 2, 8, 2, 0, 0, 0, 0, 0,
                       3, 0, 0, 3, 2, 0, 0, 0, 7, 0, 2, 0, 3, 0, 0,
                       0, 0, 3, 0, 0, 0, 3, 0, 0, 5, 6, 0, 2, 0, 0,
                       0, 1, 0, 2, 3, 6, 0, 0, 2, 3, 0, 2, 0, 6, 0,
                       0, 2, 8, 0, 3, 0, 0, 0, 6, 0, 7, 0, 0, 3, 0,
                       0, 2, 3, 0, 8, 0, 0, 3, 0, 1, 0, 0, 6, 0, 0,
                       7, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 6, 7, 0,
                       0, 0, 2, 0, 5, 2, 0, 0, 0, 7, 0, 0, 0, 0, 0,
                       0, 9, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0,
                       0, 0, 2, 0, 2, 3, 3, 0, 0, 0, 1, 0, 0, 6, 2,
                       0, 2, 9, 0, 0, 5, 2, 3, 0, 0, 0, 0, 2, 0, 0]),
      generate(colors=[3, 9, 0, 0, 0, 0, 0, 0, 0, 8, 3, 9, 3, 0, 8,
                       0, 0, 0, 4, 0, 4, 0, 0, 3, 0, 2, 7, 7, 0, 2,
                       0, 3, 3, 0, 9, 0, 9, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 0, 9, 0, 4, 0, 3, 0, 3, 3, 0, 1, 0,
                       0, 1, 0, 0, 8, 8, 0, 3, 0, 2, 9, 3, 0, 0, 0,
                       0, 9, 0, 8, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 3,
                       0, 0, 7, 2, 2, 4, 7, 0, 9, 0, 0, 0, 0, 0, 8,
                       0, 4, 0, 0, 7, 0, 0, 0, 8, 0, 3, 3, 2, 7, 0,
                       0, 3, 3, 0, 2, 0, 1, 0, 2, 3, 3, 0, 0, 0, 4,
                       0, 0, 0, 3, 0, 8, 0, 0, 0, 7, 0, 3, 0, 1, 0,
                       0, 8, 0, 0, 3, 0, 9, 9, 0, 0, 7, 3, 9, 0, 0,
                       4, 4, 3, 0, 3, 0, 7, 8, 0, 4, 0, 7, 3, 0, 9,
                       7, 0, 1, 3, 3, 0, 7, 0, 1, 7, 0, 0, 4, 0, 9,
                       3, 0, 0, 0, 7, 8, 8, 0, 0, 8, 0, 9, 0, 0, 0,
                       0, 0, 7, 0, 0, 9, 8, 0, 0, 4, 8, 3, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 7, 0, 0, 6, 0, 7, 0, 0, 0, 0, 0, 3,
                       2, 0, 4, 0, 3, 7, 0, 0, 7, 0, 7, 0, 0, 0, 8,
                       0, 0, 0, 7, 8, 0, 6, 2, 7, 0, 1, 0, 2, 7, 2,
                       0, 1, 0, 0, 2, 0, 0, 2, 6, 0, 0, 0, 0, 7, 8,
                       6, 0, 0, 6, 0, 1, 0, 0, 0, 2, 0, 0, 8, 6, 4,
                       0, 0, 4, 6, 6, 0, 0, 4, 8, 0, 0, 8, 0, 8, 7,
                       8, 7, 6, 0, 0, 0, 0, 7, 7, 4, 4, 8, 0, 0, 7,
                       3, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 7, 0, 8, 0,
                       0, 0, 8, 6, 8, 6, 7, 6, 1, 6, 6, 0, 4, 0, 7,
                       0, 8, 7, 0, 7, 8, 0, 7, 0, 8, 0, 0, 8, 0, 4,
                       4, 4, 0, 0, 0, 3, 0, 0, 2, 0, 0, 3, 8, 4, 8,
                       0, 0, 8, 0, 1, 0, 8, 3, 7, 6, 7, 8, 0, 8, 7,
                       0, 0, 0, 0, 8, 0, 0, 6, 0, 3, 0, 0, 3, 0, 0,
                       0, 6, 0, 0, 0, 0, 6, 3, 1, 0, 3, 0, 0, 1, 3,
                       4, 6, 0, 0, 0, 0, 8, 0, 0, 0, 2, 2, 0, 0, 6]),
  ]
  return {"train": train, "test": test}
