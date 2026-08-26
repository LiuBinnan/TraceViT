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


def generate(width=None, height=None, rows=None, cols=None,
             density=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    density: fraction of cells to fill (0..0.5); randomized when omitted
    num_colors: how many distinct foreground colors to use; randomized when
      omitted
  """
  pixel_colors = None
  if width is None:
    width, height = common.randint(1, 30), common.randint(1, 30)
    cells = [(r, c) for r in range(height) for c in range(width)]
    if density is None:
      num = common.randint(0, max(0, (width * height) // 2 - 1))
    else:
      num = min(len(cells), max(0, int(round(density * width * height))))
    chosen = common.sample(cells, num)
    rows = [r for r, c in chosen]
    cols = [c for r, c in chosen]
    if num_colors is None:
      num_colors = common.randint(1, min(8, num)) if num > 0 else 0
    else:
      num_colors = min(8, max(0, num_colors))
    palette = (common.random_colors(num_colors, exclude=[common.blue()])
               if num_colors > 0 else [common.red()])
    pixel_colors = [common.sample(palette, 1)[0] for r, c in chosen]

  grid, output = common.grids(width, height, common.black())
  if pixel_colors is None:
    pixel_colors = [common.red() for r, c in zip(rows, cols)]
  for (r, c), color in zip(zip(rows, cols), pixel_colors):
    output[r][c] = grid[r][c] = color
  pixels = common.edgefree_pixels(grid)
  for r, c in pixels:
    output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 0, 1, 1, 2], cols=[1, 2, 1, 2, 0]),
      generate(width=4, height=4, rows=[0, 0, 0, 1, 2, 3],
               cols=[0, 1, 2, 1, 3, 1]),
      generate(width=4, height=5, rows=[0, 0, 1, 2, 2, 2, 4, 4, 4],
               cols=[0, 1, 1, 0, 1, 3, 1, 2, 3]),
      generate(width=3, height=3, rows=[0, 0, 1, 1, 2],
               cols=[0, 1, 0, 2, 1]),
  ]
  test = [
      generate(width=4, height=5, rows=[0, 0, 0, 1, 2, 3, 4, 4],
               cols=[0, 1, 3, 1, 2, 0, 2, 3]),
  ]
  return {"train": train, "test": test}
