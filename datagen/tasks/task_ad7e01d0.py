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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    colors: A list of colors to use.
  """

  if size is None:
    size = common.randint(3, 5)
    # Color axis: decorative hues are free (non-marker, non-background)
    # colors, so sample any 2 distinct colors excluding 0 (background) and 5
    # (the fractal marker) instead of only {1,2,3}. Rule-faithful: 5 stays the
    # trigger and 0 stays blank; the copy-stamp logic is unchanged.
    hues = common.random_colors(2, exclude=[0, 5])
    colors = [0] * (size * size)
    angle = common.randint(0, 3)
    while 5 not in colors or hues[0] not in colors or hues[1] not in colors:
      r, c = common.randint(0, size - 1), common.randint(0, size - 1)
      color = common.choice(hues + [0, 5])
      colors[r * size + c] = color
      if angle == 0: colors[(size - 1 - r) * size + c] = color
      if angle == 1: colors[r * size + (size - 1 - c)] = color
      if angle == 2: colors[c * size + r] = color
      if angle == 3: colors[(size - 1 - c) * size + (size - 1 - r)] = color

  # Build the input grid.
  grid = common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color

  # Solve it forward. This is a fractal: the size*size grid becomes a
  # (size*size)*(size*size) grid where every block whose input cell is the
  # marker color (5) is replaced by a full copy of the input, and every other
  # block stays blank. Stamp one copy per marker, in reading order.
  output = common.grid(size * size, size * size)
  markers = [i for i in range(size * size) if colors[i] == 5]

  def stamp_marker(k):
    """Stamps a full copy of the input into the k-th marker's block."""
    nonlocal output
    if k >= len(markers): return
    block_row, block_col = markers[k] // size, markers[k] % size
    for j, color_j in enumerate(colors):
      output[block_row * size + j // size][block_col * size + j % size] = color_j

  stamp_marker(0)
  stamp_marker(1)
  stamp_marker(2)
  stamp_marker(3)
  stamp_marker(4)
  stamp_marker(5)
  stamp_marker(6)
  stamp_marker(7)
  stamp_marker(8)
  stamp_marker(9)
  stamp_marker(10)
  stamp_marker(11)
  stamp_marker(12)
  stamp_marker(13)
  stamp_marker(14)
  stamp_marker(15)
  stamp_marker(16)
  stamp_marker(17)
  stamp_marker(18)
  stamp_marker(19)
  stamp_marker(20)
  stamp_marker(21)
  stamp_marker(22)
  stamp_marker(23)
  stamp_marker(24)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, colors=[0, 5, 0, 3, 5, 5, 2, 0, 0, 2, 5, 5, 3, 0, 5, 0]),
      generate(size=3, colors=[2, 5, 1, 0, 5, 0, 2, 5, 1]),
      generate(size=4, colors=[5, 5, 5, 5, 5, 2, 3, 5, 5, 3, 3, 5, 5, 5, 5, 5]),
      generate(size=3, colors=[5, 0, 1, 5, 2, 0, 5, 5, 5]),
  ]
  test = [
      generate(size=5,
               colors=[1, 0, 5, 0, 1, 0, 2, 2, 2, 0, 5, 0, 5, 0, 5, 0, 2, 2, 2, 0, 1, 0, 5, 0, 1]),
  ]
  return {"train": train, "test": test}
