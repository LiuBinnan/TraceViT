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


def generate(colors=None, brow=None, bcol=None, size=24, cutout=5,
             cutout_h=None, cutout_w=None, grid_size=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    brow: a list of vertical coordinates where the cutout should be placed
    bcol: a list of horizontal coordinates where the cutout should be placed
    size: the width and height of the (square) grid
    cutout: the width and height of the (square) cutout
    cutout_h: the height (row-extent) of the cutout; defaults to cutout
    cutout_w: the width (col-extent) of the cutout; defaults to cutout
    grid_size: optional randomized square grid size
    num_colors: number of non-blue foreground colors to sample
    density: number of symmetry orbits painted with foreground colors
  """

  if colors is None:
    if grid_size is None:
      size = 2 * common.randint(3, 15)
    else:
      size = max(6, min(30, grid_size))
      if size % 2: size -= 1
    if cutout_h is None: cutout_h = common.randint(1, size)
    if cutout_w is None: cutout_w = common.randint(1, size // 2)
  else:
    if grid_size is not None: size = grid_size
    if cutout_h is None: cutout_h = cutout
    if cutout_w is None: cutout_w = cutout
  cutout_h = max(1, min(size - 1, cutout_h))
  cutout_w = max(1, min(size // 2, cutout_w))

  def draw(grid):
    for r in range(cutout_h):
      for c in range(cutout_w):
        grid[brow + r][bcol + c] = common.blue()
    idx = 0
    for r in range(size // 2):
      for c in range(r, size // 2):
        cells = [(r, c), (c, r), (r, size - 1 - c), (size - 1 - c, r),
                 (size - 1 - r, c), (c, size - 1 - r),
                 (size - 1 - r, size - 1 - c), (size - 1 - c, size - 1 - r)]
        shown = False
        for row, col in cells:
          if grid[row][col] != common.blue(): shown = True
        if not shown: return False
        for row, col in cells:
          grid[row][col] = colors[idx]
        idx += 1
    return True

  if colors is None:
    num_orbits = (size // 2) * (size // 2 + 1) // 2
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = max(1, min(8, num_colors))
    if density is None:
      density = common.randint(0, num_orbits)
    density = max(0, min(num_orbits, density))
    color_list = common.random_colors(num_colors, exclude=[common.blue()])
    colors = [common.black() for _ in range(num_orbits)]
    for idx, pos in enumerate(common.shuffle(list(range(num_orbits)))[:density]):
      colors[pos] = color_list[idx % len(color_list)]
    while True:
      brow = common.randint(0, size - cutout_h)
      bcol = common.randint(0, size - cutout_w)
      grid = common.grid(size, size)
      if draw(grid): break

  output = common.grid(size, size)
  draw(output)
  grid = common.deepcopy(output)
  for r in range(cutout_h):
    for c in range(cutout_w):
      grid[brow + r][bcol + c] = common.blue()
  output = [
      output[brow + r][bcol:bcol + cutout_w] for r in range(cutout_h)
  ]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 3, 3, 3, 3, 0, 0, 2, 2, 2, 0, 0, 3, 3, 3, 3, 0, 2, 2,
                       0, 2, 2, 0, 3, 0, 0, 3, 2, 0, 0, 2, 0, 0, 3, 3, 3, 2, 2,
                       2, 2, 2, 2, 3, 3, 0, 2, 0, 2, 2, 2, 3, 0, 0, 0, 2, 2, 2,
                       2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0,
                       2, 0],
               brow=0, bcol=18),
      generate(colors=[0, 3, 3, 3, 0, 3, 0, 8, 8, 0, 8, 8, 0, 3, 0, 3, 0, 8, 0,
                       8, 0, 0, 0, 3, 3, 3, 3, 8, 8, 8, 0, 8, 8, 0, 3, 3, 0, 0,
                       0, 8, 0, 8, 0, 0, 8, 0, 8, 0, 0, 8, 3, 8, 0, 8, 8, 8, 0,
                       6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 0, 6, 0, 6, 6, 6, 6, 6,
                       6, 0],
               brow=11, bcol=6),
      generate(colors=[0, 3, 3, 3, 3, 0, 5, 5, 5, 0, 0, 5, 3, 3, 3, 3, 3, 5, 5,
                       0, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 5, 5, 0, 0, 3, 3, 0, 0,
                       5, 0, 5, 5, 3, 0, 0, 0, 5, 5, 0, 0, 3, 5, 0, 0, 5, 0, 0,
                       0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0,
                       5, 0],
               brow=15, bcol=10),
  ]
  test = [
      generate(colors=[4, 4, 4, 0, 4, 0, 0, 3, 3, 3, 0, 0, 4, 4, 4, 0, 4, 3, 3,
                       3, 3, 0, 3, 0, 4, 0, 0, 3, 3, 0, 0, 3, 3, 0, 4, 4, 3, 3,
                       0, 0, 3, 3, 4, 4, 0, 0, 3, 3, 0, 3, 0, 0, 3, 3, 3, 3, 3,
                       8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 8, 8, 0, 8, 0, 8, 8, 8, 0,
                       8, 8],
               brow=6, bcol=9),
  ]
  return {"train": train, "test": test}
