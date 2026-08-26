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


def generate(rows=None, colors=None, size=3, gh=None, gw=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    colors: digits representing colors to be used
    size: the width and height of the (square) grid
    gh: grid height (row extent); defaults to size
    gw: grid width (column extent); defaults to size. Exactly one falling pixel
      is placed per column, so gw doubles as the (pre-merge) object count. Every
      column is extended by the band-reveal loop below, so gw is no longer tied
      to a fixed number of unrolled handlers.
  """
  if gh is None:
    gh = size
  if gw is None:
    gw = size
  # SECONDARY-COUNT GUARD: gw is the grid width and the per-column object count.
  # The extend_cols band-reveal below consumes ALL gw columns (no fixed unroll),
  # so the only cap needed is the ARC 30-cell edge to keep the canvas legal.
  gw = min(gw, 30)
  if rows is None:
    rows = [common.randint(0, gh - 1) for _ in range(gw)]
    # One independent non-background color per column (with replacement),
    # mirroring re_arc's per-pixel choice(remcols); lets gw exceed 10.
    colors = [common.random_color() for _ in range(gw)]

  grid, output = common.grids(gw, gh)
  for c, row in enumerate(rows):
    grid[row][c] = colors[c]

  def extend_cols(col_range):
    for c in col_range:
      row, color = rows[c], colors[c]
      for r in range(row, gh):
        output[r][c] = color

  # Reveal the falling columns in three left-to-right bands so the traced
  # checkpoints stay three progressive frames regardless of gw.
  extend_cols(range(0, gw // 3))
  extend_cols(range(gw // 3, 2 * gw // 3))
  extend_cols(range(2 * gw // 3, gw))
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 1, 0], colors=[3, 4, 6]),
      generate(rows=[1, 0, 1], colors=[7, 2, 8]),
      generate(rows=[0, 1, 2], colors=[4, 2, 0]),
  ]
  test = [
      generate(rows=[0, 2, 0], colors=[4, 7, 8]),
  ]
  return {"train": train, "test": test}
