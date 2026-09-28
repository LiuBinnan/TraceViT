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


def generate(width=None, height=None, colors=None, extra_rows=None,
             extra_cols=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
    extra_rows: Rows to ignore the reflection (for an ambiguous case).
    extra_cols: The number of extra columns (for an ambiguous case).
    density: The percentage chance that a generated cell contains a block.
  """

  def draw():
    redrow = None
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
      if color == 2: redrow = i // width
    queue = [(redrow, 0, 0, 1)]  # Row, col, row dir, col dir
    seen = [(redrow, 0, 0, 1)]
    extras = list(zip(extra_rows, extra_cols)) if extra_rows else []
    bounces = False
    while queue:
      r, c, dr, dc = queue.pop()
      while True:
        output[r][c] = 2
        if common.get_pixel(output, r + dr, c + dc) == -1: break  # OOB
        if common.get_pixel(output, r + dr, c + dc) not in [0, 2]:
          if (r, c) in extras: break
          bounces = True
          directions = []
          for ddr, ddc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            directions.append((r, c, ddr, ddc))
          directions.remove((r, c, dr, dc))
          directions.remove((r, c, dr * -1, dc * -1))
          for direction in directions:
            if direction in seen: continue
            seen.append(direction)
            queue.append(direction)
          break
        r, c = r + dr, c + dc
    if not bounces: return None, None
    return grid, output

  if width is None:
    if density is None:
      density = 15
    width, height = 2 * common.randint(2, 14), 2 * common.randint(2, 14)
    while True:
      grid = common.grid(width, height)
      for r in range(height):
        for c in range(width):
          if common.randint(0, 99) < density:
            grid[r][c] = common.choice([3, 6, 7, 8])
      redrow = common.randint(1, height - 2)
      if grid[redrow][1] != 0: continue
      grid[redrow][0] = 2
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  # Build the input grid (draw() draws no randomness).
  grid, _ = draw()

  # Solve forward: a red laser leaves the red pixel heading right; wherever it
  # is about to meet a colored block it stops and splits into the two
  # perpendicular beams. Trace the whole light structure wave by wave -- each
  # bounce spawns the next wave of beams.
  output = common.deepcopy(grid)

  redrow = None
  for i, color in enumerate(colors):
    if color == 2:
      redrow = i // width
  extras = list(zip(extra_rows, extra_cols)) if extra_rows else []

  # Precompute the beam waves as a BFS over bounce events (no randomness). A
  # beam travels through background and existing trail alike and only stops at a
  # colored block or the grid edge, so each segment's cells depend only on the
  # fixed input blocks. The reachable set matches the original traversal.
  waves = []
  seen = {(redrow, 0, 0, 1)}
  frontier = [(redrow, 0, 0, 1)]
  while frontier:
    wave_cells = []
    next_frontier = []
    for r0, c0, dr, dc in frontier:
      r, c = r0, c0
      cells = []
      bounce = None
      while True:
        cells.append((r, c))
        ahead = common.get_pixel(grid, r + dr, c + dc)
        if ahead == -1:
          break
        if ahead not in [0, 2]:
          bounce = (r, c)
          break
        r, c = r + dr, c + dc
      wave_cells.append(cells)
      if bounce is not None and bounce not in extras:
        br, bc = bounce
        for ddr, ddc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          if (ddr, ddc) == (dr, dc) or (ddr, ddc) == (-dr, -dc):
            continue
          state = (br, bc, ddr, ddc)
          if state in seen:
            continue
          seen.add(state)
          next_frontier.append(state)
    waves.append(wave_cells)
    frontier = next_frontier

  def draw_wave(i):
    """Paints wave i's beams red; the last call absorbs any deeper waves."""
    if i >= len(waves):
      return
    wave_ids = range(i, len(waves)) if i >= 3 else [i]
    for wid in wave_ids:
      for cells in waves[wid]:
        for r, c in cells:
          output[r][c] = 2

  draw_wave(0)
  draw_wave(1)
  draw_wave(2)
  draw_wave(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=8, colors=[0, 7, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 3,
                                          0, 0, 0, 0, 0, 0, 0, 0,
                                          2, 0, 8, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 7, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=12, height=12,
               colors=[0, 0, 0, 0, 3, 7, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0, 3,
                       0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0,
                       2, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0,
                       0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0,
                       0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 0, 0, 0, 8, 3, 0, 0, 0,
                       0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
               extra_rows=[1, 10], extra_cols=[3, 4]),
      generate(width=6, height=6, colors=[0, 0, 3, 0, 0, 7,
                                          0, 0, 0, 0, 0, 0,
                                          2, 0, 0, 0, 3, 0,
                                          0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 8,
                                          0, 0, 3, 0, 0, 0]),
      generate(width=6, height=4, colors=[0, 0, 0, 0, 0, 0,
                                          2, 0, 0, 0, 8, 0,
                                          0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0]),
      generate(width=10, height=10, colors=[0, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                                            0, 0, 3, 0, 0, 0, 0, 0, 7, 0,
                                            2, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 0, 0, 0, 7, 0, 8, 0, 0, 6,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 7, 0, 0, 0, 6, 0, 0, 0, 8,
                                            0, 0, 6, 0, 8, 0, 0, 0, 0, 0,
                                            0, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                                            0, 0, 0, 0, 0, 0, 7, 0, 0, 0]),
      generate(width=6, height=8, colors=[0, 0, 0, 7, 0, 0,
                                          6, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0,
                                          2, 0, 0, 0, 8, 0,
                                          0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 8,
                                          0, 0, 0, 0, 0, 0,
                                          7, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=12, height=10,
               colors=[0, 0, 0, 8, 0, 0, 0, 0, 7, 0, 0, 3,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 6, 0, 0, 0, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                       0, 0, 0, 3, 0, 0, 0, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0,
                       0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       0, 0, 8, 0, 0, 0, 7, 0, 0, 6, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
