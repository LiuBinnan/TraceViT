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


def _flip_h(g):
  return [row[::-1] for row in g]


def _flip_v(g):
  return g[::-1]


def _transpose(g):
  return [list(col) for col in zip(*g)]


def _orient(g, quadrant):
  """Rotate a base-frame grid into the requested quadrant orientation.

  quadrant 0 -> identity, 1 -> rot90 CW, 2 -> rot90 CCW, 3 -> rot180. The same
  rotation is applied to the input and the output, so the pair stays a valid
  instance of the task's transformation in every orientation (each is one of the
  four dihedral rotations re_arc's generator/verifier already covers).
  """
  if quadrant == 1:
    return _flip_h(_transpose(g))
  if quadrant == 2:
    return _flip_v(_transpose(g))
  if quadrant == 3:
    return _flip_h(_flip_v(g))
  return g


def _forbid(forbidden, li, lj):
  """Reserve a marker's 2x2 footprint and its 4-neighbourhood so no two markers
  ever become 4-adjacent (which would merge them into one object and break the
  one-marker-per-object rule the transformation relies on)."""
  for r, c in ((li, lj), (li, lj + 1), (li + 1, lj), (li + 1, lj + 1)):
    forbidden.add((r, c))
    forbidden.add((r - 1, c))
    forbidden.add((r + 1, c))
    forbidden.add((r, c - 1))
    forbidden.add((r, c + 1))


def generate(quadrant=None, size=3, bh=None, bw=None, grid_h=None, grid_w=None,
             count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    quadrant: the quadrant to be filled (marker orientation, one of 0-3)
    size: the width and height of the (square) single-marker input grid
    bh: the height (rows) of each green block in the single-marker output
    bw: the width (cols) of each green block in the single-marker output
    grid_h: input rows for the multi-marker variant (re_arc band 3-10)
    grid_w: input cols for the multi-marker variant (re_arc band 3-10)
    count: total markers for the multi-marker variant (area-scaled when None)
  """
  if quadrant is None:
    quadrant = common.randint(0, 3)
  if bh is None:
    bh = size + 1
  if bw is None:
    bw = size + 1
  # Build the base-frame (quadrant-0) geometry: input grid dims, the marker
  # top-left positions, and the per-block extent. The single-marker default
  # reproduces the original task byte-for-byte; the multi-marker branch mirrors
  # re_arc's generate_4522001f (independent h,w in 3-10, area-scaled marker
  # count, 3x output, fixed 4x4 blocks) so re_arc's verifier reproduces every
  # widened output.
  if grid_h is None and grid_w is None and count is None:
    ih, iw = size, size
    blk_h, blk_w = bh, bw
    oh, ow = 2 * bh + 1, 2 * bw + 1
    placements = [(0, 0)]
  else:
    ih = grid_h if grid_h is not None else common.randint(3, 10)
    iw = grid_w if grid_w is not None else common.randint(3, 10)
    blk_h, blk_w = 4, 4
    oh, ow = 3 * ih, 3 * iw
    noccs = max(0, count - 1) if count is not None \
        else common.randint(0, (ih * iw) // 9)
    forbidden = set()
    fli, flj = common.randint(0, ih - 2), common.randint(0, iw - 2)
    placements = [(fli, flj)]
    _forbid(forbidden, fli, flj)
    tries = 0
    while tries < 60 * noccs + 15 and len(placements) < noccs + 1:
      tries += 1
      li, lj = common.randint(0, ih - 2), common.randint(0, iw - 2)
      cells = ((li, lj), (li, lj + 1), (li + 1, lj), (li + 1, lj + 1))
      if any(cell in forbidden for cell in cells):
        continue
      placements.append((li, lj))
      _forbid(forbidden, li, lj)
  grid = common.grid(iw, ih)
  for li, lj in placements:
    grid[li][lj] = common.green()
    grid[li][lj + 1] = common.green()
    grid[li + 1][lj] = common.green()
    grid[li + 1][lj + 1] = common.red()
  canvas = common.grid(ow, oh)
  for li, lj in placements:
    for r in range(blk_h):
      for c in range(blk_w):
        canvas[li + r][lj + c] = common.green()
  output = _orient(canvas, quadrant)
  for li, lj in placements:
    for r in range(blk_h):
      for c in range(blk_w):
        canvas[li + blk_h + r][lj + blk_w + c] = common.green()
  output = _orient(canvas, quadrant)
  grid = _orient(grid, quadrant)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(quadrant=0),
      generate(quadrant=3),
  ]
  test = [
      generate(quadrant=1),
  ]
  return {"train": train, "test": test}
