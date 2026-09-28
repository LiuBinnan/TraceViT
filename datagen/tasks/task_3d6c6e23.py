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


def generate(width=None, height=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if width is None:
    # First, decide the grid dimensions + number of lines + size of bases.
    num_lines, height = common.randint(1, 2), common.randint(15, 30)
    bases = [3 if common.randint(0, 1) else 5 for _ in range(num_lines)]
    if num_lines == 1:
      width = 2 * common.randint(3, 10) + 1
      cols = [width // 2]
    else:
      side, mid = common.randint(0, 3), common.randint(2, 6)
      width = sum(bases) + 2 * side + mid
      cols = [bases[0] // 2 + side, width - bases[1] // 2 - 1 - side]
    # Next, determine the colors and spacing of each line.
    while True:
      colors, good = [], True
      for base in bases:
        hues = []
        for segment_length in range(1, base + 1, 2):
          hues.extend([common.random_color()] * segment_length)
        row, spacing = 0, common.randint(1, 6)
        for hue in hues:
          for _ in range(common.randint(0, spacing)):
            colors, row = colors + [0], row + 1
          colors, row = colors + [hue], row + 1
        if row + base > height: good = False
        while row < height:
          colors, row = colors + [0], row + 1
      if good: break
    colors = "".join(str(c) for c in colors)

  row_offsets = [[1, 0, 0, 0], [2, 1, 1, 1, 0, 0, 0, 0, 0]]
  col_offsets = [[0, -1, 0, 1], [0, -1, 0, 1, -2, -1, 0, 1, 2]]
  grid = common.grid(width, height)
  output = common.grid(width, height)
  stacks = []
  for i, col in enumerate(cols):
    values = []
    for r in range(height):
      color = int(colors[i * height + r])
      grid[r][col] = color
      if color:
        values.append(color)
    idx = 0 if len(values) == 4 else 1
    cells = []
    for roff, coff, value in zip(row_offsets[idx], col_offsets[idx], values):
      cells.append((height - 1 - roff, col + coff, roff, value))
    stacks.append(cells)
  for cells in stacks:
    for row, col, roff, value in cells:
      if roff > 0:
        output[row][col] = value
  for cells in stacks:
    for row, col, roff, value in cells:
      if roff == 0:
        output[row][col] = value
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=16, cols=[6],
               colors="07707770707770000"),
      generate(width=11, height=16, cols=[5], colors="7007007007000000"),
      generate(width=9, height=21, cols=[4], colors="477706060060606000000"),
  ]
  test = [
      generate(width=10, height=30, cols=[2, 8],
               colors="220221101101000000000000000000700000000000700000007007000000"),
  ]
  return {"train": train, "test": test}
