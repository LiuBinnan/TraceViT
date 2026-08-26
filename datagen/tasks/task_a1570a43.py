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


def generate(width=None, height=None, roff=None, coff=None, brow=None,
             bcol=None, rows=None, cols=None, size=7, box_height=None,
             box_width=None, num_colors=None, bg_color=None,
             corner_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    roff: a vertical offset for the red sprite
    coff: a horizontal offset for the red sprite
    brow: a vertical coordinate where the green box should be placed
    bcol: a horizontal coordinate where the green box should be placed
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    box_height: the height of the corner-marked box
    box_width: the width of the corner-marked box
    num_colors: the number of colors to use for the shifted sprite
    bg_color: the background color
    corner_color: the color of the four box corners
  """
  randomizing = any(x is None for x in [
      width, height, roff, coff, brow, bcol, rows, cols])
  if width is None:
    width = common.randint(4, 30)
  if height is None:
    height = common.randint(4, 30)
  if box_width is None and (randomizing or size is None):
    box_width = common.randint(3, width)
  if box_height is None and (randomizing or size is None):
    box_height = common.randint(3, height)
  if box_width is None:
    box_width = size
  if box_height is None:
    box_height = size
  box_width = max(3, min(box_width, width))
  box_height = max(3, min(box_height, height))
  if brow is None:
    brow = common.randint(0, height - box_height)
  if bcol is None:
    bcol = common.randint(0, width - box_width)
  if rows is None or cols is None:
    tries = max(box_height + box_width - 1, (box_height * box_width) // 2)
    rows, cols = common.conway_sprite(box_width - 2, box_height - 2, tries)
  if roff is None or coff is None:
    if common.randint(0, 1):  # TODO: Also allow a diagonal shift.
      roff, coff = 0, 0 - common.randint(1, bcol + 1)
    else:
      roff, coff = 0 - common.randint(1, brow + 1), 0
  if bg_color is None:
    bg_color = common.black() if not randomizing else common.randint(0, 9)
  if corner_color is None:
    if not randomizing:
      corner_color = common.green()
    else:
      corner_choices = [color for color in range(10) if color != bg_color]
      corner_color = common.choice(corner_choices)
  if num_colors is None:
    num_colors = 1 if not randomizing else common.randint(1, 8)
  sprite_choices = [
      color for color in range(10) if color not in [bg_color, corner_color]]
  sprite_colors = common.sample(sprite_choices, min(num_colors,
                                                    len(sprite_choices)))
  if not randomizing:
    sprite_colors = [common.red()]

  grid, output = common.grids(width, height, bg_color)
  corners = [(0, 0), (0, box_width - 1), (box_height - 1, 0),
             (box_height - 1, box_width - 1)]
  for r, c in corners:
    output[brow + r][bcol + c] = grid[brow + r][bcol + c] = corner_color
  colors = common.shuffle(
      [sprite_colors[idx % len(sprite_colors)] for idx in range(len(rows))])
  for row, col, color in zip(rows, cols, colors):
    r, c = brow + row + 1, bcol + col + 1
    output[r][c] = grid[roff + r][coff + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, roff=-1, coff=-1, brow=0, bcol=0,
               rows=[0, 1, 1, 2, 2, 2, 2, 2, 3, 4, 4],
               cols=[2, 1, 2, 0, 1, 2, 3, 4, 1, 1, 2]),
      generate(width=9, height=9, roff=0, coff=-2, brow=1, bcol=1,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4],
               cols=[2, 3, 4, 0, 1, 2, 0, 2, 0, 1, 2, 3, 3]),
      generate(width=10, height=9, roff=-2, coff=0, brow=1, bcol=1,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4],
               cols=[1, 2, 0, 1, 2, 3, 2, 3, 4, 2, 1, 2]),
      generate(width=8, height=9, roff=0, coff=-1, brow=0, bcol=0,
               rows=[0, 1, 1, 1, 2, 3, 3, 3, 3, 3, 4],
               cols=[3, 1, 2, 3, 1, 0, 1, 2, 3, 4, 1]),
  ]
  test = [
      generate(width=8, height=10, roff=0, coff=-1, brow=1, bcol=0,
               rows=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4],
               cols=[0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 0]),
  ]
  return {"train": train, "test": test}
