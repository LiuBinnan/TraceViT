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


def generate(rows=None, cols=None, width=3, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    width: the width of one grid half
    height: the height of the grid
  """
  if rows is None:
    while True:
      pixels = common.random_pixels(2 * width + 1, height)
      if not [p for p in pixels if p[1] < width]: continue
      if not [p for p in pixels if p[1] > width]: continue
      break
    rows, cols = zip(*pixels)

  grid, output = common.grid(2 * width + 1, height), common.grid(width, height)
  for r, c in zip(rows, cols):
    grid[r][c] = common.blue()
  for r in range(height):
    grid[r][width] = common.gray()

  def mark_left_candidates():
    """Copies the left-half blue cells into the comparison canvas."""
    for r, c in zip(rows, cols):
      if c < width:
        output[r][c] = common.blue()

  def merge_right_candidates():
    """Marks cells red where the right half overlaps a left candidate."""
    for r, c in zip(rows, cols):
      if c <= width:
        continue
      c -= width + 1
      output[r][c] = (common.red() if output[r][c] != common.black()
                      else common.blue())

  def keep_overlaps():
    """Keeps only the cells that appeared in both halves."""
    for r in range(height):
      for c in range(width):
        output[r][c] = (common.red() if output[r][c] == common.red()
                        else common.black())

  mark_left_candidates()
  merge_right_candidates()
  keep_overlaps()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2, 0, 1, 1, 1], cols=[0, 1, 0, 5, 4, 5, 6]),
      generate(rows=[0, 0, 1, 2, 2, 0, 1, 1, 1, 2],
               cols=[0, 1, 2, 0, 1, 5, 4, 5, 6, 5]),
      generate(rows=[0, 1, 1, 2, 2, 1, 1, 2, 2],
               cols=[2, 0, 1, 1, 2, 4, 6, 4, 6]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2, 2, 0, 0, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 4, 6, 4, 6, 5]),
  ]
  return {"train": train, "test": test}
