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


def generate(colors=None, panel_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the input pixels.
    panel_count: The number of three-column glyph panels.
  """

  if panel_count is None:
    panel_count = 3
  if colors is None:
    colors = common.sample([1, 3, 4, 6, 9], panel_count)

  grid = common.grid(len(colors) * 3, 3)
  for i, color in enumerate(colors):
    if color == 1:
      grid[2][i * 3] = grid[2][i * 3 + 1] = grid[2][i * 3 + 2] = 5
    if color == 3:
      grid[0][i * 3] = grid[0][i * 3 + 1] = grid[0][i * 3 + 2] = 5
      grid[1][i * 3] = grid[1][i * 3 + 2] = 5
      grid[2][i * 3] = grid[2][i * 3 + 1] = grid[2][i * 3 + 2] = 5
    if color == 4:
      grid[1][i * 3 + 1] = 5
    if color == 6:
      grid[0][i * 3] = grid[0][i * 3 + 1] = grid[0][i * 3 + 2] = 5
    if color == 9:
      grid[2][i * 3] = grid[1][i * 3 + 1] = grid[0][i * 3 + 2] = 5
  output = common.grid(len(colors) * 3, 3)

  def fill_panel(i):
    if i >= len(colors):
      return
    color = colors[i]
    common.rect(output, 3, 3, 0, i * 3, color)

  fill_panel(0)
  fill_panel(1)
  fill_panel(2)
  fill_panel(3)
  fill_panel(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 3, 1]),
      generate(colors=[9, 1, 4]),
      generate(colors=[4, 6, 3]),
      generate(colors=[3, 4, 9]),
  ]
  test = [
      generate(colors=[1, 9, 6]),
  ]
  return {"train": train, "test": test}
