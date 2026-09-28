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


def generate(prow=None, pcol=None, rows=None, cols=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the green pixel.
    pcol: The column of the green pixel.
    rows: The rows of the red pixels.
    cols: The columns of the red pixels.
    gsize: The side length of the square grid.
  """

  if prow is None:
    if gsize is None:
      gsize = common.randint(9, 27)
    center = gsize // 2
    prow = common.randint(center - 1, center + 1)
    pcol = common.randint(center - 1, center + 1)
    num_reds = common.randint(0, min(2 + gsize, gsize * gsize // 10))
    while True:
      rows, cols = [], []
      for _ in range(num_reds):
        rows.append(common.randint(0, gsize - 1))
        cols.append(common.randint(0, gsize - 1))
      if all((row, col) != (prow - 1, pcol)
             for row, col in zip(rows, cols)):
        break
  elif gsize is None:
    gsize = 11

  # Input: scattered red obstacles plus the single green seed pixel.
  grid = common.grid(gsize, gsize)
  for row, col in zip(rows, cols):
    grid[row][col] = common.red()
  grid[prow][pcol] = common.green()
  output = common.deepcopy(grid)

  def plan_spiral():
    """Precomputes the outward spiral, arm by arm, halting before a red."""
    segments = []
    pr, pc = prow, pcol
    rdir, cdir, length = -1, 0, 2
    for _ in range(2 * gsize):
      arm, blocked = [], False
      for _ in range(length):
        if common.get_pixel(grid, pr, pc) == common.red():
          blocked = True
          break
        arm.append((pr, pc))
        pr, pc = pr + rdir, pc + cdir
      segments.append(arm)
      if blocked:
        break
      if rdir == -1:
        rdir, cdir = 0, 1
      elif cdir == 1:
        rdir, cdir = 1, 0
      elif rdir == 1:
        rdir, cdir = 0, -1
      elif cdir == -1:
        rdir, cdir = -1, 0
      if cdir == 0:
        length += 2
    return segments

  segments = plan_spiral()

  def grow_half_turn(i):
    """Extends the spiral by a half turn (its next two equal-length arms)."""
    nonlocal output
    for arm in segments[2 * i:2 * i + 2]:
      for r, c in arm:
        common.draw(output, r, c, common.green())

  grow_half_turn(0)
  grow_half_turn(1)
  grow_half_turn(2)
  grow_half_turn(3)
  grow_half_turn(4)
  grow_half_turn(5)
  grow_half_turn(6)
  for i in range(7, (len(segments) + 1) // 2):
    grow_half_turn(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=5, pcol=5, rows=[0, 0, 2, 3, 3, 8, 8, 9, 10],
               cols=[2, 7, 10, 1, 8, 2, 10, 0, 5]),
      generate(prow=4, pcol=5, rows=[], cols=[]),
      generate(prow=4, pcol=4, rows=[0, 0, 1, 4, 5, 6, 8, 8, 9, 10],
               cols=[6, 10, 1, 9, 1, 8, 0, 3, 8, 5]),
  ]
  test = [
      generate(prow=5, pcol=6, rows=[0, 1, 1, 3, 5, 5, 8, 9, 9, 10],
               cols=[10, 1, 6, 1, 3, 8, 0, 1, 10, 6]),
  ]
  return {"train": train, "test": test}
