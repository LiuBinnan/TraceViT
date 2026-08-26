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


def generate(size=None, colors=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: a list of digits representing the colors to be used
    height: number of rows (defaults to size, for rectangular grids)
    width: number of columns (defaults to size, for rectangular grids)
  """
  if size is None:
    if height is None:
      height = common.randint(8, 22)
    if width is None:
      width = common.randint(8, 22)
    colors = []
    for _ in range(height * width):
      color = common.black() if common.randint(0, 1) else common.random_color()
      colors.append(color)
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid, output = common.grids(width, height)
  blues = []
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c] = colors[r * width + c]
      if colors[r * width + c] == common.blue():
        blues.append((r, c))
  frontier = blues[:]

  def expand_wave():
    nonlocal frontier
    next_frontier = []
    for r, c in frontier:
      for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= height or nc < 0 or nc >= width:
          continue
        if output[nr][nc] != common.black():
          continue
        output[nr][nc] = common.blue()
        next_frontier.append((nr, nc))
    frontier = next_frontier

  def finish_flood_fill():
    while frontier:
      expand_wave()

  def expand_near_blue():
    for _ in range(3):
      if frontier:
        expand_wave()

  expand_near_blue()
  finish_flood_fill()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=13,
               colors=[9, 0, 0, 0, 0, 2, 8, 0, 9, 0, 2, 0, 9, 1, 0, 0, 6, 0, 0,
                       0, 0, 0, 0, 0, 9, 5, 9, 0, 4, 9, 3, 0, 0, 5, 7, 0, 8, 0,
                       8, 0, 0, 8, 6, 0, 6, 0, 1, 0, 0, 0, 4, 1, 3, 6, 0, 1, 0,
                       3, 9, 0, 0, 4, 5, 7, 2, 0, 8, 0, 0, 0, 0, 0, 0, 7, 1, 8,
                       0, 0, 9, 0, 0, 2, 0, 0, 0, 7, 5, 7, 0, 8, 4, 0, 0, 0, 8,
                       7, 5, 0, 0, 7, 0, 0, 5, 0, 9, 9, 0, 0, 0, 0, 5, 0, 0, 5,
                       0, 0, 0, 8, 0, 0, 8, 0, 6, 5, 0, 0, 0, 0, 9, 0, 4, 0, 0,
                       6, 0, 7, 9, 9, 8, 0, 5, 7, 3, 0, 0, 0, 0, 0, 0, 0, 7, 2,
                       0, 0, 0, 8, 0, 0, 0, 7, 5, 0, 5, 0, 0, 0, 0, 0, 3]),
      generate(size=15,
               colors=[0, 0, 2, 0, 9, 6, 5, 5, 5, 0, 2, 1, 0, 0, 0, 3, 0, 4, 4,
                       9, 0, 0, 0, 3, 9, 0, 0, 0, 5, 0, 8, 9, 2, 0, 1, 0, 6, 8,
                       0, 0, 0, 8, 0, 8, 0, 6, 0, 4, 0, 4, 0, 0, 1, 6, 1, 6, 9,
                       1, 4, 2, 7, 7, 7, 3, 0, 0, 6, 4, 0, 4, 0, 1, 3, 0, 0, 7,
                       6, 0, 4, 0, 2, 0, 0, 4, 0, 8, 0, 0, 7, 6, 0, 0, 4, 7, 8,
                       3, 0, 4, 0, 0, 5, 0, 6, 0, 3, 0, 8, 0, 0, 2, 0, 0, 0, 1,
                       0, 2, 0, 0, 1, 0, 3, 3, 1, 0, 2, 0, 0, 6, 0, 8, 6, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 9, 0, 4, 0, 2, 8, 0, 0,
                       4, 1, 4, 9, 0, 7, 0, 1, 0, 5, 0, 0, 8, 7, 2, 0, 0, 4, 5,
                       1, 0, 9, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 9, 6, 3, 1, 3, 3,
                       9, 0, 0, 0, 5, 0, 5, 0, 4, 0, 7, 9, 9, 0, 0, 0, 0, 9, 4,
                       0, 0, 9, 8, 8, 0, 6, 8, 0, 0, 0, 8, 0, 0, 0, 0]),
      generate(size=16,
               colors=[7, 4, 4, 0, 4, 0, 0, 6, 1, 1, 1, 0, 0, 6, 0, 5, 1, 1, 3,
                       3, 4, 0, 3, 8, 5, 3, 4, 5, 0, 8, 2, 8, 8, 0, 4, 8, 8, 5,
                       0, 9, 0, 0, 0, 5, 5, 8, 5, 8, 0, 2, 6, 0, 0, 0, 0, 3, 0,
                       1, 0, 8, 0, 4, 0, 8, 8, 0, 2, 8, 0, 7, 0, 0, 0, 9, 0, 7,
                       3, 0, 3, 6, 0, 0, 0, 0, 0, 0, 5, 3, 0, 6, 0, 6, 0, 4, 5,
                       7, 6, 6, 0, 0, 3, 1, 0, 0, 2, 5, 0, 0, 0, 3, 4, 5, 7, 0,
                       7, 8, 0, 1, 0, 0, 0, 9, 0, 7, 3, 0, 3, 0, 0, 6, 0, 0, 5,
                       6, 6, 5, 9, 8, 3, 9, 0, 7, 0, 0, 7, 5, 0, 0, 0, 8, 0, 6,
                       9, 0, 0, 7, 1, 0, 0, 0, 6, 5, 3, 4, 3, 0, 6, 9, 4, 1, 8,
                       9, 2, 8, 7, 7, 8, 6, 8, 6, 3, 2, 7, 3, 0, 2, 0, 0, 2, 1,
                       0, 0, 9, 0, 0, 0, 6, 1, 8, 0, 3, 3, 0, 2, 0, 2, 1, 4, 0,
                       4, 0, 0, 0, 0, 1, 0, 0, 0, 6, 0, 4, 4, 5, 6, 0, 5, 0, 8,
                       3, 2, 1, 0, 5, 9, 1, 8, 7, 0, 2, 7, 0, 9, 0, 1, 8, 6, 0,
                       9, 9, 8, 0, 9, 0, 0, 3, 0]),
  ]
  test = [
      generate(size=16,
               colors=[0, 0, 0, 8, 0, 5, 0, 0, 9, 0, 6, 0, 0, 0, 0, 5, 6, 7, 6,
                       0, 4, 0, 2, 0, 0, 8, 3, 6, 2, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                       5, 4, 1, 0, 1, 7, 6, 0, 0, 0, 0, 5, 8, 0, 9, 0, 0, 2, 2,
                       0, 8, 0, 4, 0, 0, 7, 4, 0, 0, 4, 2, 2, 7, 3, 2, 0, 6, 4,
                       9, 9, 9, 0, 0, 1, 8, 0, 5, 0, 0, 0, 2, 0, 0, 8, 0, 9, 6,
                       6, 9, 9, 0, 2, 8, 0, 0, 3, 0, 0, 2, 0, 0, 5, 8, 0, 1, 3,
                       0, 1, 6, 1, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 7,
                       4, 0, 0, 4, 0, 0, 5, 8, 0, 4, 0, 0, 0, 0, 6, 0, 6, 0, 0,
                       0, 0, 0, 8, 0, 1, 4, 4, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 1,
                       5, 0, 6, 0, 0, 6, 0, 7, 5, 9, 0, 7, 0, 0, 0, 4, 6, 0, 2,
                       8, 0, 5, 0, 0, 0, 1, 0, 2, 4, 8, 0, 0, 3, 0, 9, 0, 8, 1,
                       0, 0, 2, 4, 0, 0, 0, 1, 7, 0, 0, 0, 0, 5, 0, 6, 9, 0, 0,
                       7, 7, 1, 0, 2, 0, 0, 9, 1, 0, 3, 0, 1, 8, 3, 0, 0, 9, 7,
                       0, 2, 7, 2, 0, 8, 9, 0, 0]),
  ]
  return {"train": train, "test": test}
