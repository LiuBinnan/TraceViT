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
             megarows=None, megacols=None, mags=None, hflips=None, vflips=None,
             b=None, num_megas=None, sprite_size=None, max_mag=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where 6aa20dc0 should be placed
    mags: a list of sprite magnifiers to be used
    hflips: a list of horizontal flips to be used
    vflips: a list of vertical flips to be used
    b: the integer used for all background cells
  """
  if rows is None:
    while True:
      cand_width = common.randint(10, 30) if width is None else width
      cand_height = common.randint(10, 30) if height is None else height
      cand_sprite_size = (
          common.randint(2, 3) if sprite_size is None else sprite_size)
      cand_max_mag = 4 if max_mag is None else max_mag
      cand_max_mag = min(cand_max_mag,
                         max(1, min(cand_width, cand_height) //
                             cand_sprite_size))
      max_megas = max(
          2, (cand_width * cand_height) //
          (cand_sprite_size * cand_sprite_size * 2))
      cand_num_megas = (
          common.randint(2, min(35, max_megas))
          if num_megas is None else num_megas)
      cand_num_megas = max(2, min(cand_num_megas, 35))
      color_list = common.random_colors(4)
      # First, generate the (diagonally symmetric) sprite.
      end = cand_sprite_size - 1
      rows, cols, colors = [0, end], [0, end], [color_list[0], color_list[1]]
      pixels = [(r, c) for r in range(cand_sprite_size)
                for c in range(cand_sprite_size)
                if (r, c) not in [(0, 0), (end, end)]]
      n_extra = common.randint(
          1, max(1, (cand_sprite_size * cand_sprite_size - 2) // 2))
      pixels = set(common.sample(pixels, n_extra))
      pixels.add(common.choice([(0, 1), (1, 0)]))
      pixels.add(common.choice([(end - 1, end), (end, end - 1)]))
      pixels |= set((col, row) for row, col in pixels)
      for row, col in sorted(pixels):
        rows.append(row)
        cols.append(col)
        colors.append(color_list[2])
      # Second, place the magnified sprites.
      megarows, megacols, megamags, mags = [], [], [], []
      tries = 0
      while len(mags) < cand_num_megas and tries < cand_num_megas * 80:
        tries += 1
        mag = 1 if not mags else common.randint(1, cand_max_mag)
        mega_size = cand_sprite_size * mag
        if mega_size > cand_height or mega_size > cand_width:
          continue
        megarow = common.randint(0, cand_height - mega_size)
        megacol = common.randint(0, cand_width - mega_size)
        if common.overlaps(megarows + [megarow], megacols + [megacol],
                           megamags + [mega_size],
                           megamags + [mega_size], 2):
          continue
        megarows.append(megarow)
        megacols.append(megacol)
        megamags.append(mega_size)
        mags.append(mag)
      if len(mags) >= 2:
        width, height = cand_width, cand_height
        break
    hflips = [common.randint(0, 1) for _ in mags]
    vflips = [common.randint(0, 1) for _ in mags]
    # Third, set the background color.
    b = color_list[3]

  grid, output = common.grids(width, height, b)
  for idx, mag in enumerate(mags):
    mrow, mcol, h, v = megarows[idx], megacols[idx], hflips[idx], vflips[idx]
    for row, col, color in zip(rows, cols, colors):
      for dr in range(mag):
        for dc in range(mag):
          r, c = row * mag + dr, col * mag + dc
          extent = (max(rows + cols) + 1) * mag
          r, c = extent - r - 1 if v else r, extent - c - 1 if h else c
          if idx > 0 and (row, col) not in [
              (0, 0), (max(rows + cols), max(rows + cols))]:
            continue  # hide pixels
          grid[mrow + r][mcol + c] = color

  def reveal_sprite(idx):
    if idx >= len(mags):
      return
    mag = mags[idx]
    mrow, mcol, h, v = megarows[idx], megacols[idx], hflips[idx], vflips[idx]
    for row, col, color in zip(rows, cols, colors):
      for dr in range(mag):
        for dc in range(mag):
          r, c = row * mag + dr, col * mag + dc
          extent = (max(rows + cols) + 1) * mag
          r, c = extent - r - 1 if v else r, extent - c - 1 if h else c
          output[mrow + r][mcol + c] = color

  reveal_sprite(0)
  reveal_sprite(1)
  reveal_sprite(2)
  reveal_sprite(3)
  reveal_sprite(4)
  reveal_sprite(5)
  reveal_sprite(6)
  reveal_sprite(7)
  reveal_sprite(8)
  reveal_sprite(9)
  reveal_sprite(10)
  reveal_sprite(11)
  reveal_sprite(12)
  reveal_sprite(13)
  reveal_sprite(14)
  reveal_sprite(15)
  reveal_sprite(16)
  reveal_sprite(17)
  reveal_sprite(18)
  reveal_sprite(19)
  reveal_sprite(20)
  reveal_sprite(21)
  reveal_sprite(22)
  reveal_sprite(23)
  reveal_sprite(24)
  reveal_sprite(25)
  reveal_sprite(26)
  reveal_sprite(27)
  reveal_sprite(28)
  reveal_sprite(29)
  reveal_sprite(30)
  reveal_sprite(31)
  reveal_sprite(32)
  reveal_sprite(33)
  reveal_sprite(34)
  reveal_sprite(35)
  reveal_sprite(36)
  reveal_sprite(37)
  reveal_sprite(38)
  reveal_sprite(39)
  reveal_sprite(40)
  reveal_sprite(41)
  reveal_sprite(42)
  reveal_sprite(43)
  reveal_sprite(44)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=20, rows=[0, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 2], colors=[2, 8, 8, 8, 8, 8, 3],
               megarows=[4, 1, 11], megacols=[5, 13, 5], mags=[1, 1, 2],
               hflips=[0, 0, 1], vflips=[0, 0, 0], b=1),
      generate(width=21, height=20, rows=[0, 0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 0, 2, 0, 1, 2], colors=[6, 1, 1, 1, 1, 1, 1, 2],
               megarows=[2, 7], megacols=[3, 5], mags=[1, 3],
               hflips=[1, 0], vflips=[0, 1], b=4),
      generate(width=22, height=21, rows=[0, 0, 1, 1, 1, 2, 2],
               cols=[0, 1, 0, 1, 2, 1, 2], colors=[2, 3, 3, 3, 3, 3, 4],
               megarows=[5, 10, 14], megacols=[6, 13, 5], mags=[1, 1, 1],
               hflips=[0, 1, 1], vflips=[0, 1, 0], b=8),
  ]
  test = [
      generate(width=22, height=22, rows=[0, 0, 1, 1, 2, 2],
               cols=[0, 1, 0, 2, 1, 2], colors=[4, 8, 8, 8, 8, 1],
               megarows=[4, 1, 13, 13], megacols=[5, 10, 1, 11],
               mags=[1, 3, 1, 2], hflips=[1, 0, 1, 0], vflips=[0, 0, 1, 1],
               b=3),
  ]
  return {"train": train, "test": test}
