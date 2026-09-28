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


def generate(width=None, height=None, color=None, brows=None, bcols=None,
             lengthss=None, turnss=None, idxss=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    color: The color of the lines.
    brows: The row indices of the start of each box.
    bcols: The column indices of the start of each box.
    lengthss: The lengths of each segment.
    turnss: The turns at the end of each segment.
    idxss: The box indices of each segment.
  """

  def draw():
    num_reds = 0
    grid = common.grid(width, height)
    for bidx, (brow, bcol) in enumerate(zip(brows, bcols)):
      lengths = [int(length) for length, idx in zip(lengthss, idxss) if idx == str(bidx)]
      turns = [turn for turn, idx in zip(turnss, idxss) if idx == str(bidx)]
      # First, draw the pixels.
      row, col = brow, bcol
      rdirs, cdirs, angle = [0, 1, 0, -1], [1, 0, -1, 0], 0
      for length, turn in zip(lengths, turns):
        for i in range(length - 1):
          common.draw(grid, row, col, color)
          row, col = row + rdirs[angle], col + cdirs[angle]
        if turn == "L":
          angle = (angle + 3) % 4
          num_reds += 1
        elif turn == "R":
          angle = (angle + 1) % 4
      # Second, ensure that each pixel has exactly two neighbors.
      row, col = brow, bcol
      rdirs, cdirs, angle = [0, 1, 0, -1], [1, 0, -1, 0], 0
      for length, turn in zip(lengths, turns):
        for _ in range(length - 1):
          if row < 0 or row >= height or col < 0 or col >= width:
            return None, None  # Out of bounds.
          neighbors = 0
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if common.get_pixel(grid, row + dr, col + dc) == color:
              neighbors += 1
          if neighbors != 2: return None, None
          row, col = row + rdirs[angle], col + cdirs[angle]
        if turn == "L":
          angle = (angle + 3) % 4
        elif turn == "R":
          angle = (angle + 1) % 4
    if num_reds < 5: return None, None
    return grid, None

  if width is None:
    width, height = common.randint(12, 16), common.randint(12, 16)
    color, num_boxes = common.random_color(exclude=[2, 4]), common.randint(2, 3)
    attempts = 0
    while True:
      attempts += 1
      if attempts > 1000:
        # Bound the rejection tail with separated, guaranteed-simple loops.
        # Each outward detour contributes two left turns, so either layout has
        # six left turns in total and therefore keeps the bend-marking rule
        # non-degenerate.
        one_detour = ("22322454", "LRRLRRRR", 5)
        two_detours = ("223225223225", "LRRLRRLRRLRR", 7)
        left = common.randint(0, width - 11)
        if num_boxes == 2:
          shapes = [two_detours, one_detour]
          if common.randint(0, 1): shapes.reverse()
          bcols = [left, left + 6]
          brows = [common.randint(1, height - shape[2] + 1)
                   for shape in shapes]
        else:
          shapes = [one_detour, one_detour, one_detour]
          top = common.randint(0, height - 11)
          bcols = [left, left + 6, left + 6 * common.randint(0, 1)]
          brows = [top + 1, top + 1, top + 7]
        lengthss = "".join(shape[0] for shape in shapes)
        turnss = "".join(shape[1] for shape in shapes)
        idxss = "".join(str(i) * len(shape[0])
                        for i, shape in enumerate(shapes))
        break
      wides = [common.randint(3, 10) for _ in range(num_boxes)]
      talls = [common.randint(3, 10) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      lengthss, turnss, idxss = [], [], []
      for bidx, (wide, tall) in enumerate(zip(wides, talls)):
        lengths = [wide, tall, wide, tall]
        turns = ["R", "R", "R", "R"]
        idxs = [bidx] * 4
        for _ in range((wide + tall) // 4):
          idx = common.randint(0, len(lengths) - 1)
          if lengths[idx] < 5: continue
          segment = common.randint(3, lengths[idx] - 2)
          start = common.randint(1, lengths[idx] - segment - 1)
          depth = common.randint(2, 4)
          length = [start + 1, depth, segment, depth, lengths[idx] - (start + segment) + 1]
          turn = ["L", "R", "R", "L"] if common.randint(0, 1) else ["R", "L", "L", "R"]
          lengths = lengths[:idx] + length + lengths[idx + 1:]
          turns = turns[:idx] + turn + turns[idx:]
          idxs = idxs[:idx] + [bidx] * 4 + idxs[idx:]
        lengthss.extend(lengths)
        turnss.extend(turns)
        idxss.extend(idxs)
      lengthss = "".join(str(length) for length in lengthss)
      turnss = "".join(turnss)
      idxss = "".join(str(idx) for idx in idxss)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()

  def bend_batches():
    """Splits each path's bends into an early and a late half, in tracing order."""
    batches = [[] for _ in range(6)]
    for bidx, (brow, bcol) in enumerate(zip(brows, bcols)):
      lengths = [int(length) for length, idx in zip(lengthss, idxss)
                 if idx == str(bidx)]
      turns = [turn for turn, idx in zip(turnss, idxss)
               if idx == str(bidx)]
      bends = []
      row, col = brow, bcol
      rdirs, cdirs, angle = [0, 1, 0, -1], [1, 0, -1, 0], 0
      for length, turn in zip(lengths, turns):
        row += rdirs[angle] * (length - 1)
        col += cdirs[angle] * (length - 1)
        bends.append((row, col, turn))
        if turn == "L":
          angle = (angle + 3) % 4
        elif turn == "R":
          angle = (angle + 1) % 4
      half = (len(bends) + 1) // 2
      slot = min(bidx, 2)  # Paths past the third fold into the last pair.
      batches[2 * slot] += bends[:half]
      batches[2 * slot + 1] += bends[half:]
    return batches

  bend_groups = bend_batches()
  output = common.deepcopy(grid)

  def mark_bend_batch(i):
    """Colors half of one path's bends: left bends red, right bends yellow."""
    if output is None or i >= len(bend_groups): return
    for row, col, turn in bend_groups[i]:
      turn_color = common.red() if turn == "L" else common.yellow()
      common.draw(output, row, col, turn_color)

  mark_bend_batch(0)
  mark_bend_batch(1)
  mark_bend_batch(2)
  mark_bend_batch(3)
  mark_bend_batch(4)
  mark_bend_batch(5)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=12, color=8, brows=[1, 4, 9], bcols=[1, 10, 2],
               lengthss="75423423 5523533323 3333",
               turnss="RRLRRLRR RRLRRRLLRR RRRR",
               idxss="00000000 1111111111 2222"),
      generate(width=13, height=13, color=3, brows=[2, 8], bcols=[2, 4],
               lengthss="32443244 5322364254", turnss="LRRRLRRR LRLRRRLRRR",
               idxss="00000000 111111111111"),
      generate(width=16, height=14, color=1, brows=[1, 10], bcols=[1, 3],
               lengthss="6235324434 62324224323283",
               turnss="RLRRLRRLRR LRLRRLRRRLLRRR",
               idxss="0000000000 11111111111111"),
  ]
  test = [
      generate(width=16, height=15, color=3, brows=[2, 4, 12], bcols=[1, 11, 3],
               lengthss="22324235432342443334 49543423 3333",
               turnss="LRRLLRRRLLRRLRRRLLRR RRRRLLRR RRRR",
               idxss="00000000000000000000 11111111 2222"),
  ]
  return {"train": train, "test": test}
