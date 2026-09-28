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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             prow=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the lines.
    cols: The columns of the lines.
    colors: The colors of the lines.
    prow: The row of the pixel.
    xpose: Whether to transpose the grid.
  """

  def draw():
    nonlocal prow, xpose
    grid = common.grid(width, height)
    for row, col, color in zip(rows, cols, colors):
      for r in range(3):
        common.draw(grid, row + r, col, color)
    row, col, zags = prow, 0, 0
    grid[row][col] = common.red()
    segments, segment, turning = [], [], False
    while True:
      if row < 0 or col < 0 or row >= height or col >= width: return None, None
      segment.append((row, col))
      if col + 1 >= width:
        if segments:
          segments[-1].extend(segment)
        else:
          segments.append(segment)
        break
      if grid[row][col + 1] == 1 + 2 * xpose:
        row, zags, turning = row - 1, zags + 1, True
      elif grid[row][col + 1] == 3 - 2 * xpose:
        row, zags, turning = row + 1, zags + 1, True
      else:
        col += 1
        if turning:
          segments.append(segment)
          segment, turning = [], False
    if xpose: grid = common.transpose(grid)
    if zags < 10: return None, None
    return grid, segments

  if width is None:
    width, height = common.randint(15, 30), common.randint(10, 18)
    lines = common.randint(4, 2 * width // 3)
    for _ in range(300):
      rows = [common.randint(-1, height - 2) for _ in range(lines)]
      cols = [common.randint(2, width - 2) for _ in range(lines)]
      if common.overlaps(rows, cols, [2] * lines, [4] * lines): continue
      colors = [2 * common.randint(1, 2) - 1 for _ in range(lines)]
      prow, xpose = common.randint(3, height - 4), common.randint(0, 1)
      grid, output = draw()
      if grid: break
    else:
      prow, xpose = common.randint(3, height - 4), common.randint(0, 1)
      distractor_cols = list(range(2, width - 1, 2))
      ladder_count = max(4, lines - len(distractor_cols))
      ladder_cols = [2]
      for idx in range(1, ladder_count):
        ladder_cols.append(ladder_cols[-1] + (2, 3, 4)[(idx - 1) % 3])
      rows, colors = [], []
      for idx in range(ladder_count):
        rows.append(prow - 2 if idx % 2 == 0 else prow - 3)
        colors.append(1 + 2 * xpose if idx % 2 == 0 else 3 - 2 * xpose)
      distractors = lines - ladder_count
      cols = ladder_cols + distractor_cols[:distractors]
      rows.extend([prow + 2] * distractors)
      colors.extend([1 + 2 * ((idx + xpose) % 2)
                     for idx in range(distractors)])

  grid, route = draw()
  output = common.deepcopy(grid)

  def reveal_event_batch(batch):
    """Reveals the next ordered batch of obstacle-turn episodes."""
    batch_size = (len(route) + 6) // 7
    start = batch * batch_size
    for segment in route[start:min(start + batch_size, len(route))]:
      for row, col in segment:
        if xpose:
          output[col][row] = common.red()
        else:
          output[row][col] = common.red()

  reveal_event_batch(0)
  reveal_event_batch(1)
  reveal_event_batch(2)
  reveal_event_batch(3)
  reveal_event_batch(4)
  reveal_event_batch(5)
  reveal_event_batch(6)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=12,
               rows=[4, 2, 6, 1, 5, 9, 2, 7, 6, 7, 4, 8, 3, 10],
               cols=[2, 4, 4, 6, 6, 6, 9, 9, 11, 14, 17, 17, 19, 19],
               colors=[1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3],
               prow=5, xpose=1),
      generate(width=22, height=12, rows=[2, 0, 2, -1, 4, 5, 3, 7, 1, 6],
               cols=[2, 5, 7, 9, 9, 12, 15, 15, 19, 19],
               colors=[3, 1, 1, 1, 1, 3, 3, 3, 1, 1], prow=3, xpose=1),
      generate(width=19, height=13, rows=[2, 3, 2, 4], cols=[3, 6, 9, 12],
               colors=[3, 1, 3, 3], prow=3, xpose=0),
      generate(width=22, height=12, rows=[2, 2, 2, 4, 4],
               cols=[6, 13, 20, 9, 17], colors=[3, 3, 1, 1, 1], prow=3,
               xpose=0),
  ]
  test = [
      generate(width=29, height=13,
               rows=[1, 2, 3, 3, 3, 5, 6, 6, 6, 8, 8, 8, 10],
               cols=[7, 22, 4, 10, 18, 2, 7, 14, 22, 4, 10, 18, 22],
               colors=[1, 1, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 1], prow=6, xpose=0),
  ]
  return {"train": train, "test": test}
