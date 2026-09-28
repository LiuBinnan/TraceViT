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

  if colors is None:
    gsize = common.randint(6, 10)
    shape = common.randint(0, 1)
    while True:
      colors = [0] * (gsize * gsize)
      rows = [common.randint(0, gsize - 2) for _ in range(4)]
      cols = [common.randint(0, gsize - 2) for _ in range(4)]
      good = True  # First, check that no overlap
      for row, col  in zip(rows, cols):
        for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          if shape == 0 and r == 0 and c == 0: continue
          if colors[(row + r) * gsize + col + c]: good = False
          colors[(row + r) * gsize + col + c] = 1
      if not good: continue
      if shape == 0:
        good = False  # If shape is 0, check that there's some "nesting."
        for row, col in zip(rows, cols):
          if colors[row * gsize + col]: good = True
      if good: break
    colors = "".join(map(str, colors))

  gsize = int(round(len(colors) ** 0.5))
  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = 8 * int(color)

  # Recognize the repeated shape: a full 2x2 block, or -- when only 12 cells
  # are lit, i.e. four L-triominoes -- a 2x2 with the top-left corner removed.
  offsets = [(0, 1), (1, 0), (1, 1)]
  if colors.count("1") != 12:
    offsets = [(0, 0)] + offsets

  output = common.grid(5, 5)
  quadrants = [(0, 0), (0, 3), (3, 0), (3, 3)]

  def stamp_copy(q):
    """Stamps one copy of the recognized shape into output quadrant q."""
    nonlocal output
    qrow, qcol = quadrants[q]
    for drow, dcol in offsets:
      output[qrow + drow][qcol + dcol] = 8

  stamp_copy(0)
  stamp_copy(1)
  stamp_copy(2)
  stamp_copy(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="111100111111011011011000000000000000"),
      generate(colors="001100111100111111001111000000000000"),
      generate(colors="000100011100111010011110000000000000"),
      generate(colors="000100011110111110011000000000000000"),
      generate(colors="000100001110010110111000011000000000"),
  ]
  test = [
      generate(colors="010100111110000111000011000000000000"),
      generate(colors="001100111100110110011110011000000000"),
  ]
  return {"train": train, "test": test}
