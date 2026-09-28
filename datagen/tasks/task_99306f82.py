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


def generate(size=None, width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    width: The width of the box.
    height: The height of the box.
    colors: The colors of the pixels.
  """

  if size is None:
    colors = common.random_colors(common.randint(2, 6), exclude=[1])
    width = 2 * len(colors) + 1 + common.randint(0, 4)
    height = 2 * len(colors) + 1 + common.randint(0, 4)
    size = min(30, len(colors) + max(width, height) + common.randint(1, 5))

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    output[i][i] = grid[i][i] = color
  row, col, i = len(colors), len(colors), -1
  common.hollow_rect(grid, width, height, row, col, 1)
  common.hollow_rect(output, width, height, row, col, 1)

  # Precompute the nested rings inside the blue box. The diagonal legend gives
  # the ring colors from outermost to innermost (the last color repeats once the
  # legend runs out). Bookkeeping only -- no output writes, no randomness.
  rings = []
  w, h, r, c, j = width, height, row, col, -1
  while True:
    w, h, r, c, j = w - 2, h - 2, r + 1, c + 1, j + 1
    if w <= 0 or h <= 0: break
    rings.append((w, h, r, c, colors[j if j < len(colors) else -1]))

  # Output solving story: fill the concentric rings outermost first, coloring
  # each from the legend. The catch-all completes any rings beyond the six
  # individually traced stages.
  def draw_ring(k):
    if k >= len(rings): return
    w, h, r, c, color = rings[k]
    common.hollow_rect(output, w, h, r, c, color)

  draw_ring(0)
  draw_ring(1)
  draw_ring(2)
  draw_ring(3)
  draw_ring(4)
  draw_ring(5)
  for k in range(6, len(rings)):
    draw_ring(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, width=9, height=9, colors=[2, 6, 4]),
      generate(size=10, width=6, height=6, colors=[3, 2]),
      generate(size=15, width=10, height=10, colors=[8, 6, 4, 2]),
  ]
  test = [
      generate(size=20, width=14, height=13, colors=[2, 3, 9, 8, 7]),
  ]
  return {"train": train, "test": test}
