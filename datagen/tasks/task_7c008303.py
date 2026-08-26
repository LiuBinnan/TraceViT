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


def generate(rows=None, cols=None, colors=None, flip_horiz=None, flip_vert=None,
             size=6, height=None, width=None, num_colors=None, density=None,
             height_units=None, width_units=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of four digits representing the colors to be used
    flip_horiz: whether to flip the grid horizontally
    flip_vert: whether to flip the grid vertically
    size: the width and height of the (square) grid
    height: number of content rows (defaults to size); decouples the grid shape
    width: number of content columns (defaults to size); decouples the grid shape
    num_colors: number of legal quadrant colors to sample from
    density: percentage of content pixels to mark as foreground
    height_units: number of two-row key segments in the content area
    width_units: number of two-column key segments in the content area
  """
  if height is None:
    if height_units is None:
      height = size
    else:
      height_units = min(13, max(2, height_units))
      height = 2 * height_units
  if width is None:
    if width_units is None:
      width = size
    else:
      width_units = min(13, max(2, width_units))
      width = 2 * width_units
  if rows is None:
    area = width * height
    if density is None:
      max_deviation = area // 2
      deviation = common.randint(0, max_deviation)
      pixel_count = common.choice([deviation, area - deviation])
    else:
      density = min(100, max(0, density))
      pixel_count = (area * density + 50) // 100
    pixels = common.sample(common.all_pixels(width, height), pixel_count)
    rows, cols = zip(*pixels) if pixels else ([], [])
    if colors is None:
      if num_colors is None:
        num_colors = common.randint(1, 4)
      num_colors = min(4, max(1, num_colors))
      palette = common.random_colors(
          num_colors, exclude=[common.green(), common.cyan()])
      colors = [common.choice(palette) for _ in range(4)]
      if width % 2:
        colors[1] = colors[0]
        colors[3] = colors[2]
      if height % 2:
        colors[2] = colors[0]
        colors[3] = colors[1]
    flip_horiz, flip_vert = common.randint(0, 1), common.randint(0, 1)

  def orient(thegrid):
    if flip_horiz:
      thegrid = common.flip_horiz(thegrid)
    if flip_vert:
      thegrid = thegrid[::-1]
    return thegrid

  grid = common.grid(width + 3, height + 3)
  for i in range(3 + height):
    grid[i][2] = common.cyan()
  for i in range(3 + width):
    grid[2][i] = common.cyan()
  grid[0][0] = colors[0]
  grid[0][1] = colors[1]
  grid[1][0] = colors[2]
  grid[1][1] = colors[3]
  for r, c in zip(rows, cols):
    grid[r + 3][c + 3] = common.green()
  canonical = common.grid(width, height)
  for r, c in zip(rows, cols):
    canonical[r][c] = common.green()
  output = orient([row[:] for row in canonical])
  for r, c in zip(rows, cols):
    if r < height // 2 and c < width // 2:
      color = colors[0]
    elif r < height // 2 and c >= width // 2:
      color = colors[1]
    else:
      continue
    canonical[r][c] = color
  output = orient([row[:] for row in canonical])
  for r, c in zip(rows, cols):
    if r < height // 2:
      continue
    if c < width // 2:
      color = colors[2]
    elif r >= height // 2 and c < width // 2:
      color = colors[2]
    else:
      color = colors[3]
    canonical[r][c] = color
  output = orient([row[:] for row in canonical])
  grid = orient(grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5,
                     5],
               cols=[1, 4, 0, 1, 2, 3, 4, 5, 1, 4, 1, 4, 0, 1, 2, 3, 4, 5, 1,
                     4],
               colors=[2, 4, 1, 6], flip_horiz=0, flip_vert=0),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4, 5],
               cols=[0, 2, 3, 4, 5, 0, 2, 4, 5, 1, 0, 1, 2, 3, 4, 5, 1],
               colors=[2, 1, 1, 4], flip_horiz=1, flip_vert=0),
      generate(rows=[0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5],
               cols=[1, 5, 1, 3, 4, 0, 1, 3, 4, 2, 5, 2, 5],
               colors=[6, 5, 2, 4], flip_horiz=0, flip_vert=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5],
               cols=[3, 0, 4, 2, 3, 4, 0, 2, 4, 0, 2, 4, 5, 2],
               colors=[7, 4, 1, 2], flip_horiz=1, flip_vert=1),
  ]
  return {"train": train, "test": test}
