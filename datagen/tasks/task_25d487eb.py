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


def generate(width=None, height=None, depth=None, row=None, col=None,
             colors=None, gravity=None, num_lasers=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of one grid half
    height: the height of the grid
    depth: how deep the laser is
    row: a vertical coordinate where the laser should be placed
    col: a horizontal coordinate where the laser should be placed
    colors: the colors of the laser and its beam
    gravity: which direction the laser should be oriented
    num_lasers: how many independent lasers to place (random path only)
    num_colors: size of the color pool the lasers draw from (random path only)
  """
  if width is None:
    return _generate_random(num_lasers, num_colors)

  grid, output = common.grids(width, height)
  for d in range(depth):
    for dc in range(d - depth + 1, depth - d):
      output[row + d][col + dc] = grid[row + d][col + dc] = colors[0]
  output[row][col] = grid[row][col] = colors[1]
  for r in range(row + depth, height):
    output[r][col] = colors[1]
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


# Each laser points one of four ways.  Entry = (forward unit vector,
# perpendicular unit vector).  The emitter is a solid triangle that narrows
# toward its tip along `forward`; the marker cell sits at the base center and
# the beam continues from the tip to the grid edge along `forward`.
_LASER_DIRS = (
    ((1, 0), (0, 1)),    # down
    ((-1, 0), (0, 1)),   # up
    ((0, 1), (1, 0)),    # right
    ((0, -1), (1, 0)),   # left
)


def _draw_laser(grid, output, height, width, blocked, marker, forward, perp,
                depth, tri_color, beam_color):
  """Try to place one laser; paint it and return True iff it fits cleanly.

  Rejected unless the whole triangle stays in bounds, the cell behind the
  marker is in bounds (so the emitter keeps a background side that fixes the
  beam direction), the beam has at least one cell, and no output cell touches
  previously placed content (orthogonal margin -> every emitter stays a
  4-connected separate object and no beam crosses another triangle, exactly as
  the single-laser rule / reference verifier require).
  """
  (vi, vj), (pi, pj) = forward, perp
  r, c = marker
  if not (0 <= r - vi < height and 0 <= c - vj < width):
    return False
  in_cells = []          # triangle + marker (present in input and output)
  for d in range(depth):
    half = depth - 1 - d
    for off in range(-half, half + 1):
      rr, cc = r + d * vi + off * pi, c + d * vj + off * pj
      if not (0 <= rr < height and 0 <= cc < width):
        return False
      color = beam_color if (d == 0 and off == 0) else tri_color
      in_cells.append((rr, cc, color))
  beam_cells = []        # beam (present only in output)
  step = depth
  while 0 <= r + step * vi < height and 0 <= c + step * vj < width:
    beam_cells.append((r + step * vi, c + step * vj, beam_color))
    step += 1
  if not beam_cells:
    return False
  for rr, cc, _ in in_cells + beam_cells:
    if (rr, cc) in blocked:
      return False
  for rr, cc, color in in_cells:
    grid[rr][cc] = output[rr][cc] = color
  for rr, cc, color in beam_cells:
    output[rr][cc] = color
  for rr, cc, _ in in_cells + beam_cells:
    blocked.add((rr, cc))
    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      blocked.add((rr + da, cc + db))
  return True


def _generate_random(num_lasers, num_colors):
  """Random instance: one or more non-touching lasers over a shared palette.

  Every laser is an independent copy of the single-laser rule (a triangular
  emitter whose beam shoots to the grid edge), so the transformation is
  unchanged; only the emitter count and palette size are widened toward the
  reference band (area-scaled count, 2-8 color pool).
  """
  width, height = common.randint(10, 30), common.randint(10, 30)
  num_colors = common.randint(2, 9) if num_colors is None else max(2, num_colors)
  palette = common.random_colors(num_colors)
  if num_lasers is None:
    num_lasers = common.randint(1, max(1, (width * height) // 30))
  num_lasers = max(1, num_lasers)

  grid, output = common.grids(width, height)
  blocked = set()
  placed = 0
  for _ in range(10 * num_lasers + 10):
    if placed >= num_lasers:
      break
    forward, perp = _LASER_DIRS[common.randint(0, 3)]
    depth = common.randint(3, 4)
    tri_color, beam_color = common.sample(palette, 2)
    marker = (common.randint(0, height - 1), common.randint(0, width - 1))
    if _draw_laser(grid, output, height, width, blocked, marker, forward, perp,
                   depth, tri_color, beam_color):
      placed += 1

  if placed == 0:                       # guarantee at least one laser
    col = width // 2
    _draw_laser(grid, output, height, width, blocked, (1, col), (1, 0),
                (0, 1), 3, palette[0], palette[1])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=15, depth=3, row=3, col=4, colors=[2, 1],
               gravity=1),
      generate(width=12, height=12, depth=4, row=3, col=6, colors=[8, 3],
               gravity=2),
      generate(width=12, height=15, depth=3, row=2, col=4, colors=[3, 2],
               gravity=0),
  ]
  test = [
      generate(width=11, height=16, depth=4, row=1, col=4, colors=[4, 8],
               gravity=2),
  ]
  return {"train": train, "test": test}
