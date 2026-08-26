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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None,
             bidxs=None, size=10, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    bidxs: a list of indices into the sprite list
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    swidth, sheight = common.randint(3, 4), common.randint(2, 4)
    wides, talls, bidxs = [swidth, swidth, swidth - 1], [sheight] * 3, [0, 0, 1]
    while True:
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    rows, cols, idxs = [], [], []
    # Sometimes make a box.
    if common.randint(0, 1):
      for r in range(sheight):
        for c in range(swidth):
          if r not in [0, sheight - 1] and c not in [0, swidth - 1]: continue
          rows.append(r)
          cols.append(c)
          idxs.append(0)
    # Otherwise, make a creature (and use up each of the columns!)
    else:
      num_pixels = common.randint(swidth * sheight // 2, swidth * sheight)
      while True:
        pixels = common.continuous_creature(num_pixels, swidth, sheight)
        if max([p[1] for p in pixels]) + 1 == swidth: break
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([0] * len(pixels))
    # Pick some "bad" column to remove from the sprite to create a smaller one.
    xrows, xcols, xidxs, badcol = [], [], [], common.randint(0, swidth - 1)
    for r, c in zip(rows, cols):
      if c == badcol: continue
      xrows.append(r)
      xcols.append(c if c < badcol else c - 1)
      xidxs.append(1)
    rows.extend(xrows)
    cols.extend(xcols)
    idxs.extend(xidxs)

  grid = common.grid(width, height)
  for brow, bcol, bidx in zip(brows, bcols, bidxs):
    for row, col, idx in zip(rows, cols, idxs):
      if bidx != idx: continue
      grid[brow + row][bcol + col] = common.cyan()
  output = common.grid(width, height)

  def reveal_kind(target_idx):
    for brow, bcol, bidx in zip(brows, bcols, bidxs):
      if bidx != target_idx:
        continue
      for row, col, idx in zip(rows, cols, idxs):
        if idx != target_idx:
          continue
        output[brow + row][bcol + col] = (
            common.red() if target_idx else common.blue())

  reveal_kind(0)
  reveal_kind(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 3, 0, 3, 0, 1, 2, 3, 0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
               brows=[1, 2, 7],
               bcols=[7, 1, 5],
               bidxs=[1, 0, 0]),
      generate(rows=[0, 0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 3, 2, 3, 2, 3, 4, 0, 1, 2, 3, 2, 3, 2, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
               brows=[1, 2, 6], bcols=[6, 1, 3], bidxs=[1, 0, 0]),
      generate(rows=[0, 0, 0, 1, 1, 0, 0, 1, 1],
               cols=[0, 1, 2, 0, 2, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1],
               brows=[1, 5, 6], bcols=[1, 0, 3], bidxs=[0, 1, 0]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 2, 3, 3, 3, 3, 0, 0, 1, 2, 3, 3, 3],
               cols=[0, 1, 2, 2, 1, 0, 1, 2, 3, 0, 1, 1, 0, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               brows=[1, 1, 6], bcols=[1, 6, 3], bidxs=[1, 0, 0]),
  ]
  return {"train": train, "test": test}
