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


def generate(steps=None, rows=None, cols=None, flip=None, width=3, height=6,
             extended=9, num_pixels=None, input_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    steps: the step size used for the stencil pattern
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flip: whether to perdiodically flip the pattern left-to-right 
    width: the width of the grid
    height: the height of the grid
    extended: the height of the extended output grid
    num_pixels: the number of pixels in one repeated stencil period
    input_color: the color used for the input pattern
  """
  if steps is None:
    height = common.randint(3, 10) * 2
    width = common.randint(2, 30)
    extended = height + height // 2
    steps = common.randint(1, max(1, height * 2 // 3))
    area = width * steps
    if num_pixels is None:
      sparse_pixels = common.randint(0, area // 2)
      num_pixels = sparse_pixels if common.randint(0, 1) == 0 else area - sparse_pixels
    num_pixels = min(max(1, num_pixels), area)
    pixels = common.all_pixels(width, steps)
    pixels = common.sample(pixels, num_pixels)
    rows, cols = zip(*pixels)
    flip = 0
    if input_color is None:
      input_color = common.random_color(exclude=[common.red()])
  if input_color is None:
    input_color = common.blue()

  grid = common.grid(width, height)
  flipped = 0
  for offset in range(0, height, steps):
    for row, col in zip(rows, cols):
      r = offset + row
      c = col if flipped == 0 else width - col - 1
      if r < height:
        grid[r][c] = input_color
    flipped = flipped if flip == 0 else 1 - flipped
  output = common.grid(width, extended)

  def recolor_visible_pattern():
    flipped = 0
    for offset in range(0, height, steps):
      for row, col in zip(rows, cols):
        r = offset + row
        c = col if flipped == 0 else width - col - 1
        if r < height:
          output[r][c] = common.red()
      flipped = flipped if flip == 0 else 1 - flipped

  def extend_recolored_pattern():
    flipped = 0
    for offset in range(0, extended, steps):
      for row, col in zip(rows, cols):
        r = offset + row
        c = col if flipped == 0 else width - col - 1
        if height <= r < extended:
          output[r][c] = common.red()
      flipped = flipped if flip == 0 else 1 - flipped

  recolor_visible_pattern()
  extend_recolored_pattern()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(steps=2, rows=[0, 1, 1], cols=[1, 0, 1], flip=1),
      generate(steps=2, rows=[0, 1, 1], cols=[1, 0, 2], flip=0),
      generate(steps=3, rows=[0, 1, 1, 2], cols=[1, 0, 1, 1], flip=0),
  ]
  test = [
      generate(steps=3, rows=[0, 0, 0, 1, 2], cols=[0, 1, 2, 1, 1], flip=0),
  ]
  return {"train": train, "test": test}
