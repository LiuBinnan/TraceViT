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


def generate(size=None, idxs=None, colors=(6, 2, 1, 7), height=None, width=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    idxs: a list of indices into the colors list
    colors: a list of colors to be used for the pixels
    height: the number of rows (defaults to size, for a square grid)
    width: the number of columns (defaults to size, for a square grid)
    num_colors: how many distinct foreground colors to scatter onto the random
      background (defaults to a re_arc-style area-scaled random draw); only used
      on the random-input path (when idxs is not supplied).
  """
  if size is None:
    if height is None:
      height = common.randint(3, 23)
    if width is None:
      width = common.randint(3, 23)
    # Build the random input the way re_arc's generator does: paint a single
    # background color, then scatter a variable number of foreground colors,
    # each over an area-scaled random number of cells. This widens the
    # color-count / density / object-count variety of the inputs without
    # touching the transformation rule (the output still mirrors each row).
    cell_count = height * width
    domain = list(common.internal_colors)
    bgc = common.choice(domain)
    remcols = [c for c in domain if c != bgc]
    if num_colors is None:
      num_colors = common.randint(0, min(len(remcols), cell_count))
    num_colors = min(num_colors, len(remcols), cell_count)
    fgcols = common.sample(remcols, num_colors)
    colors = [bgc] + fgcols
    idxs = [0] * cell_count
    free = list(range(cell_count))
    for fg_index in range(len(fgcols)):
      if not free:
        break
      cap = max(1, len(free) // max(1, num_colors))
      num = min(len(free), common.randint(1, cap))
      chosen_set = set(common.sample(free, num))
      for cell in chosen_set:
        idxs[cell] = fg_index + 1
      free = [c for c in free if c not in chosen_set]
  else:
    if height is None:
      height = size
    if width is None:
      width = size

  grid = []
  for r in range(height):
    grid.append([colors[idxs[r * width + c]] for c in range(width)])
  output = [row[::-1] for row in grid]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, idxs=[0, 0, 0, 1,
                             0, 2, 0, 1,
                             3, 1, 3, 1,
                             2, 3, 1, 1]),
      generate(size=7, idxs=[3, 3, 3, 0, 0, 0, 1,
                             0, 3, 2, 2, 3, 3, 2,
                             3, 3, 1, 2, 1, 0, 0,
                             1, 1, 3, 3, 3, 1, 1,
                             3, 1, 3, 2, 1, 3, 1,
                             0, 0, 0, 1, 1, 2, 2,
                             0, 1, 0, 0, 0, 0, 0]),
      generate(size=6, idxs=[2, 1, 3, 2, 2, 2,
                             1, 2, 3, 3, 1, 0,
                             1, 2, 1, 0, 1, 2,
                             2, 1, 2, 3, 0, 1,
                             1, 3, 2, 1, 3, 2,
                             1, 2, 0, 1, 3, 3]),
  ]
  test = [
      generate(size=3, idxs=[3, 0, 2,
                             0, 3, 0,
                             0, 1, 1]),
  ]
  return {"train": train, "test": test}
