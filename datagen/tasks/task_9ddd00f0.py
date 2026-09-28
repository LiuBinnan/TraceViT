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


def generate(length=None, color=None, shown=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the boxes.
    color: The color of the boxes.
    shown: Whether each box is shown.
  """

  if length is None:
    length, color = common.randint(2, 5), common.random_color()
    while True:
      shown = [common.randint(0, 1) for _ in range(length * length)]
      if abs(sum(shown) - length * length // 2) <= 1: break

  # Lay out the input: a length x length arrangement of length x length boxes
  # (separated by one-cell gaps), but draw only the boxes flagged in `shown`.
  # Each box omits the inner cell at its own (row, col) coordinate.
  size = length * (length + 1) - 1
  grid = common.grid(size, size)
  for row in range(length):
    for col in range(length):
      for r in range(length):
        for c in range(length):
          if row == r and col == c: continue
          if shown[row * length + col]:
            grid[row * (length + 1) + r][col * (length + 1) + c] = color

  # Solve by filling in every missing box. A box that belongs at (row, col)
  # always carries its hole at inner cell (row, col), so each gap reveals the
  # coordinate of the box that completes it. Reveal one missing box per frame.
  output = common.deepcopy(grid)
  missing = [(row, col) for row in range(length) for col in range(length)
             if not shown[row * length + col]]

  def reveal_box(k):
    """Draws the k-th missing box, hole at its own (row, col) coordinate."""
    if k >= len(missing): return
    row, col = missing[k]
    for r in range(length):
      for c in range(length):
        if row == r and col == c: continue
        output[row * (length + 1) + r][col * (length + 1) + c] = color

  reveal_box(0)
  reveal_box(1)
  reveal_box(2)
  reveal_box(3)
  reveal_box(4)
  reveal_box(5)
  reveal_box(6)
  reveal_box(7)
  reveal_box(8)
  for k in range(9, length * length):
    reveal_box(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, color=8, shown=[0, 0, 1, 1]),
      generate(length=3, color=2, shown=[0, 1, 1, 0, 1, 0, 0, 1, 1]),
  ]
  test = [
      generate(length=4, color=1,
               shown=[0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0]),
  ]
  return {"train": train, "test": test}
