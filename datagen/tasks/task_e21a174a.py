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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
  """

  def bands(g):
    """Returns the heights of the stacked one-color bands, top to bottom."""
    last, length, lengths = -1, 1, []
    for row in range(1, height - 1):
      subset = list(set(g[row]))
      if 0 in subset: subset.remove(0)
      if subset[0] == last:
        length += 1
      else:
        if last != -1: lengths.append(length)
        last, length = subset[0], 1
    lengths.append(length)
    return lengths

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
    inrow, outrow = 1, height - 1
    for length in bands(grid):
      outrow -= length
      for _ in range(length):
        output[outrow] = grid[inrow]
        inrow, outrow = inrow + 1, outrow + 1
      outrow -= length
    # Check that the input and output grids are connected.
    for g in [grid, output]:
      pixels = []
      for r in range(height):
        for c in range(width):
          if g[r][c]: pixels.append((r, c))
      if not common.diagonally_connected(pixels): return None, None
    return grid, output

  if width is None:
    width, height = common.randint(7, 16), common.randint(7, 16)
    colors = common.random_colors(height // 3 + 1)
    while True:
      lengths = [common.randint(1, len(colors)) for _ in colors]
      if sum(lengths) + 2 == height: break
    band_colors = colors  # The resample loop below overwrites `colors`.
    while True:
      offset = 1
      grid = common.grid(width, height)
      for i, color in enumerate(band_colors):
        spacing = common.randint(1, max(1, width // 2 - 3))
        while True:
          sprite = common.grid(width, lengths[i])
          for r in range(lengths[i]):
            for c in range(spacing, width - spacing):
              if common.randint(0, 3): continue
              sprite[r][c] = sprite[r][width - 1 - c] = color
          good, pixels = True, []
          for r in range(lengths[i]):
            covered = False
            for c in range(1, width - 1):
              if not sprite[r][c]: continue
              covered = True
              pixels.append((r, c))
            if not covered: good = False
          if good and pixels and common.diagonally_connected(pixels): break
        for r in range(lengths[i]):
          for c in range(1, width - 1):
            grid[offset + r][c] = sprite[r][c]
        offset += lengths[i]
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()

  # Solve the puzzle forward on a copy of the input: the input is a pile of
  # one-color bands and the answer is the same pile stacked in reverse order,
  # so lift the lowest band that has not moved yet onto the answer pile (which
  # grows downward from the top row) and let the bands still waiting slide down
  # to stay packed underneath it.  Every band is visible in every frame; after
  # the last lift the pile is fully reversed.  Random generation yields
  # height // 3 + 1 <= 6 bands (height <= 16) and the hardcoded validate()
  # examples have 3 to 5, so we unroll to 5 (extra calls are no-ops) and use a
  # catch-all for any additional randomly generated bands.
  lengths = bands(grid)
  tops = [1 + sum(lengths[:i]) for i in range(len(lengths))]
  output = common.deepcopy(grid)

  def restack(k):
    """Lifts band `len(lengths) - 1 - k` (counting from the bottom of the
    input pile) onto the answer pile, sliding the bands that are still waiting
    down by that band's height so that they stay packed below the answer."""
    if k >= len(lengths): return
    moved, row = len(lengths) - 1 - k, 1
    for i in range(len(lengths) - 1, moved - 1, -1):  # Bands already restacked.
      for r in range(lengths[i]):
        output[row] = list(grid[tops[i] + r])
        row += 1
    for i in range(moved):  # Bands still waiting their turn, in input order.
      for r in range(lengths[i]):
        output[row] = list(grid[tops[i] + r])
        row += 1

  restack(0)
  restack(1)
  restack(2)
  restack(3)
  restack(4)
  for k in range(5, len(lengths)):
    restack(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7,
               colors=[0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 1, 1, 0,
                       0, 0, 2, 2, 2, 0, 0,
                       0, 0, 2, 2, 2, 0, 0,
                       0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0]),
      generate(width=13, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                       0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
                       0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=13, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=10, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 3, 0, 3, 3, 0, 3, 0, 0,
                       0, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                       0, 0, 4, 4, 4, 4, 4, 4, 0, 0,
                       0, 0, 0, 8, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 0, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 6, 6, 6, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=7, height=7,
               colors=[0, 0, 0, 0, 0, 0, 0,
                       0, 4, 4, 4, 4, 4, 0,
                       0, 4, 0, 4, 0, 4, 0,
                       0, 0, 5, 5, 5, 0, 0,
                       0, 6, 0, 6, 0, 6, 0,
                       0, 0, 6, 0, 6, 0, 0,
                       0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
