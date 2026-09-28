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


def generate(vals=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: The values of the pixels.
    color: The color of the grid.
  """

  if vals is None:
    color = common.random_color()
    while True:
      vals = [1 if common.randint(0, 1) else 0 for _ in range(9)]
      if sum(vals) != 0: break

  # Input is a 3x3 pattern: colored where vals[i] is set, background elsewhere.
  # The 9x9 output is a fractal: each background cell of the input hosts a copy
  # of the inverse pattern (the background cells lit up in the same color) in its
  # 3x3 block, while foreground cells leave their block empty. Solving stamps one
  # background block at a time.
  grid = common.grid(3, 3)
  for i, val in enumerate(vals):
    grid[i // 3][i % 3] = val * color

  output = common.grid(9, 9)
  bg_blocks = [j for j in range(9) if vals[j] == 0]

  def stamp_block(k):
    """Stamps the inverse pattern into the k-th background cell's block."""
    nonlocal output
    if k >= len(bg_blocks): return
    j = bg_blocks[k]
    jr, jc = j // 3, j % 3
    for ir in range(3):
      for ic in range(3):
        if vals[3 * ir + ic] == 0:
          output[3 * jr + ir][3 * jc + ic] = color

  stamp_block(0)
  stamp_block(1)
  stamp_block(2)
  stamp_block(3)
  stamp_block(4)
  stamp_block(5)
  stamp_block(6)
  stamp_block(7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[1, 1, 0, 0, 1, 1, 0, 1, 0], color=8),
      generate(vals=[1, 1, 0, 0, 0, 1, 0, 1, 0], color=9),
      generate(vals=[1, 0, 1, 1, 1, 1, 0, 1, 0], color=7),
  ]
  test = [
      generate(vals=[1, 1, 0, 0, 1, 0, 1, 0, 1], color=1),
  ]
  return {"train": train, "test": test}
