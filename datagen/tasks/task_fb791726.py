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


def generate(size=None, pcolor=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    pcolor: The color of the pixels.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
  """

  if size is None:
    size = common.randint(4, 14)
    pcolor = common.random_color(exclude=[3])
    pcols = [common.randint(0, size - 1)]
    pcol = common.randint(0, size - 1)
    if size >= 6 and pcol not in pcols:
      prows = [common.randint(1, size - 5)]
      pcols.append(pcol)
      prows.append(min(size - 2, prows[0] + 3))
    else:
      prows = [common.randint(1, size - 2)]

  # Input: each pair is two pixels straddling a one-cell vertical gap.
  grid = common.grid(size, size)
  for prow, pcol in zip(prows, pcols):
    grid[prow - 1][pcol] = grid[prow + 1][pcol] = pcolor

  # Output lives on a canvas twice as wide and tall.
  output = common.grid(2 * size, 2 * size)

  def place_source():
    """Reproduces the input pattern in the top-left quadrant."""
    for prow, pcol in zip(prows, pcols):
      output[prow - 1][pcol] = output[prow + 1][pcol] = pcolor

  def echo_diagonal():
    """Echoes each pair diagonally down-right into the bottom-right quadrant."""
    for prow, pcol in zip(prows, pcols):
      output[prow - 1 + size][pcol + size] = pcolor
      output[prow + 1 + size][pcol + size] = pcolor

  def draw_beams():
    """Draws a full-width green beam through each pair's midline (both copies)."""
    for prow, pcol in zip(prows, pcols):
      for c in range(2 * size):
        output[prow][c] = common.green()
        output[prow + size][c] = common.green()

  place_source()
  echo_diagonal()
  draw_beams()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, pcolor=8, prows=[1], pcols=[1]),
      generate(size=6, pcolor=4, prows=[1, 4], pcols=[1, 4]),
      generate(size=7, pcolor=7, prows=[1], pcols=[2]),
  ]
  test = [
      generate(size=4, pcolor=9, prows=[1], pcols=[0]),
  ]
  return {"train": train, "test": test}
