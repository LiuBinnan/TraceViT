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


def generate(size=None, height=None, width=None, rows=None, cols=None,
             idxs=None, colors=(1, 2, 3, 5, 6, 7, 8, 9, 4)):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: digits representing colors to be used
    colors: an ordered list of colors to sample from
  """
  if size is None:
    if height is None: height = common.randint(2, 8)
    if width is None: width = common.randint(2, 8)
    while True:
      pixels = common.random_pixels(width, height)
      if pixels: break
    rows, cols = zip(*pixels)
    # num_colors is a count derived from the grid extent that indexes into the
    # fixed-length `colors` tuple; cap it so a widened dim cannot overrun.
    num_colors = min(len(colors), max(height, width) + 1)
    idxs = [common.randint(0, num_colors - 1) for _ in pixels]
  else:
    height = width = size

  enhance = 2
  b = common.black()
  ingrid = common.grid(width, height, b)
  output = common.grid(width * enhance, height * enhance, b)
  for r, c, idx in zip(rows, cols, idxs):
    ingrid[r][c] = colors[idx]
    for dr in range(enhance):
      for dc in range(enhance):
        output[r * enhance + dr][c * enhance + dc] = colors[idx]
  return {"input": ingrid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[0, 0, 1, 1, 1, 2, 2], cols=[1, 2, 0, 1, 2, 0, 1],
               idxs=[3, 0, 3, 3, 3, 1, 3]),
      generate(size=2, rows=[0, 0, 1, 1], cols=[0, 1, 0, 1],
               idxs=[1, 0, 2, 0]),
      generate(size=4, rows=[0, 0, 1, 1, 1, 2, 2, 3, 3],
               cols=[0, 2, 0, 1, 2, 2, 3, 2, 3],
               idxs=[1, 2, 1, 0, 2, 2, 2, 2, 3]),
  ]
  test = [
      generate(size=5, rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
               cols=[0, 3, 4, 0, 1, 2, 1, 2, 3, 0, 1, 2, 1],
               idxs=[1, 5, 6, 1, 0, 0, 3, 4, 4, 2, 3, 4, 3]),
  ]
  return {"train": train, "test": test}
