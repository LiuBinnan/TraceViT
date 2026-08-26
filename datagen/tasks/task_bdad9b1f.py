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


def generate(row=None, col=None, flip=None, size=6, height=None, width=None,
             numh=None, numw=None, numcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where a horizontal street should be placed
    col: a horizontal coordinate where a vertical street should be placed
    flip: whether to flip the grid horizontally
    size: the size of the grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    numh: number of horizontal streets (defaults to an area-scaled random count)
    numw: number of vertical streets (defaults to an area-scaled random count)
    numcols: size of the street color palette (defaults to a random count)
  """
  if height is None: height = size
  if width is None: width = size
  if row is None:
    numh = numh if numh is not None else common.randint(1, max(1, height // 2 - 1))
    numw = numw if numw is not None else common.randint(1, max(1, width // 2 - 1))
    numcols = numcols if numcols is not None else common.randint(2, 8)
    hlocs = sorted(common.sample(list(range(2, height - 1)), numh))
    wlocs = sorted(common.sample(list(range(2, width - 1)), numw))
    ccols = common.random_colors(numcols, exclude=[common.yellow()])
    hstreets, fc = [], -1
    for loc in hlocs:
      color = common.sample([c for c in ccols if c != fc], 1)[0]
      fc = color
      hstreets.append((loc, color, common.randint(2, loc)))
    vstreets, fc = [], -1
    for loc in wlocs:
      color = common.sample([c for c in ccols if c != fc], 1)[0]
      fc = color
      vstreets.append((loc, color, common.randint(2, loc)))
    if flip is None: flip = common.randint(0, 1)
  else:
    hstreets = [(row, common.red(), 2)]
    vstreets = [(col, common.cyan(), 2)]

  grid, output = common.grids(width, height)
  for loc, color, stub in hstreets:
    for i in range(width):
      if i < stub: grid[loc][i] = color
      output[loc][i] = color
  for loc, color, stub in vstreets:
    for i in range(height):
      if i < stub: grid[i][loc] = color
      output[i][loc] = color
  for hloc, _, _ in hstreets:
    for wloc, _, _ in vstreets:
      output[hloc][wloc] = common.yellow()
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=4, flip=0),
      generate(row=3, col=4, flip=1),
  ]
  test = [
      generate(row=4, col=3, flip=0),
  ]
  return {"train": train, "test": test}
