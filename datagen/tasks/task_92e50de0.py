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


def generate(size=None, brow=None, bcol=None, values=None, bgcolor=None,
             fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    brow: The row of the shown sprite.
    bcol: The column of the shown
    values: The values of the sprite.
    bgcolor: The background color.
    fgcolor: The foreground color.
  """

  if size is None:
    size = 2 * common.randint(6, 14) + 1
    brow = common.randint(0, (size - 3) // 4)
    bcol = common.randint(0, (size - 3) // 4)
    pixels = common.diagonally_connected_sprite()
    values = []
    for row in range(3):
      for col in range(3):
        values.append(1 if (row, col) in pixels else 0)
    values = "".join(str(v) for v in values)
    colors = common.random_colors(2)
    bgcolor, fgcolor = colors[0], colors[1]

  grid, output = common.grids(size, size)

  # Background gridlines, shared by the input and the output canvas.
  for i in range(size):
    for j in range(3, size, 4):
      output[i][j] = output[j][i] = grid[i][j] = grid[j][i] = bgcolor

  # Input: the sprite is shown in the single cell (brow, bcol).
  for r in range(3):
    for c in range(3):
      grid[brow * 4 + r][bcol * 4 + c] = fgcolor * int(values[r * 3 + c])

  # Output: replicate the sprite into every cell whose row/column parity matches
  # the shown cell -- a checkerboard of same-colored cells, revealed band by
  # band down the grid. ncells = size // 4 + 1 <= 8, so at most four matching
  # cell-row bands share the shown cell's parity.
  ncells = size // 4 + 1

  def stamp_row(k):
    """Stamps the sprite across the k-th matching band of cell-rows."""
    row = brow % 2 + 2 * k
    if row >= ncells:
      return
    for col in range(ncells):
      if col % 2 != bcol % 2:
        continue
      for r in range(3):
        for c in range(3):
          color = fgcolor * int(values[r * 3 + c])
          common.draw(output, row * 4 + r, col * 4 + c, color)

  stamp_row(0)
  stamp_row(1)
  stamp_row(2)
  stamp_row(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=23, brow=2, bcol=1, values="010101010", bgcolor=2, fgcolor=4),
      generate(size=27, brow=1, bcol=1, values="110111010", bgcolor=1, fgcolor=3),
      generate(size=25, brow=0, bcol=5, values="110010011", bgcolor=8, fgcolor=2),
  ]
  test = [
      generate(size=29, brow=1, bcol=4, values="010110001", bgcolor=3, fgcolor=8),
  ]
  return {"train": train, "test": test}
