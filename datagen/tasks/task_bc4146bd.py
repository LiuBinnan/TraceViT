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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: digits representing the colors to be used
  """

  if colors is None:
    num_colors = common.randint(2, 4)
    values = common.random_colors(num_colors)
    while True:
      colors = [common.choice(values) for _ in range(16)]
      if len(set(colors)) == num_colors: break

  grid = common.grid(4, 4)
  for i in range(16):
    grid[i // 4][i % 4] = colors[i]

  # Solve the puzzle forward: unfold the 4x4 tile into five panels, mirroring
  # across each vertical seam (original, flipped, original, flipped, original).
  output = common.grid(20, 4)

  def unfold_panel(k):
    """Stamps panel k next to the previous one: even k copies the tile as-is,
    odd k reflects it horizontally across the shared seam."""
    nonlocal output
    for i in range(16):
      row, col = i // 4, i % 4
      dst = col if k % 2 == 0 else 3 - col
      output[row][4 * k + dst] = grid[row][col]

  unfold_panel(0)
  unfold_panel(1)
  unfold_panel(2)
  unfold_panel(3)
  unfold_panel(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 2, 5, 2, 3, 3, 2, 5, 2, 5, 3, 3, 5, 3, 2]),
      generate(colors=[9, 5, 1, 5, 1, 5, 9, 1, 9, 1, 5, 5, 5, 5, 5, 1]),
      generate(colors=[4, 1, 1, 4, 7, 7, 4, 7, 1, 4, 1, 1, 4, 1, 1, 1]),
      generate(colors=[2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 8, 2, 8, 2, 8, 8]),
  ]
  test = [
      generate(colors=[5, 5, 4, 4, 5, 5, 5, 2, 2, 5, 5, 5, 5, 5, 2, 4]),
  ]
  return {"train": train, "test": test}
