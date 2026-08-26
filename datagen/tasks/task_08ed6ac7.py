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


def _bars(rank, order, layout):
  """Columns and input colors of the bars belonging to one height-rank.

  layout is None on the validate() path (and any explicit-heights call), giving
  a single gray bar per rank at the canonical column -- byte-identical to the
  original generator. When generate() randomizes its own layout it passes the
  widened list (canonical + extra bars, each carrying its own input color).
  """
  if layout is None:
    return [(order[rank] * 2 + 1, common.gray())]
  return layout[rank]


def generate(heights=None, order=None, size=9, height=None, width=None,
             num_bars=None, layout=None):
  """Returns input and output grids according to the given parameters.

  Args:
    heights: a list of different bar heights in descending order
    order: maps each bar to its order index in the grid (left to right)
    size: the width and height of the (square) grid
    height: number of rows (defaults to size)
    width: number of columns (defaults to size)
    num_bars: how many bars to draw (>= len(heights)); the extra bars reuse the
      same four heights so the output colors always stay 1..4
    layout: per-rank list of (column, input_color) pairs; randomized internally
      when heights is randomized, left None (canonical gray bars) otherwise
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if heights is None:
    bars = common.randint(4, 4)
    heights = sorted(common.sample(range(1, min(10, height + 1)), bars),
                     reverse=True)
    order = common.shuffle(range(bars))
    max_slot = (width - 2) // 2
    n_slots = max_slot + 1
    if num_bars is None:
      num_bars = common.randint(bars, n_slots)
    num_bars = max(bars, min(num_bars, n_slots))
    slots = common.sample(range(n_slots), num_bars)
    layout = [[] for _ in range(bars)]
    for i, slot in enumerate(slots):
      rank = i if i < bars else common.randint(0, bars - 1)
      layout[rank].append((slot * 2 + 1, common.random_color()))

  grid = common.grid(width, height)
  for bar in range(min(4, len(heights))):
    for c, icolor in _bars(bar, order, layout):
      for r in range(height - heights[bar], height):
        grid[r][c] = icolor
  output = common.grid(width, height)

  def recolor_height_rank(bar):
    if bar >= len(heights):
      return
    for c, _ in _bars(bar, order, layout):
      for r in range(height - heights[bar], height):
        output[r][c] = bar + 1

  recolor_height_rank(0)
  recolor_height_rank(1)
  recolor_height_rank(2)
  recolor_height_rank(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(heights=[9, 8, 6, 3], order=[2, 0, 1, 3]),
      generate(heights=[8, 5, 4, 2], order=[3, 1, 2, 0]),
  ]
  test = [
      generate(heights=[8, 7, 5, 3], order=[0, 2, 3, 1]),
  ]
  return {"train": train, "test": test}
