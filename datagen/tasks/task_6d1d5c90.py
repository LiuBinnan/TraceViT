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


def generate(colors=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    height: The height of the mosaic.
    width: The width of the mosaic.
  """

  if colors is None:
    if height is None:
      height = common.randint(5, 8)
    if width is None:
      width = common.randint(5, 8)
    while True:
      colors = ([6] + [5] * width) * height
      for _ in range(10):
        length = common.randint(2, min(4, height, width))
        cdir = common.randint(0, 1)
        if cdir:
          row = common.randint(0, height - length)
          col = common.randint(0, width - 1)
        else:
          row = common.randint(0, height - 1)
          col = common.randint(0, width - length)
        color = common.choice([1, 3, 4, 8, 9])
        for i in range(length):
          if cdir: colors[(row + i) * (width + 1) + col + 1] = color
          else: colors[row * (width + 1) + col + i + 1] = color
      colors[common.randint(0, height - 1) * (width + 1)] = 2
      if len(set(colors)) == 7: break
  else:
    if height is None:
      height = 6
    if width is None:
      width = 6

  grid = common.grid(width + 1, height)
  for i, color in enumerate(colors):
    grid[i // (width + 1)][i % (width + 1)] = color
  offset = [r for r in range(height) if colors[(width + 1) * r] == 2][0]
  output = common.grid(width, height)
  for src_row in range(height - offset):
    dst_row = src_row + offset
    for col in range(width):
      output[dst_row][col] = grid[src_row][col + 1]
  for src_row in range(height - offset, height):
    dst_row = src_row + offset - height
    for col in range(width):
      output[dst_row][col] = grid[src_row][col + 1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 1, 1, 1, 1, 9, 8,
                       6, 4, 3, 9, 9, 9, 8,
                       6, 4, 3, 9, 3, 8, 8,
                       6, 4, 3, 3, 3, 8, 8,
                       6, 4, 8, 8, 5, 5, 5,
                       6, 4, 5, 5, 5, 3, 3]),
      generate(colors=[6, 8, 8, 8, 4, 4, 4,
                       6, 9, 9, 8, 3, 4, 4,
                       2, 9, 9, 8, 3, 3, 3,
                       6, 9, 1, 1, 1, 5, 3,
                       6, 4, 4, 1, 5, 5, 5,
                       6, 4, 4, 1, 5, 5, 5]),
      generate(colors=[6, 8, 8, 8, 4, 4, 4,
                       6, 8, 9, 8, 4, 9, 1,
                       6, 8, 9, 9, 9, 9, 1,
                       2, 5, 5, 3, 3, 3, 1,
                       6, 5, 5, 3, 4, 3, 1,
                       6, 5, 5, 3, 4, 4, 4]),
  ]
  test = [
      generate(colors=[6, 5, 8, 8, 8, 9, 9,
                       2, 5, 4, 4, 4, 4, 9,
                       6, 5, 3, 1, 1, 4, 9,
                       6, 5, 3, 1, 1, 4, 8,
                       6, 1, 3, 3, 3, 8, 8,
                       6, 1, 1, 3, 8, 8, 9]),
  ]
  return {"train": train, "test": test}
