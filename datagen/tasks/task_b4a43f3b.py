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


def generate(colors=None, pattern=None, lsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    pattern: A list of patterns to use.
    lsize: The side length of the square layout.
  """

  if colors is None:
    lsize = 6 if lsize is None else lsize
    sprite = common.diagonally_connected_sprite(3, 3)
    colors = ""
    for r in range(3):
      for c in range(3):
        colors += str(common.choice([1, 2, 3, 6]) if (r, c) in sprite else 0)
    grid = common.grid(lsize, lsize)
    for _ in range(common.randint(2, 4)):
      length = common.randint(1, lsize)
      pos = common.randint(0, lsize - length)
      val = common.randint(0, lsize - 1)
      cdir = common.randint(0, 1)
      for i in range(pos, pos + length):
        grid[val if cdir else i][i if cdir else val] = 2
    pattern = "".join(str(x) for x in common.flatten(grid))

  grid, output = (
      common.grid(max(6, (lsize := 6 if lsize is None else lsize)),
                  lsize + 7),
      common.grid(lsize * 3, lsize * 3),
  )
  for c in range(max(6, lsize)):
    grid[6][c] = 5
  for row in range(3):
    for col in range(3):
      common.rect(grid, 2, 2, row * 2, col * 2, int(colors[row * 3 + col]))
  for row in range(lsize):
    for col in range(lsize):
      if pattern[row * lsize + col] != "0":
        grid[row + 7][col] = 2

  # The output places the 3x3 color key (encoded in `colors`) at every marked
  # cell of the square layout (encoded in `pattern`), scaling the layout 3x.
  # Solve it band by band: reveal the output three rows at a time, one populated
  # layout row per frame, in top-to-bottom reading order.
  on_rows = [r for r in range(lsize)
             if any(pattern[r * lsize + c] != "0" for c in range(lsize))]

  def stamp_band(k):
    """Stamps the 3x3 key at every marked cell of the k-th populated row."""
    if k >= len(on_rows):
      return
    row = on_rows[k]
    for col in range(lsize):
      if pattern[row * lsize + col] == "0":
        continue
      for r in range(3):
        for c in range(3):
          output[row * 3 + r][col * 3 + c] = int(colors[r * 3 + c])

  stamp_band(0)
  stamp_band(1)
  stamp_band(2)
  stamp_band(3)
  stamp_band(4)
  stamp_band(5)
  for k in range(6, len(on_rows)):
    stamp_band(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="101020320",
               pattern="000000002000022220002000000000000000"),
      generate(colors="136010221",
               pattern="000000220000220000002000000200000000"),
      generate(colors="101010333",
               pattern="000000000000002000002000022200000000"),
      generate(colors="320020061",
               pattern="000000020000002000022220000000000000"),
  ]
  test = [
      generate(colors="010303020",
               pattern="202000002000222222002000002000002000"),
  ]
  return {"train": train, "test": test}
