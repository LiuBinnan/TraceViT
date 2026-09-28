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


def generate(jcol=None, brow=None, bcol=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    jcol: The column of the J.
    brow: The top row of the colored key shape.
    bcol: The left column of the colored key shape.
    colors: A list of colors to use.
    gsize: The odd side length of the square canvas.
  """

  def draw():
    # Certain parts of the shape need to be colored in.
    if colors[2] + colors[3] == 0: return None, None
    if colors[4] + colors[5] == 0: return None, None
    if colors[0] + colors[2] + colors[4] == 0: return None, None
    if colors[1] + colors[3] + colors[5] == 0: return None, None
    # The shape and the J can't overlap.
    if bcol >= jcol - 4 and bcol <= jcol + 1: return None, None
    grid, output = common.grids(gsize, gsize, 7)
    # Draw the pink J.
    output[0][jcol] = grid[gsize // 2 + 1][jcol] = 6
    output[1][jcol] = grid[gsize // 2 + 2][jcol] = 6
    output[2][jcol] = grid[gsize // 2 + 3][jcol] = 6
    output[3][jcol - 1] = grid[gsize // 2 + 4][jcol - 1] = 6
    output[2][jcol - 2] = grid[gsize // 2 + 3][jcol - 2] = 6
    # Draw the shape.
    for i, color in enumerate(colors):
      if not color: continue
      grid[brow + i // 2][bcol + i % 2] = color
      output[i // 2][jcol - 3 + i % 2] = color
    # Draw the yellow line.
    for c in range(gsize):
      if grid[gsize // 2][c] != 7: return None, None
      output[gsize // 2][c] = grid[gsize // 2][c] = 4
    return grid, output

  if jcol is None:
    if gsize is None:
      gsize = common.choice([9, 11, 13, 15])
    hue = common.random_color(exclude=[4, 6, 7])
    # Choose the shape colors.
    for _ in range(500):
      colors = [hue * common.randint(0, 1) for _ in range(6)]
      jcol = common.randint(3, gsize - 1)
      brow = common.randint(gsize // 2, gsize - 3)
      bcol = common.randint(0, gsize - 2)
      grid, _ = draw()
      if grid: break
    else:
      colors = [hue] * 6
      jcol = 3
      brow = gsize // 2 + 1
      bcol = gsize - 2
  elif gsize is None:
    gsize = 11

  # `draw()` lays out the input (J and key scattered in the bottom half, split
  # off by the yellow line). Rebuild the output forward: keep the divider, then
  # relocate the two pieces into their assembled position at the top.
  grid, _ = draw()
  if grid is None:
    return {"input": None, "output": None}
  output = common.grid(gsize, gsize, common.orange())
  for c in range(gsize):
    output[gsize // 2][c] = common.yellow()

  def place_j():
    """Lifts the pink J up to the top edge of the grid."""
    output[0][jcol] = common.pink()
    output[1][jcol] = common.pink()
    output[2][jcol] = common.pink()
    output[3][jcol - 1] = common.pink()
    output[2][jcol - 2] = common.pink()

  def dock_shape():
    """Slots the colored key into place against the lifted J."""
    for i, color in enumerate(colors):
      if not color: continue
      output[i // 2][jcol - 3 + i % 2] = color

  place_j()
  dock_shape()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(jcol=10, brow=5, bcol=4, colors=[0, 0, 2, 0, 2, 2]),
      generate(jcol=8, brow=7, bcol=1, colors=[0, 0, 8, 8, 8, 8]),
      generate(jcol=5, brow=5, bcol=8, colors=[0, 0, 0, 1, 1, 0]),
  ]
  test = [
      generate(jcol=8, brow=7, bcol=2, colors=[0, 8, 8, 0, 0, 8]),
  ]
  return {"train": train, "test": test}
