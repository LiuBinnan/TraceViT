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


def generate(top=None, bottom=None, width=4, height=4):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    width = common.randint(3, 8)
    height = common.randint(3, 10)
    while True:
      top = [common.randint(0, 1) for _ in range(width * height)]
      bottom = [common.randint(0, 1) for _ in range(width * height)]
      nor_count = sum(not a and not b for a, b in zip(top, bottom))
      if 0 < nor_count < width * height:
        break

  grid = common.grid(2 * width, height)
  for i in range(len(top)):
    grid[i // width][i % width] = 6 if top[i] else 0
  for i in range(len(bottom)):
    grid[i // width][width + i % width] = 5 if bottom[i] else 0

  # The answer marks every cell that is empty in BOTH the top (magenta) and the
  # bottom (gray) grid - the logical NOR of the two overlaid patterns. Solve it
  # by elimination: assume every cell qualifies, then cross off the cells that
  # each grid fills.
  output = common.grid(width, height)

  def mark_all_empty():
    """Assumes every cell is empty in both grids: mark them all yellow."""
    for i in range(len(top)):
      output[i // width][i % width] = common.yellow()

  def clear_top_marks():
    """Cross off the cells the top grid fills - not empty in both."""
    for i in range(len(top)):
      if top[i]:
        output[i // width][i % width] = common.black()

  def clear_bottom_marks():
    """Cross off the cells the bottom grid fills - not empty in both."""
    for i in range(len(bottom)):
      if bottom[i]:
        output[i // width][i % width] = common.black()

  mark_all_empty()
  clear_top_marks()
  clear_bottom_marks()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
               bottom=[0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0]),
      generate(top=[0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0],
               bottom=[1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1]),
      generate(top=[1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
               bottom=[1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]),
      generate(top=[1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
               bottom=[1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0]),
  ]
  test = [
      generate(top=[0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
               bottom=[0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1]),
      generate(top=[1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
               bottom=[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
