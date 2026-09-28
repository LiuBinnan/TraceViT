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


def generate(colors=None, pattern=None, shown=None, psize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    pattern: The bitmap pattern.
    shown: A list of shown pixel indices.
    psize: The height and width of each pattern quadrant.
  """

  if colors is None:
    if psize is None:
      psize = 4
    while True:
      colors = []
      for _ in range(4):
        colors.extend(common.sample(list(range(0, 10)), 2))
      if len(set(colors)) >= 7: break  # We want them mostly different.
    pattern_cells = psize * psize
    min_ones = round(pattern_cells * 6 / 16)
    max_ones = round(pattern_cells * 10 / 16)
    while True:
      pattern = [common.randint(0, 1) for _ in range(pattern_cells)]
      if sum(pattern) >= min_ones and sum(pattern) <= max_ones: break
    shown = []
    for _ in range(3):
      while True:
        pair = common.sample(list(range(pattern_cells)), 2)
        if pattern[pair[0]] != pattern[pair[1]]: break
      shown.extend(pair)
    pattern = "".join(str(p) for p in pattern)
  elif psize is None:
    psize = 4

  grid = common.grid(2 * psize + 2, 2 * psize + 2)
  for i, char in enumerate(pattern):
    p = int(char)
    grid[i // psize + 1][i % psize + 1] = colors[p + 0]
    if i in shown[0:2]:
      grid[i // psize + 1][2 * psize - i % psize] = colors[p + 2]
    if i in shown[2:4]:
      grid[2 * psize - i // psize][i % psize + 1] = colors[p + 4]
    if i in shown[4:6]:
      grid[2 * psize - i // psize][2 * psize - i % psize] = colors[p + 6]

  output = common.deepcopy(grid)

  def complete_top_right():
    """Completes the top-right quadrant with the pattern in its two colors."""
    nonlocal output
    for i, char in enumerate(pattern):
      p = int(char)
      output[i // psize + 1][2 * psize - i % psize] = colors[p + 2]

  def complete_bottom_left():
    """Completes the bottom-left quadrant with the pattern in its two colors."""
    nonlocal output
    for i, char in enumerate(pattern):
      p = int(char)
      output[2 * psize - i // psize][i % psize + 1] = colors[p + 4]

  def complete_bottom_right():
    """Completes the bottom-right quadrant with the pattern in its two colors."""
    nonlocal output
    for i, char in enumerate(pattern):
      p = int(char)
      output[2 * psize - i // psize][2 * psize - i % psize] = colors[p + 6]

  complete_top_right()
  complete_bottom_left()
  complete_bottom_right()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 8, 9, 7, 4, 1, 2, 5], pattern="0000001101010110",
               shown=[3, 7, 11, 15, 10, 11]),
      generate(colors=[2, 1, 8, 3, 4, 7, 5, 0], pattern="0101110100011111",
               shown=[0, 15, 0, 15, 0, 15]),
      generate(colors=[8, 2, 1, 6, 4, 5, 3, 1], pattern="0100111101000100",
               shown=[7, 14, 13, 14, 5, 15]),
  ]
  test = [
      generate(colors=[4, 1, 5, 8, 6, 7, 0, 3], pattern="0011011111101100",
               shown=[3, 15, 8, 14, 10, 15]),
  ]
  return {"train": train, "test": test}
