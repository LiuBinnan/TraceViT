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


def generate(size=None, rows=None, cols=None, cdirs=None, expected=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the lines.
    cols: The columns of the lines.
    cdirs: The directions of the lines.
    expected: The expected number of stars.
  """

  def draw():
    grid, output = common.grids(size, size, 8)
    def put(coords, value):
      # First, check that each coord is clear, and has no blue neighbors.
      for row, col in coords:
        if output[row][col] != 8: return False
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          if common.get_pixel(output, row + dr, col + dc) == 1: return False
      # Second, draw the coords.
      for row, col in coords:
        output[row][col] = grid[row][col] = value
      return True
    # Draw all the blue lines.
    for row, col, cdir in zip(rows, cols, cdirs):
      if not put([(row, col), (row + cdir, col + 1 - cdir)], 1):
        return None, None
    # Now, find the stars and draw them.
    num_stars = 0
    for row in range(3, size - 3):
      for col in range(3, size - 3):
        good = True
        for i in range(2, 4):
          if grid[row - i][col] != 1: good = False
          if grid[row + i][col] != 1: good = False
          if grid[row][col - i] != 1: good = False
          if grid[row][col + i] != 1: good = False
        if good:
          if output[row][col] != 8: return None, None
          output[row][col] = 4
          num_stars += 1
    if num_stars != expected: return None, None  # ensure no accidental stars
    return grid, output

  if size is None:
    # WIDEN: extend the grid-size ladder from {8,12,16,20} up to 28 (<=30).
    size = 4 * common.randint(2, 7)
    # Star count grows slowly with grid size and is capped at 4 to match the
    # four unrolled place_star() handlers in the traced output stage (an
    # expected>4 would leave later crosses unmarked -> unroll overrun).
    min_stars, max_stars = 1, 1
    if size == 16: min_stars, max_stars = 1, 2
    if size == 20: min_stars, max_stars = 3, 4
    if size == 24: min_stars, max_stars = 3, 4
    if size == 28: min_stars, max_stars = 3, 4
    expected = common.randint(min_stars, max_stars)
    # Debris count scales with area (~size*size/20), extending the original
    # ladder (8->1, 12->3, 16->6, 20->20) upward to the new sizes.
    debris = 1
    if size == 12: debris = 3
    if size == 16: debris = 6
    if size == 20: debris = 20
    if size == 24: debris = 29
    if size == 28: debris = 39
    # Place the crosses; cap attempts and shed a star on repeated collision so a
    # dense large grid cannot hang the rejection loop.
    attempts = 0
    while True:
      rows, cols, cdirs = [], [], []
      for _ in range(expected):
        row = common.randint(3, size - 4)
        col = common.randint(3, size - 4)
        rows.extend([row - 3, row, row, row + 2])
        cols.extend([col, col - 3, col + 2, col])
        cdirs.extend([1, 0, 0, 1])
      grid, _ = draw()
      if grid: break
      attempts += 1
      if attempts >= 300 and expected > 1:
        expected -= 1
        attempts = 0
    # Scatter debris; cap per-debris retries and stop early when the grid is too
    # full to accept another segment (constructive fallback, never hangs).
    for _ in range(debris):
      placed = False
      for _try in range(200):
        rows.append(common.randint(0, size - 2))
        cols.append(common.randint(0, size - 2))
        cdirs.append(common.randint(0, 1))
        grid, _ = draw()
        if grid:
          placed = True
          break
        rows.pop()
        cols.pop()
        cdirs.pop()
      if not placed:
        break

  grid, reference = draw()

  # Detected star centers and the eight arm cells that form each cross.
  stars = [(r, c) for r in range(size) for c in range(size)
           if reference[r][c] == common.yellow()]
  relevant = set()
  for r, c in stars:
    for dr, dc in [(-3, 0), (-2, 0), (2, 0), (3, 0),
                   (0, -3), (0, -2), (0, 2), (0, 3)]:
      relevant.add((r + dr, c + dc))

  output = common.deepcopy(grid)

  def isolate_targets():
    # Strip the scattered distractor segments, leaving only the crosses.
    for r in range(size):
      for c in range(size):
        if output[r][c] == common.blue() and (r, c) not in relevant:
          output[r][c] = common.cyan()

  def place_star(i):
    # Mark the center of the i-th cross formation with a star.
    if i >= len(stars):
      return
    r, c = stars[i]
    output[r][c] = common.yellow()

  def restore_field():
    # Bring the distractor segments back around the now-marked stars.
    for r in range(size):
      for c in range(size):
        if grid[r][c] == common.blue():
          output[r][c] = common.blue()

  isolate_targets()
  place_star(0)
  place_star(1)
  place_star(2)
  place_star(3)
  restore_field()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, rows=[2, 2, 4, 5, 5, 7, 8, 11, 12, 12],
               cols=[4, 10, 12, 1, 6, 4, 8, 11, 2, 9],
               cdirs=[1, 0, 1, 0, 0, 1, 1, 0, 1, 0], expected=1),
      generate(size=8, rows=[1, 2, 4, 4, 6], cols=[3, 6, 0, 5, 3],
               cdirs=[1, 0, 0, 0, 1], expected=1),
      generate(size=16, rows=[1, 2, 5, 5, 5, 7, 7, 8, 10, 11, 11, 12, 12, 13, 14],
               cols=[5, 10, 2, 7, 12, 5, 10, 12, 3, 9, 14, 0, 5, 12, 3],
               cdirs=[1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1], expected=2),
  ]
  test = [
      generate(size=20,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 4, 4, 4, 6, 6, 6, 6, 6, 8, 9, 9, 9, 11, 11, 11, 11, 12, 13, 13, 14, 14, 15, 15, 16, 16, 16, 17, 18, 18, 18, 19],
               cols=[0, 7, 16, 14, 4, 10, 18, 3, 7, 11, 16, 0, 5, 8, 14, 19, 3, 5, 10, 16, 3, 8, 10, 14, 18, 0, 5, 7, 12, 3, 15, 6, 10, 14, 0, 3, 8, 18, 11],
               cdirs=[0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0], expected=4),
  ]
  return {"train": train, "test": test}
