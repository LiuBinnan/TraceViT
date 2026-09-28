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


def generate(row=None, col=None, index=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: The row index of the pixel.
    col: The column index of the pixel.
    index: The index of the pixel.
    gsize: The side length of the (square) canvas.
  """

  colors = [0, 5, 2, 8, 9, 6, 1, 3, 4]
  if index is None:
    index = common.randint(0, 8)
    if gsize is None:
      gsize = common.randint(6, 18)
    row, col = common.randint(0, gsize - 1), common.randint(0, gsize - 1)
  elif gsize is None:
    gsize = 8

  grid = common.grid(gsize, gsize, common.orange())
  grid[row][col] = colors[index]
  output = common.deepcopy(grid)

  maxdist = max(row + col, row + (gsize - 1) - col,
                (gsize - 1) - row + col, 2 * (gsize - 1) - row - col)
  step = (maxdist + 6) // 6

  def paint_ring_band(b):
    """Paints the b-th outward band of concentric diamond rings.

    The color wave spreads outward from the seed pixel by `step` Manhattan
    distance levels per band: every cell whose distance d to the seed lies in
    [b * step, (b + 1) * step - 1] takes the color d positions after the
    seed's in the fixed 9-color cycle.
    """
    for r in range(gsize):
      for c in range(gsize):
        d = abs(r - row) + abs(c - col)
        if b * step <= d < (b + 1) * step:
          output[r][c] = colors[(index + d) % 9]

  paint_ring_band(0)
  paint_ring_band(1)
  paint_ring_band(2)
  paint_ring_band(3)
  paint_ring_band(4)
  paint_ring_band(5)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=0, col=6, index=7),
      generate(row=5, col=2, index=1),
  ]
  test = [
      generate(row=2, col=1, index=0),
  ]
  return {"train": train, "test": test}
