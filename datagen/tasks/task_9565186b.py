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


def generate(colors=None, size=3, height=None, width=None, num_colors=None,
             density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
    height: the number of rows (defaults to size)
    width: the number of columns (defaults to size)
    num_colors: the number of non-gray colors to use
    density: percent position in the feasible non-majority density band
  """
  if height is None:
    height = size
  if width is None:
    width = size
  if colors is None:
    area = height * width
    max_num_colors = min(area - 1, 8)
    if num_colors is None:
      num_colors = common.randint(2, max_num_colors)
    num_colors = max(2, min(num_colors, max_num_colors))
    color_list = common.random_colors(num_colors, exclude=[common.gray()])
    mode = color_list[common.randint(0, len(color_list) - 1)]

    min_mode_count = area // num_colors + 1
    max_mode_count = area - num_colors + 1
    max_deviation = max_mode_count - min_mode_count
    if density is None:
      mode_deviation = common.randint(0, max_deviation)
    else:
      density = max(0, min(density, 100))
      mode_deviation = round(max_deviation * density / 100)
    mode_count = max_mode_count - mode_deviation

    other_colors = [c for c in color_list if c != mode]
    colors = [mode for _ in range(mode_count)] + other_colors
    color_counts = {c: 1 for c in other_colors}
    available_colors = list(other_colors)
    for _ in range(area - len(colors)):
      if available_colors:
        color = available_colors[common.randint(0, len(available_colors) - 1)]
        colors.append(color)
        color_counts[color] += 1
        if color_counts[color] == mode_count - 1:
          available_colors.remove(color)
      else:
        colors.append(mode)
    colors = common.shuffle(colors)

  grid, output = common.grids(width, height)
  mode = max(set(colors), key=colors.count)
  for r in range(height):
    for c in range(width):
      color = colors[r * width + c]
      grid[r][c] = color
      output[r][c] = color if color == mode else common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 2, 2, 1, 8, 2, 8, 8]),
      generate(colors=[1, 1, 1, 8, 1, 3, 8, 2, 2]),
      generate(colors=[2, 2, 2, 8, 8, 2, 2, 2, 2]),
      generate(colors=[3, 3, 8, 4, 4, 4, 8, 1, 1]),
  ]
  test = [
      generate(colors=[1, 3, 2, 3, 3, 2, 1, 3, 2]),
  ]
  return {"train": train, "test": test}
