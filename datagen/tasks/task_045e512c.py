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


def generate(rows=None, cols=None, srow=None, scol=None, rdirs=None, cdirs=None,
             colors=None, size=21, height=None, width=None, obj_height=None,
             obj_width=None, density=None, num_colors=None,
             num_directions=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    srow: the vertical coordinate of the middle sprite
    scol: the horizontal coordinate of the middle sprite
    rdirs: a list of vertical directions to stamp the sprite
    cdirs: a list of horizontal directions to stamp the sprite
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    obj_height: the height of the sprite to sample
    obj_width: the width of the sprite to sample
    density: the number of extra cells to add to the sprite backbone
    num_colors: the size of the direction-color pool
    num_directions: the number of non-center directions to stamp
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    sampled_rows = True
    # First, choose a connected sprite that touches all four sides.
    if obj_height is None: obj_height = common.randint(2, min(4, (height - 2) // 3))
    if obj_width is None: obj_width = common.randint(2, min(4, (width - 2) // 3))
    vcol = common.randint(0, obj_width - 1)
    hrow = common.randint(0, obj_height - 1)
    pixels = [(r, vcol) for r in range(obj_height)]
    pixels += [(hrow, c) for c in range(obj_width)]
    pixels = common.remove_duplicates(pixels)
    rem = []
    for r in range(obj_height):
      for c in range(obj_width):
        if (r, c) not in pixels: rem.append((r, c))
    extra = common.randint(0, len(rem)) if density is None else density
    extra = min(max(0, extra), len(rem))
    for _ in range(extra):
      frontier = []
      for pixel in rem:
        r, c = pixel
        if (r - 1, c) in pixels or (r + 1, c) in pixels:
          frontier.append(pixel)
        elif (r, c - 1) in pixels or (r, c + 1) in pixels:
          frontier.append(pixel)
      if not frontier: break
      pixel = common.choice(frontier)
      pixels.append(pixel)
      rem.remove(pixel)
    rows, cols = zip(*common.shuffle(pixels))
    rows, cols = list(rows), list(cols)
    # Second, choose a placement for the middle sprite.
    srow = common.randint(obj_height + 1, height - 2 * obj_height - 1)
    scol = common.randint(obj_width + 1, width - 2 * obj_width - 1)
    # Third, sample directions to stamp the sprite.
    dirs = []
    for rdir in [-1, 0, 1]:
      for cdir in [-1, 0, 1]:
        if rdir == 0 and cdir == 0: continue
        dirs.append((rdir, cdir))
    ndirs = common.randint(1, 8) if num_directions is None else num_directions
    ndirs = min(max(1, ndirs), len(dirs))
    dirs = [(0, 0)] + common.sample(dirs, ndirs)
    rdirs, cdirs = zip(*dirs)
    color = common.random_color()  # We'll pick a special color for the middle.
    ncols = common.randint(1, 8) if num_colors is None else num_colors
    ncols = min(max(1, ncols), 8)
    ccols = common.random_colors(ncols, exclude=[color])
    colors = [color] + [ccols[i % ncols] for i in range(len(dirs) - 1)]
    colors = [colors[0]] + common.shuffle(colors[1:])
  else:
    sampled_rows = False

  grid = common.grid(width, height)
  def put(thegrid, r, c, thecolor):
    if r >= 0 and r < height and c >= 0 and c < width:
      thegrid[r][c] = thecolor

  sprite_height = max(rows) + 1
  sprite_width = max(cols) + 1
  directions = list(zip(rdirs, cdirs, colors))

  def indicator_pixels_for(rdir, cdir):
    """Returns the visible edge of the first sprite in a direction."""
    indicator_pixels = []
    if sampled_rows:
      for (ir, ic) in zip(rows, cols):
        indicator = False
        if rdir == 1 and ir == 0: indicator = True
        if rdir == -1 and ir == sprite_height - 1: indicator = True
        if cdir == 1 and ic == 0: indicator = True
        if cdir == -1 and ic == sprite_width - 1: indicator = True
        if indicator: indicator_pixels.append((ir, ic))
      if len(indicator_pixels) == len(rows):
        indicator_pixels.pop()
    else:
      for (r, c) in zip(rows, cols):
        indicator = r * rdir + 1 - rdir + c * cdir + 1 - cdir < 2
        if indicator: indicator_pixels.append((r, c))
    return indicator_pixels

  for rdir, cdir, color in directions:
    row = srow + (sprite_height + 1) * rdir
    col = scol + (sprite_width + 1) * cdir
    if rdir == 0 and cdir == 0:
      for (r, c) in zip(rows, cols):
        put(grid, srow + r, scol + c, color)
    else:
      for (r, c) in indicator_pixels_for(rdir, cdir):
        put(grid, row + r, col + c, color)

  output = common.grid(width, height)

  def stamp_direction(idx):
    if idx >= len(directions):
      return
    rdir, cdir, color = directions[idx]
    row, col = srow, scol
    while True:
      row = row + (sprite_height + 1) * rdir
      col = col + (sprite_width + 1) * cdir
      for (r, c) in zip(rows, cols):
        put(output, row + r, col + c, color)
      if rdir == 0 and cdir == 0:
        break
      if row < -5 or row > height or col < -5 or col > width:
        break

  stamp_direction(0)
  stamp_direction(1)
  stamp_direction(2)
  stamp_direction(3)
  stamp_direction(4)
  stamp_direction(5)
  stamp_direction(6)
  stamp_direction(7)
  stamp_direction(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               srow=6, scol=6, rdirs=[0, 1, 0], cdirs=[0, 0, 1],
               colors=[8, 2, 3]),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], srow=7, scol=11,
               rdirs=[0, 0, -1, 0], cdirs=[0, -1, 0, 1], colors=[1, 2, 4, 4]),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 1, 0, 2, 1, 2], srow=7, scol=6,
               rdirs=[0, -1, 1], cdirs=[0, 1, 1], colors=[5, 6, 1]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 0, 2, 0, 2], srow=7,
               scol=6, rdirs=[0, -1, 0, 1], cdirs=[0, 1, 1, 0],
               colors=[8, 4, 2, 3]),
  ]
  return {"train": train, "test": test}
