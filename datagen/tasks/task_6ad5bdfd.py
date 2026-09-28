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


def generate(width=None, height=None, brows=None, bcols=None, cdirs=None,
             colors=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    cdirs: The directions of the boxes.
    colors: The colors of the boxes.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  def cells(idx, row):
    """The two cells box idx covers with its head at (row, bcols[idx])."""
    cdir, col = cdirs[idx], bcols[idx]
    return [(row, col), ((row + 1) if cdir else row, col if cdir else (col + 1))]

  def settle():
    """Where each box comes to rest, and which layer of the stack it lands in.

    A box rises toward the wall until the wall or an already-risen box stops
    it, so the boxes must be settled nearest to the wall first -- the order in
    which every original example lists them. Settling a distant box first lets
    it rise through a nearer box that is not in place yet, which is a result no
    solver could read off the input.
    """
    output = common.grid(width, height)
    for c in range(width):
      output[0][c] = 2
    rests, layers, owner = [0] * len(brows), [0] * len(brows), {}
    for idx in sorted(range(len(brows)), key=lambda box: brows[box]):
      row, col, cdir = brows[idx], bcols[idx], cdirs[idx]
      while True:
        if cdir == 1 and output[row - 1][col]: break
        if cdir == 0 and output[row - 1][col] + output[row - 1][col + 1]: break
        row -= 1
      rests[idx] = row
      box = cells(idx, row)
      above = [(r - 1, c) for r, c in box if (r - 1, c) not in box]
      # A box either reaches the wall (layer 0) or rests on the boxes above it.
      layers[idx] = 0 if row == 1 else 1 + max(
          layers[owner[cell]] for cell in above if cell in owner)
      for r, c in box:
        output[r][c], owner[(r, c)] = colors[idx], idx
    return rests, layers

  def draw():
    """The boxes where they start, and the stack they settle into."""
    grid, output = common.grids(width, height)
    for c in range(width):
      output[0][c] = grid[0][c] = 2
    rests, _ = settle()
    for idx in range(len(brows)):
      for row, col in cells(idx, brows[idx]):
        grid[row][col] = colors[idx]
      for row, col in cells(idx, rests[idx]):
        output[row][col] = colors[idx]
    return grid, output

  if width is None:
    width, height = common.randint(5, 10), common.randint(9, 13)
    num_boxes = (width * height - 1) // 10 + 1
    cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
    colors = [common.random_color(exclude=[2]) for _ in range(num_boxes)]
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    while True:
      wides = [2 - cdir for cdir in cdirs]
      talls = [1 + cdir for cdir in cdirs]
      brows = [common.randint(1, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls): continue
      if common.some_abutted(brows, bcols, wides, talls): continue
      # Corners can touch, but only if colors are distinct.
      grid, _ = draw()
      good = True
      for row in range(1, height - 1):
        for col in range(1, width - 1):
          if grid[row][col] == 0: continue
          for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if grid[row + dr][col + dc] == grid[row][col]: good = False
      if good: break

  grid, _ = draw()
  if flip: grid = common.flip(grid)
  if xpose: grid = common.transpose(grid)
  rests, layers = settle()
  output = common.deepcopy(grid)

  def put(row, col, color):
    """Writes a canonical cell, in the orientation the grids are returned in."""
    if flip: row = height - 1 - row
    if xpose: row, col = col, row
    output[row][col] = color

  def rise(layer):
    """Slides every box of stacking layer `layer` up to its resting place.

    Layer 0 is the boxes that reach the wall itself; layer k rests on layer
    k - 1. Boxes of the later layers stay where they started, so each frame
    shows a partly settled stack. A layer can hold at most one box per row of
    the stack, so nine layers is the most that fit under the wall.
    """
    for idx in sorted(range(len(brows)), key=lambda box: brows[box]):
      if layers[idx] != layer: continue
      for row, col in cells(idx, brows[idx]):
        put(row, col, common.black())
      for row, col in cells(idx, rests[idx]):
        put(row, col, colors[idx])

  rise(0)
  rise(1)
  rise(2)
  rise(3)
  rise(4)
  rise(5)
  rise(6)
  rise(7)
  rise(8)
  rise(9)
  for layer in range(10, height):
    rise(layer)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=11, brows=[2, 3, 5, 7, 7, 8], bcols=[4, 0, 1, 0, 3, 2], cdirs=[1, 1, 0, 1, 0, 1], colors=[7, 3, 5, 4, 8, 6], flip=False, xpose=True),
      generate(width=6, height=10, brows=[3, 5, 5, 7, 7, 9], bcols=[2, 0, 5, 0, 3, 4], cdirs=[0, 0, 1, 1, 1, 0], colors=[5, 1, 6, 3, 4, 8], flip=True, xpose=False),
      generate(width=5, height=10, brows=[2, 4, 5, 7, 8], bcols=[1, 3, 1, 0, 3], cdirs=[0, 1, 1, 1, 0], colors=[6, 8, 5, 4, 9], flip=True, xpose=True),
  ]
  test = [
      generate(width=10, height=10, brows=[1, 1, 2, 3, 4, 5, 6, 6, 8, 8, 9], bcols=[2, 7, 5, 1, 8, 4, 2, 8, 0, 5, 7], cdirs=[0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0], colors=[3, 6, 7, 8, 6, 3, 9, 4, 3, 1, 5], flip=False, xpose=False),
  ]
  return {"train": train, "test": test}
