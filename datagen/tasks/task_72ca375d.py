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


def generate(rows=None, cols=None, idxs=None, colors=None, brows=None,
             bcols=None, size=10, num_boxes=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the boxes that should be placed
    colors: a list of colors to use for the boxes
    brows: a list of vertical coordinates where the boxes should be placed
    bcols: a list of horizontal coordinates where the boxes should be placed
    size: the size of the input and output grids
    num_boxes: the number of boxes to place
    num_colors: the number of foreground colors to use
  """

  def is_symmetric(pixels):
    max_col = max([p[1] for p in pixels])
    for r, c in pixels:
      if (r, max_col - c) not in pixels: return False
    return True

  def is_rotational(pixels):
    max_row, max_col = max([p[0] for p in pixels]), max([p[1] for p in pixels])
    for r, c in pixels:
      if (max_row - r, max_col - c) not in pixels: return False
    return True

  def place_boxes(wides, talls):
    placed_rows, placed_cols = [0] * num_boxes, [0] * num_boxes
    occupied = set()
    for idx in sorted(range(num_boxes), key=lambda i: wides[i] * talls[i],
                      reverse=True):
      candidates = []
      for row in range(size - talls[idx] + 1):
        for col in range(size - wides[idx] + 1):
          blocked = False
          for rr in range(row - 1, row + talls[idx] + 1):
            for cc in range(col - 1, col + wides[idx] + 1):
              if (rr, cc) in occupied:
                blocked = True
                break
            if blocked: break
          if not blocked: candidates.append((row, col))
      if not candidates: return None, None
      placed_rows[idx], placed_cols[idx] = common.choice(candidates)
      for rr in range(placed_rows[idx], placed_rows[idx] + talls[idx]):
        for cc in range(placed_cols[idx], placed_cols[idx] + wides[idx]):
          occupied.add((rr, cc))
    return placed_rows, placed_cols

  if rows is None:
    if num_boxes is None:
      num_boxes = common.randint(2, max(2, size * size // 25 + 1))
    num_boxes = max(1, min(num_boxes, max(1, size * size // 4)))
    if num_colors is None: num_colors = min(num_boxes, 9)
    num_colors = max(1, min(num_colors, 9))
    for _ in range(200):
      dense = num_boxes > max(9, size * size // 40)
      source_max = 4 if dense else 8
      wides = [common.randint(2, min(source_max, size))]
      talls = [common.randint(2, min(source_max, size))]
      for _ in range(num_boxes - 1):
        if dense:
          wides.append(common.randint(2, min(3, size)))
          talls.append(common.randint(2, min(3, size)))
        else:
          wide = common.randint(2, min(5, size))
          wides.append(wide)
          talls.append(common.randint(2, min(7 - wide, size)))
      brows, bcols = place_boxes(wides, talls)
      if brows is not None: break
    if brows is None:
      wides, talls = [2] * num_boxes, [2] * num_boxes
      brows, bcols = place_boxes(wides, talls)
    rows, cols, idxs = [], [], []
    for idx in range(num_boxes):
      wide, tall = wides[idx], talls[idx]
      if not idx:
        pixels = common.all_pixels(wide, tall)
      else:
        for _ in range(100):
          num_pixels = common.randint(max(2, wide * tall // 2),
                                      max(2, wide * tall - 1))
          pixels = common.continuous_creature(num_pixels, wide, tall)
          if is_symmetric(pixels): continue
          if is_rotational(pixels): continue
          break
        if is_symmetric(pixels) or is_rotational(pixels):
          pixels = [(0, 0), (1, 0), (1, 1)]
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))
    palette = common.random_colors(num_colors)
    colors = []
    for idx in range(num_boxes):
      colors.append(palette[idx] if idx < num_colors else common.choice(palette))

  width = max([c for c, i in zip(cols, idxs) if not i]) + 1
  height = max([r for r, i in zip(rows, idxs) if not i]) + 1
  grid, output = common.grid(size, size), common.grid(width, height)
  for r, c, idx in zip(rows, cols, idxs):
    grid[brows[idx] + r][bcols[idx] + c] = colors[idx]
    if not idx: output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
               cols=[0, 1, 2, 3, 1, 2, 0, 1, 1, 2, 3, 1, 2, 0, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               colors=[6, 2, 7], brows=[6, 1, 2], bcols=[3, 1, 6]),
      generate(rows=[0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
               cols=[0, 1, 0, 1, 0, 1, 2, 0, 2, 3, 1, 2, 3, 4, 0, 1, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
               colors=[4, 8, 2], brows=[1, 2, 7], bcols=[2, 6, 1]),
      generate(rows=[0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               cols=[0, 3, 0, 1, 2, 3, 0, 1, 1, 1, 3, 4, 5, 0, 1, 2, 3, 5, 6],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               colors=[5, 3, 8], brows=[2, 1, 7], bcols=[5, 1, 0]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0,
                     1, 1, 1],
               cols=[1, 2, 1, 2, 0, 1, 2, 3, 0, 3, 0, 1, 2, 3, 3, 0, 1, 2, 3, 4,
                     0, 3, 4],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                     2, 2, 2],
               colors=[9, 3, 4], brows=[2, 1, 7], bcols=[0, 5, 4]),
  ]
  return {"train": train, "test": test}
