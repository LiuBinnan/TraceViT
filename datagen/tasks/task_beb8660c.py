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


def generate(colors=None, rows=None, cols=None, gap=None, width=None,
             height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing colors to be used
    rows: a list of row indices for each color
    cols: a list of column indices for each color
    gap: how much space to leave at the top
    width: the width of the grid
    height: the height of the grid
  """
  if colors is None:
    if width is None:
      width = common.randint(3, 30)
    if height is None:
      height = common.randint(3, 30)
    num_colors = common.randint(3, min(9, width, height))
    colors = common.random_colors(num_colors - 1, exclude=[common.cyan()])
    colors.append(common.cyan())
    gap = height - num_colors
    rows = common.sample(range(height - 1), num_colors - 1)
    rows.append(height - 1)
    cols = [common.randint(0, width - 1 - i) for i in range(num_colors)]

  if width is None:
    width = len(colors)
  if height is None:
    height = len(colors) + gap
  grid, output = common.grids(width, height)
  for color_idx, color in enumerate(colors):
    for idx in range(color_idx + 1):
      grid[rows[color_idx]][cols[color_idx] + idx] = color
      output[color_idx + gap][width - 1 - color_idx + idx] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 2, 1, 4, 6, 5, 8], rows=[1, 0, 2, 7, 6, 4, 9],
               cols=[4, 1, 0, 3, 0, 1, 0], gap=3),
      generate(colors=[1, 3, 2, 8], rows=[0, 4, 2, 6], cols=[3, 1, 0, 0],
               gap=3),
      generate(colors=[4, 2, 8], rows=[1, 0, 2], cols=[1, 0, 0], gap=0),
  ]
  test = [
      generate(colors=[9, 7, 6, 1, 4, 3, 2, 8], rows=[8, 4, 0, 1, 3, 7, 6, 10],
               cols=[1, 5, 0, 4, 1, 2, 0, 0], gap=3),
  ]
  return {"train": train, "test": test}
