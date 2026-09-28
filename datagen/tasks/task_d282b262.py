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


def generate(sizes=None, brows=None, bcols=None, evens=None, odds=None,
             gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    sizes: The sizes of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    evens: The "even" colors.
    odds: The "odd" colors.
    gsize: The height and width of the square grid.
  """

  if sizes is None:
    if gsize is None:
      gsize = common.randint(12, 22)
    num_boxes = min(7, max(4, gsize * gsize // 36))
    while True:
      sizes = [common.randint(2, 5) for _ in range(num_boxes)]
      padded = [s + 1 for s in sizes]
      for _ in range(500):
        brows = [common.randint(0, gsize - s) for s in sizes]
        bcols = [common.randint(0, gsize - s) for s in sizes]
        if not common.overlaps(brows, bcols, padded, padded, 0):
          break
      else:
        continue
      break
    evens, odds = [], []
    for _ in range(num_boxes):
      colors = common.random_colors(2)
      evens, odds = evens + [colors[0]], odds + [colors[1]]
  elif gsize is None:
    gsize = 15

  # Draw the scattered checkerboard boxes on the input grid (logic unchanged).
  grid, output = common.grids(gsize, gsize)
  entries = []
  for size, brow, bcol, even, odd in zip(sizes, brows, bcols, evens, odds):
    entries.append((bcol, size, brow, even, odd))
    for r in range(size):
      for c in range(size):
        grid[brow + r][bcol + c] = even if (r + c) % 2 == 0 else odd

  # Slide every box to the right: process the rightmost box first, packing each
  # box against the right wall and against any box already resting in its rows.
  entries = sorted(entries, reverse=True)
  lengths = [0 for _ in range(gsize)]
  placements = []
  for entry in entries:
    _, size, brow, even, odd = entry
    max_length = 0
    for r in range(brow, brow + size):
      max_length = max(max_length, lengths[r])
    for r in range(brow, brow + size):
      lengths[r] = max_length + size
    bcol = gsize - max_length - size
    placements.append((brow, bcol, size, even, odd))

  def slide_box(i):
    """Drops box i to its packed resting place against the right side."""
    if i >= len(placements):
      return
    brow, bcol, size, even, odd = placements[i]
    for r in range(size):
      for c in range(size):
        output[brow + r][bcol + c] = even if (r + c) % 2 == 0 else odd

  slide_box(0)
  slide_box(1)
  slide_box(2)
  slide_box(3)
  slide_box(4)
  slide_box(5)
  for i in range(6, len(placements)):
    slide_box(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(sizes=[2, 2, 2, 2, 2], brows=[2, 3, 7, 8, 10], bcols=[2, 7, 5, 1, 9], evens=[1, 5, 6, 8, 2], odds=[2, 8, 4, 9, 1]),
      generate(sizes=[3, 3, 3, 3, 3], brows=[1, 5, 7, 9], bcols=[1, 3, 8, 1], evens=[8, 2, 1, 7], odds=[3, 1, 4, 6]),
      generate(sizes=[2, 3, 3, 2, 2], brows=[1, 2, 7, 9, 12], bcols=[2, 9, 5, 11, 2], evens=[9, 3, 6, 8, 2], odds=[2, 7, 8, 5, 5]),
  ]
  test = [
      generate(sizes=[3, 5, 2, 2, 3, 2], brows=[0, 2, 5, 9, 10, 13], bcols=[3, 7, 2, 1, 7, 2], evens=[6, 2, 2, 3, 8, 1], odds=[8, 5, 1, 5, 4, 7]),
  ]
  return {"train": train, "test": test}
