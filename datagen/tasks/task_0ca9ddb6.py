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


def generate(rows=None, cols=None, colors=None, size=9, twinklers=(1, 2),
             height=None, width=None, count=None, background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
    twinklers: a list of integers representing stars that twinkle
  """
  if height is None: height = size
  if width is None: width = size
  if rows is None:
    if background is None: background = common.choice([0, 3, 5, 9])
    still_colors = [color for color in [0, 3, 5, 6, 8, 9]
                    if color != background]
    target_count = count
    while True:
      pixels = common.all_pixels(width, height)
      if target_count is None:
        target_count = common.randint(1, max(1, width * height // 4))
      pixels = common.sample(pixels, target_count)
      rows, cols = [p[0] for p in pixels], [p[1] for p in pixels]
      colors = [common.choice([1, 2] + still_colors) for _ in pixels]
      # Scooch any twinkling stars away from the edges.
      for idx in range(len(pixels)):
        if colors[idx] not in twinklers: continue
        rows[idx] = rows[idx] if rows[idx] > 0 else 1
        rows[idx] = rows[idx] if rows[idx] < height - 1 else height - 2
        cols[idx] = cols[idx] if cols[idx] > 0 else 1
        cols[idx] = cols[idx] if cols[idx] < width - 1 else width - 2
      # Only keep stars that don't clobber each other.
      keep = []
      for idx in range(len(pixels)):
        good = True
        my_radius = 1 if colors[idx] in twinklers else 0
        for prev in range(idx):
          prev_radius = 1 if colors[prev] in twinklers else 0
          radius = my_radius + prev_radius
          if abs(rows[idx] - rows[prev]) > radius: continue
          if abs(cols[idx] - cols[prev]) > radius: continue
          good = False
        if good:
          keep.append(idx)
      rows = [rows[idx] for idx in keep]
      cols = [cols[idx] for idx in keep]
      colors = [colors[idx] for idx in keep]
      if any(color in twinklers for color in colors): break
  elif background is None:
    background = 0

  grid, output = common.grids(width, height, background)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
  for r, c, color in zip(rows, cols, colors):
    if color == twinklers[0]:  # blue stars twinkle like a rook
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        output[r + dr][c + dc] = 7
  for r, c, color in zip(rows, cols, colors):
    if color == twinklers[1]:  # red stars twinkle like a bishop
      for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        output[r + dr][c + dc] = 4
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 6], cols=[2, 6], colors=[2, 1]),
      generate(rows=[0, 2, 3, 6, 7], cols=[3, 6, 2, 6, 1],
               colors=[8, 2, 1, 1, 2]),
      generate(rows=[2, 5, 7], cols=[2, 6, 3], colors=[2, 6, 1]),
  ]
  test = [
      generate(rows=[2, 3, 5, 7, 7], cols=[6, 2, 5, 7, 1],
               colors=[1, 2, 8, 2, 6]),
  ]
  return {"train": train, "test": test}
