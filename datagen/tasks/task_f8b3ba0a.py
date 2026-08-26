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


def generate(width=None, colors=None, cell_h=1, cell_w=2):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid (number of lattice cells across)
    colors: a list of digits representing the colors to be used
    cell_h: pixel height of each lattice cell (gridlines add one more)
    cell_w: pixel width of each lattice cell (gridlines add one more)
  """
  if width is None:
    cell_h, cell_w = common.randint(1, 5), common.randint(1, 5)
    width = common.randint(3, 29 // (cell_w + 1))
    height = common.randint(3, 29 // (cell_h + 1))
    color_budget = common.randint(1, max(1, (width * height) // 2 - 1))
    counts = []
    remaining = color_budget + 1
    while remaining > 1 and color_budget > 0 and len(counts) < 8:
      step = int(0.5 * (8 * color_budget + 1) ** 0.5 - 1)
      remaining = min(max(1, step), remaining - 1)
      counts.append(remaining)
      color_budget -= remaining
    color_list = common.random_colors(len(counts) + 1)
    bitmap = common.grid(width, height, color_list[0])
    for idx, count in enumerate(counts):
      for _ in range(count):
        while True:
          r, c = common.randint(0, height - 1), common.randint(0, width - 1)
          if bitmap[r][c] != color_list[0]: continue
          bitmap[r][c] = color_list[idx + 1]
          break
    colors = []
    for row in bitmap:
      colors.extend(row)

  height = len(colors) // width
  grid = common.grid(width * (cell_w + 1) + 1, height * (cell_h + 1) + 1)
  for r in range(height):
    for c in range(width):
      for dh in range(cell_h):
        for dw in range(cell_w):
          grid[r * (cell_h + 1) + 1 + dh][c * (cell_w + 1) + 1 + dw] = (
              colors[r * width + c])
  counts_to_colors = {colors.count(x): x for x in colors}
  counts = sorted(counts_to_colors.keys(), reverse=True)
  output = common.deepcopy(grid)

  def drop_majority():
    for row in output:
      for c in range(len(row)):
        if row[c] == counts_to_colors[counts[0]]: row[c] = common.black()

  drop_majority()
  output = common.grid(1, len(set(colors)) - 1)

  def reveal_rank(rank):
    if rank < len(counts):
      output[rank - 1][0] = counts_to_colors[counts[rank]]

  reveal_rank(1)
  reveal_rank(2)
  reveal_rank(3)
  reveal_rank(4)
  reveal_rank(5)
  reveal_rank(6)
  reveal_rank(7)
  reveal_rank(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4,
               colors=[3, 1, 1, 1, 1, 1, 4, 4, 1, 4, 1, 1, 2, 1, 1, 1, 1, 2, 1,
                       1, 1, 1, 1, 1]),
      generate(width=5,
               colors=[6, 8, 8, 8, 8, 8, 8, 2, 6, 8, 1, 8, 1, 8, 8, 8, 1, 8, 8,
                       8, 8, 8, 6, 8, 6, 8, 8, 8, 8, 8]),
      generate(width=3,
               colors=[3, 3, 3, 1, 3, 3, 3, 8, 3, 3, 8, 3, 3, 2, 2, 2, 3, 3]),
      generate(width=4,
               colors=[1, 1, 8, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 8, 1, 1, 8, 1,
                       4, 1, 8, 1, 1]),
  ]
  test = [
      generate(width=4,
               colors=[2, 4, 2, 2, 1, 2, 4, 2, 8, 2, 2, 8, 2, 2, 1, 2, 4, 2, 2,
                       2, 2, 1, 2, 4, 2, 2, 4, 2]),
  ]
  return {"train": train, "test": test}
