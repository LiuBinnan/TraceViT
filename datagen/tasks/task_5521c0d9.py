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


def generate(cols=None, wides=None, talls=None, colors=None, size=15, boxes=3,
             height=None, width=None, num_boxes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of colors to be used
    size: the width and height of the (square) grid
    boxes: the number of boxes to be placed
    height: the number of grid rows (defaults to size)
    width: the number of grid columns (defaults to size)
    num_boxes: number of boxes to place (defaults to a width-scaled random
      count); widens object-count / #colors / density toward re_arc
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if cols is None:
    # Widen structural variation (mirrors re_arc generate_5521c0d9): sample a
    # variable number of boxes, each a distinct random color, to drive object-
    # count and #colors. Box columns use re_arc's split-point construction --
    # 2*boxes distinct INTERIOR columns, sorted and paired into non-overlapping
    # [start, end] intervals -- so widths vary widely (wide boxes make denser
    # grids) with no rejection loop to stall. Two guards keep the puzzle rule
    # exact: (1) the interior-only columns leave a background margin on both
    # side edges, so the input stays unambiguously bottom-anchored for the
    # solving rule (a box growing from a side edge would be orientation-
    # ambiguous); (2) every box height <= height//2 so no box moves off the top
    # edge. Count <= 9 gives each box a distinct color; the mild max-of-two
    # height draw widens the colored-area (density) band.
    if num_boxes is None:
      boxes = common.randint(2, min(9, max(2, (width - 1) // 3)))
    else:
      boxes = num_boxes
    tallcap = max(1, height // 2)
    speps = sorted(common.sample(list(range(1, width - 1)), 2 * boxes))
    cols = speps[0::2]
    ends = speps[1::2]
    wides = [ends[i] - cols[i] + 1 for i in range(boxes)]
    talls = [max(common.randint(1, tallcap), common.randint(1, tallcap))
             for _ in range(boxes)]
    colors = common.random_colors(boxes)

  grid, output = common.grids(width, height)
  for idx in range(min(1, len(colors))):
    col, wide, tall, color = cols[idx], wides[idx], talls[idx], colors[idx]
    for r in range(height - tall, height):
      for c in range(col, col + wide):
        grid[r][c] = color
        output[r - tall][c] = color
  for idx in range(1, min(2, len(colors))):
    col, wide, tall, color = cols[idx], wides[idx], talls[idx], colors[idx]
    for r in range(height - tall, height):
      for c in range(col, col + wide):
        grid[r][c] = color
        output[r - tall][c] = color
  for idx in range(2, len(colors)):
    col, wide, tall, color = cols[idx], wides[idx], talls[idx], colors[idx]
    for r in range(height - tall, height):
      for c in range(col, col + wide):
        grid[r][c] = color
        output[r - tall][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[1, 4, 9], wides=[2, 4, 4], talls=[4, 2, 4],
               colors=[1, 2, 4]),
      generate(cols=[1, 7, 11], wides=[4, 2, 2], talls=[6, 2, 5],
               colors=[4, 1, 2]),
      generate(cols=[1, 7, 11], wides=[4, 1, 2], talls=[1, 4, 3],
               colors=[2, 1, 4]),
  ]
  test = [
      generate(cols=[0, 5, 10], wides=[4, 3, 5], talls=[7, 6, 3],
               colors=[2, 4, 1]),
  ]
  return {"train": train, "test": test}
