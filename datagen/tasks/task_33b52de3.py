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


def generate(width=None, height=None, brow=None, bcol=None, srow=None,
             scol=None, shape=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the color grid.
    height: The height of the color grid.
    brow: The row where the boxes start.
    bcol: The column where the boxes start.
    srow: The row where the colorful sprite starts.
    scol: The column where the colorful sprite starts.
    shape: The shape of the sprite.
    colors: The colors of the boxes.
    gsize: The side length of the square canvas.
  """

  if width is None:
    canvas_size = 23 if gsize is None else gsize
    if canvas_size < 20:
      raise ValueError("gsize must be at least 20")
    shape = [1] * 9
    shape[common.randint(0, 8)] = shape[common.randint(0, 8)] = 0
    while True:
      width, height = common.randint(3, 5), common.randint(3, 5)
      if width + height >= 10: continue
      if canvas_size < 4 * max(width, height) + 2: continue
      if canvas_size < 5 * min(width, height) + 2: continue
      break
    subset = common.sample([1, 2, 3, 4, 8], common.randint(3, 5))
    colors = common.choices(subset, width * height)
    while True:
      brow = common.randint(1, canvas_size - 4 * height)
      bcol = common.randint(1, canvas_size - 4 * width)
      srow = common.randint(1, canvas_size - height - 1)
      scol = common.randint(1, canvas_size - width - 1)
      if srow + height < brow or scol + width < bcol: break
      if brow + 4 * height < srow or bcol + 4 * width < scol: break

  grid = common.grid(23 if gsize is None else gsize,
                     23 if gsize is None else gsize)
  for row in range(height):
    for col in range(width):
      grid[srow + row][scol + col] = colors[row * width + col]
      for r in range(3):
        for c in range(3):
          if not shape[r * 3 + c]: continue
          grid[brow + row * 4 + r][bcol + col * 4 + c] = common.gray()
  output = common.deepcopy(grid)

  def recolor_box_row(row):
    if row >= height: return
    for col in range(width):
      color = colors[row * width + col]
      for r in range(3):
        for c in range(3):
          if not shape[r * 3 + c]: continue
          output[brow + row * 4 + r][bcol + col * 4 + c] = color

  recolor_box_row(0)
  recolor_box_row(1)
  recolor_box_row(2)
  recolor_box_row(3)
  recolor_box_row(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=4, brow=1, bcol=6, srow=3, scol=1,
               shape=[1, 1, 1, 0, 1, 0, 1, 1, 1],
               colors=[1, 8, 1, 8, 8, 8, 1, 1, 1, 1, 4, 1, 1, 1, 4, 4]),
      generate(width=5, height=3, brow=1, bcol=2, srow=19, scol=1,
               shape=[1, 1, 1, 1, 0, 1, 1, 1, 1],
               colors=[2, 1, 1, 3, 1, 1, 2, 2, 1, 1, 2, 1, 2, 3, 2]),
  ]
  test = [
      generate(width=4, height=5, brow=1, bcol=7, srow=2, scol=1,
               shape=[1, 1, 1, 1, 0, 1, 1, 0, 1],
               colors=[2, 1, 2, 2, 8, 1, 4, 4, 3, 1, 4, 4, 8, 1, 3, 1, 8, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
