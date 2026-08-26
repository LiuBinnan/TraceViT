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


def reveal_color(output, cols, position, color, segment_width=1):
  """Fills every row whose gray pixel sits in `position` with `color`.

  Each call is one progressive step: it reveals the output color that the rule
  assigns to one of the three gray-column bands, leaving the other rows
  untouched. Calling reveal_color for bands 0, 1, 2 in turn paints the whole
  output one color at a time.
  """
  for r, col in enumerate(cols):
    if col // segment_width == position:
      for c in range(len(output[r])):
        output[r][c] = color


def generate(cols=None, colors=(2, 4, 3), size=3, height=None, width=None,
             segment_width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digit representing colors to be used
    size: the width and height of the (square) grid
    height: number of rows (grid extent); defaults to size
    width: number of columns (grid extent); defaults to size
    segment_width: width of each of the three gray-column bands
  """
  if height is None:
    height = len(cols) if cols is not None else common.randint(2, 30)
  if width is None:
    width = size if cols is not None else (segment_width or common.randint(1, 10)) * len(colors)
  # The gray pixel column indexes the fixed-size `colors` tuple via its band,
  # so random columns must stay inside complete bands. SECONDARY-COUNT GUARD:
  # cap generated columns to the complete-band extent.
  segment_width, col_max = (
      min(segment_width or max(1, width // len(colors)),
          max(1, width // len(colors))),
      min(width, min(segment_width or max(1, width // len(colors)),
                     max(1, width // len(colors))) * len(colors)))
  if cols is None:
    cols = []
    for _ in range(height):
      band = common.randint(0, len(colors) - 1)
      dev = common.randint(0, segment_width // 2 + 1)
      loc = segment_width // 3 + common.choice((dev, -dev))
      loc = min(max(0, loc), segment_width - 1)
      cols.append(min(col_max - 1, band * segment_width + loc))

  grid, output = common.grids(width, height)
  for r, col in enumerate(cols):
    grid[r][col] = common.gray()
  # Progressive reveal: paint the output one gray-column color at a time so each
  # statement is its own checkpoint (positions 0 -> 1 -> 2). Together they fill
  # exactly the rows the single-pass rule would, so `output` is unchanged.
  reveal_color(output, cols, 0, colors[0], segment_width)
  reveal_color(output, cols, 1, colors[1], segment_width)
  reveal_color(output, cols, 2, colors[2], segment_width)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[2, 1, 0]),
      generate(cols=[2, 2, 2]),
      generate(cols=[0, 1, 0]),
      generate(cols=[1, 2, 1]),
  ]
  test = [
      generate(cols=[2, 0, 1]),
  ]
  return {"train": train, "test": test}
