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


def generate(width=None, height=None, rowoffset=None, coloffset=None, rows=None,
             cols=None, colors=None, maxsprite=3):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rowoffset: the number of rows to shift the sprite
    coloffset: the number of columns to shift the sprite
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    maxsprite: the upper bound on the sprite's width/height when randomizing.
      The default of 3 reproduces the original (sprites up to 3x3 on grids up to
      7x7); the randomized branch raises it to grow richer/larger foregrounds.
  """
  if width is None:
    # Bigger maxsprite => larger, more varied foreground (more pixels, more
    # distinct silhouettes). maxsprite == 3 falls back to the original ranges
    # (grid 5..7, sprite 2..3, up to 3 carved cells) with the same draw order.
    maxsprite = common.randint(3, 20)
    width, height = common.randint(5, maxsprite + 4), common.randint(
        5, maxsprite + 4)
    wide, tall = common.randint(2, maxsprite), common.randint(2, maxsprite)
    # Keep the grid at least as big as the sprite (no-op at the default) and
    # never exceed the 30x30 grid limit.
    width, height = min(30, max(width, wide + 2)), min(30, max(height, tall + 2))
    rowoffset = common.randint(0, height - tall)
    coloffset = common.randint(0, width - wide)
    rows, cols = common.hollow_conway(wide, tall, common.randint(0, maxsprite))
    color_list = common.random_colors(2, exclude=[common.blue()])
    colors = [common.choice(color_list) for _ in rows]

  wide, tall = max(cols) + 1, max(rows) + 1
  grid = common.grid(width, height, common.blue())
  output = common.grid(wide, tall, common.black())
  for row, col, color in zip(rows, cols, colors):
    output[row][col] = grid[rowoffset + row][coloffset + col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=5, rowoffset=1, coloffset=1,
               rows=[0, 0, 1, 1, 1, 2], cols=[0, 1, 0, 1, 2, 2],
               colors=[2, 2, 2, 2, 3, 2]),
      generate(width=7, height=7, rowoffset=1, coloffset=2, rows=[0, 0, 1, 1],
               cols=[0, 2, 0, 2], colors=[3, 2, 3, 2]),
      generate(width=6, height=7, rowoffset=2, coloffset=1,
               rows=[0, 0, 1, 1, 2, 2], cols=[0, 1, 0, 1, 0, 1],
               colors=[5, 5, 5, 5, 6, 6]),
  ]
  test = [
      generate(width=6, height=6, rowoffset=2, coloffset=2, rows=[0, 1, 1],
               cols=[1, 0, 1], colors=[2, 2, 3]),
  ]
  return {"train": train, "test": test}
