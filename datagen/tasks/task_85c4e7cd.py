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


def generate(colors=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors.
    height: The number of rows in the (rectangular) grid.
    width: The number of columns in the (rectangular) grid.
  """
  if colors is None:
    colors = common.random_colors(common.randint(3, 9))

  size = 2 * len(colors)
  # Square fallback: when height/width are omitted both collapse to `size`,
  # so validate()'s hardcoded calls reproduce the original square output.
  if height is None:
    height = size
  if width is None:
    width = size

  # SECONDARY-COUNT GUARD: the ring count is len(colors), but a rectangular grid
  # only has min(height, width) // 2 ring layers. Cap the number of rings (and the
  # colors used) to what fits so input and output stay a recolor-pair over the same
  # color set. In the square fallback min(h, w) // 2 == len(colors) -> no change.
  num = max(1, min(len(colors), min(height, width) // 2))
  colors = colors[:num]
  grid, output = common.grids(width, height)

  def ring_index(r, c):
    # Distance from the nearest edge, clamped to the last (innermost) color so
    # any leftover interior block belongs to the innermost named ring.
    return min(min(r, height - 1 - r, c, width - 1 - c), num - 1)

  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[ring_index(r, c)]

  def reveal_ring_range(start, stop):
    stop = min(stop, num)
    for ring_idx in range(start, stop):
      color = colors[num - 1 - ring_idx]
      for r in range(height):
        for c in range(width):
          if ring_index(r, c) == ring_idx:
            output[r][c] = color

  def reveal_outer_rings():
    reveal_ring_range(0, (num + 1) // 2)

  def reveal_inner_rings():
    reveal_ring_range((num + 1) // 2, num)

  reveal_outer_rings()
  reveal_inner_rings()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 2, 1, 3, 5, 8]),
      generate(colors=[2, 1, 6]),
      generate(colors=[8, 1, 2, 4]),
      generate(colors=[7, 2, 4, 1, 3]),
  ]
  test = [
      generate(colors=[8, 2, 4, 3, 7, 6, 5]),
  ]
  return {"train": train, "test": test}
