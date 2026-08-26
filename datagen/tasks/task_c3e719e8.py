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
    height: the number of rows of the input grid (defaults to size)
    width: the number of columns of the input grid (defaults to size)
    num_colors: the number of input colors to sample
    density: the target number of non-mode input cells
  """
  if height is None: height = size if colors is not None else common.randint(2, 5)
  if width is None: width = size if colors is not None else common.randint(2, 5)
  height = min(height, 5)
  width = min(width, 5)

  if colors is None:
    area = height * width
    if num_colors is None:
      num_colors = common.randint(1, min(9, area))
    num_colors = max(1, min(num_colors, 9, area))
    color_list = common.random_colors(num_colors)
    mode = color_list[0]
    foreground_count = 0
    if num_colors > 1:
      if density is None:
        mode_floor = max(1, area // num_colors + 1)
        foreground_count = area - common.randint(mode_floor, area)
      else:
        foreground_count = density
      foreground_count = max(0, min(foreground_count, area - 1))
      while foreground_count:
        max_other = (foreground_count + num_colors - 2) // (num_colors - 1)
        if max_other < area - foreground_count:
          break
        foreground_count -= 1
    colors = [mode for _ in range(area)]
    locs = common.sample(list(range(area)), foreground_count)
    other_colors = common.shuffle(color_list[1:])
    for idx, loc in enumerate(locs):
      colors[loc] = other_colors[idx % len(other_colors)]

  grid, output = common.grids(width, height)
  mode = max(set(colors), key=colors.count)
  mode_cells = []
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
      if colors[r * width + c] != mode: continue
      mode_cells.append((r, c))

  def identify_mode_cells():
    for r, c in mode_cells:
      output[r][c] = mode

  identify_mode_cells()
  output = common.grid(width * width, height * height)

  def reveal_mode_block(block_idx):
    if block_idx >= len(mode_cells):
      return
    r, c = mode_cells[block_idx]
    for dr in range(height):
      for dc in range(width):
        output[r * height + dr][c * width + dc] = colors[dr * width + dc]

  reveal_mode_block(0)
  reveal_mode_block(1)
  reveal_mode_block(2)
  reveal_mode_block(3)
  reveal_mode_block(4)
  reveal_mode_block(5)
  reveal_mode_block(6)
  reveal_mode_block(7)
  reveal_mode_block(8)
  reveal_mode_block(9)
  reveal_mode_block(10)
  reveal_mode_block(11)
  reveal_mode_block(12)
  reveal_mode_block(13)
  reveal_mode_block(14)
  reveal_mode_block(15)
  reveal_mode_block(16)
  reveal_mode_block(17)
  reveal_mode_block(18)
  reveal_mode_block(19)
  reveal_mode_block(20)
  reveal_mode_block(21)
  reveal_mode_block(22)
  reveal_mode_block(23)
  reveal_mode_block(24)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 8, 7, 9, 3, 8, 7, 9, 3]),
      generate(colors=[8, 6, 8, 3, 3, 8, 8, 8, 8]),
      generate(colors=[6, 9, 9, 4, 6, 8, 9, 9, 8]),
  ]
  test = [
      generate(colors=[1, 1, 7, 7, 4, 1, 5, 1, 7]),
  ]
  return {"train": train, "test": test}
