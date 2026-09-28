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


def generate(width=None, height=None, bgcolor=None, brows=None, bcols=None,
             colors=None, pattern=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    pattern: The pattern of the composition.
    gsize: The side length of the square input grid.
  """

  def draw():
    if "0" not in pattern: return None, None  # Ensure some background exposed.
    # Ensure that all components are connected.
    for color in colors:
      pixels = []
      for row in range(height):
        for col in range(width):
          if int(pattern[row * width + col]) == color: pixels.append((row, col))
      if not common.connected(pixels): return None, None
    # Ensure that the whole thing is connected.
    pixels = []
    for row in range(height):
      for col in range(width):
        if int(pattern[row * width + col]): pixels.append((row, col))
    if not common.connected(pixels): return None, None
    canvas_size = gsize if gsize is not None else 16
    grid, output = common.grid(canvas_size, canvas_size, bgcolor), common.grid(
        width, height)
    for brow, bcol, color in zip(brows, bcols, colors):
      common.rect(grid, width, height, brow, bcol, 0)
      for row in range(height):
        for col in range(width):
          if int(pattern[row * width + col]) == color:
            grid[brow + row][bcol + col] = color
      for row in range(height):
        for col in range(width):
          output[row][col] = int(pattern[row * width + col])
    return grid, output

  def paint_component(canvas, color):
    if color is None:
      return
    for row in range(height):
      for col in range(width):
        if int(pattern[row * width + col]) == color:
          canvas[row][col] = color

  if width is None:
    if gsize is None:
      gsize = common.randint(14, 24)
    # Jointly sample a pattern and color count that can be packed on the chosen
    # canvas.  The original extreme-shape exclusion is extended from 3..5 to
    # 3..6: exclude only 3x3 and 6x6.
    for _ in range(100):
      width, height = common.randint(3, 6), common.randint(3, 6)
      if max(width, height) == 3 or min(width, height) == 6:
        continue
      bgcolor = common.random_color()
      colors = common.random_colors(common.randint(2, 4), exclude=[bgcolor])
      row_slots = list(range(1, gsize - height, height + 2))
      col_slots = list(range(1, gsize - width, width + 2))
      if len(row_slots) * len(col_slots) >= len(colors):
        break
    else:
      # 3x4 always admits four mutually separated boxes at the minimum gsize.
      width, height = 3, 4
      bgcolor = common.random_color()
      colors = common.random_colors(common.randint(2, 4), exclude=[bgcolor])
      row_slots = list(range(1, gsize - height, height + 2))
      col_slots = list(range(1, gsize - width, width + 2))

    for _ in range(128):
      brows = [common.randint(1, gsize - 1 - height) for _ in colors]
      bcols = [common.randint(1, gsize - 1 - width) for _ in colors]
      if not common.overlaps(brows, bcols, [width] * len(colors),
                             [height] * len(colors), 2):
        break
    else:
      slots = common.shuffle([(row, col) for row in row_slots
                              for col in col_slots])
      selected = slots[:len(colors)]
      brows = [row for row, _ in selected]
      bcols = [col for _, col in selected]

    for _ in range(256):  # Keep going until the problem is legal.
      grid = common.grid(width, height)
      subset = set()
      for _ in range(128):  # Keep going until all colors are used.
        color = common.choice(colors)
        if common.randint(0, 1):
          length = common.randint(2, width)
          pos = common.randint(0, width - length)
          val = common.randint(0, height - 1)
          for c in range(pos, pos + length):
            grid[val][c] = color
        else:
          length = common.randint(2, height)
          pos = common.randint(0, height - length)
          val = common.randint(0, width - 1)
          for r in range(pos, pos + length):
            grid[r][val] = color
        subset = set(common.flatten(grid))
        if 0 in subset: subset.remove(0)
        if len(subset) == len(colors) and common.randint(0, 1): break
      if len(subset) != len(colors):
        continue
      pattern = "".join(map(str, common.flatten(grid)))
      grid, _ = draw()
      if grid: break
    else:
      # Guaranteed legal fallback: partition a prefix of a 4-connected snake
      # into one contiguous segment per color, leaving at least one zero cell.
      path = []
      if common.randint(0, 1):
        for row in range(height):
          cols = range(width) if row % 2 == 0 else range(width - 1, -1, -1)
          path.extend((row, col) for col in cols)
      else:
        for col in range(width):
          rows = range(height) if col % 2 == 0 else range(height - 1, -1, -1)
          path.extend((row, col) for row in rows)
      if common.randint(0, 1):
        path = path[::-1]
      total = common.randint(2 * len(colors), width * height - 1)
      grid = common.grid(width, height)
      cursor, remaining = 0, total
      for i, color in enumerate(common.shuffle(colors)):
        colors_left = len(colors) - i - 1
        length = (remaining if colors_left == 0 else
                  common.randint(2, remaining - 2 * colors_left))
        for row, col in path[cursor:cursor + length]:
          grid[row][col] = color
        cursor += length
        remaining -= length
      pattern = "".join(map(str, common.flatten(grid)))
      grid, _ = draw()

  grid, output = draw()
  if grid is None:
    return {"input": grid, "output": output}
  output = common.grid(width, height)
  paint_component(output, colors[0])
  paint_component(output, colors[1])
  paint_component(output, colors[2] if len(colors) > 2 else None)
  paint_component(output, colors[3] if len(colors) > 3 else None)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, bgcolor=8, brows=[1, 2, 8, 12],
               bcols=[1, 9, 3, 9], colors=[1, 3, 2, 4], pattern="003311240224"),
      generate(width=4, height=4, bgcolor=1, brows=[1, 2, 10], bcols=[1, 10, 5],
               colors=[2, 3, 4], pattern="4444330033000220"),
      generate(width=5, height=4, bgcolor=9, brows=[1, 8, 2, 6], bcols=[2, 6],
               colors=[1, 2], pattern="01000112200112000020"),
  ]
  test = [
      generate(width=3, height=5, bgcolor=1, brows=[1, 1, 8, 9],
               bcols=[1, 8, 3, 11], colors=[2, 3, 4, 6],
               pattern="023223444640660"),
  ]
  return {"train": train, "test": test}
