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


def generate(width=None, height=None, row=None, lengths=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the pixel.
    lengths: The lengths of the lines.
    flip: Whether to flip the grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    r, c = row, 0
    grid[r][c] = 3
    for i, length in enumerate(lengths):
      for j in range(length):
        if r >= height or c >= width: return None, None
        output[r][c] = 3
        if j + 1 == length and i + 1 < len(lengths):
          if i % 2 == 0:
            if r >= height or c + 1 >= width: return None, None
            output[r][c + 1] = grid[r][c + 1] = 8 if flip else 6
          else:
            if r + 1 >= height or c >= width: return None, None
            output[r + 1][c] = grid[r + 1][c] = 6 if flip else 8
          continue
        if i % 2 == 0: c += 1
        else: r += 1
    if flip: grid, output = common.flip(grid), common.flip(output)
    return grid, output

  if width is None:
    while True:
      width, height = common.randint(6, 20), common.randint(6, 20)
      row = common.randint(2, 4)
      flip = common.randint(0, 1)
      r, c, lengths = row, 0, []
      while r + 1 < height and c + 1 < width:
        length = common.randint(3, 5)
        if len(lengths) % 2 == 0:
          if c + length - 1 >= width: length = width - c
          c += length - 1
        else:
          if r + length - 1 >= height: length = height - r
          r += length - 1
        lengths.append(length)
      if 0 in lengths: continue  # These don't occur in the test cases.
      if 1 in lengths: continue  # These don't occur in the test cases.
      grid, _ = draw()
      if grid: break

  # Input: the green start pixel plus the corner clue markers, produced by the
  # same deterministic (randomness-free) helper the sampler used to validate.
  grid, _ = draw()

  # Output: walk the green staircase one straight run at a time. The clue
  # markers (already in the input) stay put; each stage extends the path
  # through the next segment up to its corner, tracing how it is solved.
  output = common.deepcopy(grid)

  # Precompute each segment's path cells (bookkeeping, in pre-flip coordinates,
  # replicating draw()'s walk). Not a checkpoint: it never writes to output.
  segments = []
  r, c = row, 0
  for i, length in enumerate(lengths):
    cells = []
    for j in range(length):
      cells.append((r, c))
      if j + 1 == length and i + 1 < len(lengths):
        continue
      if i % 2 == 0:
        c += 1
      else:
        r += 1
    segments.append(cells)

  def put(rr, cc):
    output[height - 1 - rr if flip else rr][cc] = 3

  def draw_segment(k):
    """Paints the green path of staircase segment k up to its corner."""
    if k >= len(segments): return
    for rr, cc in segments[k]:
      put(rr, cc)

  # Keep the original twelve explicit stage calls, then cover any additional
  # runs made possible by the widened canvas band.
  draw_segment(0)
  draw_segment(1)
  draw_segment(2)
  draw_segment(3)
  draw_segment(4)
  draw_segment(5)
  draw_segment(6)
  draw_segment(7)
  draw_segment(8)
  draw_segment(9)
  draw_segment(10)
  draw_segment(11)
  for k in range(12, len(segments)):
    draw_segment(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, row=3, lengths=[4, 3], flip=True),
      generate(width=6, height=8, row=3, lengths=[4, 3, 3], flip=False),
      generate(width=8, height=8, row=2, lengths=[4, 3, 4, 4], flip=False),
      generate(width=8, height=9, row=4, lengths=[3, 4, 4, 2], flip=True),
      generate(width=6, height=6, row=2, lengths=[3, 4], flip=False),
  ]
  test = [
      generate(width=12, height=10, row=2, lengths=[3, 4, 5, 3, 4, 2, 3], flip=True),
  ]
  return {"train": train, "test": test}
