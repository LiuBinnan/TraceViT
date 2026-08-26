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


def generate(size=None, rows=None, cols=None, wides=None, talls=None,
             dotrow=None, dotcol=None, flip=None, xpose=None,
             height=None, width=None, count=None, num_colors=None,
             colors=None, background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    dotrow: the vertical coordinate of the dot
    dotcol: the horizontal coordinate of the dot
    flip: a boolean indicating whether the grids should be flipped
    xpose: a boolean indicating whether the grids should be transposed
    height: the (logical) vertical extent of the grid; defaults to size
    width: the (logical) horizontal extent of the grid; defaults to size
    count: the number of independent box-and-dot objects to attempt
    num_colors: the number of non-background colors available to the objects
    colors: optional non-background color palette
    background: the background color
  """
  if size is None:
    if height is None:
      height = common.randint(8, 30)
    if width is None:
      width = common.randint(8, 30)
    if count is None:
      count = common.randint(1, 10)
    if background is None:
      background = common.randint(0, 9)
    if num_colors is None:
      num_colors = common.randint(2, 9)
    palette = [color for color in range(10) if color != background]
    num_colors = max(2, min(num_colors, len(palette)))
    colors = common.sample(palette, num_colors) if colors is None else colors
    colors = [color for color in colors if color != background]
    while len(colors) < 2:
      color = common.choice(palette)
      if color not in colors:
        colors.append(color)
    if flip is None:
      flip = common.randint(0, 1)
    if xpose is None:
      xpose = common.randint(0, 1)
  else:
    height = width = size
    if background is None:
      background = common.black()
    if colors is None:
      colors = [common.green(), common.red()]
    if flip is None:
      flip = 0
    if xpose is None:
      xpose = 0

  def coords(r, c):
    if flip:
      r = height - 1 - r
    if xpose:
      r, c = c, r
    return r, c

  def set_both(r, c, color):
    r, c = coords(r, c)
    output[r][c] = grid[r][c] = color

  def set_output(r, c, color):
    r, c = coords(r, c)
    output[r][c] = color

  def line_from(r, c, dr, dc):
    pixels = []
    while 0 <= r < height and 0 <= c < width:
      pixels.append((r, c))
      r += dr
      c += dc
    return pixels

  def neighbors(pixels):
    out = set()
    for r, c in pixels:
      for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
          nr, nc = r + dr, c + dc
          if 0 <= nr < height and 0 <= nc < width:
            out.add((nr, nc))
    return out

  # Logical drawing happens in a (height x width) frame; xpose swaps the physical
  # axes, so the physical grid is transposed accordingly. When height == width
  # (e.g. validate()), both branches collapse to grids(size, size).
  if xpose:
    grid, output = common.grids(height, width, background)
  else:
    grid, output = common.grids(width, height, background)
  if rows is None:
    occupied = set()
    placed = 0
    tries = 0
    while placed < count and tries < 50 * count:
      tries += 1
      short_max = max(3, min(height, width) // 2 - 1)
      short = common.randint(3, short_max)
      long = common.randint(2 * short + 1, max(2 * short + 1,
                                              min(height, width) - 1))
      if common.randint(0, 1):
        tall, wide = long, short
      else:
        tall, wide = short, long
      row_cands = list(range(1, height - tall))
      col_cands = list(range(1, width - wide))
      if not row_cands or not col_cands:
        continue
      row = common.choice(row_cands)
      col = common.choice(col_cands)
      body = set((row + r, col + c) for r in range(tall) for c in range(wide))
      if wide < tall:
        left = [(row + r, col) for r in range(wide - 1, tall - wide + 1)]
        right = [(r, col + wide - 1) for r, _ in left]
        dot = common.choice(left + right)
        dr, dc = (0, -1) if dot in left else (0, 1)
        radius = wide - 1
      else:
        top = [(row, col + c) for c in range(tall - 1, wide - tall + 1)]
        bottom = [(row + tall - 1, c) for _, c in top]
        dot = common.choice(top + bottom)
        dr, dc = (-1, 0) if dot in top else (1, 0)
        radius = tall - 1
      line = set(line_from(dot[0], dot[1], dr, dc))
      shell = set()
      for r, c in line:
        for delta in range(-radius, radius + 1):
          nr, nc = (r + delta, c) if dc else (r, c + delta)
          if 0 <= nr < height and 0 <= nc < width:
            shell.add((nr, nc))
      footprint = body | shell
      if footprint & occupied:
        continue
      sqc, dotc = common.sample(colors, 2)
      for r, c in body:
        set_both(r, c, sqc)
      set_both(dot[0], dot[1], dotc)
      for r, c in shell:
        set_output(r, c, sqc)
      for r, c in line:
        set_output(r, c, dotc)
      occupied |= footprint | neighbors(body)
      placed += 1
    return {"input": grid, "output": output}

  defect = rows[1] + talls[1] < rows[0] + dotrow - wides[0]  # Aims at partner!
  for idx in range(min(1, len(rows))):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    for r in range(tall):
      for c in range(wide):
        set_both(row + r, col + c, common.green())
    r, c = row + dotrow * (1 - idx), col + dotcol * idx
    if defect and not idx: c += wides[0] - 1
    set_both(r, c, common.red())
  for idx in range(1, len(rows)):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    for r in range(tall):
      for c in range(wide):
        set_both(row + r, col + c, common.green())
    r, c = row + dotrow * (1 - idx), col + dotcol * idx
    set_both(r, c, common.red())
  locol = 0 if not defect else cols[0] + wides[0]
  hicol = cols[0] if not defect else width
  for c in range(locol, hicol):
    r = rows[0] + dotrow
    for dr in range(-wides[0] + 1, wides[0]):
      set_output(r + dr, c, common.green())
    set_output(r, c, common.red())
  for r in range(0, rows[1]):
    c = cols[1] + dotcol
    for dc in range(-talls[1] + 1, talls[1]):
      set_output(r, c + dc, common.green())
    set_output(r, c, common.red())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[2, 4], cols=[3, 6], wides=[2, 4], talls=[6, 2],
               dotrow=3, dotcol=2, flip=1, xpose=0),
      generate(size=20, rows=[1, 10], cols=[4, 10], wides=[2, 10],
               talls=[18, 3], dotrow=4, dotcol=5, flip=1, xpose=1),
      generate(size=20, rows=[0, 10], cols=[3, 9], wides=[3, 11],
               talls=[14, 5], dotrow=5, dotcol=5, flip=0, xpose=1),
      generate(size=20, rows=[5, 4], cols=[0, 6], wides=[5, 11],
               talls=[15, 4], dotrow=10, dotcol=6, flip=1, xpose=1),
  ]
  test = [
      generate(size=20, rows=[0, 14], cols=[4, 7], wides=[3, 13],
               talls=[11, 6], dotrow=5, dotcol=6, flip=0, xpose=0),
  ]
  return {"train": train, "test": test}
