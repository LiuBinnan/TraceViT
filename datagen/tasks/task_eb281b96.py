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


def generate(stretch=None, color=None, width=17, height=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    stretch: how much to stretch the middle bit
    color: a digit representing a color to be used
    width: the width of the grid
    height: the height of a sampled input grid
    num_colors: how many foreground colors may appear
    density: how many cells to paint in a sampled input grid
  """
  if height is None and num_colors is None and density is None:
    if stretch is None:
      stretch = common.randint(1, 4)
      color = common.random_color()

    grid = common.grid(width, 2 + stretch)

    def paint_segment(ingrid, row, top_mod, bottom_mod):
      for c in range(width):
        if c % 4 == top_mod:
          ingrid[row][c] = color
        if c % 4 == bottom_mod:
          ingrid[row + stretch + 1][c] = color
        if c % 4 not in [0, 2]:
          for r in range(1, stretch + 1):
            ingrid[row + r][c] = color

    paint_segment(grid, 0, 2, 0)
  else:
    if height is None:
      height = common.randint(3, 8)
    if num_colors is None:
      num_colors = common.randint(1, 9)
    if density is None:
      density = common.randint(1, width * height)

    density = min(max(1, density), width * height)
    num_colors = min(max(1, num_colors), 9)
    colors = common.random_colors(num_colors)
    grid = common.grid(width, height)
    pixels = common.sample(common.all_pixels(width, height), density)
    colors = common.shuffle(colors)
    for idx, (r, c) in enumerate(pixels):
      grid[r][c] = colors[idx % num_colors]

  output = [row[:] for row in grid]
  output += [row[:] for row in grid[-2::-1]]
  output += [row[:] for row in output[-2::-1]]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(stretch=1, color=8),
      generate(stretch=2, color=2),
  ]
  test = [
      generate(stretch=3, color=3),
  ]
  return {"train": train, "test": test}
