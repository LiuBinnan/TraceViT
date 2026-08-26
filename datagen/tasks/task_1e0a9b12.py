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


def generate(colors=None, active=None, height=None, width=None, count=None,
             num_colors=None, background=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    active: a list for each color, indicating which rows that color is active
    height: the number of rows (drop space); defaults to len(colors) for
      explicit examples so the original square examples are reproduced exactly.
    width: the number of columns for generated examples.
    count: the number of active columns for generated examples.
    num_colors: the number of foreground colors for generated examples.
    background: the background color for generated examples.
  """
  if colors is None:
    if background is None:
      background = common.randint(0, 9)
    if height is None:
      height = common.randint(3, 30)
    if width is None:
      width = common.randint(3, 30)
    if count is None:
      count = common.randint(1, width)
    count = min(count, width)
    if num_colors is None:
      num_colors = common.randint(1, min(9, count))
    num_colors = min(num_colors, count, 9)
    while True:
      colors = [background] * width
      active = [[] for _ in range(width)]
      active_cols = common.sample(range(width), count)
      palette = list(range(10))
      palette.remove(background)
      palette = common.sample(palette, num_colors)
      column_colors = palette[:]
      for _ in range(count - num_colors):
        column_colors.append(common.choice(palette))
      for c, color in zip(active_cols, column_colors):
        colors[c] = color
        active[c] = common.sample(range(height),
                                  common.randint(1, height - 1))
      background_count = width * height - sum([len(c) for c in active])
      foreground = []
      for color in set(colors):
        if color == background:
          continue
        foreground.append(sum([len(active[c]) for c in range(width)
                               if colors[c] == color]))
      if not foreground or background_count > max(foreground): break

  if background is None:
    background = 0
  if height is None:
    height = len(colors)
  width = len(colors)
  grid, output = common.grids(width, height, background)
  def drop_color(c):
    if c >= width:
      return
    for r in range(len(active[c])):
      output[height - r - 1][c] = grid[active[c][r]][c] = colors[c]

  drop_color(0)
  drop_color(1)
  drop_color(2)
  drop_color(3)
  drop_color(4)
  drop_color(5)
  for c in range(6, width):
    drop_color(c)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 4, 6, 9], active=[[3], [0, 2], [2], [0]]),
      generate(colors=[4, 0, 7, 8, 0, 9],
               active=[[3, 4, 5], [], [4, 5], [1, 4], [], [0]]),
      generate(colors=[6, 3, 0, 1, 2],
               active=[[3], [1, 2, 4], [], [0, 2], [2]]),
  ]
  test = [
      generate(colors=[5, 2, 6, 4, 3],
               active=[[1, 3, 4], [0, 3], [2], [0, 3], [0]]),
  ]
  return {"train": train, "test": test}
