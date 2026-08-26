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


def generate(colors=None, size=3, height=None, width=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: number of rows of the input grid (defaults to size)
    width: number of columns of the input grid (defaults to size)
    num_colors: number of colors to sample when colors is not provided
    density: number of non-background cells when colors is not provided
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    area = height * width
    if num_colors is None:
      num_colors = common.randint(1, min(10, area))
    num_colors = max(1, min(num_colors, 10, area))
    bg = common.randint(0, 9)
    palette = [bg]
    if num_colors > 1:
      choices = [color for color in range(10) if color != bg]
      palette.extend(common.sample(choices, num_colors - 1))
    if density is None:
      density = common.randint(0, area)
    density = max(0, min(density, area))
    colors = [bg for _ in range(area)]
    if len(palette) == 1:
      density = 0
    if density:
      idxs = common.sample(range(area), density)
      for i, idx in enumerate(idxs):
        if i < len(palette) - 1:
          colors[idx] = palette[i + 1]
        else:
          colors[idx] = palette[common.randint(1, len(palette) - 1)]

  grid = common.grid(width, height)
  output = common.grid(2 * width, 2 * height)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
  for r in range(height):
    for c in range(width):
      output[r][c] = colors[r * width + c]
  for r in range(height):
    for c in range(width):
      output[2 * height - 1 - r][c] = colors[r * width + c]
  for r in range(height):
    for c in range(width):
      output[r][2 * width - 1 - c] = colors[r * width + c]
  for r in range(height):
    for c in range(width):
      output[2 * height - 1 - r][2 * width - 1 - c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 3, 3, 0, 2, 2, 1, 1, 0]),
      generate(colors=[3, 3, 1, 1, 3, 0, 0, 2, 2]),
      generate(colors=[2, 1, 0, 0, 2, 3, 0, 3, 0]),
  ]
  test = [
      generate(colors=[1, 1, 0, 0, 3, 2, 3, 3, 0]),
  ]
  return {"train": train, "test": test}
