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


def generate(width=None, height=None, line=None, rows=None, cols=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    line: The row of the line.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    count: The number of yellow pixels to place.
  """

  def draw():
    bounces = False
    grid, output = common.grids(width, height)
    for c in range(width):
      output[line][c] = grid[line][c] = 2
    for row, col in zip(rows, cols):
      if grid[row][col] != 0: return None, None, None
      grid[row][col] = 4
      bounces = bounces or row + 2 == line
      for c in range(width):
        if row + 2 != line and c != col: continue
        the_row = row + 1 - abs(col - c)
        if common.get_pixel(output, the_row, c) not in [-1, 0]:
          return None, None, None
        common.draw(output, the_row, c, 4)
    return grid, output, bounces

  if width is None or rows is None or cols is None:
    if width is None:
      width = common.randint(3, 12)
    if height is None:
      height = common.randint(6, 18)
    if line is None:
      line = common.randint(3, height - 1)
    if count is None:
      count = common.randint(1, (width + 1) // 2)
    expected_bounces = True if common.randint(0, 4) else False

    # Rows line-1 and line cannot produce a clean one-row fall. The unique
    # row line-2 is reserved for the optional bouncer, preserving the original
    # at-most-one-bouncer invariant. Count is also capped by the distinct-column
    # sampling budget; widening width raises the original ceiling from 4 to 6.
    nonbounce_rows = [
        row for row in range(height - 1)
        if row not in [line - 2, line - 1, line]
    ]
    capacity = len(nonbounce_rows) + (1 if expected_bounces else 0)
    num_pixels = min(max(1, count), (width + 1) // 2, capacity)

    for _ in range(200):
      rows = common.sample(list(range(height - 1)), num_pixels)
      cols = common.sample(list(range(width)), num_pixels)
      grid, _, bounces = draw()
      if grid and bounces == expected_bounces: break
    else:
      # Guaranteed rule-faithful fallback after the bounded rejection budget.
      # Put a requested bouncer at an edge, where each other row has at most one
      # conflicting reflected cell, then choose a distinct safe column.
      if expected_bounces:
        rows = [line - 2]
        rows.extend(common.sample(nonbounce_rows, num_pixels - 1))
        bounce_col = common.choice([0, width - 1])
        cols = [bounce_col]
        available = [col for col in range(width) if col != bounce_col]
        for row in rows[1:]:
          blocked = None
          if row < line - 2:
            distance = line - row - 2
            blocked = (bounce_col + distance if bounce_col == 0
                       else bounce_col - distance)
          choices = [col for col in available if col != blocked]
          col = common.choice(choices)
          cols.append(col)
          available.remove(col)
      else:
        rows = common.sample(nonbounce_rows, num_pixels)
        cols = common.sample(list(range(width)), num_pixels)

  grid, _, _ = draw()
  output = common.deepcopy(grid)

  # A point's fall lands it flush against the red line exactly when
  # row + 2 == line, and rows are sampled WITHOUT replacement, so at most one
  # point can ever bounce. The fall puts that point on the apex of its own
  # reflected path, which is why dropping everything first is the natural
  # first move: the bounce then just opens outward from where it landed.
  bouncers = [i for i in range(len(rows)) if rows[i] + 2 == line]
  fallen = [False for _ in rows]
  reflected = [False for _ in rows]

  def render():
    """Redraws the grid at the current solving state."""
    nonlocal output
    output = common.deepcopy(grid)
    for i in range(len(rows)):
      if fallen[i]:
        output[rows[i]][cols[i]] = common.black()
    for i in range(len(rows)):
      if not fallen[i]:
        continue
      row, col = rows[i], cols[i]
      if reflected[i]:
        for c in range(width):
          common.draw(output, row + 1 - abs(col - c), c, common.yellow())
      else:
        common.draw(output, row + 1, col, common.yellow())

  def drop_all():
    """Every yellow point falls one row."""
    for i in range(len(rows)):
      fallen[i] = True
    render()

  def bounce(k):
    """A point that landed on the red line reflects out of it at 45 degrees."""
    if k >= len(bouncers):
      return
    reflected[bouncers[k]] = True
    render()

  drop_all()
  bounce(0)
  bounce(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=12, line=9, rows=[0, 1, 4, 7, 10],
               cols=[1, 5, 2, 4, 3]),
      generate(width=6, height=10, line=5, rows=[2, 3], cols=[1, 4]),
      generate(width=3, height=6, line=4, rows=[1], cols=[1]),
      generate(width=5, height=7, line=6, rows=[4], cols=[2]),
  ]
  test = [
      generate(width=8, height=12, line=3, rows=[0, 1, 6], cols=[4, 0, 1]),
  ]
  return {"train": train, "test": test}
