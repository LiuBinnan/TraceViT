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


def generate(width=None, height=None, rows=None, cols=None, boxrow=None,
             boxcol=None, spriterow=None, spritecol=None, magnifier=None,
             color=None, num_colors=None, sprite_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxrow: a vertical coordinate where the box should be placed
    boxcol: a horizontal coordinate where the box should be placed
    spriterow: a vertical coordinate where the sprite should be placed
    spritecol: a horizontal coordinates where the sprite should be placed
    magnifier: a list of vertical coordinates where magnifiers should be placed
    color: a digit representing a color to be used
    num_colors: the number of colors to use in the sprite
    sprite_colors: a list of colors, one per sprite pixel
  """
  if rows is None:
    if width is None:
      width = common.randint(6, 30)
    if height is None:
      height = common.randint(6, 30)
    while True:
      spriteh = common.randint(2, min(5, (height - 2) // 2))
      spritew = common.randint(2, min(5, (width - 2) // 2))
      max_magnifier = min((height - spriteh - 2) // spriteh,
                          (width - 2) // spritew)
      if max_magnifier >= 1:
        break
    magnifier = common.randint(1, max_magnifier)
    path = [(0, 0)]
    while path[-1] != (spriteh - 1, spritew - 1):
      r, c = path[-1]
      if r == spriteh - 1:
        c += 1
      elif c == spritew - 1:
        r += 1
      else:
        direction = common.randint(0, 5)
        if direction != 4:
          r += 1
        if direction != 5:
          c += 1
      path.append((r, c))
    pixels = set(path)
    extras = common.randint(0, min(9 - len(pixels), spriteh * spritew - len(pixels)))
    for _ in range(extras):
      candidates = []
      for r, c in pixels:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
              continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < spriteh and 0 <= nc < spritew and (nr, nc) not in pixels:
              candidates.append((nr, nc))
      if not candidates:
        break
      pixels.add(candidates[common.randint(0, len(candidates) - 1)])
    pixels = common.shuffle(list(pixels))
    rows, cols = [r for r, _ in pixels], [c for _, c in pixels]
    outh, outw = spriteh * magnifier + 2, spritew * magnifier + 2
    boxrow = common.randint(0, height - outh - spriteh)
    boxcol = common.randint(0, width - outw)
    spriterow = common.randint(boxrow + outh, height - spriteh)
    spritecol = common.randint(0, width - spritew)
    if num_colors is None:
      num_colors = common.randint(1, 8)
    palette = common.random_colors(min(num_colors, len(rows)),
                                   exclude=[common.red()])
    sprite_colors = common.shuffle(
        [palette[i % len(palette)] for i in range(len(rows))])

  spriteh, spritew, sprite_colors = (max(rows) + 1, max(cols) + 1,
                                     sprite_colors or [color] * len(rows))
  outh, outw = spriteh * magnifier + 2, spritew * magnifier + 2
  grid, output = common.grid(width, height), common.grid(outw, outh)
  for idx, (r, c) in enumerate(zip(rows, cols)):
    grid[spriterow + r][spritecol + c] = sprite_colors[idx]

  def draw_border():
    for i in range(outw):
      output[0][i] = output[outh - 1][i] = common.red()
      grid[boxrow + 0][boxcol + i] = grid[boxrow + outh - 1][boxcol + i] = common.red()
    for i in range(outh):
      output[i][0] = output[i][outw - 1] = common.red()
      grid[boxrow + i][boxcol + 0] = grid[boxrow + i][boxcol + outw - 1] = common.red()

  def reveal_pixel(idx):
    if idx >= len(rows):
      return
    r, c = rows[idx], cols[idx]
    for dr in range(magnifier):
      for dc in range(magnifier):
        output[r * magnifier + dr + 1][c * magnifier + dc + 1] = sprite_colors[idx]

  draw_border()
  reveal_pixel(0)
  reveal_pixel(1)
  reveal_pixel(2)
  reveal_pixel(3)
  reveal_pixel(4)
  reveal_pixel(5)
  reveal_pixel(6)
  reveal_pixel(7)
  reveal_pixel(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=18, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1],
               boxrow=7, boxcol=6, spriterow=2, spritecol=5, magnifier=2,
               color=8),
      generate(width=22, height=19, rows=[0, 0, 1, 2, 2], cols=[1, 2, 0, 1, 2],
               boxrow=2, boxcol=2, spriterow=9, spritecol=10, magnifier=1,
               color=1),
      generate(width=24, height=21, rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 2, 2],
               boxrow=1, boxcol=2, spriterow=15, spritecol=13, magnifier=3,
               color=4),
  ]
  test = [
      generate(width=26, height=24, rows=[0, 1, 1, 2], cols=[1, 0, 2, 1],
               boxrow=4, boxcol=2, spriterow=4, spritecol=20, magnifier=4,
               color=3),
  ]
  return {"train": train, "test": test}
