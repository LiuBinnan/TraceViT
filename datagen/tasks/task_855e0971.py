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


def generate(width=None, colors=None, heights=None, strata=None, rows=None,
    cols=None, xpose=None, num_strata=None, max_markers=None, count=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    colors: a list of colors (one per strata)
    heights: a list of heights (one per strata)
    strata: a list of strata indices (one for each pixel)
    rows: a list of row indices (one for each pixel)
    cols: a list of column indices (one for each pixel)
    xpose: a boolean indicating whether to transpose the grid
  """
  if (width is None or colors is None or heights is None or strata is None or
      rows is None or cols is None or xpose is None):
    if width is None:
      width = common.randint(3, 30)
    if xpose is None:
      xpose = common.randint(0, 1)
    if num_strata is None:
      num_strata = common.choice([3, 4, 7, 8, 9])
    num_strata = min(9, max(2, num_strata))
    if max_markers is None:
      max_markers = max(1, width // 2)
    max_markers = max(1, min(width, max_markers, max(1, width // 2)))

    colors = common.random_colors(num_strata)
    total_height = common.randint(2 * num_strata, 30)
    heights = [2 for _ in range(num_strata)]
    while sum(heights) < total_height:
      heights[common.randint(0, num_strata - 1)] += 1

    strata, rows, cols = [], [], []
    lower_bounds = [common.randint(0, 1) for _ in range(num_strata)]
    if sum(lower_bounds) < min(2, num_strata):
      for idx in common.sample(range(num_strata), min(2, num_strata)):
        lower_bounds[idx] = 1
    for idx, (height, lower_bound) in enumerate(zip(heights, lower_bounds)):
      if count is None:
        num_pixels = common.randint(lower_bound, max_markers)
      else:
        num_pixels = max(lower_bound, min(max_markers, count))
      candidates = common.sample(
          [(row, col) for row in range(height) for col in range(width)],
          height * width)
      chosen, used_cols = [], set()
      for row, col in candidates:
        if col in used_cols:
          continue
        if any(abs(row - prev_row) + abs(col - prev_col) == 1
               for prev_row, prev_col in chosen):
          continue
        chosen.append((row, col))
        used_cols.add(col)
        if len(chosen) == num_pixels:
          break
      for row, col in chosen:
        strata.append(idx)
        rows.append(row)
        cols.append(col)

  grid, floor = [], 0
  for idx, (color, height) in enumerate(zip(colors, heights)):
    for _ in range(height):
      grid.append([color for _ in range(width)])
    for stratum, col, row in zip(strata, cols, rows):
      if stratum != idx: continue
      grid[floor + row][col] = common.black()
    floor += height
  output = [row[:] for row in grid]
  stratum_floors = []
  floor = 0
  for height in heights:
    stratum_floors.append(floor)
    floor += height
  if xpose:
    grid = common.transpose(grid)
    output = common.transpose(output)

  def extend_stratum(stratum_idx):
    if stratum_idx >= len(colors):
      return
    floor = stratum_floors[stratum_idx]
    for stratum, col in zip(strata, cols):
      if stratum != stratum_idx:
        continue
      for r in range(heights[stratum_idx]):
        if xpose:
          output[col][floor + r] = common.black()
        else:
          output[floor + r][col] = common.black()

  extend_stratum(0)
  extend_stratum(1)
  extend_stratum(2)
  extend_stratum(3)
  extend_stratum(4)
  extend_stratum(5)
  extend_stratum(6)
  extend_stratum(7)
  extend_stratum(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, colors=[5, 4, 8], heights=[2, 7, 6], strata=[1, 2, 1],
               rows=[3, 3, 1], cols=[4, 9, 13], xpose=0),
      generate(width=14, colors=[2, 1], heights=[5, 8], strata=[0, 1],
               rows=[2, 3], cols=[3, 11], xpose=1),
      generate(width=15, colors=[8, 2, 3], heights=[5, 5, 3],
               strata=[0, 0, 1, 2], rows=[2, 3, 2, 1], cols=[3, 11, 5, 7],
               xpose=0),
      generate(width=14, colors=[2, 5, 4], heights=[4, 5, 6], strata=[1, 2, 2],
               rows=[2, 1, 3], cols=[6, 12, 2], xpose=1),
  ]
  test = [
      generate(width=15, colors=[8, 1, 4, 2], heights=[4, 4, 5, 4],
               strata=[0, 0, 1, 2, 3], rows=[0, 2, 2, 2, 2],
               cols=[4, 12, 6, 10, 1], xpose=0),
  ]
  return {"train": train, "test": test}
