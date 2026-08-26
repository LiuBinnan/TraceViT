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


def generate(width=None, height=None, boxwidth=None, boxheight=None, row=None,
             col=None, rows=None, cols=None, boxcolor=None, dotcolor=None,
             b=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    boxwidth: the width of the box
    boxheight: the height of the box
    row: the row of the box
    col: the column of the box
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxcolor: the color of the box
    dotcolor: the color of the dots
    b: the integer used for all background cells
    count: the number of dots
  """
  extra_pixels = []
  if width is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    boxwidth = common.randint(2, width // 2)
    boxheight = common.randint(2, height // 2)
    row = common.randint(1, height - boxheight - 2)
    col = common.randint(1, width - boxwidth - 2)
    eligible = []
    for r, c in common.all_pixels(width, height):
      if r + 1 >= row and r <= row + boxheight:
        if c + 1 >= col and c <= col + boxwidth:
          continue
      eligible.append((r, c))
    max_count = max(1, len(eligible) // 4)
    if count is None:
      count = common.randint(1, max_count)
    count = min(count, max_count)
    pixels, rows, cols = common.sample(eligible, count), [], []
    for r, c in pixels:
      rows.append(r)
      cols.append(c)
    remaining = [pixel for pixel in eligible if pixel not in pixels]
    extras = common.remove_neighbors(common.shuffle(remaining))
    if len(extras) > count and common.randint(0, 2) == 0:
      extra_pixels = extras[:count + 1]
    colors = common.sample(list(range(10)), 4 if extra_pixels else 3)
    boxcolor, dotcolor, b = colors[0], colors[1], colors[2]
    if extra_pixels:
      extracolor = colors[3]

  grid, output = common.grids(width, height, b)
  for r in range(row, row + boxheight):
    for c in range(col, col + boxwidth):
      output[r][c] = grid[r][c] = boxcolor
  for r, c in extra_pixels:
    grid[r][c] = extracolor
  for r, c in zip(rows, cols):
    grid[r][c] = dotcolor
  output = [row[:] for row in grid]

  connections = []
  for idx in range(len(rows)):
    r, c = rows[idx], cols[idx]
    rdiff, cdiff = 0, 0
    rdiff = rdiff if r >= row else 1
    rdiff = rdiff if r < row + boxheight else -1
    cdiff = cdiff if c >= col else 1
    cdiff = cdiff if c < col + boxwidth else -1
    if rdiff != 0 and cdiff != 0:
      continue
    nr, nc = r + rdiff, c + cdiff
    if output[nr][nc] == boxcolor:
      continue
    connections.append((idx, rdiff, cdiff))

  def project_connection(connection_idx):
    if connection_idx >= len(connections):
      return
    idx, rdiff, cdiff = connections[connection_idx]
    r, c = rows[idx], cols[idx]
    while output[r + rdiff][c + cdiff] != boxcolor:
      output[r + rdiff][c + cdiff] = dotcolor
      r, c = r + rdiff, c + cdiff

  project_connection(0)
  project_connection(1)
  project_connection(2)
  project_connection(3)
  project_connection(4)
  project_connection(5)
  project_connection(6)
  project_connection(7)
  project_connection(8)
  project_connection(9)
  project_connection(10)
  project_connection(11)
  for idx in range(12, len(connections)):
    project_connection(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=9, boxwidth=3, boxheight=4, row=1, col=2,
               rows=[3, 7], cols=[9, 7], boxcolor=3, dotcolor=4, b=8),
      generate(width=12, height=10, boxwidth=3, boxheight=3, row=2, col=3,
               rows=[8], cols=[3], boxcolor=1, dotcolor=8, b=2),
      generate(width=12, height=14, boxwidth=4, boxheight=4, row=4, col=3,
               rows=[0, 6, 11], cols=[4, 10, 1], boxcolor=4, dotcolor=2, b=1),
      generate(width=18, height=14, boxwidth=5, boxheight=4, row=5, col=7,
               rows=[1, 3, 4, 5, 11], cols=[8, 11, 15, 2, 13], boxcolor=5,
               dotcolor=4, b=1),
  ]
  test = [
      generate(width=21, height=19, boxwidth=8, boxheight=6, row=5, col=7,
               rows=[1, 2, 2, 3, 7, 9, 13, 17, 17],
               cols=[9, 2, 17, 13, 19, 2, 15, 3, 11], boxcolor=8, dotcolor=1,
               b=2),
  ]
  return {"train": train, "test": test}
