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


def generate(fgcolor=None, bgcolor=None, colors=None, wides=None, talls=None,
             brows=None, bcols=None, prows=None, pcols=None, pidxs=None,
             gsize=30):
  """Returns input and output grids according to the given parameters.

  Args:
    fgcolor: The color of the foreground.
    bgcolor: The color of the background.
    colors: The colors of the borders.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the top left corners of the boxes.
    bcols: The column indices of the top left corners of the boxes.
    prows: The row indices of the pluses.
    pcols: The column indices of the pluses.
    pidxs: The box indices of the pluses.
    gsize: The side length of the square grid.
  """

  def draw():
    grid, output = common.grids(gsize, gsize)
    common.rect(grid, gsize - 2, gsize - 2, 1, 1, bgcolor)
    common.rect(output, gsize - 2, gsize - 2, 1, 1, bgcolor)
    for i in range(1, gsize - 1):
      output[0][i] = grid[0][i] = colors[0]
      output[i][gsize - 1] = grid[i][gsize - 1] = colors[1]
      output[gsize - 1][i] = grid[gsize - 1][i] = colors[2]
      output[i][0] = grid[i][0] = colors[3]
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      common.rect(grid, wide, tall, brow, bcol, fgcolor)
      common.rect(output, wide, tall, brow, bcol, fgcolor)
    for prow, pcol, pidx in zip(prows, pcols, pidxs):
      color = bgcolor
      if prow == 0: color = colors[0]
      if pcol == wides[pidx] - 1: color = colors[1]
      if prow == talls[pidx] - 1: color = colors[2]
      if pcol == 0: color = colors[3]
      for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
        row, col = brows[pidx] + prow + dr, bcols[pidx] + pcol + dc
        if grid[row][col] not in [fgcolor, bgcolor]: return None, None
        grid[row][col] = bgcolor
        output[row][col] = color
    return grid, output

  if fgcolor is None:
    colors = common.shuffle([1, 2, 3, 4, 6, 8])
    fgcolor = colors.pop()
    bgcolor = colors.pop()
    num_boxes = common.randint(3, 4)
    max_box = min(gsize - 10, 2 * gsize - 40)
    while True:
      wides = [common.randint(5, max_box) for _ in range(num_boxes)]
      talls = [common.randint(5, max_box) for _ in range(num_boxes)]
      brows = [common.randint(2, gsize - 2 - tall) for tall in talls]
      bcols = [common.randint(2, gsize - 2 - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    while True:
      prows, pcols, pidxs = [], [], []
      for bidx, (wide, tall) in enumerate(zip(wides, talls)):
        sides = common.sample([0, 1, 2, 3], common.randint(1, 3))
        if 0 in sides:
          prows.append(0)
          pcols.append(common.randint(2, wide - 3))
          pidxs.append(bidx)
        if 1 in sides:
          prows.append(common.randint(2, tall - 3))
          pcols.append(wide - 1)
          pidxs.append(bidx)
        if 2 in sides:
          prows.append(tall - 1)
          pcols.append(common.randint(2, wide - 3))
          pidxs.append(bidx)
        if 3 in sides:
          prows.append(common.randint(2, tall - 3))
          pcols.append(0)
          pidxs.append(bidx)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()
  output = [row[:] for row in grid]

  def hole_color(prow, pcol, pidx):
    color = bgcolor
    if prow == 0: color = colors[0]
    if pcol == wides[pidx] - 1: color = colors[1]
    if prow == talls[pidx] - 1: color = colors[2]
    if pcol == 0: color = colors[3]
    return color

  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    if pidx != 0: continue
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
      output[brows[pidx] + prow + dr][bcols[pidx] + pcol + dc] = hole_color(prow, pcol, pidx)
  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    if pidx != 1: continue
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
      output[brows[pidx] + prow + dr][bcols[pidx] + pcol + dc] = hole_color(prow, pcol, pidx)
  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    if pidx != 2: continue
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
      output[brows[pidx] + prow + dr][bcols[pidx] + pcol + dc] = hole_color(prow, pcol, pidx)
  for prow, pcol, pidx in zip(prows, pcols, pidxs):
    if pidx != 3: continue
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
      output[brows[pidx] + prow + dr][bcols[pidx] + pcol + dc] = hole_color(prow, pcol, pidx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(fgcolor=6, bgcolor=1, colors=[3, 2, 4, 8], wides=[15, 9, 11, 9],
               talls=[5, 5, 15, 9], brows=[3, 9, 10, 16], bcols=[2, 14, 2, 18],
               prows=[0, 2, 4, 6, 14, 3, 5], pcols=[5, 14, 4, 0, 4, 8, 0],
               pidxs=[0, 0, 1, 2, 2, 3, 3]),
      generate(fgcolor=2, bgcolor=4, colors=[1, 8, 6, 3], wides=[10, 10, 10],
               talls=[10, 10, 10], brows=[2, 4, 16], bcols=[3, 17, 13],
               prows=[0, 3, 9], pcols=[4, 0, 4], pidxs=[0, 1, 2]),
  ]
  test = [
      generate(fgcolor=1, bgcolor=3, colors=[2, 6, 4, 8], wides=[9, 12, 6, 9],
               talls=[5, 20, 6, 7], brows=[3, 3, 10, 20], bcols=[3, 14, 5, 3],
               prows=[0, 0, 6, 19, 2, 3, 3, 4], pcols=[3, 5, 11, 7, 0, 5, 0, 8],
               pidxs=[0, 1, 1, 1, 2, 2, 3, 3]),
  ]
  return {"train": train, "test": test}
