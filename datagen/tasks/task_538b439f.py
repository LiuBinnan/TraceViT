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


def generate(width=None, height=None, lcol=None, lcolor=None, bcolor=None,
             flop=None, xpose=None, wides=None, talls=None, brows=None,
             bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    lcol: The column of the line.
    lcolor: The color of the line.
    bcolor: The color of the boxes.
    flop: Whether to flip the grids horizontally.
    xpose: Whether to transpose the grids.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the tops of the boxes.
    bcols: The column indices of the left sides of the boxes.
    colors: The colors of the background.
  """

  if width is None:
    width, height = common.randint(18, 28), common.randint(18, 28)
    lcol = common.randint(9, max(9, width - 10))
    hues = common.random_colors(4)
    lcolor = hues.pop()
    bcolor = hues.pop()
    colors = [common.randint(0, 19) for _ in range(width * height)]
    colors = [hues[0] if color else hues[1] for color in colors]
    num_boxes = common.randint(1, 3)
    while True:
      talls = [common.randint(2, 5) for _ in range(num_boxes)]
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      if not common.overlaps_1d(brows, talls, 1): break
    wides = [common.randint(2, 5) for _ in range(num_boxes)]
    bcols = [common.randint(1, lcol - wide - 1) for wide in wides]
    flop, xpose = common.randint(0, 1), common.randint(0, 1)
    if xpose: width, height = height, width

  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  if xpose:
    grid = common.transpose(grid)
    width, height = height, width
  if flop: grid = common.flop(grid)
  for r in range(height):
    grid[r][lcol] = lcolor
  for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
    common.rect(grid, wide, tall, brow, bcol, bcolor)
  if flop: grid = common.flop(grid)
  if xpose: grid = common.transpose(grid)
  output = common.deepcopy(grid)

  def put(row, col, color):
    """Paints an output cell, addressed in the orientation of the line."""
    if row < 0 or col < 0 or row >= height or col >= width: return
    if flop: col = width - 1 - col
    if xpose: row, col = col, row
    output[row][col] = color

  def mirror(i):
    """Returns the box and the column its reflection starts at."""
    wide, tall, brow, bcol = wides[i], talls[i], brows[i], bcols[i]
    return wide, tall, brow, bcol, lcol + (lcol - bcol) - wide + 1

  def project_beam(i):
    """Beams box i through the line, in the line's color."""
    if i >= len(wides): return
    wide, tall, brow, bcol, mcol = mirror(i)
    for row in range(brow, brow + tall):
      for col in range(bcol + wide, mcol):
        put(row, col, lcolor)

  def land_reflection(i):
    """Lands box i's reflection at the far end of its beam."""
    if i >= len(wides): return
    wide, tall, brow, bcol, mcol = mirror(i)
    for row in range(brow, brow + tall):
      for col in range(mcol, mcol + wide):
        put(row, col, bcolor)

  project_beam(0)
  land_reflection(0)
  project_beam(1)
  land_reflection(1)
  project_beam(2)
  land_reflection(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=20, lcol=9, lcolor=1, bcolor=8, flop=0, xpose=0,
               wides=[3, 4], talls=[3, 2], brows=[1, 13], bcols=[1, 3],
               colors=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 4, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       4, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
      generate(width=18, height=21, lcol=12, lcolor=2, bcolor=3, flop=1, xpose=1,
               wides=[2, 3], talls=[2, 3], brows=[1, 9], bcols=[5, 4],
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8,
                       8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8,
                       8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8,
                       8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8,
                       8, 8, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8,
                       8, 1, 8, 8, 8, 8, 8, 1, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1,
                       8, 8, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8,
                       1, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8,
                       8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8,
                       8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 1, 8, 8, 1, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8,
                       1, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 1, 8, 8, 8, 8, 1,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 1, 8, 8])
  ]
  test = [
      generate(width=23, height=19, lcol=9, lcolor=3, bcolor=2, wides=[2, 3, 3],
               talls=[2, 5, 3], brows=[1, 6, 15], bcols=[5, 2, 3],
               colors=[4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4,
                       4, 4, 9, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 9, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4,
                       4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 9, 4, 4, 4, 4, 4, 9, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       9, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 9, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
  ]
  return {"train": train, "test": test}
