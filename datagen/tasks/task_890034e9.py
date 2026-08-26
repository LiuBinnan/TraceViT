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


def generate(width=None, height=None, rows=None, cols=None, boxcolor=None,
    colors=None, size=21, gh=None, gw=None,
    num_bg_colors=None, density=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the cutouts
    height: the height of the cutouts
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    boxcolor: the color of the boxes
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    gh: the height (rows) of the grid; defaults to size
    gw: the width (cols) of the grid; defaults to size
    num_bg_colors: the number of non-box background colors
    density: the percentage of random background pixels that are black
  """

  if gh is None: gh = size
  if gw is None: gw = size

  def draw(grid, output):
    for r in range(gh):
      for c in range(gw):
        output[r][c] = grid[r][c] = colors[r * gw + c]
    for idx in range(len(rows)):
      row, col = rows[idx], cols[idx]
      for r in range(row - 1, row + height + 1):
        output[r][col - 1] = output[r][col + width] = boxcolor
        if idx > 0: continue
        grid[r][col - 1] = grid[r][col + width] = boxcolor
      for c in range(col - 1, col + width + 1):
        output[row - 1][c] = output[row + height][c] = boxcolor
        if idx > 0: continue
        grid[row - 1][c] = grid[row + height][c] = boxcolor
    # Check if there are any holes that we didn't mean to create.
    boxes = list(zip(rows, cols))
    for row in range(gh):
      for col in range(gw):
        if (row, col) in boxes: continue
        hole = True
        for r in range(height):
          for c in range(width):
            if common.get_pixel(grid, row + r, col + c) != common.black():
              hole = False
        if hole: return False
    return True


  if width is None:
    while True:
      width, height = common.randint(2, 5), common.randint(2, 5)
      if width == 2 and height == 2: continue
      if gh > 2 * height + 6 or gw > 2 * width + 6: break
    if num_bg_colors is None:
      num_bg_colors = common.randint(1, 8)
    if density is None:
      density = common.randint(0, 50)
    color_list = common.random_colors(num_bg_colors + 1)
    while True:
      boxcolor, bg_colors, colors = color_list[0], color_list[1:], []
      for _ in range(gh * gw):
        if common.randint(1, 100) <= density:
          colors.append(common.black())
          continue
        colors.append(bg_colors[common.randint(0, len(bg_colors) - 1)])
      while True:
        rows = [common.randint(2, gh - height - 2) for _ in range(2)]
        cols = [common.randint(2, gw - width - 2) for _ in range(2)]
        if rows[0] + height + 2 < rows[1] or rows[1] + height + 2 < rows[0]:
          break
        if cols[0] + width + 2 < cols[1] or cols[1] + width + 2 < cols[0]: break
      for row, col in zip(rows, cols):
        for r in range(row, row + height):
          for c in range(col, col + width):
            colors[r * gw + c] = common.black()
      boxes = set(zip(rows, cols))
      intended_holes = set()
      for row, col in boxes:
        for r in range(row, row + height):
          for c in range(col, col + width):
            intended_holes.add((r, c))

      def break_extra_holes():
        for row in range(gh - height + 1):
          for col in range(gw - width + 1):
            if (row, col) in boxes: continue
            hole_pixels = set()
            for r in range(row, row + height):
              hole_pixels.add((r, col))
              hole_pixels.add((r, col + width - 1))
            for c in range(col, col + width):
              hole_pixels.add((row, c))
              hole_pixels.add((row + height - 1, c))
            hole = True
            for pixel in hole_pixels:
              if colors[pixel[0] * gw + pixel[1]] != common.black():
                hole = False
            if not hole: continue
            candidates = list(hole_pixels - intended_holes)
            if not candidates: continue
            r, c = common.choice(candidates)
            colors[r * gw + c] = bg_colors[common.randint(0, len(bg_colors) - 1)]

      def break_extra_boxes():
        for _ in range(3):
          changed = False
          seen = set()
          for row in range(gh):
            for col in range(gw):
              if (row, col) in seen: continue
              color = colors[row * gw + col]
              queue, pixels = [(row, col)], set()
              seen.add((row, col))
              while queue:
                r, c = queue.pop()
                pixels.add((r, c))
                for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                  if nr < 0 or nr >= gh or nc < 0 or nc >= gw: continue
                  if (nr, nc) in seen: continue
                  if colors[nr * gw + nc] != color: continue
                  seen.add((nr, nc))
                  queue.append((nr, nc))
              if color == boxcolor: continue
              rs, cs = [p[0] for p in pixels], [p[1] for p in pixels]
              h, w = max(rs) - min(rs) + 1, max(cs) - min(cs) + 1
              if h <= 2 or w <= 2: continue
              outline = set()
              for r in range(min(rs), max(rs) + 1):
                outline.add((r, min(cs)))
                outline.add((r, max(cs)))
              for c in range(min(cs), max(cs) + 1):
                outline.add((min(rs), c))
                outline.add((max(rs), c))
              if pixels != outline: continue
              candidates = list(pixels - intended_holes)
              if not candidates: continue
              r, c = common.choice(candidates)
              replacements = [bg for bg in bg_colors if bg != color]
              replacement = (replacements[common.randint(0, len(replacements) - 1)]
                             if replacements else common.black())
              if color == common.black():
                replacement = bg_colors[common.randint(0, len(bg_colors) - 1)]
              colors[r * gw + c] = replacement
              changed = True
          if not changed: break

      break_extra_holes()
      break_extra_boxes()
      break_extra_holes()
      break_extra_boxes()
      grid, output = common.grids(gw, gh)
      if draw(grid, output): break

  grid, output = common.grids(gw, gh)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=3, rows=[3, 14], cols=[7, 10], boxcolor=2,
               colors=[0, 8, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 8, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0,
                       1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1,
                       8, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1,
                       1, 1, 1, 1, 8, 1, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 2, 1,
                       0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0,
                       2, 1, 8, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 2,
                       2, 2, 2, 1, 0, 1, 0, 0, 1, 1, 8, 0, 0, 8, 0, 1, 8, 0, 0,
                       1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 8, 1, 1, 0, 0, 1, 1, 1,
                       8, 8, 1, 1, 1, 0, 0, 8, 1, 1, 1, 1, 1, 8, 1, 0, 0, 1, 8,
                       1, 0, 1, 1, 1, 1, 0, 8, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
                       1, 8, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 8, 1,
                       1, 8, 1, 1, 1, 1, 8, 1, 0, 1, 1, 8, 1, 0, 1, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 0, 8, 1, 1, 8, 0, 1, 1, 1, 1, 1, 1, 1,
                       0, 1, 0, 8, 1, 1, 1, 1, 1, 8, 1, 1, 1, 0, 1, 0, 0, 1, 1,
                       0, 8, 1, 0, 1, 0, 1, 1, 8, 1, 1, 1, 1, 1, 1, 0, 0, 8, 1,
                       0, 0, 1, 1, 8, 1, 1, 8, 1, 0, 1, 8, 8, 8, 1, 1, 1, 1, 8,
                       1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 8, 0,
                       0, 8, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 8, 8, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1,
                       8, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1,
                       1, 1, 0, 0, 8, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 8, 0, 0,
                       0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0,
                       8, 1, 8, 0]),
      generate(width=3, height=2, rows=[11, 8], cols=[4, 12], boxcolor=8,
               colors=[3, 0, 3, 4, 3, 3, 3, 3, 0, 3, 3, 4, 0, 3, 0, 4, 3, 4, 4,
                       0, 0, 3, 3, 0, 0, 3, 3, 3, 4, 0, 0, 4, 4, 4, 3, 0, 0, 3,
                       3, 4, 0, 3, 4, 4, 4, 3, 4, 3, 0, 3, 0, 0, 4, 3, 0, 3, 3,
                       4, 3, 0, 0, 3, 0, 0, 4, 4, 4, 3, 0, 3, 3, 3, 0, 3, 0, 3,
                       0, 0, 0, 0, 3, 4, 3, 3, 3, 3, 0, 4, 3, 3, 0, 0, 0, 0, 3,
                       0, 4, 4, 4, 3, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0,
                       3, 0, 0, 0, 3, 3, 3, 3, 4, 3, 0, 3, 0, 3, 0, 0, 3, 4, 0,
                       3, 4, 0, 4, 4, 0, 0, 3, 4, 0, 0, 0, 3, 3, 0, 3, 3, 3, 0,
                       4, 4, 3, 4, 3, 0, 3, 3, 3, 4, 0, 3, 0, 3, 3, 3, 4, 0, 4,
                       3, 4, 3, 4, 4, 0, 0, 4, 0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0,
                       0, 4, 0, 0, 0, 0, 3, 4, 4, 3, 4, 0, 0, 0, 4, 0, 0, 4, 3,
                       3, 3, 0, 0, 8, 8, 8, 8, 8, 4, 3, 0, 3, 3, 0, 4, 4, 0, 4,
                       4, 4, 4, 3, 3, 0, 8, 0, 0, 0, 8, 3, 0, 0, 0, 0, 4, 0, 3,
                       3, 0, 4, 3, 3, 0, 0, 0, 8, 0, 0, 0, 8, 3, 3, 0, 3, 3, 4,
                       3, 0, 4, 0, 3, 0, 0, 3, 0, 4, 8, 8, 8, 8, 8, 0, 3, 0, 3,
                       0, 0, 3, 3, 3, 0, 4, 3, 0, 4, 0, 0, 0, 0, 3, 0, 4, 0, 0,
                       3, 0, 0, 3, 3, 3, 4, 0, 4, 0, 3, 0, 0, 4, 3, 0, 0, 0, 3,
                       0, 0, 3, 4, 0, 0, 4, 0, 0, 3, 4, 3, 4, 4, 4, 0, 0, 3, 0,
                       3, 4, 4, 3, 4, 3, 4, 0, 4, 4, 0, 3, 4, 3, 4, 3, 4, 3, 3,
                       0, 0, 0, 0, 3, 0, 3, 4, 0, 0, 0, 3, 3, 3, 3, 0, 3, 0, 0,
                       0, 0, 0, 3, 0, 3, 3, 4, 0, 3, 3, 3, 4, 0, 4, 0, 3, 4, 0,
                       3, 3, 3, 0, 4, 0, 4, 3, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 4,
                       3, 0, 0, 4, 3, 3, 3, 0, 4, 4, 3, 4, 3, 4, 0, 4, 3, 4, 4,
                       0, 0, 4, 0]),
      generate(width=4, height=3, rows=[4, 15], cols=[5, 11], boxcolor=4,
               colors=[0, 0, 3, 0, 3, 2, 0, 2, 0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2,
                       3, 3, 3, 2, 2, 0, 3, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2,
                       2, 0, 3, 2, 3, 3, 0, 3, 0, 0, 3, 2, 2, 2, 2, 3, 2, 2, 2,
                       2, 3, 0, 0, 3, 2, 2, 2, 3, 2, 4, 4, 4, 4, 4, 4, 3, 0, 3,
                       2, 0, 2, 2, 2, 0, 0, 3, 3, 3, 2, 0, 4, 0, 0, 0, 0, 4, 2,
                       0, 2, 2, 0, 2, 3, 0, 2, 2, 0, 3, 2, 2, 2, 4, 0, 0, 0, 0,
                       4, 0, 3, 2, 2, 3, 2, 2, 3, 3, 2, 0, 2, 0, 2, 0, 4, 0, 0,
                       0, 0, 4, 2, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 0, 2, 4,
                       4, 4, 4, 4, 4, 2, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 0, 2,
                       2, 2, 0, 2, 0, 2, 0, 3, 2, 3, 3, 0, 2, 0, 0, 0, 2, 2, 0,
                       2, 3, 0, 3, 0, 2, 3, 2, 2, 2, 0, 2, 0, 0, 0, 2, 2, 3, 2,
                       0, 3, 0, 2, 0, 2, 0, 0, 2, 2, 0, 3, 3, 2, 3, 0, 3, 3, 0,
                       0, 3, 0, 2, 3, 0, 3, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2,
                       0, 3, 0, 0, 2, 3, 2, 2, 0, 2, 0, 2, 2, 0, 3, 2, 2, 2, 2,
                       3, 0, 2, 2, 2, 2, 2, 3, 3, 3, 2, 0, 2, 0, 2, 0, 3, 2, 2,
                       2, 0, 0, 3, 2, 2, 3, 2, 2, 0, 0, 2, 2, 2, 3, 2, 0, 0, 2,
                       3, 2, 0, 3, 0, 2, 2, 3, 2, 2, 0, 2, 2, 2, 2, 2, 3, 2, 3,
                       3, 3, 2, 0, 0, 0, 0, 2, 0, 0, 2, 3, 0, 2, 2, 2, 2, 3, 0,
                       0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 2, 2, 3, 2, 0, 2, 0, 3, 2,
                       2, 2, 3, 2, 3, 3, 3, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 2, 2, 3, 0, 0, 2, 2, 0, 0,
                       0, 3, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 3, 0, 2, 0, 0, 0,
                       3, 2, 2, 3, 2, 2, 2, 0, 0, 3, 2, 0, 3, 2, 0, 2, 2, 2, 3,
                       0, 0, 2, 2]),
  ]
  test = [
      generate(width=2, height=5, rows=[14, 4], cols=[2, 13], boxcolor=3,
               colors=[0, 2, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1, 1, 0,
                       1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 2, 1, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                       1, 1, 2, 0, 1, 1, 1, 1, 0, 2, 1, 0, 1, 1, 2, 2, 1, 1, 0,
                       1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 1, 1, 0, 1, 1, 1,
                       1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1,
                       1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 2,
                       1, 0, 1, 2, 2, 1, 1, 2, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 1,
                       0, 1, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0,
                       1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0,
                       1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
                       0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                       0, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 1, 2, 0, 2, 1, 1, 0,
                       1, 0, 0, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 3, 1, 0, 1, 0, 1,
                       0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 3, 0, 0, 3, 1, 1, 2,
                       0, 1, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 3, 0, 0, 3, 1,
                       2, 0, 0, 0, 1, 2, 1, 1, 1, 2, 1, 0, 1, 0, 1, 1, 3, 0, 0,
                       3, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 3,
                       0, 0, 3, 1, 0, 2, 0, 1, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1,
                       1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1,
                       1, 0, 1, 1, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                       1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
