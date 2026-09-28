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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, trims=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row indices of the tops of the rectangles.
    bcols: The column indices of the lefts of the rectangles.
    trims: The rows by which to trim the input rectangles.
    count: The number of rectangles.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls, 5): return None, None
    grid, output = common.grids(width, height)
    for wide, tall, brow, bcol, trim in zip(wides, talls, brows, bcols, trims):
      common.rect(grid, wide, tall, brow, bcol, 8)
      common.rect(output, wide, tall, brow, bcol, 8)
    # Draw the tops and bots.
      bot, top, left, rite, i = brow, brow + tall - 1, bcol, bcol + wide, 0
      while True:
        bot, top, left, rite = bot - 1, top + 1, left + 1, rite - 1
        if left >= rite: break
        for col in range(left, rite):
          if i < trim:
            common.draw(grid, bot, col, 8)
            common.draw(grid, top, col, 8)
            if common.get_pixel(output, bot, col) in [4, 8]: return None, None
            if common.get_pixel(output, top, col) in [4, 8]: return None, None
            common.draw(output, bot, col, 8)
            common.draw(output, top, col, 8)
          else:
            if common.get_pixel(output, bot, col) in [4, 8]: return None, None
            if common.get_pixel(output, top, col) in [4, 8]: return None, None
            common.draw(output, bot, col, 4)
            common.draw(output, top, col, 4)
        i += 1
      # Draw the lefts and rights.
      bot, top, left, rite = brow, brow + tall, bcol, bcol + wide - 1
      while True:
        bot, top, left, rite = bot + 1, top - 1, left - 1, rite + 1
        if bot >= top: break
        for row in range(bot, top):
          if common.get_pixel(output, row, left) in [4, 8]: return None, None
          if common.get_pixel(output, row, rite) in [4, 8]: return None, None
          common.draw(output, row, left, 4)
          common.draw(output, row, rite, 4)
    return grid, output

  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    if count is None: count = common.randint(1, 3)
    attempts = 0
    while True:
      # Three mutually separated octagons need smaller source rectangles to
      # keep the strict five-cell rejection sampler practical.
      max_wide = 2 * width // 3 if count < 3 else width // 3 + 2
      max_tall = height // 2 if count < 3 else height // 3
      wides = [common.randint(5, max_wide) for _ in range(count)]
      talls = [common.randint(3, max_tall) for _ in range(count)]
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      trims = [common.randint(1, (wide - 3) // 2) for wide in wides]
      grid, _ = draw()
      if grid: break
      attempts += 1
      if attempts >= 1000 and count == 3:
        # Guaranteed rule-faithful packing for the vanishingly rare unlucky
        # rejection streak; it keeps the widened count axis bounded in time.
        width, height = 30, 30
        wides, talls, trims = [5, 5, 5], [3, 3, 3], [1, 1, 1]
        brows, bcols = [3, 3, 15], [3, 15, 3]
        grid, _ = draw()
        if grid: break

  # Build the input: filled azure rectangles, each already wearing a short
  # azure staircase on its top and bottom (trimmed to `trim` layers).
  grid = common.grid(width, height)
  for wide, tall, brow, bcol, trim in zip(wides, talls, brows, bcols, trims):
    common.rect(grid, wide, tall, brow, bcol, common.cyan())
    bot, top, left, rite, i = brow, brow + tall - 1, bcol, bcol + wide, 0
    while True:
      bot, top, left, rite = bot - 1, top + 1, left + 1, rite - 1
      if left >= rite: break
      for col in range(left, rite):
        if i < trim:
          common.draw(grid, bot, col, common.cyan())
          common.draw(grid, top, col, common.cyan())
      i += 1

  # Solve it by completing each shape into a full octagon: first extend its
  # azure spikes up and down to their points in yellow, then grow yellow
  # staircases out to the left and right.
  output = common.deepcopy(grid)

  def complete_vertical(k):
    """Extends shape k's top and bottom staircase to its points, in yellow."""
    if k >= len(wides): return
    wide, tall, brow, bcol, trim = (
        wides[k], talls[k], brows[k], bcols[k], trims[k])
    bot, top, left, rite, i = brow, brow + tall - 1, bcol, bcol + wide, 0
    while True:
      bot, top, left, rite = bot - 1, top + 1, left + 1, rite - 1
      if left >= rite: break
      for col in range(left, rite):
        if i >= trim:
          common.draw(output, bot, col, common.yellow())
          common.draw(output, top, col, common.yellow())
      i += 1

  def complete_horizontal(k):
    """Grows shape k's left and right staircase outward, in yellow."""
    if k >= len(wides): return
    wide, tall, brow, bcol, trim = (
        wides[k], talls[k], brows[k], bcols[k], trims[k])
    bot, top, left, rite = brow, brow + tall, bcol, bcol + wide - 1
    while True:
      bot, top, left, rite = bot + 1, top - 1, left - 1, rite + 1
      if bot >= top: break
      for row in range(bot, top):
        common.draw(output, row, left, common.yellow())
        common.draw(output, row, rite, common.yellow())

  complete_vertical(0)
  complete_horizontal(0)
  complete_vertical(1)
  complete_horizontal(1)
  for k in range(2, len(wides)):
    complete_vertical(k)
  for k in range(2, len(wides)):
    complete_horizontal(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=22, wides=[7, 11], talls=[6, 3], brows=[3, 15],
               bcols=[3, 6], trims=[1, 2]),
      generate(width=29, height=26, wides=[17, 7], talls=[8, 3], brows=[3, 19],
               bcols=[1, 14], trims=[4, 2]),
  ]
  test = [
      generate(width=20, height=20, wides=[9, 5], talls=[7, 4], brows=[2, 14],
               bcols=[3, 13], trims=[2, 1]),
  ]
  return {"train": train, "test": test}
