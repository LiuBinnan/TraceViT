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


def generate(rows=None, cols=None, wides=None, talls=None, lights=None,
             colors=None, size=10, num_lights=3, height=None, width=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    lights: a list of light locations
    colors: a list of colors to be used
    size: the width and height of the (square) grid
    num_lights: the number of lights
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: the number of light/box pairs
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    max_count = max(1, min(8, width // 3, (height * width) // 36))
    if count is None:
      count = common.randint(1, max_count)
    else:
      count = max(1, min(count, max_count))
    colors = common.random_colors(count, exclude=[common.gray()])

    if count == 3:
      lights = [common.randint(0, 2), common.randint(4, 5),
                common.randint(7, 9)]
      while True:
        wides = [common.randint(2, 5) for _ in range(count)]
        talls = [common.randint(2, 7) for _ in range(count)]
        rows = [common.randint(2, height - tall) for tall in talls]
        cols = [common.randint(0, width - wide) for wide in wides]
        if len(set(rows)) == 1: continue  # Boxes need to have different rows.
        overlaps = False
        for j in range(count):
          for i in range(count):
            under = cols[j] <= lights[i] and cols[j] + wides[j] > lights[i]
            overlaps = overlaps or (under != (i == j))
          for i in range(j):
            if rows[i] + talls[i] < rows[j] or rows[j] + talls[j] < rows[i]:
              continue
            if cols[i] + wides[i] < cols[j] or cols[j] + wides[j] < cols[i]:
              continue
            overlaps = True
        if not overlaps: break
    else:
      wides = []
      remaining_width = width - (count - 1)
      for idx in range(count):
        remaining_count = count - idx - 1
        max_wide = min(7, remaining_width - 2 * remaining_count)
        wide = common.randint(2, max_wide)
        wides.append(wide)
        remaining_width -= wide
      gap_slots = [0 for _ in range(count + 1)]
      slack = width - sum(wides) - (count - 1)
      for _ in range(slack):
        gap_slots[common.randint(0, count)] += 1
      cols = []
      col = gap_slots[0]
      for idx, wide in enumerate(wides):
        cols.append(col)
        if idx < count - 1:
          col += wide + 1 + gap_slots[idx + 1]
      talls = [common.randint(2, min(7, height - 2)) for _ in range(count)]
      rows = [common.randint(2, height - tall) for tall in talls]
      lights = [common.randint(col, col + wide - 1)
                for col, wide in zip(cols, wides)]

  grid, output = common.grids(width, height)
  for idx in range(min(1, len(colors))):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    output[0][lights[idx]] = grid[0][lights[idx]] = colors[idx]
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
        output[r][c] = colors[idx]
  for idx in range(1, min(2, len(colors))):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    output[0][lights[idx]] = grid[0][lights[idx]] = colors[idx]
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
        output[r][c] = colors[idx]
  for idx in range(2, len(colors)):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    output[0][lights[idx]] = grid[0][lights[idx]] = colors[idx]
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
        output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[4, 2, 7], cols=[1, 4, 7], wides=[2, 4, 3], talls=[5, 4, 3],
               lights=[2, 5, 9], colors=[2, 6, 8]),
      generate(rows=[2, 7, 2], cols=[0, 3, 7], wides=[4, 4, 3], talls=[4, 2, 4],
               lights=[1, 5, 8], colors=[1, 4, 7]),
      generate(rows=[2, 5, 3], cols=[1, 3, 7], wides=[2, 3, 3], talls=[3, 3, 2],
               lights=[1, 5, 8], colors=[1, 6, 7]),
  ]
  test = [
      generate(rows=[7, 2, 2], cols=[0, 2, 8], wides=[4, 5, 2], talls=[2, 4, 7],
               lights=[0, 4, 8], colors=[3, 6, 9]),
  ]
  return {"train": train, "test": test}
