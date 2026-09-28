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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
  """

  def matching_row_specs():
    specs = []
    for r in range(height):
      row = [color for color in colors[r * width:(r + 1) * width]]
      pair = [color for color in row if color]
      if pair == [7, 4] or pair == [4, 7] or pair == [1, 8] or pair == [8, 1]:
        specs.append((r, row.index(pair[0]), row.index(pair[1]), pair[1]))
    return specs

  def copy_input_rows():
    """Starts the answer as a row-by-row copy of the input."""
    for i, color in enumerate(colors):
      output[i // width][i % width] = color

  def erase_spaced_endpoints():
    """Removes the colored endpoint that must slide leftward."""
    for r, _, second_col, _ in matching_rows:
      output[r][second_col] = 0

  def tuck_endpoints_next_to_partner():
    """Places each removed endpoint immediately after its partner color."""
    for r, first_col, _, moving_color in matching_rows:
      output[r][first_col + 1] = moving_color

  if width is None:
    expected_matches = common.randint(2, 5)
    legendary_pairs = [[7, 4], [4, 7], [1, 8], [8, 1]]
    while True:
      width, height = common.randint(3, 13), common.randint(3, 13)
      colors = []
      for r in range(height):
        row = [0] * width
        if r not in [0, height - 1] or common.randint(0, 1):
          pair, wide = common.random_colors(2), common.randint(3, width)
          if expected_matches == 5 and common.randint(0, 3) == 0:
            pair = legendary_pairs[common.randint(0, 3)]
          col = common.randint(0, width - wide)
          row[col], row[col + wide - 1] = pair[0], pair[1]
        colors += row
      matches = len(matching_row_specs())
      if matches == expected_matches: break

  grid, output = common.grids(width, height)
  matching_rows = matching_row_specs()
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  copy_input_rows()
  erase_spaced_endpoints()
  tuck_endpoints_next_to_partner()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, colors=[0, 0, 8, 0, 0, 0, 0, 9, 0, 0,
                                            0, 0, 6, 0, 0, 0, 0, 7, 0, 0,
                                            0, 7, 0, 0, 0, 0, 0, 0, 0, 4,
                                            0, 0, 0, 2, 0, 4, 0, 0, 0, 0,
                                            0, 0, 0, 0, 1, 0, 0, 0, 0, 8,
                                            0, 0, 3, 0, 0, 0, 9, 0, 0, 0,
                                            6, 0, 0, 0, 0, 0, 0, 4, 0, 0,
                                            0, 0, 4, 0, 0, 7, 0, 0, 0, 0,
                                            0, 0, 0, 0, 0, 0, 8, 0, 1, 0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=5, height=3, colors=[4, 0, 7, 0, 0,
                                          0, 9, 0, 0, 2,
                                          0, 0, 1, 0, 4]),
      generate(width=7, height=4, colors=[0, 8, 0, 4, 0, 0, 0,
                                          4, 0, 0, 0, 0, 0, 7,
                                          0, 0, 1, 0, 0, 8, 0,
                                          0, 9, 0, 0, 4, 0, 0]),
      generate(width=8, height=7, colors=[0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 1, 0, 8, 0, 0, 0, 0,
                                          0, 0, 6, 0, 0, 0, 0, 7,
                                          0, 0, 0, 4, 0, 7, 0, 0,
                                          3, 0, 0, 0, 4, 0, 0, 0,
                                          0, 2, 0, 0, 0, 9, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=4, height=4, colors=[0, 7, 0, 4,
                                          6, 0, 8, 0,
                                          8, 0, 1, 0,
                                          0, 4, 0, 3]),
  ]
  return {"train": train, "test": test}
