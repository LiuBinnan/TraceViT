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


def generate(rows=None, cols=None, size=3, width=None, height=None,
             ncolors=None, density=None):
  """Returns input and output grids according to the given parameters.

  The transformation stacks the input on top of its horizontal mirror
  (output = vconcat(input, hmirror(input))); it preserves whatever colors the
  input carries, so widening the palette/size does not change the rule.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the input (square) grid, used only when the
      explicit rows/cols path (validate) is taken
    width: number of columns of the (randomized) input grid; sampled 1..30 when
      omitted so the output width tail decouples from the height
    height: number of rows of the (randomized) input grid; sampled 1..15 when
      omitted so the mirrored output height 2*height stays <= 30
    ncolors: number of distinct pixel colors (1..min(9, painted cells)); sampled
      when omitted
    density: fraction of input cells that carry a pixel; sampled when omitted
  """
  if rows is None:
    # Decouple the two grid axes (re_arc bands: width in 1..30, height in 1..15
    # so the mirrored output height 2*height stays <= 30) instead of forcing a
    # single square `size`; this widens the distinct output-size tail.
    if width is None:
      width = common.randint(1, 30)
    if height is None:
      height = common.randint(1, 15)
    cells = [(r, c) for r in range(height) for c in range(width)]
    # Density: how many cells carry a (mirrored) pixel, 1..all cells.
    if density is None:
      num_pixels = common.randint(1, len(cells))
    else:
      num_pixels = max(1, min(len(cells), round(density * len(cells))))
    # Number of distinct pixel colors (re_arc numc: 1..min(9, painted cells)).
    if ncolors is None:
      ncolors = common.randint(1, min(9, num_pixels))
    else:
      ncolors = max(1, min(ncolors, 9, num_pixels))
    palette = common.random_colors(ncolors)
    chosen = common.sample(cells, num_pixels)
    grid, output = common.grid(width, height), common.grid(width, 2 * height)
    for i, (r, c) in enumerate(chosen):
      color = palette[i % ncolors]
      output[2 * height - 1 - r][c] = output[r][c] = grid[r][c] = color
    return {"input": grid, "output": output}

  grid, output = common.grid(size, size), common.grid(size, 2 * size)
  for r, c in zip(rows, cols):
    output[2 * size - 1 - r][c] = output[r][c] = grid[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1], cols=[0, 1, 0, 1, 2]),
      generate(rows=[1, 1, 2, 2], cols=[0, 2, 0, 1]),
      generate(rows=[1, 2], cols=[2, 2]),
  ]
  test = [
      generate(rows=[1, 2], cols=[2, 0]),
  ]
  return {"train": train, "test": test}
