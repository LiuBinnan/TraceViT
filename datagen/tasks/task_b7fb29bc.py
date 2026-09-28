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


def generate(prow=None, pcol=None, isize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the pixel.
    pcol: The column of the pixel.
    isize: The width and height of the box interior.
  """

  if prow is None:
    if isize is None:
      isize = common.randint(5, 19)
    prow = common.randint(0, isize - 1)
    pcol = common.randint(0, isize - 1)

  if isize is None:
    isize = 7

  # Build the input grid: the green box border and the single green pixel.
  grid = common.grid(isize + 8, isize + 8)
  for i in range(isize + 2):
    grid[2][3 + i] = common.green()
    grid[isize + 3][3 + i] = common.green()
    grid[2 + i][3] = common.green()
    grid[2 + i][isize + 4] = common.green()
  grid[prow + 3][pcol + 4] = common.green()

  # Solve forward: ripples emanate from the marked pixel. Each concentric square
  # ring (Chebyshev distance from the pixel) is filled, alternating red at even
  # distance and yellow at odd distance; the pixel itself stays green.
  output = common.deepcopy(grid)

  def reveal_ring(d):
    """Fills the ring at Chebyshev distance d from the pixel (d >= 1)."""
    color = common.red() if d % 2 == 0 else common.yellow()
    for r in range(isize):
      for c in range(isize):
        if max(abs(prow - r), abs(pcol - c)) == d:
          output[3 + r][4 + c] = color

  reveal_ring(1)
  reveal_ring(2)
  reveal_ring(3)
  reveal_ring(4)
  reveal_ring(5)
  reveal_ring(6)
  for d in range(7, isize):
    reveal_ring(d)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=5, pcol=1),
      generate(prow=3, pcol=3),
      generate(prow=0, pcol=5),
  ]
  test = [
      generate(prow=2, pcol=0),
  ]
  return {"train": train, "test": test}
