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


def generate(wide=None, tall=None, patches=None, lengths=None, depths=None,
             rowoffset=None, coloffset=None, size=21, width=None, height=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: the width of the patch grid
    tall: the height of the patch grid
    patches: the colors in the patch grid
    lengths: the lengths of the patches
    depths: the depths of the patches
    rowoffset: the row offset for the quilt
    coloffset: the column offset for the quilt
    size: the width and height of the input grid
    width: the width of the input grid
    height: the height of the input grid
    num_colors: the number of colors used to sample the patch grid
  """
  sampling = any(v is None for v in [
      wide, tall, patches, lengths, depths, rowoffset, coloffset])
  if wide is None:
    wide = common.randint(2, 10)
  if tall is None:
    tall = common.randint(2, 10)
  if num_colors is None:
    num_colors = common.randint(2, 9)
  if width is None:
    width = common.randint(wide, 30) if sampling else size
  else:
    width = max(wide, min(width, 30))
  if height is None:
    height = common.randint(tall, 30) if sampling else size
  else:
    height = max(tall, min(height, 30))

  if patches is None:
    while (num_colors ** wide < 2 * tall or
           num_colors ** tall < 2 * wide) and num_colors < 9:
      num_colors += 1
    colors = common.random_colors(num_colors)
    while True:
      patches = [common.choice(colors) for _ in range(wide * tall)]
      rows, cols = set(), set()
      for r in range(tall):
        rows.add(tuple(patches[r * wide:(r + 1) * wide]))
      for c in range(wide):
        cols.add(tuple(patches[r * wide + c] for r in range(tall)))
      if len(rows) == tall and len(cols) == wide: break
  if lengths is None:
    lengths = [1 for _ in range(wide)]
    for _ in range(common.randint(0, width - wide)):
      lengths[common.randint(0, wide - 1)] += 1
  if depths is None:
    depths = [1 for _ in range(tall)]
    for _ in range(common.randint(0, height - tall)):
      depths[common.randint(0, tall - 1)] += 1
  if rowoffset is None:
    rowoffset = common.randint(0, height - sum(depths))
  if coloffset is None:
    coloffset = common.randint(0, width - sum(lengths))

  grid, _ = common.grids(width, height)
  output = common.grid(wide, tall)
  for row in range(tall):
    for col in range(wide):
      output[row][col] = patches[row * wide + col]
      for dr in range(depths[row]):
        for dc in range(lengths[col]):
          r = rowoffset + sum(depths[:row]) + dr
          c = coloffset + sum(lengths[:col]) + dc
          grid[r][c] = output[row][col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=3, tall=3, patches=[8, 7, 7, 3, 4, 1, 2, 5, 5],
               lengths=[8, 6, 6], depths=[6, 4, 5], rowoffset=1, coloffset=1),
      generate(wide=2, tall=2, patches=[2, 8, 1, 4], lengths=[7, 8],
               depths=[8, 7], rowoffset=1, coloffset=1),
      generate(wide=2, tall=3, patches=[8, 2, 3, 3, 4, 1], lengths=[6, 6],
               depths=[5, 6, 6], rowoffset=2, coloffset=2),
  ]
  test = [
      generate(wide=3, tall=3, patches=[2, 4, 1, 8, 3, 8, 2, 4, 2],
               lengths=[5, 8, 5], depths=[6, 8, 4], rowoffset=1, coloffset=1),
  ]
  return {"train": train, "test": test}
