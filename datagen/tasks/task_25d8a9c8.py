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


def _is_coherent(row):
  """A row is coherent iff every cell shares a single color."""
  return len(set(row)) == 1


def drop_incoherent_rows(grid):
  """Step 1: wipe each incoherent (non-uniform) row to the background color.

  Coherent rows keep their original colors; incoherent rows become all-black.
  """
  result = [row[:] for row in grid]
  for r, row in enumerate(grid):
    if not _is_coherent(row):
      result[r] = [common.black()] * len(row)
  return result


def recolor_survivors_gray(grid, survivors):
  """Step 2: turn the surviving (coherent) rows gray, leaving the rest as-is."""
  result = [row[:] for row in grid]
  for r in survivors:
    result[r] = [common.gray()] * len(grid[r])
  return result


def generate(colors=None, size=3, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    # Take 3 or 4 random colors
    color_list = common.random_colors(common.randint(3, 4),
                                      exclude=[common.gray()])
    # Create the solid rows first
    rows = []
    for i in range(common.randint(1, 2)):
      rows.append([color_list[i]] * width)
    # Create the other rows, where each has two different (shuffled) colors
    while len(rows) < height:
      idxs = common.sample(color_list, 2)
      rows.append(common.shuffle([idxs[0]] * (width - 1) + [idxs[1]]))
    # Shuffle the rows and combine them into a single flat list
    rows = common.shuffle(rows)
    colors = []
    for row in rows:
      colors.extend(row)

  grid = common.grid(width, height)
  for r in range(height):
    row = colors[r * width:(r + 1) * width]
    grid[r] = row

  # The coherent (single-color) rows are the ones that survive.
  survivors = [r for r in range(height) if _is_coherent(grid[r])]

  # Step 1: drop every incoherent row, leaving the coherent rows in their
  # original colors.
  output = drop_incoherent_rows(grid)
  # Step 2: turn the surviving coherent rows gray to produce the final answer.
  output = recolor_survivors_gray(output, survivors)

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 4, 2, 3, 2, 2, 3, 3]),
      generate(colors=[7, 3, 3, 6, 6, 6, 3, 7, 7]),
      generate(colors=[2, 9, 2, 4, 4, 4, 9, 9, 9]),
      generate(colors=[2, 2, 4, 2, 2, 4, 1, 1, 1]),
  ]
  test = [
      generate(colors=[4, 4, 4, 3, 2, 3, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
