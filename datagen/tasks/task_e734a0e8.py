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


def generate(minisize=None, megasize=None, pattern="", dots=""):
  """Returns input and output grids according to the given parameters.

  Args:
    minisize: The size of the mini square.
    megasize: The number of mini squares per side.
    pattern: The pattern of the mini square.
    dots: The pattern of the dots.
  """

  if minisize is None:
    while True:
      megasize = common.randint(2, 5)
      minisize = common.choice([3, 5, 7])
      if (minisize + 1) * megasize - 1 <= 30: break
    while True:
      dots = [common.randint(0, 1) for _ in range(megasize * megasize)]
      dots[common.randint(0, len(dots) - 1)] = 2
      if len(set(dots)) == 3: break
    color = common.random_color(exclude=[7])
    while True:
      pixels = []
      for row in range(minisize):
        for col in range(minisize):
          if common.randint(0, 2) == 0: pixels.append((row, col))
      if pixels and common.diagonally_connected(pixels): break
    pattern = []
    for row in range(minisize):
      for col in range(minisize):
        pattern.append(color if (row, col) in pixels else 7)
    dots = "".join(map(str, dots))
    pattern = "".join(map(str, pattern))

  # Build the input: a lattice of empty mini-squares, one holding the key
  # stencil (dot 2) and the marked cells carrying a single center dot (dot 1).
  size = (minisize + 1) * megasize - 1
  grid = common.grid(size, size)
  for megarow in range(megasize):
    for megacol in range(megasize):
      common.rect(grid, minisize, minisize, megarow * (minisize + 1),
                  megacol * (minisize + 1), 7)
      dot = int(dots[megarow * megasize + megacol])
      if dot == 0: continue
      if dot == 1:
        row = megarow * (minisize + 1) + minisize // 2
        col = megacol * (minisize + 1) + minisize // 2
        grid[row][col] = 0
      if dot == 2:
        for row in range(minisize):
          for col in range(minisize):
            r = megarow * (minisize + 1) + row
            c = megacol * (minisize + 1) + col
            grid[r][c] = int(pattern[row * minisize + col])

  # Solve forward: the key stencil is already visible; copy it into every
  # marked cell (dot 1), one cell per frame, overwriting its center dot.
  output = common.deepcopy(grid)
  markers = []
  for megarow in range(megasize):
    for megacol in range(megasize):
      if int(dots[megarow * megasize + megacol]) == 1:
        markers.append((megarow, megacol))

  def stamp_row(megarow):
    """Stamps the key stencil into every marked cell on lattice row megarow."""
    nonlocal output
    for mr, megacol in markers:
      if mr != megarow: continue
      for row in range(minisize):
        for col in range(minisize):
          r = mr * (minisize + 1) + row
          c = megacol * (minisize + 1) + col
          output[r][c] = int(pattern[row * minisize + col])

  # One frame per lattice row holding markers (megasize <= 5 by sampling);
  # rows without markers produce empty frames that dedup removes.
  stamp_row(0)
  stamp_row(1)
  stamp_row(2)
  stamp_row(3)
  stamp_row(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(minisize=5, megasize=4, pattern="7779977797777977999779777",
               dots="0100010000211001"),
      generate(minisize=3, megasize=3, pattern="727727727", dots="200010011"),
  ]
  test = [
      generate(minisize=5, megasize=3, pattern="7747744444774777474747774",
               dots="002010101"),
  ]
  return {"train": train, "test": test}
