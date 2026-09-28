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


def generate(selected=None, top=None, rows=None, cols=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    selected: The selected index.
    top: Whether to shade the top of the line.
    rows: The rows of the lines.
    cols: The columns of the lines.
    gsize: The width and height of the square canvas.
  """

  if selected is None:
    if gsize is None:
      gsize = common.randint(14, 22)
    selected, top = common.randint(1, 4), common.randint(0, 1)
    num_lines = common.randint(10, 15)
    for _ in range(1000):
      rows = [
          common.randint(0, gsize - max(10 - 2 * idx, 2))
          for idx in range(num_lines)
      ]
      cols = [common.randint(0, gsize - 1) for _ in range(num_lines)]
      wides = [2] * num_lines
      talls = [max(10 - 2 * idx, 2) + 1 for idx in range(num_lines)]
      if not common.overlaps(rows, cols, wides, talls): break
    else:
      lane_cols = common.shuffle(list(range(0, gsize, 2)))
      lane_ends = [0] * len(lane_cols)
      line_lanes = []
      rows, cols = [], []
      for idx in range(num_lines):
        lane = lane_ends.index(min(lane_ends))
        rows.append(lane_ends[lane])
        cols.append(lane_cols[lane])
        line_lanes.append(lane)
        lane_ends[lane] += max(10 - 2 * idx, 2) + 1
      offsets = [common.randint(0, gsize + 1 - end) for end in lane_ends]
      rows = [row + offsets[lane] for row, lane in zip(rows, line_lanes)]
  elif gsize is None:
    gsize = 16

  grid = common.grid(gsize, gsize, common.orange())
  for idx, (row, col) in enumerate(zip(rows, cols)):
    length = max(10 - 2 * idx, 2)
    for i in range(length):
      grid[row + i][col] = common.cyan()
      if idx == selected and (i >= length // 2) != int(top):
        grid[row + i][col] = common.maroon()
  output = common.deepcopy(grid)

  def erase_source_marker():
    """Restores the marked line to its original cyan color."""
    row, col = rows[selected], cols[selected]
    length = max(10 - 2 * selected, 2)
    for i in range(length):
      output[row + i][col] = common.cyan()

  erase_source_marker()

  def mark_next_longer_line():
    """Marks the same half of the immediately longer line."""
    target = selected - 1
    row, col = rows[target], cols[target]
    length = max(10 - 2 * target, 2)
    for i in range(length):
      if (i >= length // 2) != int(top):
        output[row + i][col] = common.maroon()

  mark_next_longer_line()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(selected=3, top=1, rows=[0, 8, 1, 3, 7, 10, 11, 11, 13, 14],
               cols=[6, 14, 2, 9, 12, 1, 4, 12, 7, 4]),
      generate(selected=4, top=0,
               rows=[6, 4, 7, 1, 9, 0, 1, 5, 6, 6, 12, 12, 13],
               cols=[4, 9, 1, 1, 13, 15, 11, 7, 11, 14, 13, 15, 11]),
      generate(selected=1, top=0,
               rows=[0, 0, 10, 0, 1, 5, 5, 6, 8, 8, 8, 10, 12, 13, 14],
               cols=[14, 9, 1, 2, 5, 6, 11, 1, 5, 7, 12, 3, 11, 8, 5]),
  ]
  test = [
      generate(selected=2, top=1, rows=[1, 1, 10, 7, 3, 10, 10, 12, 13, 13],
               cols=[15, 7, 1, 10, 4, 4, 7, 14, 12, 5]),
  ]
  return {"train": train, "test": test}
