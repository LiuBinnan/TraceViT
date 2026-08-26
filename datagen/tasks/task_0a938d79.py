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


def generate(width=None, height=None, start=None, sep=None, bottoms=None,
             colors=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    start: the columns index where the pattern starts
    sep: how much separation to leave between columns
    bottoms: for each color, whether we should show it on the bottom
    colors: a list of two colors
    xpose: whether to transpose the grid
  """
  if width is None:
    width, height = common.randint(20, 30), common.randint(6, 12)
    start = common.randint(1, width // 2)
    sep = common.randint(1, 5)
    num = common.randint(2, 2)
    bottoms = [common.randint(0, 1) for _ in range(num)]
    colors = common.random_colors(num)
    xpose = common.randint(0, 1)

  grid, _ = common.grids(width, height)
  grid[bottoms[0] * (height - 1)][start] = colors[0]
  grid[bottoms[1] * (height - 1)][start + sep + 1] = colors[1]
  if xpose:
    grid = common.transpose(grid)
    output = common.grid(height, width)
  else:
    output = common.grid(width, height)

  for color_idx in range(len(colors)):
    c = start + color_idx * (sep + 1)
    if c >= width: continue
    for r in range(height):
      if xpose:
        output[c][r] = colors[color_idx]
      else:
        output[r][c] = colors[color_idx]
  for c in range(start + len(colors) * (sep + 1), width, sep + 1):
    color_idx = ((c - start) // (sep + 1)) % len(colors)
    for r in range(height):
      if xpose:
        output[c][r] = colors[color_idx]
      else:
        output[r][c] = colors[color_idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=25, height=10, start=5, sep=1, bottoms=[0, 1],
               colors=[2, 8], xpose=0),
      generate(width=23, height=7, start=5, sep=2, bottoms=[0, 1],
               colors=[1, 3], xpose=0),
      generate(width=22, height=9, start=5, sep=1, bottoms=[0, 1],
               colors=[2, 3], xpose=1),
      generate(width=24, height=8, start=7, sep=3, bottoms=[0, 0],
               colors=[4, 1], xpose=1),
  ]
  test = [
      generate(width=27, height=11, start=5, sep=4, bottoms=[0, 1],
               colors=[3, 4], xpose=0),
  ]
  return {"train": train, "test": test}
