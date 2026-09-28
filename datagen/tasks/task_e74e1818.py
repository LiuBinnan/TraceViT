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

  def draw():
    """Builds the input grid, plus the row height of each of its shapes.

    The grid is a stack of shapes: each shape is a maximal run of consecutive
    rows painted in one color, and the shapes tile every row but the first and
    the last. The sampling section calls this to rebuild the grid it just
    flattened (and ignores the shape heights).
    """
    grid = common.grid(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
    last, length, lengths = -1, 1, []
    for row in range(1, height - 1):
      subset = list(set(grid[row]))
      if 0 in subset: subset.remove(0)
      if subset[0] == last:
        length += 1
      else:
        if last != -1: lengths.append(length)
        last, length = subset[0], 1
    lengths.append(length)
    return grid, lengths

  if width is None:
    width = height = 2 * common.randint(3, 14) + 1
    while True:
      while True:
        color_count = common.randint(3, height // 2)
        # random_colors draws distinct values from the nine nonzero ARC colors.
        if color_count > 9: continue
        colors = common.random_colors(color_count)
        # The loop below draws len(colors) shape heights in [1, len(colors)] and
        # needs them to sum to height - 2; unless that total lies between
        # len(colors) and len(colors) ** 2 it is unreachable, so redraw the
        # colors until the shapes can tile the grid.
        if len(colors) <= height - 2 <= len(colors) ** 2: break
      for _ in range(500):
        lengths = [common.randint(1, len(colors)) for _ in colors]
        if sum(lengths) + 2 == height: break
      else:
        continue
      offset = 1
      grid = common.grid(width, height)
      failed = False
      for i, color in enumerate(colors):
        # max() keeps the range legal for width 7, where width // 2 - 3 is 0
        # and randint(1, 0) raised ValueError.
        spacing = common.randint(1, max(1, width // 2 - 3))
        for _ in range(500):
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
          if good and pixels: break
        else:
          failed = True
          break
        for r in range(lengths[i]):
          for c in range(1, width - 1):
            grid[offset + r][c] = sprite[r][c]
        offset += lengths[i]
      if failed: continue
      colors = common.flatten(grid)
      grid, _ = draw()
      sampled_shapes, row = [], 1
      for length in lengths:
        if grid[row:row + length] != grid[row:row + length][::-1]:
          sampled_shapes.append((row, length))
        row += length
      if not sampled_shapes: continue
      break

  grid, lengths = draw()

  # Bookkeeping: the top row and the height of every shape a flip would visibly
  # change. A one-row shape, or one already symmetric about its middle row, is
  # its own mirror image and thus needs no move. At most one shape per color, so
  # at most height // 2 of them.
  shapes, row = [], 1
  for length in lengths:
    if grid[row:row + length] != grid[row:row + length][::-1]:
      shapes.append((row, length))
    row += length
  output = common.deepcopy(grid)

  def flip_shape(i):
    """Turns shape #i upside down, inside the band of rows it occupies."""
    if i >= len(shapes): return
    top, size = shapes[i]
    for r in range(size):
      output[top + r] = list(grid[top + size - 1 - r])

  flip_shape(0)
  flip_shape(1)
  flip_shape(2)
  flip_shape(3)
  flip_shape(4)
  flip_shape(5)
  flip_shape(6)
  for i in range(7, len(shapes)):
    flip_shape(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0,
                       0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0,
                       0, 0, 0, 5, 0, 5, 0, 5, 0, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=13, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 4, 0, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=7, height=7,
               colors=[0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 9, 9, 0, 0,
                       0, 9, 0, 9, 0, 9, 0,
                       0, 0, 4, 4, 4, 0, 0,
                       0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=15, height=15,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0,
                       0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 0, 0, 0,
                       0, 0, 0, 0, 4, 0, 4, 0, 4, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 8, 0, 8, 8, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
