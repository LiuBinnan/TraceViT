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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, trow=None, tcol=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wide: The width of the box.
    tall: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
    trow: The row of the T.
    tcol: The column of the T.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
  """

  if width is None:
    while True:
      width, height = common.randint(8, 28), common.randint(8, 28)
      wide, tall = common.randint(3, width // 2), common.randint(3, height // 2)
      brow = common.randint(1, height - tall - 1)
      bcol = common.randint(1, width - wide - 1)
      trow = common.randint(brow + 2, brow + tall - 3) if tall >= 5 else -1
      tcol = common.randint(bcol + 2, bcol + wide - 3) if wide >= 5 else -1
      prows, pcols = [], []
      eff_brow, eff_bcol, eff_wide, eff_tall = brow, bcol, wide, tall
      for i in common.shuffle(list(range(4))):
        if i == 0 and eff_brow >= 3 and common.randint(0, 3):
          prows.append(common.randint(1, eff_brow - 2))
          pcols.append(common.randint(eff_bcol + 1, eff_bcol + eff_wide - 2))
          eff_tall += (eff_brow - prows[-1] - 1)
          eff_brow = prows[-1] + 1
        if i == 1 and eff_bcol >= 3 and common.randint(0, 3):
          prows.append(common.randint(eff_brow + 1, eff_brow + eff_tall - 2))
          pcols.append(common.randint(1, eff_bcol - 2))
          eff_wide += (eff_bcol - pcols[-1] - 1)
          eff_bcol = pcols[-1] + 1
        if i == 2 and eff_brow + eff_tall + 2 < height and common.randint(0, 3):
          prows.append(common.randint(eff_brow + eff_tall + 1, height - 2))
          pcols.append(common.randint(eff_bcol + 1, eff_bcol + eff_wide - 2))
          eff_tall += prows[-1] - (eff_brow + eff_tall)
        if i == 3 and eff_bcol + eff_wide + 2 < width and common.randint(0, 3):
          prows.append(common.randint(eff_brow + 1, eff_brow + eff_tall - 2))
          pcols.append(common.randint(eff_bcol + eff_wide + 1, width - 2))
          eff_wide += pcols[-1] - (eff_bcol + eff_wide)
      if len(prows) in [2, 3, 4]: break

  # Input: a small hollow box (with optional internal T-lines) plus loose
  # 6-pixels sitting just outside it. Solving stretches the box so each wall
  # reaches out to the pixel on that side; the internal T-lines grow with it.
  grid, output = common.grids(width, height)
  common.hollow_rect(grid, wide, tall, brow, bcol, 3)
  if trow != -1:
    for col in range(bcol, bcol + wide):
      grid[trow][col] = 3
  if tcol != -1:
    for row in range(brow, brow + tall):
      grid[row][tcol] = 3
  for prow, pcol in zip(prows, pcols):
    grid[prow][pcol] = 6

  # Bookkeeping (no frame): the box dimensions after reaching each pixel in
  # turn, folded exactly as the sampling grew the effective box.
  dims = []
  w, t, r0, c0 = wide, tall, brow, bcol
  for prow, pcol in zip(prows, pcols):
    if prow < r0: t, r0 = t + (r0 - prow) - 1, prow + 1
    if prow >= r0 + t: t = prow - r0
    if pcol < c0: w, c0 = w + (c0 - pcol) - 1, pcol + 1
    if pcol >= c0 + w: w = pcol - c0
    dims.append((w, t, r0, c0))

  def reach_pixel(i):
    """Stretches the box out to reach pixel `i` (redraws at the grown size)."""
    nonlocal output
    if i >= len(dims): return
    w, t, r0, c0 = dims[i]
    output = common.grid(width, height)
    for prow, pcol in zip(prows, pcols):
      output[prow][pcol] = 6
    common.hollow_rect(output, w, t, r0, c0, 3)
    if trow != -1:
      for col in range(c0, c0 + w):
        output[trow][col] = 3
    if tcol != -1:
      for row in range(r0, r0 + t):
        output[row][tcol] = 3

  reach_pixel(0)
  reach_pixel(1)
  reach_pixel(2)
  for i in range(3, len(dims)):
    reach_pixel(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=11, wide=3, tall=3, brow=2, bcol=4, trow=-1,
               tcol=-1, prows=[3, 9], pcols=[1, 5]),
      generate(width=17, height=8, wide=6, tall=4, brow=1, bcol=1, trow=-1,
               tcol=3, prows=[2, 6], pcols=[11, 4]),
      generate(width=15, height=15, wide=6, tall=5, brow=3, bcol=4, trow=5,
               tcol=7, prows=[4, 6, 14], pcols=[12, 1, 7]),
  ]
  test = [
      generate(width=17, height=16, wide=3, tall=6, brow=2, bcol=5, trow=5,
               tcol=-1, prows=[4, 11, 12], pcols=[1, 13, 6]),
  ]
  return {"train": train, "test": test}
