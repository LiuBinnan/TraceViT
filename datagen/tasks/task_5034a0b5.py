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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the grid.
  """

  def analyze(colors):
    bgcolor = colors[0]
    top_color = colors[size // 2]
    left_color = colors[(size // 2) * size]
    bottom_color = colors[(size - 1) * size + size // 2]
    right_color = colors[(size // 2) * size + size - 1]
    placements = []
    occupied = set()
    for r in range(1, size - 1):
      for c in range(1, size - 1):
        color = colors[r * size + c]
        if color == bgcolor: continue
        if color == top_color:
          direction, tr, tc = "up", max(r - 1, 1), c
        elif color == left_color:
          direction, tr, tc = "left", r, max(c - 1, 1)
        elif color == bottom_color:
          direction, tr, tc = "down", min(r + 1, size - 2), c
        elif color == right_color:
          direction, tr, tc = "right", r, min(c + 1, size - 2)
        else:
          direction, tr, tc = "stay", r, c
        if (tr, tc) in occupied: return None
        occupied.add((tr, tc))
        placements.append((direction, tr, tc, color))
    return bgcolor, top_color, left_color, bottom_color, right_color, placements

  if size is None:
    size = common.randint(8, 14)
    sides = common.sample(list(range(10)), 5)
    bgcolor = sides.pop()
    while True:
      grid = common.grid(size, size, bgcolor)
      for i in range(1, size - 1):
        grid[0][i] = sides[0]
        grid[i][0] = sides[1]
        grid[size - 1][i] = sides[2]
        grid[i][size - 1] = sides[3]
      for r in range(1, size - 1):
        for c in range(1, size - 1):
          if common.randint(0, 9) == 0: grid[r][c] = common.randint(0, 9)
          if common.randint(0, 3) == 0: grid[r][c] = common.choice(sides)
      colors = common.flatten(grid)
      if analyze(colors) is not None: break

  placement_data = analyze(colors)
  if placement_data is None:
    return {"input": None, "output": None}
  bgcolor, top_color, left_color, bottom_color, right_color, placements = placement_data
  grid = common.grid(size, size, bgcolor)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color

  output = common.grid(size, size, bgcolor)

  for i in range(1, size - 1):
    output[0][i] = top_color
    output[i][0] = left_color
    output[size - 1][i] = bottom_color
    output[i][size - 1] = right_color

  for direction, tr, tc, color in placements:
    if direction == "stay": output[tr][tc] = color

  for direction, tr, tc, color in placements:
    if direction == "up": output[tr][tc] = color

  for direction, tr, tc, color in placements:
    if direction == "left": output[tr][tc] = color

  for direction, tr, tc, color in placements:
    if direction == "down": output[tr][tc] = color

  for direction, tr, tc, color in placements:
    if direction == "right": output[tr][tc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, colors=[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2,
                                8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4,
                                8, 2, 2, 2, 2, 2, 2, 8, 2, 2, 4, 4,
                                8, 2, 3, 2, 2, 1, 2, 2, 2, 2, 2, 4,
                                8, 4, 2, 2, 1, 2, 1, 2, 2, 3, 2, 4,
                                8, 2, 2, 2, 2, 1, 2, 2, 3, 2, 2, 4,
                                8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4,
                                8, 2, 3, 2, 0, 2, 2, 8, 8, 8, 2, 4,
                                8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4,
                                8, 2, 2, 2, 4, 2, 4, 2, 2, 2, 2, 4,
                                8, 2, 2, 4, 2, 4, 2, 2, 2, 2, 2, 4,
                                2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]),
      generate(size=8, colors=[1, 5, 5, 5, 5, 5, 5, 1,
                               4, 1, 1, 1, 4, 1, 4, 2,
                               4, 5, 1, 1, 1, 1, 1, 2,
                               4, 1, 1, 1, 2, 1, 3, 2,
                               4, 1, 1, 3, 1, 1, 1, 2,
                               4, 1, 1, 3, 1, 1, 1, 2,
                               4, 5, 1, 1, 1, 1, 5, 2,
                               1, 3, 3, 3, 3, 3, 3, 1]),
      generate(size=13, colors=[3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3,
                                9, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 6,
                                9, 3, 6, 3, 3, 3, 3, 9, 3, 9, 3, 3, 6,
                                9, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 6,
                                9, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 6,
                                9, 3, 3, 3, 1, 3, 3, 3, 3, 6, 3, 3, 6,
                                9, 3, 3, 3, 3, 1, 3, 3, 3, 6, 3, 3, 6,
                                9, 3, 3, 3, 3, 3, 1, 3, 3, 6, 3, 3, 6,
                                9, 3, 3, 3, 4, 3, 3, 1, 3, 3, 3, 3, 6,
                                9, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 6,
                                9, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 6,
                                9, 3, 8, 3, 3, 3, 3, 3, 3, 5, 3, 3, 6,
                                3, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3]),
      generate(size=10, colors=[0, 2, 2, 2, 2, 2, 2, 2, 2, 0,
                                1, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                1, 0, 2, 0, 4, 0, 0, 0, 0, 3,
                                1, 0, 0, 0, 0, 0, 0, 1, 0, 3,
                                1, 0, 0, 0, 0, 3, 0, 0, 0, 3,
                                1, 0, 1, 0, 0, 0, 0, 0, 0, 3,
                                1, 0, 0, 0, 0, 0, 0, 4, 0, 3,
                                1, 0, 0, 0, 0, 0, 2, 0, 0, 3,
                                1, 0, 0, 3, 0, 0, 0, 0, 0, 3,
                                0, 4, 4, 4, 4, 4, 4, 4, 4, 0]),
  ]
  test = [
      generate(size=9, colors=[4, 5, 5, 5, 5, 5, 5, 5, 4,
                               3, 4, 4, 1, 4, 4, 4, 4, 9,
                               3, 4, 4, 9, 4, 9, 4, 5, 9,
                               3, 4, 4, 4, 8, 4, 4, 4, 9,
                               3, 9, 4, 2, 4, 4, 4, 4, 9,
                               3, 3, 4, 4, 4, 4, 4, 3, 9,
                               3, 4, 2, 4, 4, 4, 8, 4, 9,
                               3, 4, 3, 4, 4, 4, 4, 7, 9,
                               4, 2, 2, 2, 2, 2, 2, 2, 4]),
  ]
  return {"train": train, "test": test}
