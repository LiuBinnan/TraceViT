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

import os

import common


def generate(width=None, colors=None, thicks=None, xpose=None, num_layers=None,
             inserts=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    colors: a list of digits representing the colors to be used
    thicks: a list of integers representing the thickness of each layer
    xpose: whether to transpose the grid
    num_layers: the number of color layers before row duplication
    inserts: the number of duplicated input rows
  """
  if width is None or colors is None or thicks is None or xpose is None:
    if width is None:
      width = common.randint(1, 30)
    if colors is None:
      if num_layers is None:
        num_layers = common.randint(2, 15)
      colors = []
      for _ in range(num_layers):
        choices = [color for color in range(10)
                   if not colors or color != colors[-1]]
        colors.append(common.choice(choices))
    if thicks is None:
      if inserts is None:
        inserts = common.randint(1, max(1, 30 - len(colors)))
      inserts = min(inserts, max(0, 30 - len(colors)))
      thicks = [1 for _ in range(len(colors))]
      for _ in range(inserts):
        loc = common.randint(0, sum(thicks) - 1)
        seen = 0
        for idx, thick in enumerate(thicks):
          seen += thick
          if loc < seen:
            thicks[idx] += 1
            break
    if xpose is None:
      xpose = common.randint(0, 1)

  height = sum(thicks)
  grid, _, output = common.grids(width, height, 0) + (
      common.grid(1, len(colors), 0),)
  r = 0
  for color, thick in zip(colors, thicks):
    for _ in range(thick):
      for c in range(width):
        grid[r][c] = color
      r += 1

  def reveal_layer(idx):
    if idx >= len(colors):
      return
    stop = len(colors) if idx == 4 else idx + 1
    for pos in range(idx, stop):
      output[pos][0] = colors[pos]

  reveal_layer(0)
  reveal_layer(1)
  reveal_layer(2)
  reveal_layer(3)
  reveal_layer(4)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, colors=[1, 2, 1], thicks=[1, 1, 1], xpose=0),
      generate(width=3, colors=[3, 4, 6], thicks=[1, 1, 1], xpose=1),
      generate(width=3, colors=[2, 3, 8, 1], thicks=[1, 2, 1, 1], xpose=1),
      generate(width=2, colors=[2, 6, 8], thicks=[1, 1, 2], xpose=0),
      generate(width=4, colors=[4, 2, 8, 3], thicks=[2, 2, 1, 1], xpose=0),
  ]
  test = [
      generate(width=4, colors=[1, 2, 3, 8, 4], thicks=[2, 1, 3, 2, 1],
               xpose=1),
  ]
  return {"train": train, "test": test}
