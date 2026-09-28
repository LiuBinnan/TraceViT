# Copyright 2026 Google LLC
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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  def translated_pixel(row, col, color):
    r, c = row, col
    if color == common.blue(): r, c = r + 0, c + 1
    if color == common.red(): r, c = r + 0, c - 2
    if color == common.orange(): r, c = r - 2, c + 0
    if color == common.maroon(): r, c = r + 2, c + 0
    return r, c

  def draw():
    grid = common.grid(size, size, common.cyan())
    targets = []
    for row, col, color in zip(rows, cols, colors):
      grid[row][col] = color
      r, c = translated_pixel(row, col, color)
      if r < 0 or c < 0 or r >= size or c >= size: return None, None
      if (r, c) in targets: return None, None
      targets.append((r, c))
    return grid, targets

  if size is None:
    size = 2 * common.randint(5, 14)
    dots = size - common.randint(6, 9)
    while True:
      rows = [common.randint(0, size - 1) for _ in range(dots)]
      cols = [common.randint(0, size - 1) for _ in range(dots)]
      colors = common.choices([1, 2, 7, 9], dots)
      if len(set(zip(rows, cols))) != dots: continue
      grid, _ = draw()
      if grid: break

  grid, targets = draw()
  output = common.grid(size, size, common.cyan())

  def move_color(target_color):
    for index, color in enumerate(colors):
      if color != target_color:
        continue
      row, col = targets[index]
      output[row][col] = color

  move_color(common.blue())
  move_color(common.red())
  move_color(common.orange())
  move_color(common.maroon())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[4, 6], cols=[4, 8], colors=[7, 7]),
      generate(size=10, rows=[5, 9], cols=[7, 7], colors=[2, 2]),
      generate(size=10, rows=[4], cols=[2], colors=[9]),
      generate(size=10, rows=[5, 9], cols=[7, 7], colors=[1, 1]),
  ]
  test = [
      generate(size=16, rows=[1, 2, 3, 4, 7, 8, 10, 11, 12, 13],
               cols=[7, 2, 13, 8, 1, 8, 10, 2, 11, 5],
               colors=[9, 1, 2, 7, 9, 2, 1, 2, 9, 7]),
  ]
  return {"train": train, "test": test}
