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


def generate(width=None, height=None, length=None, spacing=None, bgcolor=None,
             fgcolor=None, wides=None, talls=None, brows=None, bcols=None,
             bcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the boxes.
    spacing: The spacing between the boxes.
    bgcolor: The color of the box borders.
    fgcolor: The color of most box centers.
    wides: The widths of the special boxes.
    talls: The heights of the special boxes.
    brows: The rows of the special boxes.
    bcols: The columns of the special boxes.
    bcolors: The colors of the special boxes.
  """

  def draw():
    # Check that the boxes don't overlap along any row or column.
    rows, cols = [], []
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      rows += [brow, brow + tall - 1]
      cols += [bcol, bcol + wide - 1]
    if len(rows) != len(set(rows)) or len(cols) != len(set(cols)):
      return None, None
    grid, output = common.grids(width, height)
    # Draw the special connecting lines.
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      for i in range(length - 2):
        r = brow * (length + spacing) + 4 - 2 + i
        c = bcol * (length + spacing) + 4 - 2 + i
        w = wide * length + (wide - 1) * spacing - 2 - 2 * i
        t = tall * length + (tall - 1) * spacing - 2 - 2 * i
        common.hollow_rect(output, w, t, r, c, bcolor)
    # Draw the "standard" boxes (with the default fgcolor centers).
    for row in range(1, height, length + spacing):
      for col in range(1, width, length + spacing):
        common.hollow_rect(grid, length, length, row, col, bgcolor)
        common.hollow_rect(output, length, length, row, col, bgcolor)
        common.rect(grid, length - 2, length - 2, row + 1, col + 1, fgcolor)
        common.rect(output, length - 2, length - 2, row + 1, col + 1, fgcolor)
    # Draw the special centers.
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      coords = []
      coords.append((brow, bcol))
      coords.append((brow + tall - 1, bcol))
      coords.append((brow, bcol + wide - 1))
      coords.append((brow + tall - 1, bcol + wide - 1))
      for row, col in coords:
        r, c = row * (length + spacing) + 2, col * (length + spacing) + 2
        common.rect(grid, length - 2, length - 2, r, c, bcolor)
        common.rect(output, length - 2, length - 2, r, c, bcolor)
    return grid, output

  if width is None:
    if length is None:
      length = common.randint(3, 6)
    if spacing is None:
      spacing = common.randint(1, 4)
    max_num_boxes = (30 + spacing) // (length + spacing) // 2
    num_boxes = min(common.randint(1, 2), max_num_boxes)
    min_size = max(15, 2 * num_boxes * (length + spacing) - spacing)
    while True:
      width = common.randint(min_size, 30)
      height = common.randint(min_size, 30)
      eff_width = (width + spacing) // (length + spacing)
      eff_height = (height + spacing) // (length + spacing)
      colors = common.shuffle([1, 2, 3, 4, 8])
      bgcolor = colors.pop()
      fgcolor = colors.pop()
      wides, talls, brows, bcols, bcolors = [], [], [], [], []
      for _ in range(num_boxes):
        wide, tall = common.randint(2, eff_width), common.randint(2, eff_height)
        brow = common.randint(0, eff_height - tall)
        bcol = common.randint(0, eff_width - wide)
        bcolor = colors.pop()
        wides.append(wide)
        talls.append(tall)
        brows.append(brow)
        bcols.append(bcol)
        bcolors.append(bcolor)
      grid, _ = draw()
      if grid: break

  # Build the input grid (draw() draws no randomness).
  grid, _ = draw()

  # Solve forward: the input shows a lattice of identical boxes, with a few
  # boxes marked in a special color at the four corners of a rectangle. Connect
  # each set of four same-colored corner boxes by drawing the rectangle's sides
  # through the background gutters between boxes (a side never covers a box).
  output = common.deepcopy(grid)

  def paint_band(row, col, w, h, color):
    """Paints a solid band, but only over the background gutter cells."""
    for r in range(row, row + h):
      for c in range(col, col + w):
        if grid[r][c] == common.black():
          output[r][c] = color

  def box_frame(k):
    """Geometry of special box k's connecting rectangle: (row, col, w, h, th)."""
    r0 = brows[k] * (length + spacing) + 2
    c0 = bcols[k] * (length + spacing) + 2
    w0 = wides[k] * length + (wides[k] - 1) * spacing - 2
    t0 = talls[k] * length + (talls[k] - 1) * spacing - 2
    return r0, c0, w0, t0, length - 2

  def connect_horizontal(k):
    """Connects box k's marked corners along the top and bottom sides."""
    if k >= len(bcolors):
      return
    r0, c0, w0, t0, th = box_frame(k)
    paint_band(r0, c0, w0, th, bcolors[k])
    paint_band(r0 + t0 - th, c0, w0, th, bcolors[k])

  def connect_vertical(k):
    """Connects box k's marked corners along the left and right sides."""
    if k >= len(bcolors):
      return
    r0, c0, w0, t0, th = box_frame(k)
    paint_band(r0, c0, th, t0, bcolors[k])
    paint_band(r0, c0 + w0 - th, th, t0, bcolors[k])

  connect_horizontal(0)
  connect_vertical(0)
  connect_horizontal(1)
  connect_vertical(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=29, height=24, length=4, spacing=1, bgcolor=3, fgcolor=2,
               wides=[3, 4], talls=[4, 3], brows=[0, 2], bcols=[3, 1],
               bcolors=[8, 4]),
      generate(width=28, height=23, length=3, spacing=2, bgcolor=2, fgcolor=4,
               wides=[4, 2], talls=[3, 3], brows=[1, 0], bcols=[1, 2],
               bcolors=[1, 3]),
      generate(width=29, height=26, length=3, spacing=3, bgcolor=1, fgcolor=2,
               wides=[4], talls=[3], brows=[1], bcols=[0], bcolors=[3]),
  ]
  test = [
      generate(width=30, height=30, length=5, spacing=2, bgcolor=4, fgcolor=2,
               wides=[4, 2], talls=[3, 3], brows=[0, 1], bcols=[0, 1],
               bcolors=[3, 8]),
  ]
  return {"train": train, "test": test}
