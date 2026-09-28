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


def generate(size=None, diag=None, offdiag=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    diag: The diagonal values.
    offdiag: The off-diagonal values.
    flop: Whether to flop the input and output grids.
  """

  if size is None:
    while True:
      size = common.randint(5, 14)
      subset = common.random_colors(4)
      diag = common.choices(subset, 2)
      offdiag = common.choices(subset + [0], 2)
      if size > 5 and 0 not in offdiag and common.randint(0, 1):
        diag = [diag[0], diag[1], diag[1]]
        offdiag = [offdiag[0], offdiag[0], offdiag[1]]
      if len(set(diag + offdiag)) >= 3: break
    flop = common.randint(0, 1)

  grid = common.grid(size, size)
  output = common.grid(2 * size, 2 * size)

  def fc(col, width):
    """Column index, mirrored when flop is set (matches common.flop)."""
    return width - 1 - col if flop else col

  # Input: the given tridiagonal band fragment -- the main diagonal cycles
  # `diag`, the two flanking diagonals cycle `offdiag` -- oriented by `flop`.
  for i in range(size):
    grid[i][fc(i, size)] = diag[i % len(diag)]
    if i + 1 < size:
      c = offdiag[(i + 1) % len(offdiag)]
      grid[i][fc(i + 1, size)] = c
      grid[i + 1][fc(i, size)] = c

  # Output: the same periodic band continued onto a canvas twice as large.
  def draw_band(lo, hi):
    """Extends the band's three diagonals over diagonal indices [lo, hi)."""
    for i in range(lo, hi):
      output[i][fc(i, 2 * size)] = diag[i % len(diag)]
      if i + 1 < 2 * size:
        c = offdiag[(i + 1) % len(offdiag)]
        output[i][fc(i + 1, 2 * size)] = c
        output[i + 1][fc(i, 2 * size)] = c

  def place_given_band():
    """Lays the given fragment's band onto the doubled canvas."""
    draw_band(0, size)

  def continue_band():
    """Continues the periodic band across the rest of the doubled canvas."""
    draw_band(size, 2 * size)

  place_given_band()
  continue_band()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, diag=[2, 2], offdiag=[0, 5], flop=False),
      generate(size=6, diag=[4, 3, 3], offdiag=[1, 1, 2], flop=False),
      generate(size=8, diag=[1, 6], offdiag=[0, 0], flop=True),
  ]
  test = [
      generate(size=10, diag=[6, 8], offdiag=[4, 6], flop=True),
  ]
  return {"train": train, "test": test}
