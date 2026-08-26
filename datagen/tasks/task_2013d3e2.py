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


def generate(row=None, col=None, rows=None, cols=None, idxs=None, colors=None,
             size=10, zoom_size=3, num_colors=None, num_cells=None,
             seed_size=None, grid_size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical offset for the pinwheel
    col: a horizontal offset for the pinwheel
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the color list
    colors: a list of colors to be used
    size: the width and height of the (square) input grid
    zoom_size: the width and height of the (square) output grid
    num_colors: how many distinct colors the pinwheel seed may use
    num_cells: how many colored cells the seed contains
    seed_size: the (square) output/seed edge length (widens output sizes)
    grid_size: the (square) input edge length (widens foreground density)
  """
  if row is None:
    # Widened, rule-preserving structural sampling (mirrors re_arc's bands).
    # The 90-degree pinwheel rule forces a SQUARE seed, so the output size is
    # a single edge length; sampling it widens the output-size axis.
    if seed_size is None:
      seed_size = common.randint(3, 11)
    zoom_size = min(15, max(1, seed_size))
    # The input must be at least large enough to hold the 2*zoom_size pinwheel;
    # widening it (independently of the seed) widens the foreground density.
    if grid_size is None:
      grid_size = common.randint(2 * zoom_size, 30)
    size = min(30, max(grid_size, 2 * zoom_size))
    # Number of distinct seed colors (drives the color-count axis).
    if num_colors is None:
      num_colors = common.randint(1, 8)
    num_colors = max(1, min(9, num_colors))
    colors = common.random_colors(num_colors)
    # Number of colored seed cells, capped at the seed's capacity (drives the
    # object-count and density axes).
    max_cells = zoom_size * zoom_size - 1
    if num_cells is None:
      num_cells = common.randint(2, max_cells) if max_cells >= 2 else 1
    num_cells = max(1, min(max_cells if max_cells >= 1 else 1, num_cells))
    # Grow an 8-connected seed shape: diagonal-only links keep it a single
    # blob while fragmenting it into many 4-connected pieces, mirroring
    # re_arc's neighbors-based growth (drives the object-count axis).
    free = {(r, c) for r in range(zoom_size) for c in range(zoom_size)}
    start = sorted(free)[common.randint(0, len(free) - 1)]
    obj = {start}
    free.discard(start)
    for _ in range(num_cells - 1):
      frontier = set()
      for (r, c) in obj:
        for dr in (-1, 0, 1):
          for dc in (-1, 0, 1):
            if (dr or dc) and (r + dr, c + dc) in free:
              frontier.add((r + dr, c + dc))
      if not frontier:
        break
      pick = sorted(frontier)[common.randint(0, len(frontier) - 1)]
      obj.add(pick)
      free.discard(pick)
    # Anchor the seed to its top-left corner so it always touches row 0 and
    # column 0. By the pinwheel's 4-fold symmetry this makes the input's
    # non-background bounding box exactly 2*zoom_size square, so the seed
    # (the output) stays recoverable as the box's top-left quadrant.
    minr = min(r for r, c in obj)
    minc = min(c for r, c in obj)
    cells = sorted((r - minr, c - minc) for r, c in obj)
    rows = [p[0] for p in cells]
    cols = [p[1] for p in cells]
    idxs = [common.randint(0, len(colors) - 1) for _ in cells]
    row = common.randint(0, size - 2 * zoom_size)
    col = common.randint(0, size - 2 * zoom_size)

  grid = common.grid(size, size)
  output = common.grid(zoom_size, zoom_size)
  for r, c, idx in zip(rows, cols, idxs):
    edge = 2 * zoom_size - 1
    grid[row + r][col + c] = colors[idx]
    grid[row + edge - c][col + r] = colors[idx]
    grid[row + c][col + edge - r] = colors[idx]
    grid[row + edge - r][col + edge - c] = colors[idx]
    output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=2, rows=[0, 1, 1, 2, 2, 2], cols=[2, 1, 2, 0, 1, 2],
               idxs=[0, 1, 2, 0, 2, 3], colors=[7, 6, 8, 4]),
      generate(row=1, col=1, rows=[0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 2],
               idxs=[0, 1, 2, 3, 4], colors=[1, 3, 6, 5, 2]),
  ]
  test = [
      generate(row=2, col=2, rows=[1, 1, 2, 2, 2], cols=[1, 2, 0, 1, 2],
               idxs=[0, 0, 1, 1, 2], colors=[4, 8, 3]),
  ]
  return {"train": train, "test": test}
