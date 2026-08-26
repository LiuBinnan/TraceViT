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


def generate(size=None, spacing=None, linecolor=None, brow=None, bcol=None,
             colors=None, gh=None, gw=None, boxh=None, boxw=None,
             scaleh=None, scalew=None, num_colors=None, occ_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the input grid (in cells)
    spacing: the spacing between the lines (in pixels)
    linecolor: the color of the lines
    brow: the row of the box
    bcol: the column of the box
    colors: the colors of the pixels
    gh: the height of the input grid (in cells); defaults to size
    gw: the width of the input grid (in cells); defaults to size
    boxh: the height of the colored box (in cells); defaults to 3
    boxw: the width of the colored box (in cells); defaults to 3
    scaleh: the vertical spacing between lines; defaults to spacing
    scalew: the horizontal spacing between lines; defaults to spacing
    num_colors: the number of foreground colors
    occ_count: the requested number of colored output cells
  """
  if size is None:
    if boxh is None: boxh = common.randint(2, 6)
    if boxw is None: boxw = common.randint(2, 6)
    max_scaleh = max(2, (30 - 1) // max(boxh + 2, 1) - 1)
    max_scalew = max(2, (30 - 1) // max(boxw + 2, 1) - 1)
    if scaleh is None:
      scaleh = common.randint(2, max_scaleh)
    else:
      scaleh = max(2, min(scaleh, max_scaleh))
    if scalew is None:
      scalew = common.randint(2, max_scalew)
    else:
      scalew = max(2, min(scalew, max_scalew))
    if spacing is None: spacing = common.randint(2, 4)
    min_gh = boxh + 2
    min_gw = boxw + 2
    max_gh = max(min_gh, (30 + 1) // (scaleh + 1))
    max_gw = max(min_gw, (30 + 1) // (scalew + 1))
    gh = common.randint(min_gh, max_gh)
    gw = common.randint(min_gw, max_gw)
    linecolor = common.random_color()
    while True:
      brow = common.randint(0, gh - boxh - 2)
      bcol = common.randint(0, gw - boxw - 2)
      seed_capacity = ((boxh + 1) // 2) * ((boxw + 1) // 2)
      max_colors = min(8, boxh * boxw - 1, seed_capacity)
      if num_colors is None:
        color_count = common.randint(1, max_colors)
      else:
        color_count = max(1, min(num_colors, max_colors))
      if occ_count is None:
        ncolored = common.randint(color_count, boxh * boxw - 1)
      else:
        ncolored = max(color_count, min(occ_count, boxh * boxw - 1))
      colors = None
      for _ in range(200):
        color_list = common.random_colors(color_count, exclude=[linecolor])
        cand = [common.black() for _ in range(boxh * boxw)]

        def touches_other(row, col, hue):
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if (not dr) and (not dc): continue
              r, c = row + dr, col + dc
              if r < 0 or r >= boxh or c < 0 or c >= boxw: continue
              other = cand[r * boxw + c]
              if other != common.black() and other != hue:
                return True
          return False

        cells = [(r, c) for r in range(boxh) for c in range(boxw)]
        common.shuffle(cells)
        used = {hue: [] for hue in color_list}
        for hue in color_list:
          placed = False
          for row, col in list(cells):
            if cand[row * boxw + col] != common.black(): continue
            if touches_other(row, col, hue): continue
            cand[row * boxw + col] = hue
            used[hue].append((row, col))
            placed = True
            break
          if not placed: break
        if any(not used[hue] for hue in color_list): continue
        for _ in range(ncolored - color_count):
          options = []
          for hue in color_list:
            for row, col in used[hue]:
              for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                  if (not dr) and (not dc): continue
                  r, c = row + dr, col + dc
                  if r < 0 or r >= boxh or c < 0 or c >= boxw: continue
                  if cand[r * boxw + c] != common.black(): continue
                  if touches_other(r, c, hue): continue
                  options.append((hue, r, c))
          if not options: break
          hue, row, col = common.choice(options)
          cand[row * boxw + col] = hue
          used[hue].append((row, col))
        if len(set(cand)) != color_count + 1: continue  # Need all (plus black)
        rlist = [i // boxw for i, color in enumerate(cand)
                 if color != common.black()]
        clist = [i % boxw for i, color in enumerate(cand)
                 if color != common.black()]
        if (0 not in rlist or boxh - 1 not in rlist or
            0 not in clist or boxw - 1 not in clist):
          continue  # Can't have any empty margins.
        illegal = False
        for row in range(boxh):
          for col in range(boxw):
            if cand[row * boxw + col] == common.black(): continue
            for dr in [-1, 0, 1]:
              for dc in [-1, 0, 1]:
                if (not dr) and (not dc): continue
                r, c = row + dr, col + dc
                if r < 0 or r >= boxh or c < 0 or c >= boxw:
                  continue
                if cand[r * boxw + c] == common.black():
                  continue
                if cand[r * boxw + c] != cand[row * boxw + col]:
                  illegal = True
        # All pixels of the same color must be connected.
        for hue in color_list:
          rlist = [i // boxw for i, color in enumerate(cand) if color == hue]
          clist = [i % boxw for i, color in enumerate(cand) if color == hue]
          if not common.diagonally_connected(list(zip(rlist, clist))):
            illegal = True
        # A black cell is only recoverable if its four crossing corners are
        # not all the same color; a black cell ringed by a single color stamps
        # all four corners that color, making it look like a real cell of that
        # color. Reject such "donut hole" candidates.
        def corner(cells):
          for cr, cc in cells:
            if 0 <= cr < boxh and 0 <= cc < boxw:
              hue = cand[cr * boxw + cc]
              if hue != common.black(): return hue
          return common.black()
        for row in range(boxh):
          for col in range(boxw):
            if cand[row * boxw + col] != common.black(): continue
            corners = [
                corner([(row - 1, col - 1), (row - 1, col), (row, col - 1)]),
                corner([(row - 1, col), (row - 1, col + 1), (row, col + 1)]),
                corner([(row, col - 1), (row + 1, col - 1), (row + 1, col)]),
                corner([(row, col + 1), (row + 1, col), (row + 1, col + 1)]),
            ]
            if common.black() not in corners and len(set(corners)) == 1:
              illegal = True
        if not illegal:
          colors = cand
          break
      if colors is not None: break

  if gh is None: gh = size
  if gw is None: gw = size
  if boxh is None: boxh = 3
  if boxw is None or scaleh is None or scalew is None:
    if boxw is None: boxw = 3
    if scaleh is None: scaleh = spacing
    if scalew is None: scalew = spacing

  grid = [[linecolor if ((r + 1) % (scaleh + 1) == 0 or
                         (c + 1) % (scalew + 1) == 0) else common.black()
           for c in range(gw * (scalew + 1) - 1)]
          for r in range(gh * (scaleh + 1) - 1)]
  output = common.grid(len(grid[0]), len(grid))
  for row in range(boxh):
    for col in range(boxw):
      if colors[row * boxw + col] == common.black(): continue
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        r = (brow + row + dr + 1) * (scaleh + 1) - 1
        c = (bcol + col + dc + 1) * (scalew + 1) - 1
        grid[r][c] = colors[row * boxw + col]
        output[r][c] = colors[row * boxw + col]
  output = common.grid(boxw, boxh)
  for row in range(boxh):
    for col in range(boxw):
      if colors[row * boxw + col] == common.black(): continue
      output[row][col] = colors[row * boxw + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, spacing=2, linecolor=4, brow=1, bcol=1,
               colors=[1, 0, 3, 1, 0, 0, 1, 0, 0]),
      generate(size=7, spacing=3, linecolor=3, brow=1, bcol=0,
               colors=[0, 2, 0, 2, 0, 0, 0, 0, 8]),
      generate(size=10, spacing=2, linecolor=1, brow=3, bcol=4,
               colors=[6, 6, 0, 0, 0, 0, 3, 3, 3]),
      generate(size=7, spacing=3, linecolor=8, brow=1, bcol=1,
               colors=[1, 0, 2, 0, 0, 2, 2, 2, 2]),
  ]
  test = [
      generate(size=6, spacing=4, linecolor=2, brow=0, bcol=0,
               colors=[1, 0, 4, 0, 0, 0, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
