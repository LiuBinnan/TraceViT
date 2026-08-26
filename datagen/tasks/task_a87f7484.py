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


def generate(basicrows=None, basiccols=None, weirdrows=None, weirdcols=None,
             colors=None, weird=None, xpose=None, size=3, height=None,
             width=None, num_colors=None, density=None, change_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    basicrows: a list of vertical coordinates for the basic shape
    basiccols: a list of horizontal coordinates for the basic shape
    weirdrows: a list of vertical coordinates for the weird shape
    weirdcols: a list of horizontal coordinates for the weird shape
    colors: a list of digits representing the colors of the shapes
    weird: a digit representing which color is weird
    xpose: a boolean indicating whether the shapes are transposed
    size: the width and height of the (square) tile
    height: the height (rows) of each tile; defaults to size
    width: the width (cols) of each tile; defaults to size
    num_colors: number of stacked color tiles to sample
    density: number of foreground pixels in the odd tile
    change_count: number of add/remove attempts used to form the common tile
  """
  if height is None: height = size
  if width is None: width = size
  if basicrows is None:
    max_colors = max(3, min(30 // height, 9))
    if num_colors is None:
      num_colors = common.randint(3, max_colors)
    num_colors = max(3, min(num_colors, max_colors))
    colors = common.random_colors(num_colors)
    area = width * height
    pixels = common.all_pixels(width, height)
    if density is None:
      half_count = common.randint(0, area // 2)
      density = common.choice([half_count, area - half_count])
    density = max(1, min(density, area - 1))
    if change_count is None:
      change_count = area - common.randint(0, area - 1)
    change_count = max(1, min(change_count, area))
    weirdpixels = set(common.sample(pixels, density))
    basicpixels = set(weirdpixels)
    can_remove = set(weirdpixels)
    can_add = set(pixels) - weirdpixels
    for _ in range(change_count):
      if common.choice([True, False]):
        if len(can_remove) > 1:
          pixel = common.choice(sorted(can_remove))
          basicpixels.remove(pixel)
          can_remove.remove(pixel)
        elif len(can_add) > 1:
          pixel = common.choice(sorted(can_add))
          basicpixels.add(pixel)
          can_add.remove(pixel)
      else:
        if len(can_add) > 1:
          pixel = common.choice(sorted(can_add))
          basicpixels.add(pixel)
          can_add.remove(pixel)
        elif len(can_remove) > 1:
          pixel = common.choice(sorted(can_remove))
          basicpixels.remove(pixel)
          can_remove.remove(pixel)
    if len(basicpixels) == len(weirdpixels):
      extras = sorted(set(pixels) - basicpixels)
      if extras:
        basicpixels.add(common.choice(extras))
      elif len(basicpixels) > 1:
        basicpixels.remove(common.choice(sorted(basicpixels)))
    basicpixels = common.shuffle(list(basicpixels))
    weirdpixels = common.shuffle(list(weirdpixels))
    basicrows = [r for r, _ in basicpixels]
    basiccols = [c for _, c in basicpixels]
    weirdrows = [r for r, _ in weirdpixels]
    weirdcols = [c for _, c in weirdpixels]
    weird = common.randint(0, len(colors) - 1)
    xpose = common.randint(0, 1)

  grid = common.grid(width, height * len(colors))
  output = common.grid(width, height)
  for idx, color in enumerate(colors):
    rows = weirdrows if idx == weird else basicrows
    cols = weirdcols if idx == weird else basiccols
    for r, c in zip(rows, cols):
      grid[height * idx + r][c] = color
  for r, c in zip(weirdrows, weirdcols):
    output[r][c] = colors[weird]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(basicrows=[0, 0, 1, 1, 2, 2], basiccols=[0, 2, 1, 2, 0, 2],
               weirdrows=[0, 0, 0, 1, 1, 2, 2, 2],
               weirdcols=[0, 1, 2, 0, 2, 0, 1, 2], colors=[6, 4, 8], weird=2,
               xpose=0),
      generate(basicrows=[0, 0, 1, 2], basiccols=[0, 1, 2, 2],
               weirdrows=[0, 0, 1, 2, 2], weirdcols=[0, 2, 1, 0, 2],
               colors=[2, 3, 7, 1], weird=2, xpose=1),
      generate(basicrows=[0, 1, 1, 2], basiccols=[0, 1, 2, 1],
               weirdrows=[0, 0, 0, 1, 2, 2, 2], weirdcols=[0, 1, 2, 1, 0, 1, 2],
               colors=[3, 4, 2, 8, 1], weird=1, xpose=1),
      generate(basicrows=[0, 1, 1, 2], basiccols=[0, 1, 2, 0],
               weirdrows=[0, 0, 1, 1, 2, 2], weirdcols=[1, 2, 0, 1, 0, 2],
               colors=[7, 3, 2, 8], weird=0, xpose=0),
  ]
  test = [
      generate(basicrows=[0, 1, 1, 2], basiccols=[1, 0, 2, 1],
               weirdrows=[0, 0, 1, 1, 2, 2], weirdcols=[0, 2, 0, 1, 0, 2],
               colors=[5, 3, 6, 4, 8], weird=2, xpose=0),
  ]
  return {"train": train, "test": test}
