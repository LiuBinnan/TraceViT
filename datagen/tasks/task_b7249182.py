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


def generate(width=None, height=None, row=None, col=None, half=None,
             colors=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinate where the object starts
    col: a vertical coordinate where the object starts
    half: the length of one half of the entire object
    colors: which two colors to use
    xpose: whether to transpose the grid
  """
  if width is None:
    half = common.randint(4, 10)
    width, height = 2 * half + common.randint(1, 4), common.randint(7, 10)
    col = common.randint(0, width - 2 * half)
    row = common.randint(1, height - 6)
    colors = common.random_colors(2)
    xpose = common.randint(0, 1)

  final_width, final_height = (height, width) if xpose else (width, height)
  grid, output = common.grids(final_width, final_height)

  def coords(r, c):
    return (c, r) if xpose else (r, c)

  def set_cell(bitmap, r, c, color):
    r, c = coords(r, c)
    bitmap[r][c] = color

  for color_idx in range(2):
    c = col + color_idx * (2 * half - 1)
    set_cell(grid, row + 2, c, colors[color_idx])
    set_cell(output, row + 2, c, colors[color_idx])

  def reveal_half(color_idx):
    c = col + color_idx * (2 * half - 1)
    inc = 1 if color_idx == 0 else -1
    for _ in range(half - 2):
      c += inc
      set_cell(output, row + 2, c, colors[color_idx])
    set_cell(output, row + 1, c, colors[color_idx])
    set_cell(output, row + 3, c, colors[color_idx])
    set_cell(output, row + 0, c, colors[color_idx])
    set_cell(output, row + 4, c, colors[color_idx])
    set_cell(output, row + 0, c + inc, colors[color_idx])
    set_cell(output, row + 4, c + inc, colors[color_idx])

  reveal_half(0)
  reveal_half(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=10, row=2, col=1, half=5, colors=[2, 8],
               xpose=1),
      generate(width=13, height=10, row=4, col=1, half=6, colors=[3, 1],
               xpose=0),
      generate(width=18, height=10, row=3, col=3, half=7, colors=[5, 8],
               xpose=0),
  ]
  test = [
      generate(width=19, height=9, row=1, col=1, half=8, colors=[7, 6],
               xpose=1),
  ]
  return {"train": train, "test": test}
