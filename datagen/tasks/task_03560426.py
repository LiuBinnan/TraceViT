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


def generate(widths=None, heights=None, colors=None, num_boxes=None, height=10,
             width=10):
  """Returns input and output grids according to the given parameters.

  Args:
    widths: The widths of the boxes.
    heights: The heights of the boxes.
    colors: The colors of the boxes.
    num_boxes: The number of boxes to generate.
    height: The number of rows in the grid.
    width: The number of columns in the grid.
  """

  def draw():
    grid = common.grid(width, height)
    grid_col, output_row, output_col = 0, 0, 0
    for box_width, box_height, color in zip(widths, heights, colors):
      for r in range(box_height):
        for c in range(box_width):
          if grid_col + c >= width: return None, None
          if output_row + r >= height: return None, None
          grid[height - 1 - r][grid_col + c] = color
      grid_col += box_width + 1
      output_col += box_width - 1
      output_row += box_height - 1
    if grid_col not in [width, width + 1]: return None, None
    return grid, None

  if widths is None:
    while True:
      sampled_num_boxes = (
          common.randint(3, 4) if num_boxes is None else min(4, num_boxes)
      )
      widths = [common.randint(1, 6) for _ in range(sampled_num_boxes)]
      heights = [common.randint(2, 7) for _ in range(sampled_num_boxes)]
      colors = common.random_colors(sampled_num_boxes)
      grid, _ = draw()
      if grid: break

  grid, _ = draw()
  output = common.grid(width, height)

  def place_box(i):
    """Places box i into the top-left staircase arrangement."""
    if i >= len(widths): return
    output_row = sum(height - 1 for height in heights[:i])
    output_col = sum(width - 1 for width in widths[:i])
    for r in range(heights[i]):
      for c in range(widths[i]):
        output[output_row + r][output_col + c] = colors[i]

  place_box(0)
  place_box(1)
  place_box(2)
  place_box(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(widths=[3, 2, 3], heights=[4, 2, 2], colors=[8, 7, 2]),
      generate(widths=[2, 2, 2, 1], heights=[3, 2, 2, 4], colors=[1, 2, 3, 4]),
      generate(widths=[4, 1, 3], heights=[2, 5, 3], colors=[4, 2, 3]),
  ]
  test = [
      generate(widths=[1, 2, 1, 2], heights=[4, 3, 3, 2], colors=[7, 8, 6, 3]),
  ]
  return {"train": train, "test": test}
