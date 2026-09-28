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
    height: The height of the input pattern.
    width: The width of the input pattern.
  """

  if colors is None:
    height, width = common.randint(2, 6), common.randint(2, 6)
    colors = [common.choice([5, 7, 8]) for _ in range(width * height)]
    if len(set(colors)) == 1:
      colors[-1] = common.choice([color for color in [5, 7, 8]
                                  if color != colors[0]])

  if height is None:
    height = 3
  if width is None:
    width = 3

  rows = [colors[i:i + width] for i in range(0, width * height, width)]
  grid, output = common.grid(width, height), common.grid(4 * width, height)

  def paint_mirror_then_copy(offset):
    for r, row in enumerate(rows):
      for c, color in enumerate(row):
        output[r][offset + width - 1 - c] = color
        output[r][offset + width + c] = color

  for r, row in enumerate(rows):
    for c, color in enumerate(row):
      grid[r][c] = color
  paint_mirror_then_copy(0)
  paint_mirror_then_copy(2 * width)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 8, 8, 5, 5, 7, 5, 7, 8]),
      generate(colors=[7, 7, 8, 5, 8, 8, 5, 8, 8]),
      generate(colors=[8, 8, 7, 7, 5, 5, 5, 7, 8]),
      generate(colors=[7, 5, 7, 5, 5, 7, 7, 7, 5]),
  ]
  test = [
      generate(colors=[8, 5, 7, 5, 7, 5, 8, 8, 5]),
  ]
  return {"train": train, "test": test}
