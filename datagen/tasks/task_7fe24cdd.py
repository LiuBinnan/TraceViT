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


def generate(rows=None, cols=None, idxs=None, colors=None, size=3,
             num_colors=None, num_pixels=None, height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the color list
    colors: a list of colors to be used
    size: the width and height of the (square) input grid
    num_colors: number of foreground colors in randomized examples
    num_pixels: number of colored cells in randomized examples
    height: randomized input height
    width: randomized input width
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    area = height * width
    if num_colors is None:
      num_colors = common.randint(0, min(9, area))
    num_colors = max(0, min(num_colors, 9, area))
    colors = common.random_colors(num_colors)
    pixels, idxs = [], []
    available = common.all_pixels(width, height)
    if num_colors > 0:
      if num_pixels is None:
        for idx in range(num_colors):
          count = common.randint(1, max(1, len(available) // num_colors))
          chosen = common.sample(available, min(count, len(available)))
          pixels.extend(chosen)
          idxs.extend([idx] * len(chosen))
          for pixel in chosen:
            available.remove(pixel)
      else:
        num_pixels = max(num_colors, min(num_pixels, area))
        pixels = common.sample(available, num_pixels)
        idxs = common.shuffle(
            list(range(num_colors)) +
            [common.randint(0, num_colors - 1)
             for _ in range(num_pixels - num_colors)])
    rows, cols = zip(*pixels) if pixels else ([], [])

  band = min(height, width)
  grid = common.grid(width, height)
  output = common.grid(width + height, 2 * band)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = colors[idx]
    if r < band:
      output[r][c] = colors[idx]
  for r, c, idx in zip(rows, cols, idxs):
    if width - c - 1 < band:
      output[band + width - c - 1][r] = colors[idx]
  for r, c, idx in zip(rows, cols, idxs):
    if c < band:
      output[c][width + height - r - 1] = colors[idx]
  for r, c, idx in zip(rows, cols, idxs):
    if height - r - 1 < band:
      output[band + height - r - 1][height + width - c - 1] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[0, 1, 0, 1, 2, 1, 2],
               idxs=[0, 1, 0, 1, 2, 2, 3], colors=[8, 5, 3, 2]),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 1, 2],
               idxs=[0, 1, 2, 0, 2, 2, 1, 3, 2], colors=[3, 8, 2, 5]),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], idxs=[0, 1, 1, 1, 0],
               colors=[3, 6]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2], cols=[0, 1, 0, 1, 2, 0, 1, 2],
               idxs=[0, 1, 0, 1, 2, 3, 2, 2], colors=[2, 5, 1, 3]),
  ]
  return {"train": train, "test": test}
