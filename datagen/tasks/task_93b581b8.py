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


def generate(row=None, col=None, colors=None, size=6, height=None, width=None,
             num_objects=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the center should be placed
    col: a horizontal coordinate where the center should be placed
    colors: a list of four digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows in the grid (defaults to size)
    width: the number of columns in the grid (defaults to size)
    num_objects: number of 2x2 seed blocks to place
    num_colors: number of foreground colors to draw from
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if row is None:
    if num_objects is None:
      num_objects = common.randint(1, max(1, (height * width) // 50))
    if num_colors is None:
      num_colors = common.randint(1, 9)
    palette = common.random_colors(num_colors)
    objects = []
    blocked = set()
    tries, max_tries = 0, 10 * num_objects
    while len(objects) < num_objects and tries < max_tries:
      tries += 1
      obj_row = common.randint(0, height - 2)
      obj_col = common.randint(0, width - 2)
      obj_colors = common.choices(palette, 4)
      output_pixels = set()
      input_pixels = set()
      for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        input_pixels.add((obj_row + r, obj_col + c))
      for corner_r, corner_c in [(0, 0), (2, 2), (2, -2), (-2, 2), (-2, -2)]:
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          pixel = (obj_row + corner_r + dr, obj_col + corner_c + dc)
          if 0 <= pixel[0] < height and 0 <= pixel[1] < width:
            output_pixels.add(pixel)
      if output_pixels & blocked:
        continue
      objects.append((obj_row, obj_col, obj_colors))
      blocked.update(output_pixels)
      for pixel in input_pixels:
        for dr, dc in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]:
          blocked.add((pixel[0] + dr, pixel[1] + dc))
  else:
    objects = [(row, col, colors)]

  grid, output = common.grids(width, height)
  for obj_row, obj_col, obj_colors in objects:
    for r, c, color in zip([0, 0, 1, 1], [0, 1, 0, 1], obj_colors):
      output[obj_row + r][obj_col + c] = grid[obj_row + r][obj_col + c] = color
  corners = [(2, 2, 0), (2, -2, 1), (-2, 2, 2), (-2, -2, 3)]

  def reveal_corner(corner_idx):
    if corner_idx >= len(corners):
      return
    r, c, color_idx = corners[corner_idx]
    for obj_row, obj_col, obj_colors in objects:
      color = obj_colors[color_idx]
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        common.draw(output, obj_row + r + dr, obj_col + c + dc, color)

  reveal_corner(0)
  reveal_corner(1)
  reveal_corner(2)
  reveal_corner(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=2, colors=[9, 3, 7, 8]),
      generate(row=1, col=1, colors=[4, 6, 2, 1]),
      generate(row=2, col=2, colors=[3, 6, 5, 2]),
  ]
  test = [
      generate(row=3, col=2, colors=[3, 1, 2, 5]),
  ]
  return {"train": train, "test": test}
