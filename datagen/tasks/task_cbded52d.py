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


def generate(rows=None, cols=None, idxs=None, colors=None, block_rows=None,
             block_cols=None, cell_rows=2, cell_cols=2, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of cell positions (0, 1, 2, or 3)
    colors: a list of colors for the four cell positions
    block_rows: number of 2x2 blocks down the grid (square default = 3)
    block_cols: number of 2x2 blocks across the grid (square default = 3)
    cell_rows: number of rows in each cell
    cell_cols: number of columns in each cell
    num_colors: number of marker colors/positions to sample
  """
  if block_rows is None: block_rows = 3
  if block_cols is None: block_cols = 3
  last_r, mid_r = block_rows - 1, block_rows // 2
  last_c, mid_c = block_cols - 1, block_cols // 2
  if rows is None:
    block_rows = min(block_rows, 31 // (cell_rows + 1))
    block_cols = min(block_cols, 31 // (cell_cols + 1))
    last_r, mid_r = block_rows - 1, block_rows // 2
    last_c, mid_c = block_cols - 1, block_cols // 2
    num_positions = cell_rows * cell_cols
    if num_colors is None:
      num_colors = common.randint(1, min(8, max(1, block_rows * block_rows // 3)))
    num_colors = min(num_colors, num_positions)
    active_positions = common.sample(list(range(num_positions)), num_colors)
    active_colors = common.random_colors(num_colors, exclude=[common.blue()])
    colors = [common.blue()] * num_positions
    for idx, color in zip(active_positions, active_colors):
      colors[idx] = color
    rows, cols, idxs = [], [], []
    while not idxs:  # Retry until at least one cell is placed (no empty grids).
      rows, cols, idxs = [], [], []
      for idx in active_positions:
        if common.randint(0, 1):  # Sometimes we'll do a subset of the corners
          if common.randint(0, 1):
            rows.append(0)
            cols.append(0)
            idxs.append(idx)
          if common.randint(0, 1):
            rows.append(0)
            cols.append(last_c)
            idxs.append(idx)
          if common.randint(0, 1):
            rows.append(last_r)
            cols.append(0)
            idxs.append(idx)
          if common.randint(0, 1):
            rows.append(last_r)
            cols.append(last_c)
            idxs.append(idx)
          continue
        if common.randint(0, 1):  # Sometimes we'll do left-to-right
          rows.append(mid_r)
          cols.append(0)
          idxs.append(idx)
          rows.append(mid_r)
          cols.append(last_c)
          idxs.append(idx)
          continue
        if common.randint(0, 1):  # Sometimes we'll do up-to-down
          rows.append(0)
          cols.append(mid_c)
          idxs.append(idx)
          rows.append(last_r)
          cols.append(mid_c)
          idxs.append(idx)

  gh = block_rows * (cell_rows + 1) - 1
  gw = block_cols * (cell_cols + 1) - 1
  grid, output = common.grids(gw, gh, common.blue())
  # Mark the original cells, then infer new ones.
  origs = [1] * len(idxs)
  for j in range(len(idxs)):
    for i in range(j):
      if idxs[i] != idxs[j]: continue
      if rows[i] == rows[j]:
        step = 1 if cols[i] < cols[j] else -1
        for col in range(cols[i] + step, cols[j], step):
          rows.append(rows[i])
          cols.append(col)
          idxs.append(idxs[i])
          origs.append(0)
      if cols[i] == cols[j]:
        step = 1 if rows[i] < rows[j] else -1
        for row in range(rows[i] + step, rows[j], step):
          rows.append(row)
          cols.append(cols[i])
          idxs.append(idxs[i])
          origs.append(0)
  for r in range(gh):
    for c in range(gw):
      if (r % (cell_rows + 1) == cell_rows or
          c % (cell_cols + 1) == cell_cols):
        output[r][c] = grid[r][c] = common.black()
  active_idxs = sorted(set(idxs))
  for target_idx in active_idxs[:1]:
    for r, c, i, o in zip(rows, cols, idxs, origs):
      if i != target_idx: continue
      roff, coff = i // cell_cols, i % cell_cols
      if o: grid[(cell_rows + 1) * r + roff][(cell_cols + 1) * c + coff] = colors[i]
      output[(cell_rows + 1) * r + roff][(cell_cols + 1) * c + coff] = colors[i]
  for target_idx in active_idxs[1:]:
    for r, c, i, o in zip(rows, cols, idxs, origs):
      if i != target_idx: continue
      roff, coff = i // cell_cols, i % cell_cols
      if o: grid[(cell_rows + 1) * r + roff][(cell_cols + 1) * c + coff] = colors[i]
      output[(cell_rows + 1) * r + roff][(cell_cols + 1) * c + coff] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 2, 0], idxs=[1, 1, 2, 2, 1],
               colors=[1, 4, 2, 1]),
      generate(rows=[0, 0, 0, 2, 2], cols=[0, 1, 2, 1, 2], idxs=[3, 0, 3, 0, 3],
               colors=[7, 1, 1, 3]),
      generate(rows=[1, 1], cols=[0, 2], idxs=[2, 2], colors=[1, 1, 3, 1]),
  ]
  test = [
      generate(rows=[0, 0, 2, 2, 2], cols=[0, 2, 0, 2, 2], idxs=[3, 3, 0, 0, 3],
               colors=[6, 1, 1, 8]),
  ]
  return {"train": train, "test": test}
