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


def generate(rows=None, cols=None, lengths=None, colors=None, extra=None,
             gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the diamond centers.
    cols: The columns of the diamond centers.
    lengths: The lengths of the diamonds.
    colors: The colors of the diamonds.
    extra: Extra values (if needed) to handle ambiguous cases.
    gsize: The side length of the square grid; defaults to the original 16.
  """

  def get_new_length(length, color):
    if color not in [2, 5]: return length
    return (length - 1) if color == 2 else (length + 1)

  def draw():
    size = 16 if gsize is None else gsize
    grid, output = common.grids(size, size, 7)
    # First, draw the diamonds.
    for i, (row, col, length, color) in enumerate(zip(rows, cols, lengths, colors)):
      if not common.diamond(grid, row, col, length, color, 7):
        return None, None  # we drew over another diamond.
      new_col = col + (extra[i] if extra else 0)
      new_length = get_new_length(length, color)
      if new_length < 0: return None, None  # a red imploded
      if not common.diamond(output, row, new_col, new_length, color, 7):
        return None, None  # we drew over another diamond.
    # Second, check that all of their insides are clear.
    for i, (row, col, length, color) in enumerate(zip(rows, cols, lengths, colors)):
      if not common.diamond_check_inside(grid, row, col, length, 7):
        return None, None  # there's something inside the diamond.
      new_col = col + (extra[i] if extra else 0)
      new_length = get_new_length(length, color)
      if not common.diamond_check_inside(output, row, new_col, new_length, 7):
        return None, None  # there's something inside the diamond.
    return grid, output

  if rows is None:
    if gsize is None:
      gsize = common.randint(14, 28)
    max_diamonds = min(9, 3 + gsize * gsize // 85)
    num_diamonds = common.randint(3, max_diamonds)
    attempts = 0
    while True:
      attempts += 1
      rows = [common.randint(0, gsize - 1) for _ in range(num_diamonds)]
      cols = [common.randint(0, gsize - 1) for _ in range(num_diamonds)]
      lengths = [common.randint(0, 4) for _ in range(num_diamonds)]
      colors = common.choices([2, 5, 8, 9], k=num_diamonds)
      grid = None
      if 2 in colors and 5 in colors:  # need a red and gray
        grid, _ = draw()
      if grid: break
      if attempts >= 500:
        # Bound difficult packing tails by lowering and resampling the count.
        num_diamonds = common.randint(3, max(3, num_diamonds - 1))
        attempts = 0

  # Build the (validated) input grid; the transformed output is derived forward
  # below, one diamond at a time, so draw()'s own output copy is discarded.
  grid, _ = draw()
  output = common.grid(16 if gsize is None else gsize,
                       16 if gsize is None else gsize, 7)

  def redraw_diamond(i):
    """Redraws diamond i resized by its color: red shrinks, gray grows, else same."""
    if i >= len(rows): return
    row, col, length, color = rows[i], cols[i], lengths[i], colors[i]
    new_col = col + (extra[i] if extra else 0)
    new_length = get_new_length(length, color)
    common.diamond(output, row, new_col, new_length, color, 7)

  # Redraw every diamond at its color-adjusted size. The first six calls retain
  # the original checkpoints; the catch-all completes widened 7-9 item cases.
  redraw_diamond(0)
  redraw_diamond(1)
  redraw_diamond(2)
  redraw_diamond(3)
  redraw_diamond(4)
  redraw_diamond(5)
  for i in range(6, len(rows)):
    redraw_diamond(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 4, 8, 10, 15, 15], cols=[12, 4, 10, 3, 4, 13],
               lengths=[3, 0, 2, 1, 1, 1], colors=[2, 5, 8, 2, 5, 9],
               extra=[0, 0, 0, 0, 1, 0]),
      generate(rows=[5, 6, 12], cols=[4, 14, 11], lengths=[2, 1, 1],
               colors=[2, 9, 5]),
      generate(rows=[0, 4, 11, 13], cols=[5, 13, 13, 5], lengths=[6, 1, 2, 4],
               colors=[2, 8, 8, 5]),
  ]
  test = [
      generate(rows=[1, 3, 10, 13], cols=[14, 2, 10, 4], lengths=[3, 2, 0, 0],
               colors=[5, 2, 8, 5]),
  ]
  return {"train": train, "test": test}
