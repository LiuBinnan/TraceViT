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


def generate(flop=None, col=None, pos=None, lengths=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    flop: Whether to flop the grid horizontally.
    col: The column to start drawing from.
    pos: The position of the maroon pixel.
    lengths: The lengths of the segments.
    gsize: The height and width of the square grid.
  """

  def draw():
    grid, output = common.grids(gsize, gsize)
    r, c, rdir, cdir, i, color, transparent = 0, col, 0, 1, 0, 8, -2
    for length in lengths:
      rdir, cdir = 1 - rdir, 1 - cdir
      for _ in range(length - 1):
        if r < 0 or r >= gsize or c < 0 or c >= gsize: return None, None
        if ((c == gsize - 1 and rdir)
            or (r == gsize - 1 and cdir)): return None, None
        grid[r][c] = 9 if i == pos else transparent
        output[r][c] = color if output[r][c] != 9 else 9
        r, c, i = r + rdir, c + cdir, i + 1
      if i == pos:
        if rdir == 0: return None, None  # Wrong kind of turn.
        output[r][c] = 9
        color = transparent
    if r < 0 or r >= gsize or c < 0 or c >= gsize: return None, None
    grid[r][c] = transparent
    output[r][c] = color
    r, c = r + rdir, c + cdir
    if not (r < 0 or r >= gsize or c < 0 or c >= gsize): return None, None
    # Draw the orange borders.
    for r in range(gsize):
      for c in range(gsize):
        if common.get_pixel(grid, r, c) != 0: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(grid, r + dr, c + dc) in [transparent, 9]:
              output[r][c] = grid[r][c] = 7
    # Change all the transparent pixels to black.
    for r in range(gsize):
      for c in range(gsize):
        if grid[r][c] == transparent: grid[r][c] = 0
        if output[r][c] == transparent: output[r][c] = 0
    if flop: grid, output = common.flop(grid), common.flop(output)
    return grid, output

  if flop is None:
    if gsize is None:
      gsize = common.randint(9, 16)
    flop = common.randint(0, 1)
    col = common.randint(1, gsize // 2 - 1)
    pos = -1 if common.randint(0, 1) else common.randint(6, 9)
    for _ in range(500):
      lengths = [common.randint(3, 7) for _ in range(
          common.randint(3, max(5, gsize // 2)))]
      grid, _ = draw()
      if grid: break
    else:
      # Exhaustive fallback over the original length alphabet. This preserves
      # the sampled size/column/plug while guaranteeing the rejection sampler
      # cannot hang on an unlucky stream.
      for lengths in (
          [a, b, c, d, e]
          for a in range(3, 8)
          for b in range(3, 8)
          for c in range(3, 8)
          for d in range(3, 8)
          for e in range(3, 8)):
        grid, _ = draw()
        if grid: break
      else:
        raise RuntimeError("unable to construct a valid corridor")
  elif gsize is None:
    gsize = 10

  grid, _ = draw()
  # Bookkeeping: the corridor path in flow order, segment starts, and where
  # the water stops (a maroon plug only seals the corridor when it sits at a
  # turn; mid-segment plugs are swept away by the flow).
  path, starts, r, c, rdir, cdir = [], [], 0, col, 0, 1
  for length in lengths:
    rdir, cdir = 1 - rdir, 1 - cdir
    starts.append(len(path))
    for _ in range(length - 1):
      path.append((r, c))
      r, c = r + rdir, c + cdir
  turns = starts[1:] + [len(path)]
  path.append((r, c))
  stop = pos if pos in turns else len(path)
  output = common.deepcopy(grid)

  def flow_segment(k):
    """Pours the water along corridor segment k until it exits or is plugged."""
    if k >= len(lengths): return
    hi = starts[k + 1] if k + 1 < len(lengths) else len(path)
    for i in range(starts[k], min(hi, stop)):
      row, col2 = path[i]
      output[row][gsize - 1 - col2 if flop else col2] = common.cyan()

  flow_segment(0)
  flow_segment(1)
  flow_segment(2)
  flow_segment(3)
  flow_segment(4)
  for k in range(5, len(lengths)):
    flow_segment(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(flop=1, col=3, pos=9, lengths=[4, 3, 7]),
      generate(flop=0, col=1, pos=9, lengths=[4, 4, 4, 4, 4]),
      generate(flop=0, col=3, pos=6, lengths=[4, 3, 5, 3, 3]),
      generate(flop=0, col=4, pos=-1, lengths=[4, 3, 6, 4]),
  ]
  test = [
      generate(flop=1, col=1, pos=9, lengths=[4, 4, 4, 5, 4]),
  ]
  return {"train": train, "test": test}
