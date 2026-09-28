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


def generate(colors=None, n=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    n: The side length of the compressed lattice.
  """

  if colors is None:
    while True:
      colors = [
          0 if common.randint(0, 1) else common.random_color()
          for _ in range(n * n)
      ]
      good = True
      for i in range(n):
        if sum([colors[n * i + j] for j in range(n)]) == 0: good = False
        if sum([colors[n * j + i] for j in range(n)]) == 0: good = False
      if good: break

  grid = common.grid(2 * n, 2 * n)
  output = common.grid(n, n)
  for i, color in enumerate(colors):
    grid[2 * (i // n)][2 * (i % n)] = color
  for c in range(n):
    output[0][c] = grid[0][2 * c]
  for c in range(n):
    output[1][c] = grid[2][2 * c]
  for r in range(2, n):
    for c in range(n):
      output[r][c] = grid[2 * r][2 * c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 0, 2, 8, 0, 8, 0, 1, 0]),
      generate(colors=[2, 2, 1, 2, 1, 0, 3, 0, 0]),
      generate(colors=[1, 0, 0, 0, 2, 0, 6, 0, 6]),
  ]
  test = [
      generate(colors=[3, 3, 4, 7, 0, 1, 7, 0, 1]),
  ]
  return {"train": train, "test": test}
