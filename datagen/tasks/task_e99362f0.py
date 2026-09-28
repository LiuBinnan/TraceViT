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


def generate(top=None, upper=None, lower=None, bottom=None, width=4, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    upper: Boolean values for the upper grid.
    lower: Boolean values for the lower grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    width = common.randint(3, 8)
    height = common.randint(3, 10)
    top = [common.randint(0, 1) for _ in range(width * height)]
    upper = [common.randint(0, 1) for _ in range(width * height)]
    lower = [common.randint(0, 1) for _ in range(width * height)]
    bottom = [common.randint(0, 1) for _ in range(width * height)]

  # Input: four quadrant patterns split by a yellow cross, each in its color.
  grid = common.grid(2 * width + 1, 2 * height + 1)
  output = common.grid(width, height)
  for i in range(2 * width + 1):
    grid[height][i] = common.yellow()
  for i in range(2 * height + 1):
    grid[i][width] = common.yellow()
  for i in range(len(lower)):
    if lower[i]:
      grid[height + 1 + i // width][i % width] = common.red()
  for i in range(len(upper)):
    if upper[i]:
      grid[i // width][width + 1 + i % width] = common.maroon()
  for i in range(len(top)):
    if top[i]:
      grid[i // width][i % width] = common.orange()
  for i in range(len(bottom)):
    if bottom[i]:
      grid[height + 1 + i // width][width + 1 + i % width] = common.cyan()

  # Output: overlay the four layers, later layers winning on overlap
  # (cyan > orange > maroon > red).
  def stamp_lower():
    """Overlays the bottom-left (red) layer."""
    for i in range(len(lower)):
      if lower[i]:
        output[i // width][i % width] = common.red()

  def stamp_upper():
    """Overlays the top-right (maroon) layer."""
    for i in range(len(upper)):
      if upper[i]:
        output[i // width][i % width] = common.maroon()

  def stamp_top():
    """Overlays the top-left (orange) layer."""
    for i in range(len(top)):
      if top[i]:
        output[i // width][i % width] = common.orange()

  def stamp_bottom():
    """Overlays the bottom-right (cyan) layer."""
    for i in range(len(bottom)):
      if bottom[i]:
        output[i // width][i % width] = common.cyan()

  stamp_lower()
  stamp_upper()
  stamp_top()
  stamp_bottom()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1],
               upper=[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
               lower=[0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
               bottom=[1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0]),
      generate(top=[0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
               upper=[0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
               lower=[0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
               bottom=[1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0]),
      generate(top=[1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
               upper=[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
               lower=[0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
               bottom=[0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0]),
      generate(top=[0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
               upper=[0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
               lower=[0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
               bottom=[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0]),
      generate(top=[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
               upper=[0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               lower=[1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
               bottom=[0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1]),
      generate(top=[1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
               upper=[0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
               lower=[0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
               bottom=[0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0]),
  ]
  test = [
      generate(top=[1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
               upper=[0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
               lower=[1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
               bottom=[1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
