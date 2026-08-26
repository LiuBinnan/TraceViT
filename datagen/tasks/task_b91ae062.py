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
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: digits representing indices into the colors list
    colors: digits representing the colors to be used
    size: the width and height of the (square) input grid
    height: the height (row extent) of the input grid; defaults to size
    width: the width (column extent) of the input grid; defaults to size
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if rows is None:
    pixels = common.all_pixels(width, height)
    # Cap the pixel count by the available population so rectangular grids
    # smaller than 5 cells cannot make common.sample raise.
    pixels = common.sample(pixels, common.randint(3, min(5, len(pixels))))
    rows, cols = zip(*pixels)
    colors = common.random_colors(common.randint(1, len(pixels)))
    idxs = list(range(len(colors)))  # Make sure we have one of each color
    while len(idxs) < len(pixels):
      idxs.append(common.randint(0, len(colors) - 1))
    common.shuffle(idxs)

  # Inlined rectangular form of common.grid_enhance (which only does squares):
  # height is the row extent, width is the column extent. common.grid is
  # cols-first/rows-second, so the input is grid(width, height) and the output
  # is upsampled by the enhance factor (len(colors)) on both axes.
  enhance = len(colors)
  grid = common.grid(width, height, common.black())
  output = common.grid(width * enhance, height * enhance, common.black())
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = colors[idx]
    for dr in range(enhance):
      for dc in range(enhance):
        output[r * enhance + dr][c * enhance + dc] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2], idxs=[0, 1, 0, 0],
               colors=[6, 7]),
      generate(rows=[0, 0, 1, 2], cols=[0, 2, 1, 1], idxs=[0, 1, 1, 0],
               colors=[1, 4]),
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2], idxs=[0, 1, 2, 0],
               colors=[3, 2, 7]),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 1, 2, 0, 1], idxs=[0, 1, 1, 2, 0],
               colors=[8, 6, 9]),
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 1, 2], idxs=[0, 1, 2, 2, 3],
               colors=[4, 3, 2, 8]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 1, 2, 0, 1], idxs=[0, 1, 2, 3, 3],
               colors=[1, 8, 7, 9]),
  ]
  return {"train": train, "test": test}
