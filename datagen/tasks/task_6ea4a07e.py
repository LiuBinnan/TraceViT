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


def generate(values=None, color=None, height=3, width=3, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    values: A list of integers.
    color: A color.
    height: The grid height.
    width: The grid width.
    density: Optional foreground fill percentage (an int in 1..99) that biases
      the sampled pattern toward sparse or dense shapes. When None the original
      balanced coin-flip fill is used, so explicit-`values` callers (validate)
      are byte-identical.
  """

  if values is None:
    color = common.choice([8, 3, 5])
    for _ in range(1000):
      if density is None:
        values = [common.randint(0, 1) for _ in range(height * width)]
      else:
        values = [1 if common.randint(1, 100) <= density else 0
                  for _ in range(height * width)]
      if sum(values) > 0: break
    else:
      values = [0 for _ in range(height * width)]
      values[common.randint(0, height * width - 1)] = 1

  themap = {8: 2, 3: 1, 5: 4}
  grid = common.grid(width, height)
  for i, val in enumerate(values):
    if val:
      grid[i // width][i % width] = color
  missing_color = themap[color]
  output = common.grid(width, height)
  for row in range(height - 1):
    for col in range(width):
      if not values[row * width + col]:
        output[row][col] = missing_color
  for col in range(width):
    if not values[(height - 1) * width + col]:
      output[height - 1][col] = missing_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(values=[1, 1, 1, 0, 0, 1, 0, 0, 0], color=5),
      generate(values=[0, 1, 0, 0, 1, 0, 1, 0, 0], color=8),
      generate(values=[1, 0, 1, 0, 1, 0, 0, 1, 0], color=8),
      generate(values=[0, 0, 1, 0, 1, 0, 1, 0, 0], color=3),
      generate(values=[1, 0, 0, 1, 1, 0, 1, 0, 0], color=5),
      generate(values=[1, 0, 0, 0, 1, 0, 0, 0, 0], color=8),
  ]
  test = [
      generate(values=[0, 1, 0, 1, 1, 0, 0, 0, 1], color=5),
      generate(values=[1, 0, 0, 1, 1, 1, 0, 0, 1], color=3),
  ]
  return {"train": train, "test": test}
