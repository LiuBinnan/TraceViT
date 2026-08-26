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


def generate(
    width=None, wide=None, tall=None, colors=None, offset=None, height=5
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    wide: the width of the pattern
    tall: the height of the pattern
    colors: a list of digits representing the colors to be used
    offset: the vertical offset of the pattern
    height: the height of the input grid
  """
  if width is None:
    # re_arc's generate_963e52fc structural bands: half-width w in [6, 15],
    # period p in [2, w // 2] (the input always shows >=2 full periods, so
    # "detect the horizontal period and extend to 2*width" stays exact --
    # Fine-Wilf), up to 9 pattern colors, and a sparsely painted period tile.
    width, offset = common.randint(6, 15), common.randint(1, 2)
    wide = common.randint(2, max(2, width // 2))
    tall = common.randint(1, max(1, height - offset))
    ncells = wide * tall
    # Paint a subset of the tile; unpainted cells stay background (0, the
    # common.grid fill), which spreads object-count and foreground density.
    num_painted = common.randint(1, ncells)
    # Distinct pattern colors, re_arc's numc in [1, 9], capped to painted cells.
    num_colors = common.randint(1, min(9, num_painted))
    color_list = common.random_colors(num_colors)
    # Every chosen color appears at least once; fill remaining painted cells at
    # random, then shuffle painted/background positions within the period tile.
    cells = list(color_list) + [
        common.choice(color_list) for _ in range(num_painted - num_colors)]
    cells += [0] * (ncells - num_painted)
    colors = common.sample(cells, ncells)

  grid = common.grid(width, height)
  output = common.grid(2 * width, height)
  for row in range(tall):
    for col in range(2 * width):
      color = colors[(row % tall) * wide + col % wide]
      common.draw(grid, row + offset, col, color)
      common.draw(output, row + offset, col, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, wide=2, tall=2, colors=[2, 8, 2, 8], offset=1),
      generate(width=7, wide=3, tall=1, colors=[2, 3, 3], offset=2),
      generate(width=8, wide=3, tall=2, colors=[1, 2, 2, 2, 1, 2], offset=2),
  ]
  test = [
      generate(width=9, wide=3, tall=2, colors=[3, 1, 1, 3, 1, 1], offset=1),
  ]
  return {"train": train, "test": test}
