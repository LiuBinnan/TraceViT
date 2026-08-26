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


def generate(rows=None, cols=None, minirows=None, minicols=None, colors=None,
             minisize=3, rainbow=(2, 3, 4, 6, 8), gh=None, gw=None,
             ncolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    colors: a digit representing a color to be used
    minisize: the width and height of each mini-rid
    rainbow: a list of digits representing the set of "rainbow" colors
    gh: number of block-rows (== cell-rows per block); defaults to minisize
    gw: number of block-cols (== cell-cols per block); defaults to minisize
    ncolors: number of non-background/non-gridline colors to use
  """
  # The rule maps an intra-block pixel position (mr, mc) to the block at
  # position (mr, mc), so the block-grid extent on each axis must equal the
  # per-block cell extent on that axis. Rectangular shapes therefore use gh
  # block-rows of gh cells each, and gw block-cols of gw cells each.
  if gh is None: gh = minisize
  if gw is None: gw = minisize
  if rows is None:
    rows, cols, minirows, minicols, colors = [], [], [], [], []
    chosen_row, chosen_col = common.randint(0, gh - 1), common.randint(0, gw - 1)
    cells = gh * gw
    max_rearc_count = min(7, max(2, cells - 2))
    if ncolors is None: ncolors = common.randint(2, max_rearc_count)
    # Cap the re-arc-style color/pixel count by capacity; the selected block
    # stays a strict minimum. Default explicit validate() examples bypass this.
    other_count = min(max(2, ncolors), max_rearc_count)
    sel_count = other_count - 1
    rainbow = common.random_colors(other_count, exclude=[common.gray()])
    for r in range(gh):
      for c in range(gw):
        count = sel_count if r == chosen_row and c == chosen_col else other_count
        pixels = common.sample(common.all_pixels(gw, gh), count)
        rows.extend([r] * count)
        cols.extend([c] * count)
        minirows.extend([p[0] for p in pixels])
        minicols.extend([p[1] for p in pixels])
        colors.extend(rainbow[0:count])

  grid = common.hollywood_squares(minisize, common.black(), common.gray(),
                                  block_rows=gh, block_cols=gw,
                                  row_content=gh, col_content=gw)
  counts = {}
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    grid[r * (gh + 1) + mr][c * (gw + 1) + mc] = color
    counts[(r, c)] = 1 if (r, c) not in counts else counts[(r, c)] + 1
  min_pixels = min(counts.values())
  selected = {cell for cell, count in counts.items() if count == min_pixels}
  selected_pixels = [(r, c, mr, mc, color)
                     for r, c, mr, mc, color in zip(
                         rows, cols, minirows, minicols, colors)
                     if (r, c) in selected]
  output = common.hollywood_squares(minisize, common.black(), common.gray(),
                                    block_rows=gh, block_cols=gw,
                                    row_content=gh, col_content=gw)

  def keep_minimum_blocks():
    """Keeps only the source blocks with the fewest colored pixels."""
    for r, c, mr, mc, color in selected_pixels:
      output[r * (gh + 1) + mr][c * (gw + 1) + mc] = color

  keep_minimum_blocks()
  output = common.hollywood_squares(minisize, common.black(), common.gray(),
                                    block_rows=gh, block_cols=gw,
                                    row_content=gh, col_content=gw)

  def project_selected_pixel(idx):
    """Turns one selected pixel into its output block."""
    if idx >= len(selected_pixels): return
    _, _, mr, mc, color = selected_pixels[idx]
    for dr in range(gh):
      for dc in range(gw):
        output[mr * (gh + 1) + dr][mc * (gw + 1) + dc] = color

  project_selected_pixel(0)
  project_selected_pixel(1)
  project_selected_pixel(2)
  project_selected_pixel(3)
  project_selected_pixel(4)
  project_selected_pixel(5)

  def project_remaining_pixels():
    """Handles explicit parameter sets with more selected pixels."""
    for idx in range(6, len(selected_pixels)):
      _, _, mr, mc, color = selected_pixels[idx]
      for dr in range(gh):
        for dc in range(gw):
          output[mr * (gh + 1) + dr][mc * (gw + 1) + dc] = color

  project_remaining_pixels()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 1, 1, 2, 0, 0, 1, 1, 2, 2, 0, 1, 2, 2, 0, 0, 1, 1, 2, 2,
                     0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 2, 0, 0, 1,
                     1, 2, 2, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0,
                         0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1,
                         1, 2, 2, 2, 2, 2, 2, 2],
               minicols=[0, 1, 2, 2, 1, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1, 0, 1,
                         1, 2, 2, 2, 0, 0, 1, 0, 1, 1, 2, 1, 2, 1, 1, 0, 0, 2,
                         2, 0, 2, 0, 1, 0, 1, 2],
               colors=[2, 6, 2, 4, 4, 3, 4, 8, 3, 6, 6, 3, 8, 2, 3, 8, 6, 2, 4,
                       8, 4, 4, 6, 6, 2, 3, 8, 3, 2, 3, 6, 2, 6, 2, 4, 8, 8, 8,
                       4, 6, 3, 2, 3, 4]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 1, 1, 2, 0, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2, 2,
                     0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0,
                     1, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[0, 2, 0, 1, 1, 2, 2, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 2,
                         1, 2, 2, 1, 0, 0, 2, 0, 2, 0, 2, 0, 1, 1, 2, 0, 1, 2,
                         0, 0, 2, 0, 1, 2, 0, 1],
               colors=[2, 3, 4, 6, 6, 8, 2, 4, 3, 4, 6, 3, 8, 2, 8, 4, 8, 2, 6,
                       4, 2, 3, 3, 3, 6, 4, 6, 8, 2, 3, 6, 8, 4, 2, 8, 4, 2, 8,
                       3, 2, 3, 6, 6, 4]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0, 1, 1, 2, 2,
                     0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 2, 2, 0,
                     0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[1, 1, 2, 1, 2, 0, 2, 0, 1, 2, 1, 2, 1, 0, 2, 1, 0, 2,
                         0, 1, 0, 2, 0, 2, 2, 0, 1, 1, 0, 1, 0, 1, 1, 2, 2, 1,
                         2, 0, 1, 0, 1, 0, 0, 2],
               colors=[3, 6, 3, 6, 2, 6, 4, 2, 8, 8, 2, 8, 4, 3, 4, 2, 4, 3, 3,
                       4, 4, 8, 2, 6, 2, 3, 6, 8, 8, 6, 6, 3, 3, 3, 2, 6, 4, 2,
                       8, 8, 4, 2, 4, 6]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 0, 0, 1, 2, 0, 0, 1, 1, 2,
                     0, 0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0,
                     0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[0, 1, 2, 0, 1, 0, 2, 0, 2, 0, 2, 0, 1, 1, 0, 1, 2, 0,
                         2, 1, 1, 2, 2, 1, 2, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 2,
                         1, 2, 2, 0, 1, 2, 0, 2],
               colors=[3, 8, 4, 4, 6, 2, 8, 8, 3, 6, 3, 6, 2, 2, 4, 4, 2, 8, 3,
                       4, 8, 6, 4, 2, 6, 3, 2, 6, 3, 6, 6, 2, 3, 6, 3, 8, 8, 3,
                       4, 4, 2, 4, 2, 8]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 1, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 2, 2, 0, 1, 2, 2, 2,
                     0, 0, 0, 1, 1, 1, 2, 0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2,
                     2, 1, 1, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0,
                         1, 1, 1, 1, 1, 2, 2, 2],
               minicols=[0, 1, 1, 1, 2, 0, 1, 2, 0, 2, 0, 2, 0, 0, 1, 0, 1, 0,
                         1, 2, 0, 1, 2, 0, 1, 2, 2, 1, 2, 0, 1, 2, 1, 2, 1, 2,
                         1, 2, 2, 0, 2, 0, 2, 0],
               colors=[6, 4, 3, 4, 3, 2, 8, 6, 8, 2, 2, 8, 4, 6, 3, 2, 3, 3, 6,
                       2, 3, 4, 6, 8, 4, 2, 4, 8, 6, 8, 2, 4, 6, 4, 2, 8, 6, 3,
                       3, 4, 6, 2, 8, 3]),
  ]
  return {"train": train, "test": test}
