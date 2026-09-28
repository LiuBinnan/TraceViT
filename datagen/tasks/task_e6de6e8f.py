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


def generate(commands=None, ncmd=None, nzero=None):
  """Returns input and output grids according to the given parameters.

  Args:
    commands: A list of commands to use.
    ncmd: Number of commands to generate when commands is not supplied.
    nzero: Number of straight-down commands to generate.
  """

  if commands is None:
    if ncmd is None:
      ncmd = common.randint(4, 9)
    if nzero is None:
      nzero = common.randint(1, ncmd - 2)
    if not 1 <= nzero <= ncmd - 2:
      raise ValueError("nzero must leave at least two diagonal commands")
    if 2 * (ncmd - nzero) + nzero + (ncmd - 1) > 30:
      raise ValueError("encoded command strip exceeds ARC's size limit")
    while True:
      commands = [common.randint(-1, 1) for _ in range(ncmd)]
      if commands.count(0) == nzero: break
  else:
    if ncmd is None:
      ncmd = len(commands)
    if nzero is None:
      nzero = commands.count(0)
    if len(commands) != ncmd or commands.count(0) != nzero:
      raise ValueError("commands must match ncmd and nzero")
    if not 1 <= nzero <= ncmd - 2:
      raise ValueError("nzero must leave at least two diagonal commands")
    if 2 * (ncmd - nzero) + nzero + (ncmd - 1) > 30:
      raise ValueError("encoded command strip exceeds ARC's size limit")

  # Input: a horizontal strip of 2-row glyphs, one glyph per command.
  grid = common.grid(
      2 * (ncmd - nzero) + nzero + (ncmd - 1), 2)
  col = 0
  for command in commands:
    if command == -1:
      grid[0][col + 1] = grid[1][col] = grid[1][col + 1] = common.red()
      col += 3
    if command == 0:
      grid[0][col] = grid[1][col] = common.red()
      col += 2
    if command == 1:
      grid[0][col] = grid[1][col] = grid[1][col + 1] = common.red()
      col += 3

  # Output: the decoded snake starts at the green entrance marker up top.
  output = common.grid(
      2 * (ncmd - nzero) + 1,
      1 + (ncmd - nzero) + 2 * nzero)
  output[0][ncmd - nzero] = common.green()

  # Precompute the snake's route: each command is one 2-cell segment that
  # steps the path down-left (-1), straight down (0), or down-right (1).
  segments = []
  row, col = 1, ncmd - nzero
  for command in commands:
    if command == -1:
      cells = [(row, col), (row, col - 1)]
      row, col = row + 1, col - 1
    elif command == 0:
      cells = [(row, col), (row + 1, col)]
      row += 2
    elif command == 1:
      cells = [(row, col), (row, col + 1)]
      row, col = row + 1, col + 1
    segments.append(cells)

  def draw_segment(k):
    """Extends the snake by command k's segment (its next move down)."""
    if k >= len(segments):
      return
    for r, c in segments[k]:
      output[r][c] = common.red()

  draw_segment(0)
  draw_segment(1)
  draw_segment(2)
  draw_segment(3)
  draw_segment(4)
  for k in range(5, len(segments)):
    draw_segment(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(commands=[-1, 1, 1, 0, 0]),
      generate(commands=[1, -1, 0, 1, 0]),
      generate(commands=[1, 1, 1, 0, 0]),
  ]
  test = [
      generate(commands=[0, 1, 1, -1, 0]),
  ]
  return {"train": train, "test": test}
