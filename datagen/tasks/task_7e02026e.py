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
    gsize: The width and height of the square field.
  """

  def draw():
    grid, output = common.grids(gsize, gsize)
    for i, color in enumerate(colors):
      output[i // gsize][i % gsize] = grid[i // gsize][i % gsize] = color
    num_matches = 0
    for row in range(1, gsize - 1):
      for col in range(1, gsize - 1):
        good = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
          if grid[row + dr][col + dc]: good = False
        if not good: continue
        num_matches += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
          output[row + dr][col + dc] = 3
    return grid, output, num_matches

  if colors is None:
    if gsize is None: gsize = common.randint(10, 18)
    expected_matches = common.randint(2, 5)
    for _ in range(200):
      colors = [8 if common.randint(0, 1) else 0
                for _ in range(gsize * gsize)]
      _, _, num_matches = draw()
      if num_matches == expected_matches: break
    else:
      # Guaranteed finite fallback: carve well-separated empty crosses from an
      # azure field.  Spacing their centers by three creates no extra crosses.
      colors = [8 for _ in range(gsize * gsize)]
      fallback_centers = [(row, col)
                          for row in range(1, gsize - 1, 3)
                          for col in range(1, gsize - 1, 3)]
      for row, col in fallback_centers[:expected_matches]:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
          colors[(row + dr) * gsize + col + dc] = 0
  elif gsize is None:
    gsize = 12

  # Input: a square field of azure (8) and background (0) cells.
  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color

  # Solve: every interior cell whose plus-shape (itself + 4 orthogonal
  # neighbours) is entirely empty is an "empty cross"; scan them in row order.
  centers = []
  for row in range(1, gsize - 1):
    for col in range(1, gsize - 1):
      good = True
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
        if grid[row + dr][col + dc]: good = False
      if good: centers.append((row, col))

  output = common.deepcopy(grid)

  def mark_cross(i):
    """Paints the i-th empty plus-shape (row-scan order) green."""
    if i >= len(centers): return
    row, col = centers[i]
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
      output[row + dr][col + dc] = common.green()

  # num_matches == expected_matches in [2, 5] for sampled colors, and <= 5 for
  # every validate() example, so five stamps cover all live crosses.
  mark_cross(0)
  mark_cross(1)
  mark_cross(2)
  mark_cross(3)
  mark_cross(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 0, 8, 8, 8, 8, 0, 8, 0, 8, 8, 8,
                       0, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8,
                       8, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 8, 0, 0, 8, 8, 0, 0, 0, 8, 0, 0,
                       8, 0, 8, 8, 0, 0, 8, 8, 0, 0, 8, 8,
                       8, 8, 8, 0, 8, 8, 0, 0, 8, 8, 8, 8,
                       8, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                       0, 8, 0, 8, 0, 8, 0, 0, 0, 8, 8, 0,
                       0, 8, 0, 8, 0, 0, 0, 8, 8, 0, 8, 8,
                       8, 8, 8, 8, 0, 0, 0, 0, 8, 0, 8, 0,
                       0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 0,
                       8, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8]),
      generate(colors=[8, 0, 0, 8, 0, 0, 0, 8, 8, 0, 8, 0,
                       8, 0, 8, 0, 0, 0, 8, 0, 0, 8, 0, 0,
                       0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 0, 8,
                       0, 8, 0, 8, 0, 0, 8, 0, 8, 8, 0, 0,
                       8, 0, 0, 8, 0, 0, 0, 8, 8, 8, 0, 0,
                       8, 8, 0, 8, 0, 8, 8, 8, 8, 8, 8, 0,
                       0, 8, 0, 0, 0, 8, 0, 8, 0, 8, 8, 0,
                       0, 8, 8, 8, 8, 0, 0, 8, 0, 0, 8, 8,
                       0, 8, 0, 8, 8, 8, 8, 0, 0, 8, 8, 0,
                       0, 8, 8, 8, 8, 0, 0, 0, 8, 0, 0, 8,
                       8, 0, 8, 0, 0, 0, 0, 0, 8, 8, 0, 0,
                       0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 8, 0]),
      generate(colors=[8, 8, 0, 0, 0, 8, 0, 0, 0, 0, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 8,
                       8, 8, 8, 0, 0, 8, 8, 0, 0, 0, 8, 8,
                       0, 8, 0, 8, 8, 8, 8, 0, 0, 8, 8, 8,
                       0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 8, 8, 0, 8, 0, 8, 8, 0, 0,
                       0, 0, 8, 8, 0, 8, 8, 0, 8, 8, 8, 0,
                       8, 8, 8, 0, 8, 8, 8, 8, 0, 8, 0, 8,
                       8, 8, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8,
                       8, 8, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8,
                       8, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8,
                       8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 0, 8]),
  ]
  test = [
      generate(colors=[8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 8, 0,
                       0, 8, 8, 8, 0, 0, 8, 0, 8, 0, 0, 0,
                       8, 8, 8, 8, 0, 0, 0, 8, 8, 8, 8, 8,
                       8, 0, 0, 0, 8, 0, 8, 8, 0, 0, 8, 0,
                       0, 8, 8, 8, 0, 8, 0, 8, 8, 0, 8, 8,
                       0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 8, 8, 0, 8, 8, 0, 8, 0, 0, 0,
                       0, 8, 0, 8, 0, 0, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 8, 8, 0, 0, 8, 0, 8, 0, 0,
                       0, 0, 0, 0, 8, 0, 8, 8, 0, 8, 8, 0,
                       0, 0, 0, 8, 8, 0, 8, 8, 0, 8, 8, 8,
                       8, 8, 8, 0, 8, 0, 0, 0, 0, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
