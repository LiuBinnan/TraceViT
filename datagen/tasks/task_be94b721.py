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


def _dneighbors(cell):
  i, j = cell
  return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


def _neighbors(cell):
  i, j = cell
  return ((i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
          (i, j - 1), (i, j + 1),
          (i + 1, j - 1), (i + 1, j), (i + 1, j + 1))


def _grow(avail, target):
  """Grows a random 4-connected blob of up to `target` cells within `avail`.

  `avail` (the set of still-free grid indices) is only read, not mutated.
  Because every placed object's 8-neighborhood is removed from `avail` before
  the next blob is grown, staying inside `avail` keeps blobs >=1 cell apart --
  so each object is its own connected component of a single color.
  """
  cells = sorted(avail)
  shp = {cells[common.randint(0, len(cells) - 1)]}
  cand = set(d for d in _dneighbors(next(iter(shp))) if d in avail)
  while len(shp) < target and cand:
    cl = sorted(cand)
    nxt = cl[common.randint(0, len(cl) - 1)]
    cand.discard(nxt)
    shp.add(nxt)
    for d in _dneighbors(nxt):
      if d in avail and d not in shp:
        cand.add(d)
  return shp


def _consume(avail, shp):
  """Removes a placed blob and its 8-neighborhood from the free set."""
  for cell in shp:
    avail.discard(cell)
    for d in _neighbors(cell):
      avail.discard(d)


def _bg_component_sizes(allcells, occupied):
  """Sizes (descending) of the 4-connected background regions."""
  free = allcells - occupied
  seen, sizes = set(), []
  for start in free:
    if start in seen:
      continue
    stack, sz = [start], 0
    seen.add(start)
    while stack:
      cur = stack.pop()
      sz += 1
      for d in _dneighbors(cur):
        if d in free and d not in seen:
          seen.add(d)
          stack.append(d)
    sizes.append(sz)
  sizes.sort(reverse=True)
  return sizes


def _build(height, width, no):
  """Lays out the answer blob (index 0) plus `no` smaller distractor blobs.

  Returns the list of sprite index-sets, or None if the layout is ill-posed:
  the answer must be the unique largest *object*, which means the background
  must stay the single dominant region and no background pocket may rival the
  answer sprite (else "the largest object" is ambiguous -- exactly what the
  canonical solver would then resolve differently).
  """
  allcells = set((i, j) for i in range(height) for j in range(width))
  avail = set(allcells)
  nc = common.randint(no + 1, max(no + 1, 2 * no))
  primary = _grow(avail, nc)
  _consume(avail, primary)
  prim_size = len(primary)
  sprites = [primary]
  for _ in range(no):
    if not avail:
      break
    nc2 = common.randint(1, max(1, prim_size - 1))
    sprites.append(_grow(avail, nc2))
    _consume(avail, sprites[-1])
  occupied = set()
  for sprite in sprites:
    occupied |= sprite
  bg = _bg_component_sizes(allcells, occupied)
  if not bg or bg[0] <= prim_size or (len(bg) > 1 and bg[1] >= prim_size):
    return None
  return sprites


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             brows=None, bcols=None, colors=None, count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the sprites
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    colors: a list of digits representing the colors to be used
    count: the number of smaller distractor sprites next to the answer sprite
  """
  if width is None:
    sprites = None
    for _ in range(64):
      height = common.randint(6, 30)
      width = common.randint(6, 30)
      # Number of smaller distractor sprites, area-scaled like re_arc's
      # `no = unifint(., ., (3, h*w//16))`. An explicit `count` overrides the
      # sampled value; GUARD-cap `no` by the same area budget so the sprites
      # stay placeable and the background stays the dominant region.
      cap = max(1, (width * height) // 16)
      no = count if count is not None else common.randint(3, max(3, cap))
      no = min(max(0, no), cap)
      sprites = _build(height, width, no)
      if sprites is not None:
        break
    if sprites is None:
      # Guaranteed well-posed fallback (a wide/dense grid kept resisting a
      # clean layout): one small blob in the interior, so the background is a
      # single region that dwarfs it.
      height = common.randint(6, 30)
      width = common.randint(6, 30)
      interior = set((i, j) for i in range(1, height - 1)
                     for j in range(1, width - 1))
      sprites = [_grow(interior, common.randint(2, min(6, len(interior))))]
    # Re-express the sprites as this task's placement variables (sprite 0 is
    # the answer): brows/bcols locate each sprite's bounding box, rows/cols are
    # the pixels relative to it, idxs tags each pixel with its sprite.
    rows, cols, idxs, brows, bcols = [], [], [], [], []
    for idx, sprite in enumerate(sprites):
      brow = min(i for i, j in sprite)
      bcol = min(j for i, j in sprite)
      brows.append(brow)
      bcols.append(bcol)
      for (i, j) in sorted(sprite):
        rows.append(i - brow)
        cols.append(j - bcol)
        idxs.append(idx)
    colors = [common.random_color() for _ in sprites]

  wide = max([c for c, i in zip(cols, idxs) if not i]) + 1
  tall = max([r for r, i in zip(rows, idxs) if not i]) + 1
  grid, output = common.grid(width, height), common.grid(wide, tall)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r + brows[idx]][c + bcols[idx]] = colors[idx]
    if not idx: output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=7,
               rows=[0, 0, 1, 2, 2, 3, 3, 3, 0, 0, 1, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 1, 1, 2, 0, 1, 2, 0, 1, 1, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2],
               brows=[1, 1, 2], bcols=[1, 5, 8], colors=[2, 3, 1]),
      generate(width=10, height=5,
               rows=[0, 0, 1, 1, 2, 2, 0, 1, 1, 1, 2, 0, 0, 1],
               cols=[0, 1, 0, 1, 0, 1, 1, 0, 1, 2, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               brows=[1, 1, 0], bcols=[4, 0, 7], colors=[4, 3, 6]),
      generate(width=11, height=6,
               rows=[0, 0, 0, 1, 2, 2, 3, 3, 0, 0, 1, 2, 3, 0, 1, 1, 2],
               cols=[0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 1, 2], bcols=[1, 8, 5], colors=[8, 7, 2]),
      generate(width=9, height=7,
               rows=[0, 0, 0, 1, 2, 2, 2, 0, 1, 1, 2, 0, 0, 0, 1],
               cols=[0, 1, 2, 1, 0, 1, 2, 0, 0, 1, 1, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 1, 4], bcols=[6, 3, 0], colors=[2, 7, 8]),
  ]
  test = [
      generate(width=9, height=9,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0,
                     1, 1, 0, 1, 1, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 2, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2,
                     0, 1, 0, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                     2, 2, 3, 3, 3, 3],
               brows=[2, 6, 7, 1], bcols=[3, 6, 1, 0], colors=[3, 6, 5, 4]),
  ]
  return {"train": train, "test": test}
