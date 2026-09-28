# Copyright 2026 Google LLC
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


def generate(width=None, height=None, northwests=None, northeasts=None,
             southwests=None, southeasts=None, rows=None, cols=None,
             colors=None, num_points=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    northwests: The colors of north-west corner cells.
    northeasts: The colors of north-east corner cells.
    southwests: The colors of south-west corner cells.
    southeasts: The colors of south-east corner cells.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
    num_points: The number of field pixels to expand.
  """

  def corner_matches(color):
    matches = []
    if color in northwests: matches.append((northwests, northwests.index(color)))
    if color in northeasts: matches.append((northeasts, northeasts.index(color)))
    if color in southwests: matches.append((southwests, southwests.index(color)))
    if color in southeasts: matches.append((southeasts, southeasts.index(color)))
    return matches

  def draw_legends():
    grid, output = common.grids(width, height)
    for i, color in enumerate(northwests):
      output[0][i] = grid[0][i] = color
    for i, color in enumerate(northeasts):
      offset = width - len(northeasts)
      output[0][offset + i] = grid[0][offset + i] = color
    for i, color in enumerate(southwests):
      output[height - 1][i] = grid[height - 1][i] = color
    for i, color in enumerate(southeasts):
      offset = width - len(southeasts)
      output[height - 1][offset + i] = grid[height - 1][offset + i] = color
    return grid, output

  def can_place(board, row, col, angle):
    if common.get_pixel(board, row, col - 1) not in [-1, 0]:
      return False
    if common.get_pixel(board, row, col + len(angle)) not in [-1, 0]:
      return False
    for i in range(len(angle)):
      if common.get_pixel(board, row - 1, col + i) not in [-1, 0]:
        return False
      if common.get_pixel(board, row, col + i) not in [-1, 0]:
        return False
      if common.get_pixel(board, row + 1, col + i) not in [-1, 0]:
        return False
    return True

  def draw_points(board, angle_filter=None):
    for row, col, color in zip(rows, cols, colors):
      matches = corner_matches(color)
      if len(matches) != 1: return False
      angle, index = matches[0]
      if angle_filter is not None and angle is not angle_filter: continue
      start_col = col - index
      if not can_place(board, row, start_col, angle): return False
      for i, hue in enumerate(angle):
        common.draw(board, row, start_col + i, hue)
    return True

  def draw():
    if len(set(colors)) != len(colors): return None, None  # All unique colors.
    grid, output = draw_legends()
    for row, col, color in zip(rows, cols, colors):
      grid[row][col] = color
    if not draw_points(output): return None, None
    return grid, output

  if width is None:
    height = common.randint(12, 24)
    width = height + common.randint(0, 2)
    angle_count = (2 if num_points is not None and num_points > 6
                   else common.randint(1, 3))
    angles = common.sample([0, 1, 2, 3], angle_count)
    attempts = 0
    while attempts < 10000:
      attempts += 1
      northwests, northeasts, southwests, southeasts = [], [], [], []
      if 0 in angles: northwests = common.random_colors(common.randint(3, 6))
      if 1 in angles: northeasts = common.random_colors(common.randint(3, 6))
      if 2 in angles: southwests = common.random_colors(common.randint(3, 6))
      if 3 in angles: southeasts = common.random_colors(common.randint(3, 6))
      point_count = common.randint(3, 7) if num_points is None else num_points
      point_angles = common.choices(angles, point_count)
      if len(set(point_angles)) != len(angles): continue
      rows = [common.randint(1, height - 2) for _ in range(point_count)]
      cols = [common.randint(0, width - 1) for _ in range(point_count)]
      colors = []
      if num_points is None:
        for angle in point_angles:
          if angle == 0: colors.append(common.choice(northwests))
          if angle == 1: colors.append(common.choice(northeasts))
          if angle == 2: colors.append(common.choice(southwests))
          if angle == 3: colors.append(common.choice(southeasts))
      else:
        for angle in point_angles:
          legend = [northwests, northeasts, southwests, southeasts][angle]
          candidates = [color for color in legend
                        if len(corner_matches(color)) == 1
                        and color not in colors]
          if not candidates: break
          colors.append(common.choice(candidates))
        if len(colors) != point_count: continue
      grid, _ = draw()
      if grid: break
    else:
      raise RuntimeError("Unable to place all field points")

  grid, output = draw_legends()
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
  draw_points(output, northwests)
  draw_points(output, northeasts)
  draw_points(output, southwests)
  draw_points(output, southeasts)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=13, northwests=[], northeasts=[],
               southwests=[1, 2, 4, 3], southeasts=[5, 7, 8, 6],
               rows=[1, 2, 5, 8, 8], cols=[2, 11, 4, 2, 8],
               colors=[2, 8, 1, 6, 4]),
      generate(width=14, height=12, northwests=[], northeasts=[],
               southwests=[2, 3, 5, 1, 6, 4], southeasts=[], rows=[2, 5, 7],
               cols=[7, 2, 11], colors=[2, 1, 4]),
      generate(width=13, height=13, northwests=[], northeasts=[4, 3, 7, 8],
               southwests=[1, 6, 2], southeasts=[], rows=[2, 5, 8, 9],
               cols=[2, 6, 11, 1], colors=[1, 8, 2, 4]),
  ]
  test = [
      generate(width=18, height=17, northwests=[9, 5, 3, 4], northeasts=[],
               southwests=[2, 1, 3, 8], southeasts=[4, 5, 6, 7],
               rows=[1, 3, 5, 9, 11, 13], cols=[11, 3, 13, 7, 13, 4],
               colors=[8, 9, 6, 1, 2, 7]),
  ]
  return {"train": train, "test": test}
