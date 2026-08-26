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


def _max_patch_count(height, width):
  """Maximum number of non-overlapping 3x3 patches on the placement lattice."""
  return len(range(1, height - 1, 3)) * len(range(1, width - 1, 3))


def _place_patches(count, height, width):
  """Return (rows, cols) for `count` non-overlapping 3x3 patches."""
  count = min(count, _max_patch_count(height, width))
  row_offsets = common.sample(list(range(1, min(4, height - 1))), min(3, height - 2))
  col_offsets = common.sample(list(range(1, min(4, width - 1))), min(3, width - 2))
  best_positions = []
  for row_offset in row_offsets:
    for col_offset in col_offsets:
      positions = [
          (r, c)
          for r in range(row_offset, height - 1, 3)
          for c in range(col_offset, width - 1, 3)
      ]
      if len(positions) >= count:
        chosen = common.sample(positions, count)
        return [r for r, _ in chosen], [c for _, c in chosen]
      if len(positions) > len(best_positions):
        best_positions = positions
  chosen = common.sample(best_positions, len(best_positions))
  return [r for r, _ in chosen], [c for _, c in chosen]


def generate(size=None, rows=None, cols=None, colors=None, height=None,
             width=None, count=None, background_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    count: how many isolated cells to scatter; defaults to the re_arc-style
      area-scaled band 1..max(1, height * width // 10). Each cell becomes one
      revealed 3x3 patch.
    background_color: the neutral grid color; randomized from the same legal
      re_arc background set when omitted during random generation.
  """
  if height is None: height = size
  if width is None: width = size
  if size is None:
    if height is None: height = common.randint(6, 16)
    if width is None: width = common.randint(6, 16)
    if background_color is None:
      background_color = common.choice([0, 5, 7, 9])
    if count is None:
      count = common.randint(1, max(1, (height * width) // 10))
    # Cap requested counts to what the grid can hold so explicit override
    # values at the high end remain feasible on small grids.
    count = min(count, _max_patch_count(height, width))
    rows, cols = _place_patches(count, height, width)
    # Colors come from {2, 3, 8} (the colormap keys). Keep the original
    # distinct-color behavior for the first 3 cells; allow repeats only when
    # more cells are requested than there are colors.
    colors = common.sample([2, 3, 8], min(count, 3))
    if count > 3:
      colors += common.choices([2, 3, 8], k=count - 3)
  if background_color is None:
    background_color = 0

  grid = common.grid(width, height, background_color)
  colormap = {3: 6, 8: 4, 2: 1}
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  output = [row[:] for row in grid]
  centers = list(zip(rows, cols, colors))

  def reveal_group(group_idx, num_groups=3):
    # Reveal the 3x3 patch for every cell assigned to this group (cells are
    # dealt round-robin across the groups). With three top-level calls -- groups
    # 0, 1, 2 -- this paints every patch; for the original 1..3 cells it reduces
    # to revealing one cell per call, exactly as before. The last call always
    # finishes the full output.
    for patch_idx in range(group_idx, len(centers), num_groups):
      r, c, color = centers[patch_idx]
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          output[r + dr][c + dc] = colormap[color]
      output[r][c] = color

  reveal_group(0)
  reveal_group(1)
  reveal_group(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, rows=[4, 5, 6], cols=[5, 1, 8], colors=[8, 3, 2]),
      generate(size=6, rows=[1], cols=[3], colors=[3]),
      generate(size=16, rows=[3, 10], cols=[12, 3], colors=[3, 2]),
      generate(size=6, rows=[2], cols=[2], colors=[8]),
  ]
  test = [
      generate(size=16, rows=[1, 10, 14], cols=[1, 13, 2], colors=[3, 2, 8]),
  ]
  return {"train": train, "test": test}
