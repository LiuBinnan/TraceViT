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


def generate(colors=None, row=None, col=None, last=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    row: The row of the pixel.
    col: The column of the pixel.
    last: The color of the last pixel (for the ambiguous case)
    gsize: The width and height of the square canvas.
  """

  if colors is None:
    if gsize is None: gsize = common.randint(12, 28)
    num_colors = common.randint(3, min(7, (gsize - 2) // 2))
    colors = [common.randint(0, 9) for _ in range(num_colors)]
    if colors[0] == 0: colors[0] = common.random_color()
    if colors[-1] == 0: colors[-1] = common.random_color()
    row = common.randint(2 + num_colors, gsize - num_colors)
    col = common.randint(num_colors - 1, gsize - num_colors)

  grid, output = common.grids(gsize or 16, gsize or 16)
  for i, color in enumerate(colors):
    output[0][i] = grid[0][i] = color
  for c in range(gsize or 16):
    output[1][c] = grid[1][c] = 5
  if last: output[0][len(colors) - 1] = last
  output[row][col] = grid[row][col] = colors[0]

  # Output: concentric square rings grow outward from the seed pixel, each ring
  # taking the next legend color read left-to-right (the seed itself is
  # colors[0]). num_colors = len(colors) <= 7, so at most six rings wrap it.
  def draw_ring(i):
    """Wraps a ring of legend color colors[i] around the seed."""
    if i >= len(colors): return
    common.hollow_rect(output, 2 * i + 1, 2 * i + 1, row - i, col - i, colors[i])

  draw_ring(1)
  draw_ring(2)
  draw_ring(3)
  draw_ring(4)
  draw_ring(5)
  for i in range(6, len(colors)):
    draw_ring(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 3, 3, 4, 0, 8], row=11, col=5, last=5),
      generate(colors=[1, 2, 3, 6], row=9, col=6),
  ]
  test = [
      generate(colors=[3, 2, 0, 8, 1], row=10, col=10),
  ]
  return {"train": train, "test": test}
