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


def generate(width=None, height=None, pattern=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    pattern: The pattern along the top.
    colors: The background, top, and leftmost colors.
  """

  if width is None or height is None or pattern is None or colors is None:
    if width is None:
      width = common.randint(3, 28)
    if height is None:
      height = common.randint(3, 28)
    if colors is None:
      while True:
        bgcolor = common.choice(list(range(10)))
        topcolor = common.choice(list(range(10)))
        leftcolor = common.choice(list(range(10)))
        if bgcolor == 6 or topcolor == 6: continue  # Pinks not allowed here.
        if topcolor != bgcolor and leftcolor != bgcolor: break
      colors = [bgcolor, topcolor, leftcolor]
    if pattern is None:
      while True:
        pattern = [common.randint(0, 1) for _ in range(width)]
        if sum(pattern) > 0 and sum(pattern) < width: break

  bgcolor, topcolor, leftcolor = colors[0], colors[1], colors[2]

  # Input: a tall bg field carrying the marker pattern along the top row
  # (topcolor) and a dashed left column (leftcolor on the odd rows).
  grid = common.grid(width, height, bgcolor)
  for c, bit in enumerate(pattern):
    if bit: grid[0][c] = topcolor
  for r in range(1, height, 2):
    grid[r][0] = leftcolor

  # Solve: compress the field into a three-row legend on a fresh canvas.
  output = common.grid(width, 3, bgcolor)

  def copy_top_pattern():
    """Top row: reproduce the marker pattern in its own colour."""
    for c, bit in enumerate(pattern):
      if bit: output[0][c] = topcolor

  def echo_pattern_pink():
    """Bottom row: echo the same pattern in pink."""
    for c, bit in enumerate(pattern):
      if bit: output[2][c] = common.pink()

  def mark_left_key():
    """Middle row: drop the left-column key colour at the first cell."""
    output[1][0] = leftcolor

  copy_top_pattern()
  echo_pattern_pink()
  mark_left_key()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=6, pattern=[0, 1, 0, 1, 0, 1, 0, 1], colors=[0, 7, 7]),
      generate(width=10, height=10, pattern=[0, 1, 0, 1, 0, 0, 1, 0, 1, 1], colors=[2, 1, 7]),
      generate(width=13, height=12, pattern=[1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1], colors=[4, 1, 6]),
      generate(width=11, height=8, pattern=[1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1], colors=[9, 4, 7]),
  ]
  test = [
      generate(width=5, height=3, pattern=[1, 0, 1, 0, 1], colors=[1, 8, 4]),
  ]
  return {"train": train, "test": test}
