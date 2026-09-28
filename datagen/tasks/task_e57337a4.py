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


def generate(rows=None, cols=None, color=None, bsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the black pixels.
    cols: The columns of the black pixels.
    color: The color of the grid.
    bsize: The side length of each block in the 3x3 block grid.
  """

  if rows is None:
    if bsize is None:
      bsize = common.randint(3, 9)
    while True:
      rows, cols = [], []
      for r in range(3):
        for c in range(3):
          if common.randint(0, 3): continue
          rows.append(bsize * r + common.randint(0, bsize - 1))
          cols.append(bsize * c + common.randint(0, bsize - 1))
      if len(rows) in [1, 2, 3]: break
    color = common.random_color()
  else:
    if bsize is None:
      bsize = 5

  grid = common.grid(3 * bsize, 3 * bsize, color)
  for row, col in zip(rows, cols):
    grid[row][col] = common.black()
  output = common.deepcopy(grid)

  def mark_blocks():
    """Blackens each block that holds a black pixel: the blocks that count."""
    for row, col in zip(rows, cols):
      common.rect(
          output,
          bsize,
          bsize,
          bsize * (row // bsize),
          bsize * (col // bsize),
          common.black(),
      )

  def reveal_cell(idx):
    """Shrinks the idx-th marked block down to its cell of the 3x3 answer."""
    nonlocal output
    if idx == 0:  # The marked blocks collapse onto a 3x3 answer canvas.
      output = common.grid(3, 3, color)
    if idx >= len(rows): return
    output[rows[idx] // bsize][cols[idx] // bsize] = common.black()

  mark_blocks()
  reveal_cell(0)
  reveal_cell(1)
  reveal_cell(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 7], cols=[1, 7], color=8),
      generate(rows=[2], cols=[12], color=9),
      generate(rows=[2, 2, 9], cols=[3, 11, 2], color=7),
  ]
  test = [
      generate(rows=[1, 12], cols=[5, 13], color=6),
  ]
  return {"train": train, "test": test}
