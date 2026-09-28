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
    colors: A list of colors to use.
  """

  def draw():
    grid = common.grid(3, 3)
    counts_to_colors = [(colors.count(c), c) for c in set(colors)]
    counts_to_colors.sort(reverse=True)
    if counts_to_colors[0][0] == counts_to_colors[1][0]: return None, None
    for row in range(3):
      for col in range(3):
        grid[row][col] = colors[row * 3 + col]
    return grid, counts_to_colors

  if colors is None:
    subset = common.random_colors(common.randint(2, 8))
    while True:
      colors = common.choices(subset, 9)
      if len(set(colors)) != len(subset): continue
      grid, _ = draw()
      if grid: break

  grid, counts_to_colors = draw()
  if grid is None: return {"input": grid, "output": None}
  output = common.grid(9, 9)
  winner = counts_to_colors[0][1]
  winner_cells = [i for i, color in enumerate(colors) if color == winner]

  def copy_winner_cell(i):
    """Copies the input tile into the next majority-color output block."""
    if i >= len(winner_cells): return
    row, col = winner_cells[i] // 3, winner_cells[i] % 3
    for r in range(3):
      for c in range(3):
        output[row * 3 + r][col * 3 + c] = colors[r * 3 + c]

  copy_winner_cell(0)
  copy_winner_cell(1)
  copy_winner_cell(2)
  copy_winner_cell(3)
  copy_winner_cell(4)
  copy_winner_cell(5)
  copy_winner_cell(6)
  copy_winner_cell(7)
  copy_winner_cell(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 5, 4, 2, 2, 5, 5, 5, 4]),
      generate(colors=[7, 7, 1, 4, 7, 1, 3, 3, 7]),
      generate(colors=[1, 2, 3, 9, 9, 1, 2, 9, 4]),
      generate(colors=[8, 8, 1, 8, 6, 1, 4, 9, 6]),
  ]
  test = [
      generate(colors=[9, 6, 7, 8, 7, 7, 2, 8, 7]),
  ]
  return {"train": train, "test": test}
