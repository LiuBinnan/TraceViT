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
             height=None, width=None, num_colors=None, num_pixels=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: digits representing indices into the colors list
    colors: digits representing the colors to be used
    size: the width and height of the (square) input grid
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
    num_colors: how many distinct colors to scatter (defaults to random)
    num_pixels: how many pixels to place (defaults to random, area-scaled)
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    cells = width * height
    if num_colors is None:
      num_colors = common.randint(1, min(9, cells))
    num_colors = min(9, num_colors)
    if num_pixels is None:
      num_pixels = common.randint(num_colors, cells)
    pixels = common.all_pixels(width, height)
    pixels = common.sample(pixels, num_pixels)
    rows, cols = zip(*pixels)
    colors = common.random_colors(num_colors)
    idxs = list(range(num_colors)) + [
        common.randint(0, num_colors - 1)
        for _ in range(num_pixels - num_colors)]

  grid = common.grid(width, height)
  output = common.grid(width * 3, height * 3)
  pixels = list(zip(rows, cols, idxs))
  for row, col, idx in pixels:
    grid[row][col] = colors[idx]
  color_indices = sorted(set(idxs))

  def reveal_color(color_idx):
    if color_idx >= len(color_indices):
      return
    target_idx = color_indices[color_idx]
    for row, col, idx in pixels:
      if idx != target_idx:
        continue
      for dr in range(3):
        for dc in range(3):
          output[row * 3 + dr][col * 3 + dc] = colors[idx]

  reveal_color(0)
  reveal_color(1)
  reveal_color(2)
  reveal_color(3)
  reveal_color(4)
  reveal_color(5)
  reveal_color(6)
  reveal_color(7)
  reveal_color(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 1, 0, 1, 2], idxs=[0, 0, 1, 2, 2],
               colors=[3, 7, 4]),
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 1, 2, 2], idxs=[0, 1, 1, 1, 0],
               colors=[3, 2]),
  ]
  test = [
      generate(rows=[0, 1, 2, 2], cols=[1, 2, 0, 1], idxs=[0, 1, 1, 0],
               colors=[1, 6]),
  ]
  return {"train": train, "test": test}
