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


def generate(width=None, height=None, offset=None, xpose=None, pattern=None,
             gsize=None, drow=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the pattern.
    height: The height of the pattern.
    offset: The offset of the pattern.
    xpose: Whether to transpose the pattern.
    pattern: The pattern to use for the generator.
    gsize: The width and height of the square canvas.
    drow: The row of the empty divider band before transposition.
  """

  def draw():
    grid, output = common.grids(gsize, gsize)
    for i, color in enumerate(pattern):
      row, col = offset + i // width, offset + i % width
      output[row][col] = grid[row][col] = int(color)
    for col in range(gsize):
      grid[drow][col], output[drow][col] = 0, 3
    # Make sure there isn't also a vertical line of empty space.
    for col in range(width):
      good = False
      for row in range(height):
        if grid[row + offset][col + offset]: good = True
      if not good: return None, None
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if width is None:
    if gsize is None:
      gsize = common.randint(9, 16)
    if drow is None:
      drow = common.randint(2, gsize - 3)
    max_height = max(6, gsize - 4)
    width, height = common.randint(4, 7), common.randint(5, max_height)
    offset = common.randint(1, 2)
    # Keep the divider strictly inside the sprite so its location is unique.
    offset = max(offset, drow + 2 - max_height)
    if offset >= drow:
      offset = drow - 1
    height = max(height, drow - offset + 2)
    color = common.random_color(exclude=[3])
    if xpose is None:
      xpose = common.randint(0, 1)
    likelihood = common.randint(1, 3)
    while True:
      sprite = common.grid(width, height)
      pixels, rows, cols = [], [], []
      for row in range(height):
        for col in range(width):
          if common.randint(0, likelihood): continue
          sprite[row][width - 1 - col] = sprite[row][col] = color
          rows, cols = rows + [row], cols + [col]
      if 0 not in rows or 0 not in cols: continue
      if height - 1 not in rows or width - 1 not in cols: continue
      for row in range(height):
        for col in range(width):
          if sprite[row][col]: pixels.append((row, col))
      if not common.connected(pixels): continue
      pattern = ""
      for row in range(height):
        for col in range(width):
          pattern += str(sprite[row][col])
      grid, _ = draw()
      if grid: break
  else:
    if gsize is None:
      gsize = 10
    if drow is None:
      drow = 4

  grid, _ = draw()
  output = common.deepcopy(grid)

  def draw_divider():
    """Fills the empty band cutting through the sprite with a green line."""
    if xpose:
      for row in range(gsize):
        output[row][drow] = common.green()
    else:
      for col in range(gsize):
        output[drow][col] = common.green()

  draw_divider()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=5, offset=1, xpose=1,
               pattern="555555050550505505055050555555"),
      generate(width=7, height=6, offset=1, xpose=0,
               pattern="001110001101101100011000000001101100011100"),
      generate(width=4, height=5, offset=2, xpose=0,
               pattern="22222002000020022222"),
  ]
  test = [
      generate(width=4, height=5, offset=2, xpose=1,
               pattern="06606666000066660660"),
      generate(width=4, height=5, offset=1, xpose=0,
               pattern="22222222222200002222"),
  ]
  return {"train": train, "test": test}
