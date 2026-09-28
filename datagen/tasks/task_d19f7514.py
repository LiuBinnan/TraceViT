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


def generate(top=None, bottom=None, width=4, height=6):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    width = common.randint(3, 8)
    height = common.randint(4, 11)
    while True:
      top = [common.randint(0, 1) for _ in range(width * height)]
      bottom = [common.randint(0, 1) for _ in range(width * height)]
      overlay = [top_bit or bottom_bit
                 for top_bit, bottom_bit in zip(top, bottom)]
      if any(overlay) and not all(overlay):
        break

  grid = common.grid(width, 2 * height)
  for i in range(len(top)):
    grid[i // width][i % width] = 3 if top[i] else 0
  for i in range(len(bottom)):
    grid[height + i // width][i % width] = 5 if bottom[i] else 0

  # Overlay the two stacked grids with a logical OR: a cell lights up (yellow)
  # if it is set in the top (green) grid OR in the bottom (gray) grid.
  output = common.grid(width, height)

  def reveal_from_top():
    """Lights each output cell that is set in the top (green) grid."""
    for i in range(len(top)):
      if top[i]:
        output[i // width][i % width] = common.yellow()

  def reveal_from_bottom():
    """ORs in each output cell that is set in the bottom (gray) grid."""
    for i in range(len(bottom)):
      if bottom[i]:
        output[i // width][i % width] = common.yellow()

  reveal_from_top()
  reveal_from_bottom()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
               bottom=[0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0]),
      generate(top=[1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               bottom=[1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0]),
      generate(top=[1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               bottom=[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0]),
      generate(top=[0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
               bottom=[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]),
  ]
  test = [
      generate(top=[1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
               bottom=[0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]),
  ]
  return {"train": train, "test": test}
