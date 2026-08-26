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


def generate(idxs=None, size=3, colors=(1, 6, 8),
             height=None, width=None, num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  The rule is fixed: the output is the input placed beside its left-right
  mirror (hconcat(input, vmirror(input))). Only the *input* is varied.

  Args:
    idxs: a list of indices into the colors list (validation path). When given,
      the input is a size-by-size grid whose cells are colors[idxs[...]].
    size: the width and height of the (square) grid used by the idxs path
    colors: the colors to use for the idxs path
    height: input row count (defaults to size; randomized 1..30 when idxs is
      None and this is None)
    width: input column count (defaults to size; randomized 1..15 when idxs is
      None and this is None, so the mirrored output stays within 30 columns)
    num_colors: number of distinct non-background colors to scatter (randomized
      0..min(9, height*width) when idxs is None and this is None)
    density: fraction of cells to fill (randomized when idxs is None and this
      is None)
  """
  if idxs is not None:
    # Validation path: every cell coloured per-cell via idxs (unchanged rule).
    if height is None:
      height = size
    if width is None:
      width = size
    grid = common.grid(width, height, 0)
    for r in range(height):
      for c in range(width):
        grid[r][c] = colors[idxs[r * width + c]]
  else:
    # Widened random path (rule-preserving): sample the input's shape, palette
    # size and fill density independently, mirroring re_arc's structural bands.
    if height is None:
      height = common.randint(1, 30)
    if width is None:
      width = common.randint(1, 15)
    cells = width * height
    if num_colors is None:
      num_colors = common.randint(0, min(9, cells))
    num_colors = max(0, min(num_colors, 9, cells))
    if density is None:
      fill_n = common.randint(0, cells)
    else:
      fill_n = int(round(density * cells))
    fill_n = max(0, min(fill_n, cells))
    if num_colors == 0:
      fill_n = 0
    elif fill_n < num_colors:
      fill_n = num_colors  # keep every chosen colour present at least once
    grid = common.grid(width, height, 0)
    palette = common.random_colors(num_colors, exclude=[0]) if num_colors else []
    inds = [(r, c) for r in range(height) for c in range(width)]
    chosen = common.sample(inds, fill_n) if fill_n else []
    for i, (r, c) in enumerate(chosen):
      grid[r][c] = palette[i % num_colors]

  output = common.grid(2 * width, height, 0)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c]
      output[r][2 * width - 1 - c] = grid[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idxs=[1, 1, 1, 0, 1, 0, 2, 2, 1]),
      generate(idxs=[1, 2, 0, 1, 0, 0, 0, 0, 1]),
      generate(idxs=[0, 0, 0, 2, 0, 1, 1, 2, 2]),
      generate(idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1]),
  ]
  test = [
      generate(idxs=[1, 2, 1, 2, 1, 2, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
