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


def generate(width=None, height=None, colors=None, num_colors=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: the colors of the input grid
    num_colors: how many distinct colors should appear in sampled inputs
    count: number of non-background cells to place when sampling colors
  """
  if width is None:
    width = common.randint(2, 30)
    height = common.randint(2, 30)

  if colors is None:
    area = width * height
    if num_colors is None:
      num_colors = common.randint(1, min(10, area))
    num_colors = max(1, min(num_colors, 10, area))
    background = common.choice(list(range(10)))
    colors = [background] * area
    if num_colors > 1:
      foreground_colors = common.sample(
          [color for color in range(10) if color != background],
          num_colors - 1)
      if count is None:
        count = common.randint(num_colors - 1, max(num_colors - 1, area - 1))
      count = max(num_colors - 1, min(count, area - 1))
      cells = common.sample(list(range(area)), count)
      pixel_colors = foreground_colors[:]
      while len(pixel_colors) < count:
        pixel_colors.append(
            foreground_colors[common.randint(0, len(foreground_colors) - 1)])
      pixel_colors = common.shuffle(pixel_colors)
      for cell, color in zip(cells, pixel_colors):
        colors[cell] = color

  grid, output = common.grid(width, height), common.grid(2, 2)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
      if r < 2 and c < 2: output[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6,
               colors=[4, 3, 6, 4, 0, 6, 6, 0, 0, 3, 3, 4, 6, 4, 4, 3, 3, 0, 0,
                       3, 6, 0, 4, 6, 0, 6, 3, 0, 4, 3, 3, 4, 4, 6, 6, 0]),
      generate(width=8, height=8,
               colors=[2, 4, 2, 2, 5, 2, 4, 5, 2, 5, 5, 4, 4, 2, 2, 2, 4, 5, 5,
                       2, 2, 2, 2, 4, 2, 2, 4, 2, 5, 4, 2, 5, 2, 4, 2, 2, 5, 2,
                       4, 5, 2, 5, 5, 4, 4, 2, 2, 2, 4, 5, 5, 2, 2, 2, 2, 4, 2,
                       2, 4, 2, 5, 4, 2, 5]),
      generate(width=6, height=12,
               colors=[3, 2, 1, 3, 4, 1, 1, 4, 4, 2, 2, 3, 1, 3, 3, 2, 2, 4, 4,
                       2, 1, 4, 3, 1, 4, 1, 2, 4, 3, 2, 2, 3, 3, 1, 1, 4, 2, 4,
                       4, 1, 1, 3, 3, 1, 2, 3, 4, 2, 3, 2, 1, 3, 4, 1, 1, 4, 4,
                       2, 2, 3, 1, 3, 3, 2, 2, 4, 4, 2, 1, 4, 3, 1]),
  ]
  test = [
      generate(width=8, height=4,
               colors=[9, 6, 2, 9, 9, 2, 6, 9, 2, 9, 9, 6, 6, 9, 9, 2, 6, 9, 9,
                       2, 2, 9, 9, 6, 9, 2, 6, 9, 9, 6, 2, 9]),
  ]
  return {"train": train, "test": test}
