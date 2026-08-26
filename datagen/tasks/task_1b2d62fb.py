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


def generate(rows=None, cols=None, width=3, height=5,
             left_density=None, right_density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    width: the width of one grid half
    height: the height of the grid
    left_density: percent of left-half cells that should be black
    right_density: percent of right-half cells that should be black
  """
  if rows is None:
    area = width * height

    def sample_half(density):
      if density is None:
        midpoint = area // 2
        deviation = common.randint(0, midpoint)
        if common.randint(0, 1):
          deviation = -deviation
        count = midpoint + deviation
      else:
        count = round(area * density / 100)
      count = max(0, min(area, count))
      return common.sample(common.all_pixels(width, height), count)

    left_pixels = sample_half(left_density)
    right_pixels = [(r, c + width + 1) for r, c in sample_half(right_density)]
    pixels = left_pixels + right_pixels
    rows = [r for r, _ in pixels]
    cols = [c for _, c in pixels]

  grid = common.grid(2 * width + 1, height, common.maroon())
  for r, c in zip(rows, cols):
    grid[r][c] = common.black()
  for r in range(height):
    grid[r][width] = common.blue()
  output = common.grid(width, height)

  def place_left_grid():
    # Places the left maroon grid onto the canvas.
    for r in range(height):
      for c in range(width):
        if grid[r][c] == common.maroon():
          output[r][c] = common.maroon()

  def place_right_grid():
    # Places the right maroon grid on top; cells covered by both turn gray.
    for r in range(height):
      for c in range(width):
        if grid[r][c + width + 1] == common.maroon():
          output[r][c] = (common.gray() if output[r][c] == common.maroon()
                          else common.maroon())

  def invert_overlay():
    # Only cells covered by neither grid count: invert the overlay.
    for r in range(height):
      for c in range(width):
        output[r][c] = (common.cyan() if output[r][c] == common.black()
                        else common.black())

  place_left_grid()
  place_right_grid()
  invert_overlay()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4],
               cols=[0, 0, 1, 6, 1, 6, 0, 1, 2, 5, 6, 0]),
      generate(rows=[0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 4],
               cols=[0, 1, 2, 5, 6, 1, 0, 0, 1, 2, 0]),
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4],
               cols=[1, 2, 5, 1, 2, 4, 6, 1, 2, 5, 6, 0, 4, 0, 1, 4, 6]),
      generate(rows=[0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4],
               cols=[0, 5, 1, 2, 5, 6, 0, 2, 4, 5, 6, 1, 2, 5, 6]),
      generate(rows=[0, 0, 1, 2, 2, 3, 3, 3, 3, 4, 4],
               cols=[0, 5, 1, 4, 5, 1, 2, 5, 6, 4, 5]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4],
               cols=[2, 4, 6, 0, 4, 5, 6, 2, 4, 6, 5, 0, 4]),
  ]
  return {"train": train, "test": test}
