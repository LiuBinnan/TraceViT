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


def generate(colors=None, shuffled=None, size=10, height=None, width=None,
             lines=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    shuffled: a list of those same colors in a shuffled order
    size: the width and height of the (square) grid
    height: number of rows (defaults to size)
    width: number of columns (defaults to size)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    max_lines = max(1, min(9, height // 2))
    if lines is None:
      lines = common.randint(1, max_lines)
    lines = max(1, min(lines, max_lines))
    colors = common.random_colors(lines)
    shuffled = common.sample(colors, lines)
    # Reshuffle until at least one endpoint pair matches, so the transformation
    # connects at least one row (a pure derangement leaves output == input and
    # yields no forward steps). Bounded; never reached by validate()'s explicit
    # colors/shuffled, so the original examples stay byte-identical.
    for _ in range(20):
      if any(colors[i] == shuffled[i] for i in range(lines)):
        break
      shuffled = common.sample(colors, lines)

  grid = common.grid(width, height)
  for idx in range(len(colors)):
    r = 2 * idx + 1
    grid[r][0] = colors[idx]
    grid[r][width - 1] = shuffled[idx]
  output = [row[:] for row in grid]

  def fill_matching_row(idx):
    if idx >= len(colors):
      return
    r = 2 * idx + 1
    if colors[idx] != shuffled[idx]:
      return
    for c in range(0, width):
      output[r][c] = colors[idx]

  for idx in range(len(colors)):
    fill_matching_row(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 8, 4, 6], shuffled=[6, 9, 4, 8]),
      generate(colors=[8, 4, 3, 1, 2], shuffled=[8, 2, 4, 1, 3]),
      generate(colors=[2, 3, 5, 8], shuffled=[8, 4, 3, 2]),
  ]
  test = [
      generate(colors=[4, 3, 2, 6, 9], shuffled=[2, 3, 9, 6, 4]),
  ]
  return {"train": train, "test": test}
