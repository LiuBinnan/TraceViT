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


def generate(fgcolor=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    fgcolor: The foreground color.
    colors: A list of colors to use.
    gsize: The even side length of the grid.
  """

  if fgcolor is None:
    if gsize is None:
      gsize = 2 * common.randint(4, 13)
    num_pixels = common.randint(
        int(0.18 * gsize * gsize), int(0.24 * gsize * gsize))
    subset = common.random_colors(3)
    fgcolor = subset.pop()
    grid = common.grid(gsize, gsize)
    for row in range(gsize):
      for col in range(gsize):
        grid[row][col] = common.choice(subset + [0])
    seed = (gsize // 2 - 1, gsize // 2 - 1)
    grid[seed[0]][seed[1]] = fgcolor
    queue = [seed]
    while True:
      idx = common.randint(0, len(queue) - 1)
      r, c = queue.pop(idx)
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if (1 <= nr < gsize - 1 and 0 <= nc < gsize // 2
            and grid[nr][nc] != fgcolor):
          grid[nr][nc] = fgcolor
          if common.randint(0, 1):
            grid[nr][gsize - 1 - nc] = fgcolor
          queue.append((nr, nc))
          num_pixels -= 1
      if num_pixels <= 0: break
    colors = common.flatten(grid)
  elif gsize is None:
    gsize = 10

  grid = common.grid(gsize, gsize)
  for i, color in enumerate(colors):
    grid[i // gsize][i % gsize] = color
  output = common.deepcopy(grid)

  def complete_mirror():
    """Reflects every left-half fgcolor pixel across the vertical midline."""
    for r in range(gsize):
      for c in range(gsize // 2):
        if output[r][c] == fgcolor:
          output[r][gsize - 1 - c] = fgcolor

  complete_mirror()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(fgcolor=3, colors=[9, 0, 0, 0, 0, 7, 7, 0, 9, 0,
                                  0, 0, 9, 0, 0, 0, 9, 9, 9, 0,
                                  7, 7, 0, 3, 3, 3, 3, 7, 9, 7,
                                  0, 3, 7, 3, 3, 3, 3, 9, 3, 7,
                                  0, 3, 9, 3, 3, 0, 0, 0, 3, 9,
                                  9, 3, 3, 3, 3, 0, 0, 9, 3, 0,
                                  3, 3, 3, 3, 3, 9, 0, 0, 3, 7,
                                  3, 3, 3, 3, 3, 0, 9, 9, 3, 0,
                                  0, 9, 0, 3, 3, 3, 9, 9, 9, 9,
                                  7, 9, 7, 9, 0, 0, 7, 7, 0, 0]),
      generate(fgcolor=1, colors=[6, 6, 8, 8, 8, 0, 8, 0, 6, 0,
                                  0, 8, 0, 0, 6, 6, 6, 6, 8, 0,
                                  6, 6, 0, 1, 1, 1, 1, 0, 6, 6,
                                  0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
                                  8, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                                  6, 1, 1, 1, 1, 1, 1, 1, 6, 0,
                                  6, 1, 1, 1, 1, 1, 1, 1, 6, 8,
                                  0, 8, 1, 1, 1, 8, 6, 8, 0, 0,
                                  6, 8, 6, 0, 6, 0, 8, 0, 6, 8,
                                  8, 6, 0, 6, 0, 6, 6, 8, 0, 8]),
      generate(fgcolor=2, colors=[1, 1, 0, 1, 1, 0, 0, 0, 4, 1,
                                  4, 4, 0, 4, 2, 2, 1, 4, 4, 4,
                                  4, 0, 2, 2, 2, 2, 2, 2, 1, 0,
                                  0, 4, 2, 2, 2, 0, 0, 1, 1, 0,
                                  0, 0, 1, 2, 2, 2, 1, 0, 1, 0,
                                  0, 4, 0, 2, 2, 0, 2, 0, 0, 0,
                                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                  4, 1, 4, 1, 2, 2, 4, 4, 1, 4,
                                  0, 4, 4, 4, 2, 1, 1, 4, 4, 1,
                                  4, 0, 4, 4, 0, 4, 1, 1, 4, 0]),
  ]
  test = [
      generate(fgcolor=9, colors=[0, 0, 6, 6, 6, 6, 0, 6, 6, 0,
                                  2, 6, 0, 6, 9, 0, 6, 0, 2, 6,
                                  2, 6, 6, 9, 9, 9, 9, 0, 6, 6,
                                  2, 0, 0, 9, 9, 0, 9, 6, 0, 2,
                                  9, 9, 9, 9, 9, 9, 6, 0, 0, 0,
                                  9, 9, 9, 9, 9, 9, 9, 9, 0, 0,
                                  0, 0, 9, 9, 9, 9, 6, 6, 0, 0,
                                  2, 9, 9, 9, 9, 9, 9, 6, 2, 6,
                                  0, 0, 2, 9, 0, 6, 9, 0, 2, 6,
                                  6, 0, 0, 2, 0, 6, 0, 6, 6, 2]),
  ]
  return {"train": train, "test": test}
