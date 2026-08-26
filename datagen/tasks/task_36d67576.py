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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             megarows=None, megacols=None, megarotates=None, num_sprites=None,
             num_comp_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    megarows: a list of vertical coordinates for sprite placement
    megacols: a list of horizontal coordinates for sprite placement
    megarotates: a list of digits representing the rotations of mega-sprites
    num_sprites: how many mega-sprites to place (template + completions)
    num_comp_colors: how many distinct hidden "completion" colors to use
  """
  if width is None:
    width, height = common.randint(13, 30), common.randint(13, 30)
    # Choose the dimensions of the rainbow sprites.
    sprite_type, wide, tall = common.randint(0, 2), 3, 3
    if sprite_type == 1: wide, tall = 4, 2
    if sprite_type == 2: wide, tall = 5, 1
    # Choose the positions of the yellow pixels.
    while True:
      pixels = common.sample(common.all_pixels(wide, tall), 5)
      if common.diagonally_connected(pixels): break
    extra_pixels, colors, extra_colors = [], [4] * len(pixels), []
    # The marker (red) is always visible in the partial sprites; the remaining
    # colors are the hidden "completion" colors that the template reveals. Draw
    # a variable-size palette of completion colors (mirrors re_arc's ncols band).
    comp_pool = [common.blue(), common.green(), common.gray(), common.pink(),
                 common.orange(), common.cyan(), common.maroon()]
    if num_comp_colors is None:
      num_comp_colors = common.randint(1, len(comp_pool))
    num_comp_colors = max(1, min(num_comp_colors, len(comp_pool)))
    wanted_colors = [common.red()] + common.sample(comp_pool, num_comp_colors)
    # Choose the positions of the other pixels (make sure they don't clobber).
    # Bounded tries so a crowded sprite can never hang; a color that finds no
    # free adjacent cell is simply skipped (fewer completion colors that time).
    for color in wanted_colors:
      placed = False
      for _ in range(200):
        pixel, angle = common.choice(pixels), common.randint(0, 3)
        r, c = pixel[0], pixel[1]
        if angle == 0: r -= 1
        if angle == 1: r += 1
        if angle == 2: c -= 1
        if angle == 3: c += 1
        # The red pixel is important; don't place it in the center.
        if color == common.red() and (r == tall // 2 or c == wide // 2):
          continue
        if (r, c) not in pixels and (r, c) not in extra_pixels:
          placed = True
          break
      if not placed:
        continue
      extra_pixels.append((r, c))
      extra_colors.append(color)
    # Add the extra pixels & colors, and shift the row/col values if needed.
    colors, pixels = colors + extra_colors, pixels + extra_pixels
    rows, cols = zip(*pixels)
    rows, cols = [r - min(rows) for r in rows], [c - min(cols) for c in cols]
    wide, tall = max(cols) + 1, max(rows) + 1
    # Choose how many mega-sprites to place; scale with the grid area (re_arc
    # packs many occurrences) but cap so the greedy placement stays feasible.
    if num_sprites is None:
      area_cap = (width * height) // ((wide + 1) * (tall + 1))
      num_sprites = common.randint(2, max(3, min(26, area_cap)))
    # Place the mega-sprites greedily with bounded tries (never hangs); the
    # template plus every completion sprite must be mutually non-overlapping.
    megarows, megacols, megawides, megatalls, megarotates = [], [], [], [], []
    tries = 0
    while len(megarotates) < num_sprites and tries < num_sprites * 40:
      tries += 1
      megarotate = common.randint(0, 3)
      w, t = (tall, wide) if megarotate == 1 else (wide, tall)
      if width - w < 0 or height - t < 0:
        continue
      r, c = common.randint(0, height - t), common.randint(0, width - w)
      if common.overlaps(megarows + [r], megacols + [c],
                         megawides + [w], megatalls + [t], 1):
        continue
      megarows.append(r)
      megacols.append(c)
      megawides.append(w)
      megatalls.append(t)
      megarotates.append(megarotate)

  grid, output = common.grids(width, height)
  wide, tall = max(cols) + 1, max(rows) + 1
  for i, megarotate in enumerate(megarotates):
    mr, mc = megarows[i], megacols[i]
    for row, col, color in zip(rows, cols, colors):
      r, c = row, col
      if megarotate == 1: r, c = c, tall - 1 - r
      if megarotate == 2: r, c = tall - 1 - r, wide - 1 - c
      if megarotate == 3: c = wide - 1 - c
      output[mr + r][mc + c] = color
      if i != 0 and color not in [common.yellow(), common.red()]: continue
      grid[mr + r][mc + c] = color
  output = [row[:] for row in grid]

  def complete_sprite(i):
    if i >= len(megarotates):
      return
    mr, mc = megarows[i], megacols[i]
    megarotate = megarotates[i]
    for row, col, color in zip(rows, cols, colors):
      r, c = row, col
      if megarotate == 1: r, c = c, tall - 1 - r
      if megarotate == 2: r, c = tall - 1 - r, wide - 1 - c
      if megarotate == 3: c = wide - 1 - c
      output[mr + r][mc + c] = color

  for sprite_index in range(1, len(megarotates)):
    complete_sprite(sprite_index)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[1, 3, 4, 0, 1, 2, 3, 4, 0, 2, 4],
               colors=[1, 1, 2, 4, 4, 4, 4, 4, 3, 3, 3], megarows=[1, 2, 7],
               megacols=[1, 9, 3], megarotates=[0, 1, 2]),
      generate(width=13, height=13, rows=[0, 1, 1, 1, 1, 2, 3, 3, 3, 3],
               cols=[2, 0, 1, 2, 3, 2, 0, 1, 2, 3],
               colors=[2, 4, 4, 4, 1, 4, 3, 3, 4, 3], megarows=[1, 4, 9],
               megacols=[2, 8, 3], megarotates=[0, 3, 1]),
      generate(width=13, height=13, rows=[0, 0, 1, 1, 1, 1, 2, 2, 3],
               cols=[2, 3, 0, 1, 2, 3, 1, 2, 2],
               colors=[4, 2, 1, 4, 4, 4, 3, 4, 1], megarows=[1, 5, 8],
               megacols=[1, 7, 3], megarotates=[0, 3, 2]),
  ]
  test = [
      generate(width=15, height=14, rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
               cols=[0, 1, 0, 1, 2, 0, 2, 3, 1, 2, 3],
               colors=[1, 3, 4, 4, 2, 4, 4, 3, 4, 4, 1], megarows=[2, 3, 9, 8],
               megacols=[2, 10, 0, 7], megarotates=[0, 1, 2, 3]),
  ]
  return {"train": train, "test": test}
