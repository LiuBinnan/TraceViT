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


def generate(rows=None, cols=None, lengths=None, cdirs=None, pcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: rows of the lines.
    cols: columns of the lines.
    lengths: lengths of the lines.
    cdirs: directions of the lines.
    pcol: col of the pixel.
  """

  def draw():
    pc = pcol
    grid, output = common.grids(10, 10)

    def check_for_holes(row, col):
      holes = []
      for c in range(col, 10):  # Check for a wall to the right.
        if grid[row][c] == 2: break  # We see a wall, so it's closed!
        if grid[row + 1][c] == 0: holes.append(c)
      for c in range(col, -1, -1):  # Check for a wall to the left
        if grid[row][c] == 2: break  # We see a wall, so it's closed!
        if grid[row + 1][c] == 0: holes.append(c)
      return holes

    def fill(row, col):
      while row >= 0:
        if sum([grid[row][c] for c in range(10)]) == 0: break
        for c in range(col, 10):
          if output[row][c] == 2: break
          output[row][c] = 1
        for c in range(col, -1, -1):
          if output[row][c] == 2: break
          output[row][c] = 1
        row -= 1

    # First, draw the red lines.
    for row, col, length, cdir in zip(rows, cols, lengths, cdirs):
      for i in range(length):
        r, c = row + (i if cdir else 0), col + (0 if cdir else i)
        output[r][c] = grid[r][c] = 2
    # Then, draw the blue dot.
    prow = 0
    grid[prow][pc] = 1
    # Then, the dot trickles down, and we check various conditions.
    while prow < 9:
      if grid[prow + 1][pc] == 2:
        holes = check_for_holes(prow, pc)
        if not holes:
          fill(prow, pc)
          break
        if len(holes) == 1:
          pc = holes[0]
        else: return None, None  # Ill-defined case.
      prow += 1
    # If we made it all the way down, draw the thin puddle of water.
    if prow == 9:
      for c in range(10):
        output[9][c] = 1
    return grid, output

  if rows is None:
    for _attempt in range(500):
      # First, choose the locations of all vertical lines.
      if common.randint(0, 1):  # the single case
        vrows, vcols, vlengths = [3, 3], [2, 7], [4, 4]
        middle = common.randint(0, 2)
        if middle:
          vrows.append(3)
          vcols.append(3 + middle)
          vlengths.append(4)
      else:  # the double case
        vrows, vcols, vlengths = [2, 2, 6, 6], [], [3, 3, 3, 3]
        for _ in range(2):  # For the top and bottom boxes.
          while True:
            cols = sorted(common.sample(range(10), 2))
            if cols[0] + 1 < cols[1]: break
          vcols.extend(cols)
      # Second, extend the bottom of those lines to the left, right, or neither.
      hrows, hcols, hlengths = [], [], []
      for vrow, vcol, vlength in zip(vrows, vcols, vlengths):
        col = max(vcol - common.randint(0, 3), 2)
        if col < vcol:
          hrows.append(vrow + vlength - 1)
          hcols.append(col)
          hlengths.append(vcol - col)
        col = min(vcol + common.randint(0, 3), 8)
        if col > vcol:
          hrows.append(vrow + vlength - 1)
          hcols.append(vcol)
          hlengths.append(col - vcol)
      rows = vrows + hrows
      cols = vcols + hcols
      lengths = vlengths + hlengths
      cdirs = [1] * len(vlengths) + [0] * len(hlengths)
      pcol = common.randint(1, 8)
      grid, _ = draw()
      if grid: break
    else:
      rows, cols = [3, 3, 6], [2, 7, 2]
      lengths, cdirs, pcol = [4, 4, 6], [1, 1, 0], 6

  # Rebuild the input grid and, following the falling marble, plan where the
  # water finally gathers -- pure bookkeeping over the already-sampled params,
  # drawing no randomness and touching `output` nowhere.
  def simulate():
    pc = pcol
    grid, _ = common.grids(10, 10)
    for row, col, length, cdir in zip(rows, cols, lengths, cdirs):
      for i in range(length):
        r, c = row + (i if cdir else 0), col + (0 if cdir else i)
        grid[r][c] = common.red()
    grid[0][pc] = common.blue()

    def holes_at(row, col):
      holes = []
      for c in range(col, 10):
        if grid[row][c] == common.red(): break
        if grid[row + 1][c] == common.black(): holes.append(c)
      for c in range(col, -1, -1):
        if grid[row][c] == common.red(): break
        if grid[row + 1][c] == common.black(): holes.append(c)
      return holes

    def water_span(row, col):
      cs = []
      for c in range(col, 10):
        if grid[row][c] == common.red(): break
        cs.append(c)
      for c in range(col, -1, -1):
        if grid[row][c] == common.red(): break
        cs.append(c)
      return cs

    prow, land, levels, ok = 0, None, [], True
    while prow < 9:
      if grid[prow + 1][pc] == common.red():
        holes = holes_at(prow, pc)
        if not holes:  # A sealed cup: the water pools and rises.
          land = (prow, pc)
          r = prow
          while r >= 0 and sum(grid[r][c] for c in range(10)) != 0:
            levels.append((r, water_span(r, pc)))
            r -= 1
          break
        if len(holes) == 1:  # A single leak: the marble slips through it.
          pc = holes[0]
        else:
          ok = False
          break
      prow += 1
    if ok and prow == 9:  # It fell clear through: a thin puddle on the floor.
      land = (9, pc)
      levels = [(9, list(range(10)))]
    return grid, land, levels, ok

  grid, land, levels, ok = simulate()
  if not ok:
    return {"input": None, "output": None}
  output = common.grid(10, 10)
  for row, col, length, cdir in zip(rows, cols, lengths, cdirs):
    for i in range(length):
      r, c = row + (i if cdir else 0), col + (0 if cdir else i)
      output[r][c] = common.red()

  def drop_marble():
    """The marble settles where the water will gather."""
    if land is not None:
      output[land[0]][land[1]] = common.blue()

  def pour_level(i):
    """Raises the water one row (bottom-up), or spreads the floor puddle."""
    if i >= len(levels): return
    r, cs = levels[i]
    for c in cs:
      output[r][c] = common.blue()

  drop_marble()
  pour_level(0)
  pour_level(1)
  pour_level(2)
  for i in range(3, len(levels)):
    pour_level(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 3, 3, 6], cols=[2, 5, 7, 2], lengths=[4, 4, 4, 4], cdirs=[1, 1, 1, 0], pcol=4),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 6], cdirs=[1, 1, 0], pcol=8),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 4], cdirs=[1, 1, 0], pcol=4),
      generate(rows=[3, 3, 3, 6], cols=[2, 5, 7, 4], lengths=[4, 4, 4, 4], cdirs=[1, 1, 1, 0], pcol=6),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 6], cdirs=[1, 1, 0], pcol=6),
  ]
  test = [
      generate(rows=[2, 2, 4, 6, 6, 8], cols=[5, 9, 7, 2, 8, 2], lengths=[3, 3, 3, 3, 3, 7], cdirs=[1, 1, 0, 1, 1, 0], pcol=8),
  ]
  return {"train": train, "test": test}
