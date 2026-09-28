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


def generate(colors=None, widths=None, heights=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    widths: A list of widths to use.
    heights: A list of heights to use.
    gsize: The square canvas size; drives the random-path width/height budget.
  """

  if colors is None:
    if gsize is None:
      gsize = common.randint(8, 24)
    num_colors = common.randint(3, 6)
    colors = common.random_colors(num_colors)
    base, extra = gsize // num_colors, gsize % num_colors
    widths = [base + (1 if i >= num_colors - extra else 0) for i in range(num_colors)]
    heights = list(widths)
    for _ in range(10):
      idxs, dim = common.sample(range(num_colors), 2), common.randint(0, 1)
      min_val = 1 if idxs[0] + 1 < num_colors else 2
      if dim == 0 and widths[idxs[0]] > min_val:
        widths[idxs[0]] -= 1
        widths[idxs[1]] += 1
      elif dim == 1 and heights[idxs[0]] > min_val:
        heights[idxs[0]] -= 1
        heights[idxs[1]] += 1

  # Input: the bottom-row width-runs and right-column height-runs for each color.
  # The same edge markings are the given context of the output; the interior
  # staircase of rectangles is what the solver reconstructs from them.
  grid, output = common.grids(sum(widths), sum(heights))
  size, row, col = len(output), 0, 0
  placements = []
  for color, width, height in zip(colors, widths, heights):
    placements.append((color, width, height, row, col))
    for _ in range(width):
      output[size - 1][col] = grid[size - 1][col] = color
      col += 1
    for _ in range(height):
      output[row][size - 1] = grid[row][size - 1] = color
      row += 1

  def place_rect(i):
    """Places color i's rectangle at its diagonal-staircase position.

    Its width is the color's bottom-edge run and its height the right-edge run;
    its origin is the running (row, col) accumulated from the earlier colors.
    """
    nonlocal output
    if i >= len(placements): return
    color, width, height, rr, cc = placements[i]
    common.rect(output, width, height, rr, cc, color)

  place_rect(0)
  place_rect(1)
  place_rect(2)
  place_rect(3)
  place_rect(4)
  for i in range(5, len(placements)):
    place_rect(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 6, 7, 8, 9], widths=[1, 2, 3, 1, 3], heights=[1, 2, 3, 1, 3]),
      generate(colors=[9, 8, 7, 6, 5], widths=[2, 2, 2, 2, 2], heights=[2, 2, 2, 2, 2]),
      generate(colors=[8, 4, 5, 3], widths=[2, 3, 2, 3], heights=[3, 2, 2, 3]),
  ]
  test = [
      generate(colors=[3, 4, 6, 9, 7], widths=[2, 1, 3, 2, 2], heights=[3, 2, 2, 1, 2]),
  ]
  return {"train": train, "test": test}
