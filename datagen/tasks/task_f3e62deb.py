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


def generate(row=None, col=None, color=None, gsize=None, bsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: The row of the box.
    col: The column of the box.
    color: The color of the box.
    gsize: The side length of the square canvas.
    bsize: The side length of the hollow box.
  """

  if color is None:
    if gsize is None:
      gsize = common.randint(8, 20)
    if bsize is None:
      bsize = common.randint(2, 5)
    # Keep the box separated from every wall. Only gsize=8, bsize=5 needs
    # a one-cell rather than two-cell margin to keep the full sampled bands.
    margin = min(2, (gsize - bsize) // 2)
    row = common.randint(margin, gsize - bsize - margin)
    col = common.randint(margin, gsize - bsize - margin)
    color = common.choice([3, 4, 6, 8])
  else:
    if gsize is None:
      gsize = 10
    if bsize is None:
      bsize = 3

  # Build the input grid: the hollow box at its starting position.
  grid, output = common.grids(gsize, gsize)
  common.hollow_rect(grid, bsize, bsize, row, col, color)

  # Solve forward: the box's color tells it which wall to slide to (3 = left,
  # 4 = bottom, 6 = top, 8 = right). It is a single object making a single
  # move, so there is one semantic stage. It always moves (the box starts away
  # from every wall).
  def slide_to_edge():
    """Slides the box to the wall indicated by its color."""
    r, c = row, col
    if color == 3: c = 0
    if color == 4: r = gsize - bsize
    if color == 6: r = 0
    if color == 8: c = gsize - bsize
    common.hollow_rect(output, bsize, bsize, r, c, color)

  slide_to_edge()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4, color=6),
      generate(row=4, col=2, color=6),
      generate(row=5, col=2, color=8),
      generate(row=2, col=3, color=4),
      generate(row=3, col=3, color=8),
      generate(row=2, col=2, color=8),
  ]
  test = [
      generate(row=5, col=3, color=3),
      generate(row=4, col=4, color=4),
  ]
  return {"train": train, "test": test}
