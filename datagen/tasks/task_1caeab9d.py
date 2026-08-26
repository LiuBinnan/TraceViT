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


def generate(height=None, rows=None, cols=None, megarows=None, megacols=None,
             width=10, colors=(1, 2, 4), canvas_height=None,
             canvas_width=None, miniheight=None, miniwidth=None,
             num_cells=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    megarows: a list of vertical coordinates where clusters should be placed
    megacols: a list of horizontal coordinates where clusters should be placed
    width: the width of the input grid
    colors: digits representing the colors to be used
    
  """
  if height is None:
    height = common.randint(3, 30) if canvas_height is None else canvas_height
    width = common.randint(6, 30) if canvas_width is None else canvas_width
    height, width = max(3, min(30, height)), max(6, min(30, width))
    max_miniheight, max_miniwidth = max(1, height // 2), max(1, width // 3)
    if miniheight is None:
      miniheight = common.randint(1, max_miniheight)
    else:
      miniheight = max(1, min(max_miniheight, miniheight))
    if miniwidth is None:
      miniwidth = common.randint(1, max_miniwidth)
    else:
      miniwidth = max(1, min(max_miniwidth, miniwidth))
    area = miniwidth * miniheight
    if num_cells is None:
      sparse = common.randint(0, area // 2)
      num = common.choice([sparse, area - sparse])
    else:
      num = num_cells
    num = max(1, min(area, num))
    while True:
      pixels = common.sample(common.all_pixels(miniwidth, miniheight), num)
      if common.diagonally_connected(pixels): break
    rows, cols = zip(*pixels)
    max_colors = min(8, width // miniwidth)
    if num_colors is None:
      num_colors = common.randint(2, max_colors)
    else:
      num_colors = max(2, min(max_colors, num_colors))
    colors = [1] + common.random_colors(num_colors - 1, exclude=[1])
    megarows = [common.randint(0, height - miniheight) for _ in colors]
    slots = [idx * miniwidth for idx in range(width // miniwidth)]
    megacols = common.sample(slots, num_colors)

  grid, output = common.grids(width, height)
  for idx in range(1):
    mr, mc, color = megarows[idx], megacols[idx], colors[idx]
    for r, c in zip(rows, cols):
      output[megarows[0] + r][mc + c] = grid[mr + r][mc + c] = color
  for idx in range(1, 2):
    mr, mc, color = megarows[idx], megacols[idx], colors[idx]
    for r, c in zip(rows, cols):
      output[megarows[0] + r][mc + c] = grid[mr + r][mc + c] = color
  for idx in range(2, len(colors)):
    mr, mc, color = megarows[idx], megacols[idx], colors[idx]
    for r, c in zip(rows, cols):
      output[megarows[0] + r][mc + c] = grid[mr + r][mc + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=5, rows=[0, 0, 1, 1], cols=[0, 1, 0, 1],
               megarows=[1, 0, 2], megacols=[7, 1, 4]),
      generate(height=10, rows=[0, 0, 0, 1, 1, 1], cols=[0, 1, 2, 0, 1, 2],
               megarows=[5, 2, 0], megacols=[4, 1, 7]),
      generate(height=5, rows=[0, 1], cols=[0, 0], megarows=[2, 1, 3],
               megacols=[1, 3, 6]),
  ]
  test = [
      generate(height=10, rows=[0, 0, 1, 1, 2], cols=[1, 2, 1, 2, 0],
               megarows=[2, 0, 5], megacols=[0, 7, 3]),
  ]
  return {"train": train, "test": test}
