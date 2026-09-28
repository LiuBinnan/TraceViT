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


def generate(width=None, height=None, size=None, wide=None, tall=None,
             brow=None, bcol=None, rrows=None, rcols=None, colors=None,
             patterns=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    grid = common.grid(width, height)
    common.hollow_rect(grid, wide, tall, brow, bcol, 1)
    # First, ensure the rectangles touch at least a single blue pixel.
    for rrow, rcol in zip(rrows, rcols):
      seen = False
      for row in range(size + 2):
        for col in range(size + 2):
          if grid[rrow + row][rcol + col] == 1: seen = True
      if not seen: return None, None
    # Second, determine the order of the rectangles.
    ids = common.grid(width, height, -1)
    for i, (rrow, rcol) in enumerate(zip(rrows, rcols)):
      common.hollow_rect(ids, size + 2, size + 2, rrow, rcol, i)
    order = []
    for col in range(wide):
      idx = ids[brow][bcol + col]
      if idx != -1 and idx not in order: order.append(idx)
    for row in range(tall):
      idx = ids[row][bcol + wide - 1]
      if idx != -1 and idx not in order: order.append(idx)
    for col in range(wide - 1, -1, -1):
      idx = ids[brow + tall - 1][bcol + col]
      if idx != -1 and idx not in order: order.append(idx)
    for row in range(tall - 1, -1, -1):
      idx = ids[row][bcol]
      if idx != -1 and idx not in order: order.append(idx)
    # Third, draw the rectangles.
    for i in range(len(order)):
      idx = order[i]
      rrow, rcol = rrows[idx], rcols[idx]
      common.hollow_rect(grid, size + 2, size + 2, rrow, rcol, 2)
      for row in range(size):
        for col in range(size):
          r, c = rrow + 1 + row, rcol + 1 + col
          color = int(patterns[idx * size * size + row * size + col])
          grid[r][c] = color * colors[i]
    # Fourth, ensure the corners of the box are visible.
    if grid[brow][bcol] != 1: return None, None
    if grid[brow + tall - 1][bcol] != 1: return None, None
    if grid[brow][bcol + wide - 1] != 1: return None, None
    if grid[brow + tall - 1][bcol + wide - 1] != 1: return None, None
    return grid, order

  if width is None:
    # Widened from randint(18, 27): a modest band widening that
    # keeps grids near-square (width ~ height ~ base, as the task naturally is)
    # while extending the size range to <=29.
    base = common.randint(16, 28)
    size = 3
    if base > 21: size = 4
    if base > 24: size = 5
    width, height = base + common.randint(-1, 1), base + common.randint(-1, 1)
    wide = width - common.randint(size, size * 2)
    tall = height - common.randint(size, size * 2)
    brow = common.randint(1, height - tall - 1)
    bcol = common.randint(1, width - wide - 1)
    num_rects = common.randint(3, 5)
    # Open sides can hold length-(size + 2) intervals with a one-cell gap.
    side_capacity = 2 * ((wide - 1) // (size + 3) +
                         (tall - 1) // (size + 3))
    # In the tight four-side case, extreme box offsets lose one corner slot.
    corner_slack = (wide + tall - 4 * (size + 2) +
                    min(brow, height - tall - brow) +
                    min(bcol, width - wide - bcol))
    max_rects = 3 if side_capacity == 4 and corner_slack < 4 else side_capacity
    while num_rects > max_rects:
      num_rects = common.randint(3, 5)
    colors = common.random_colors(num_rects, exclude=[1, 2])
    patterns = []
    for _ in range(num_rects):
      while True:
        pixels = []
        for row in range(size):
          for col in range(size):
            if common.randint(0, 1): pixels.append((row, col))
        if pixels and common.diagonally_connected(pixels): break
      for row in range(size):
        for col in range(size):
          patterns.append(1 if (row, col) in pixels else 0)
    patterns = "".join([str(p) for p in patterns])
    # Keep looking for legal, nonoverlapping positions until one works. On tight
    # seeds the random placement almost never satisfies touch + corner
    # visibility, so after an attempt cap (kept high so most seeds still take the
    # diverse random path) fall back to a constructive ring: seat
    # the rectangles tangent to the four box sides at (size + 3) pitch, kept a
    # cell clear of every corner. Touch and corner visibility then hold by
    # construction, and the sides occupy disjoint row/col bands so no two
    # rectangles overlap. If the tight corner slots collide the ring seats one
    # fewer, so trim colors/patterns to the count actually placed.
    sizes = [size + 2] * num_rects
    attempts = 0
    while True:
      if attempts < 8000:
        rrows = [common.randint(0, height - size - 2) for _ in range(num_rects)]
        rcols = [common.randint(0, width - size - 2) for _ in range(num_rects)]
        attempts += 1
        if common.overlaps(rrows, rcols, sizes, sizes, 1): continue
        grid, _ = draw()
        if grid: break
      else:
        step = size + 3
        ring = []
        rtop = max(0, brow - (size + 1))
        col = bcol + 1
        while col + size + 1 <= bcol + wide - 2:
          ring.append((rtop, col)); col += step
        rright = min(width - size - 2, bcol + wide - 1)
        row = brow + 1
        while row + size + 1 <= brow + tall - 2:
          ring.append((row, rright)); row += step
        rbot = min(height - size - 2, brow + tall - 1)
        col = bcol + 1
        while col + size + 1 <= bcol + wide - 2:
          ring.append((rbot, col)); col += step
        rleft = max(0, bcol - (size + 1))
        row = brow + 1
        while row + size + 1 <= brow + tall - 2:
          ring.append((row, rleft)); row += step
        chosen = []
        for cand_row, cand_col in ring:
          trow = [p[0] for p in chosen] + [cand_row]
          tcol = [p[1] for p in chosen] + [cand_col]
          tsz = [size + 2] * len(trow)
          if common.overlaps(trow, tcol, tsz, tsz, 1): continue
          chosen.append((cand_row, cand_col))
          if len(chosen) >= num_rects: break
        num_rects = len(chosen)
        rrows = [p[0] for p in chosen]
        rcols = [p[1] for p in chosen]
        colors = colors[:num_rects]
        patterns = patterns[:num_rects * size * size]
        grid, _ = draw()
        break

  grid, order = draw()
  output = common.deepcopy(grid)

  def recolor_rectangle(i):
    """Recolors rectangle i with the next color around the blue box."""
    if i >= len(order): return
    idx = order[i]
    rrow, rcol = rrows[idx], rcols[idx]
    for row in range(size):
      for col in range(size):
        color = int(patterns[idx * size * size + row * size + col])
        output[rrow + row + 1][rcol + col + 1] = (
            color * colors[(i + 1) % len(colors)])

  recolor_rectangle(0)
  recolor_rectangle(1)
  recolor_rectangle(2)
  recolor_rectangle(3)
  recolor_rectangle(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=20, size=3, wide=16, tall=14, brow=2, bcol=2,
               rrows=[1, 6, 11], rcols=[6, 15, 8], colors=[6, 3, 8],
               patterns="010111010010101010010011100"),
      generate(width=21, height=22, size=3, wide=16, tall=14, brow=3, bcol=2,
               rrows=[1, 7, 14, 6], rcols=[7, 15, 6, 1], colors=[3, 8, 6, 7],
               patterns="010111010110110001010011000011110100"),
      generate(width=26, height=26, size=5, wide=18, tall=16, brow=4, bcol=3,
               rrows=[1, 8, 10], rcols=[8, 17, 1], colors=[8, 4, 3],
               patterns="001000111001010010100000000000001101110100110000000000010100111101010000000"),
  ]
  test = [
      generate(width=27, height=27, size=5, wide=21, tall=22, brow=2, bcol=3,
               rrows=[0, 0, 10, 20, 9], rcols=[6, 15, 19, 10, 0],
               colors=[4, 3, 7, 6, 8],
               patterns="00000010100111001110001000000001110110110111000000001001111000100001110000000100111110010000100011000100001100001100001100010"),
  ]
  return {"train": train, "test": test}
