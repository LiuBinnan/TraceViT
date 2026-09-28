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


def generate(width=None, height=None, brows=None, bcols=None, rows=None,
             cols=None, groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    groups: The groups of the pixels.
  """

  if width is None:
    if common.randint(0, 1):
      width, height = 7, 7
      brows, bcols = [common.randint(1, 2)], [common.randint(1, 2)]
      rows, cols = common.conway_sprite(4, 4)
      groups = [0] * len(rows)
    else:
      width, height = 12, 8
      all_coords = [(0, 0), (0, 4), (0, 8), (4, 0), (4, 4), (4, 8)]
      coords = common.sample(all_coords, common.randint(2, 3))
      brows, bcols = zip(*coords)
      rows, cols, groups = [], [], []
      for group in range(len(coords)):
        prows, pcols = common.conway_sprite(4, 4)
        rows.extend(prows)
        cols.extend(pcols)
        groups.extend([group] * len(prows))

  # Input: sprite pixels scattered inside one or more 4x4 regions.
  grid = common.grid(width, height)
  for row, col, group in zip(rows, cols, groups):
    grid[brows[group] + row][bcols[group] + col] = 8

  # Output: enclose each cluster of pixels in a red 4x4 box, drawn *behind* the
  # pixels. For each cluster we first outline its bounding box, then shade the
  # interior, so the pixels always stay on top.
  output = common.deepcopy(grid)

  def frame_box(i):
    """Outlines cluster i's 4x4 bounding box with a red border."""
    if i >= len(brows):
      return
    brow, bcol = brows[i], bcols[i]
    for r in range(4):
      for c in range(4):
        if (r in (0, 3) or c in (0, 3)) and \
            output[brow + r][bcol + c] == common.black():
          output[brow + r][bcol + c] = common.red()

  def fill_box(i):
    """Shades the interior of cluster i's 4x4 bounding box with red."""
    if i >= len(brows):
      return
    brow, bcol = brows[i], bcols[i]
    for r in range(1, 3):
      for c in range(1, 3):
        if output[brow + r][bcol + c] == common.black():
          output[brow + r][bcol + c] = common.red()

  frame_box(0)
  fill_box(0)
  frame_box(1)
  fill_box(1)
  frame_box(2)
  fill_box(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=8, brows=[0, 0, 4], bcols=[0, 4, 8],
               rows=[0, 1, 1, 2, 2, 2, 3, 3, 0, 1, 1, 2, 2, 2, 3, 3, 3, 0, 1, 2, 2, 2, 2, 3],
               cols=[1, 1, 2, 1, 2, 3, 0, 1, 0, 0, 3, 0, 1, 2, 0, 1, 2, 1, 1, 0, 1, 2, 3, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
      generate(width=12, height=8, brows=[0, 4], bcols=[4, 8],
               rows=[0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3],
               cols=[1, 0, 1, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 0, 1, 2, 0, 1, 3, 0, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
      generate(width=7, height=7, brows=[1], bcols=[1],
               rows=[0, 0, 1, 1, 1, 1, 2, 3], cols=[0, 3, 0, 1, 2, 3, 2, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=12, height=8, brows=[0, 4, 4], bcols=[8, 0, 4],
               rows=[0, 0, 1, 2, 3, 3, 3, 3, 0, 0, 0, 1, 1, 2, 3, 0, 1, 1, 1, 2, 2, 3, 3],
               cols=[2, 3, 1, 0, 0, 1, 2, 3, 0, 1, 3, 1, 3, 2, 3, 0, 0, 2, 3, 0, 3, 0, 3],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
