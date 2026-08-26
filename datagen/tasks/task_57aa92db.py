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


def generate(width=None, height=None, rows=None, cols=None, brows=None,
             bcols=None, bmags=None, colors=None, shows=None, pcolor=None,
             num_sprites=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    bmags: a list of sprite magnifiers
    colors: a list of colors to be used for the sprites
    shows: a list of indices of the pixel to be shown for each sprite
    pcolor: a color to be used for the "signature" pixel
    num_sprites: how many sprites to place (area-scaled when omitted)
  """
  if width is None:
    wide, tall = 3, 3
    # Choose the sprite shape first: its cell count governs how densely a grid
    # can be filled before the background stops dominating.
    num_pixels = common.randint(3, 8)
    pixels = common.continuous_creature(num_pixels, wide, tall)
    rows, cols = zip(*pixels)
    # Then choose grid dimensions and greedily place as many sprites as fit. The
    # target count is area-scaled (mirroring the re_arc reference, which scales
    # its occurrence count by grid area); a per-grid magnifier regime trades
    # between many small sprites and a few large ones, spreading both the object
    # count and the fill density. Placement is incremental so wide counts can
    # never hang the way an all-or-nothing overlap retry would.
    while True:
      width, height = common.randint(10, 30), common.randint(10, 30)
      regime = (0, 0, 0, 1, 2, 2)[common.randint(0, 5)]
      mags = ((1,), (1, 1, 2, 2, 3, 4), (2, 2, 3, 3, 4, 4))[regime]
      # A single empty cell between sprites is enough to keep them separate
      # objects (this is exactly what the re_arc reference enforces); the tiny-
      # sprite regime uses that tighter spacing so many more can pack in.
      spc = 1 if regime == 0 else 2
      capn = max(2, (width * height) // 20)  # Area-scaled ceiling on the count.
      if num_sprites is not None:
        target = max(2, num_sprites)
      elif regime == 0:
        target = capn  # Pack small sprites to the limit: wide object-count range.
      else:
        target = common.randint(2, capn)
      cap = width * height // 2  # Keep <=50% filled so the background dominates.
      brows, bcols, bmags, wides, talls, used = [], [], [], [], [], 0
      tries, maxtr = 0, min(25 * target + 50, 900)
      while len(brows) < target and tries < maxtr:
        tries += 1
        bmag = 1 if not brows else mags[common.randint(0, len(mags) - 1)]
        w, t = bmag * wide, bmag * tall
        if w > width or t > height: continue  # Too big for the grid.
        if brows and used + num_pixels * bmag * bmag > cap: continue  # Too full.
        br, bc = common.randint(0, height - t), common.randint(0, width - w)
        if common.overlaps(brows + [br], bcols + [bc],
                           wides + [w], talls + [t], spc): continue  # Overlaps.
        brows.append(br); bcols.append(bc); bmags.append(bmag)
        wides.append(w); talls.append(t)
        used += num_pixels * bmag * bmag
      if len(brows) >= 2: break  # Need the key sprite plus >=1 to complete.
    num_sprites = len(brows)  # However many actually fit.
    # Each sprite reveals a connected sub-blob of the shape that includes the
    # first (signature) pixel. Partials reveal 2..num_pixels-1 cells -- always
    # fewer than the fully drawn key, so the key stays the largest single-scale
    # object; this mirrors re_arc's variable-size reveal and spreads the fill
    # density beyond a fixed two-cell hint.
    nbrs = [[j for j in range(len(pixels))
             if abs(pixels[i][0] - pixels[j][0])
             + abs(pixels[i][1] - pixels[j][1]) == 1]
            for i in range(len(pixels))]
    shows = []
    for _ in range(num_sprites):
      blob, frontier = [0], list(nbrs[0])
      want = common.randint(2, num_pixels - 1)
      while len(blob) < want and frontier:
        p = frontier.pop(common.randint(0, len(frontier) - 1))
        if p in blob:
          continue
        blob.append(p)
        frontier.extend(q for q in nbrs[p] if q not in blob)
      shows.append(tuple(blob))
    # One signature color shared by every sprite and one key color; the other
    # sprites draw with replacement from a random-sized subset of the leftover
    # colors. Replacement lets the sprite count grow past the number of distinct
    # colors, while the per-grid subset keeps the palette varied (rather than
    # every crowded grid converging on the full ten-color palette).
    pcolor = common.random_color()
    mainc = common.random_color(exclude=[pcolor])
    pool = [c for c in range(1, 10) if c not in (pcolor, mainc)]
    subset = common.sample(pool, common.randint(1, len(pool)))
    colors = [mainc] + [subset[common.randint(0, len(subset) - 1)]
                        for _ in range(num_sprites - 1)]

  def draw_sprite(idx):
    bmag = bmags[idx]
    brow, bcol, color, show = brows[idx], bcols[idx], colors[idx], shows[idx]
    shown = (0, show) if isinstance(show, int) else show
    for i in range(len(rows)):
      row, col = rows[i], cols[i]
      for dr in range(bmag):
        for dc in range(bmag):
          r, c = brow + row * bmag + dr, bcol + col * bmag + dc
          common.draw(output, r, c, color if i else pcolor)
          if not idx or i in shown:
            common.draw(grid, r, c, color if i else pcolor)

  grid, output = common.grids(width, height)
  for idx in range(min(1, len(colors))):
    draw_sprite(idx)
  for idx in range(1, len(colors)):
    draw_sprite(idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=16, rows=[1, 1, 1, 0, 2], cols=[2, 1, 0, 1, 1],
               brows=[1, 7], bcols=[2, 3], bmags=[1, 2], colors=[3, 4],
               shows=[0, 1], pcolor=1),
      generate(width=18, height=16, rows=[1, 1, 1, 1, 0, 2],
               cols=[0, 1, 2, 3, 3, 3], brows=[1, 6, 11], bcols=[2, 10, 5],
               bmags=[1, 1, 1], colors=[8, 6, 3], shows=[0, 1, 1], pcolor=2),
      generate(width=18, height=17, rows=[1, 0, 2, 1, 0, 2, 1, 0],
               cols=[1, 1, 0, 0, 0, 2, 2, 2], brows=[2, 7], bcols=[2, 6],
               bmags=[1, 3], colors=[1, 8], shows=[0, 1], pcolor=4),
      generate(width=18, height=15, rows=[1, 1, 1, 0, 2], cols=[2, 1, 0, 2, 2],
               brows=[3, 1, 7], bcols=[12, 3, 2], bmags=[1, 1, 2],
               colors=[8, 3, 4], shows=[0, 1, 3], pcolor=2),
  ]
  test = [
      generate(width=30, height=19, rows=[1, 1, 1, 0, 0, 2, 2],
               cols=[1, 0, 2, 1, 2, 0, 1], brows=[2, 0, 3, 8],
               bcols=[3, 10, 17, 4], bmags=[1, 3, 4, 2], colors=[8, 4, 2, 3],
               shows=[0, 1, 2, 6], pcolor=1),
  ]
  return {"train": train, "test": test}
