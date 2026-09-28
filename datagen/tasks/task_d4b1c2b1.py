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


def generate(colors=None, psize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    psize: The height and width of the source grid.
  """

  if colors is None:
    if psize is None:
      psize = 3
    max_colors = (5 if psize == 3 else
                  min(6, psize * psize - 1, 30 // psize))
    num_colors = common.randint(1, max_colors)
    subset = common.random_colors(num_colors)
    while True:
      colors = common.choices(subset, psize * psize)
      if len(set(colors)) == num_colors: break
  elif psize is None:
    psize = 3

  # Build the square input from the sampled colors.
  grid = common.grid(psize, psize)
  for i, color in enumerate(colors):
    grid[i // psize][i % psize] = color

  # The scale factor is the count of DISTINCT colors; the answer is the grid
  # upsampled by that factor, revealed one stretched row-band at a time.
  factor = len(set(colors))
  output = common.grid(psize * factor, psize * factor)

  def stretch_row(band):
    """Blows source row `band` up into its factor-tall, factor-wide band."""
    for col in range(psize):
      color = grid[band][col]
      for dr in range(factor):
        for dc in range(factor):
          output[band * factor + dr][col * factor + dc] = color

  stretch_row(0)
  stretch_row(1)
  stretch_row(2)
  for band in range(3, psize):
    stretch_row(band)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 7, 8, 7, 7, 8, 8, 4]),
      generate(colors=[8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(colors=[3, 3, 3, 3, 3, 3, 3, 3, 3]),
      generate(colors=[4, 2, 8, 2, 2, 5, 8, 5, 4]),
      generate(colors=[2, 2, 4, 4, 4, 4, 2, 4, 2]),
      generate(colors=[1, 1, 1, 6, 6, 6, 6, 1, 6]),
      generate(colors=[3, 6, 6, 3, 6, 6, 3, 3, 3]),
  ]
  test = [
      generate(colors=[7, 1, 7, 3, 3, 6, 8, 8, 6]),
  ]
  return {"train": train, "test": test}
