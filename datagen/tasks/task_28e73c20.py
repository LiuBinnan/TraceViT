# Copyright 2025 Google LLC
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


def _painted_grids(width, height, num_colors):
  """Returns two identical grids sharing a random-colored background.

  The spiral is drawn later, on the output only, so this shared background is
  preserved untouched everywhere the spiral is not (mirroring re_arc, whose
  verifier overlays the green path on top of whatever the input holds). The
  background never uses green so it can never be mistaken for the path. When
  num_colors is falsy the grids stay blank -- the original behavior, which is
  what validate() reproduces.
  """
  grid, output = common.grids(width, height)
  if not num_colors:
    return grid, output
  palette = [color for color in common.internal_colors
             if color != common.green()]
  num_colors = min(num_colors, len(palette))
  colors = common.sample(palette, num_colors)
  for r in range(height):
    for c in range(width):
      color = common.choice(colors)
      grid[r][c] = color
      output[r][c] = color
  return grid, output


def generate(size=None, height=None, width=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    num_colors: how many distinct non-green colors tint the shared background
      (defaults to blank, i.e. the original all-black canvas)
  """
  if size is None:
    size = common.randint(5, 20)
    if num_colors is None:
      num_colors = common.randint(1, 9)
  if height is None:
    height = size
  if width is None:
    width = size

  path = common.grid(width, height)
  cells = []
  r, c, rdir, cdir = 0, 0, 0, 1
  while True:
    if path[r][c] == common.green(): break
    if r + rdir >= 0 and r + rdir < height and c + cdir >= 0 and c + cdir < width:
      if path[r + rdir][c + cdir] == common.green(): break
    path[r][c] = common.green()
    cells.append((r, c))
    if cdir == 1 and c + 1 == width:
      rdir, cdir = 1, 0
    if cdir == 1 and c + 2 < width and path[r][c + 2] == common.green():
      rdir, cdir = 1, 0
    elif rdir == 1 and r + 1 == height:
      rdir, cdir = 0, -1
    elif rdir == 1 and r + 2 < height and path[r + 2][c] == common.green():
      rdir, cdir = 0, -1
    elif cdir == -1 and c == 0:
      rdir, cdir = -1, 0
    elif cdir == -1 and c - 2 >= 0 and path[r][c - 2] == common.green():
      rdir, cdir = -1, 0
    elif rdir == -1 and path[r - 2][c] == common.green():
      rdir, cdir = 0, 1
    c += cdir
    r += rdir
  grid, output = _painted_grids(width, height, num_colors)
  split1 = len(cells) // 4
  split2 = len(cells) // 2
  split3 = 3 * len(cells) // 4
  for r, c in cells[:split1]:
    output[r][c] = common.green()
  for r, c in cells[split1:split2]:
    output[r][c] = common.green()
  for r, c in cells[split2:split3]:
    output[r][c] = common.green()
  for r, c in cells[split3:]:
    output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=6),
      generate(size=8),
      generate(size=15),
      generate(size=13),
      generate(size=10),
  ]
  test = [
      generate(size=18),
  ]
  return {"train": train, "test": test}
