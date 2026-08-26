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


def _draw_figure(g, neck, shoulder, size, shirt, antenna):
  """Draws the bottom-left figure (two shoulders + neck) into grid `g`."""
  height = len(g)
  for c in range(shoulder, shoulder + neck):
    g[height - 1][c] = antenna
    g[height - 2][c] = shirt
  for c in range(shoulder):
    g[height - 1][c] = shirt
    g[height - 1][size - 1 - c] = shirt
  return g


def _draw_reflection_ray(g, shoulder, size, antenna, side):
  """Extends one neck-edge diagonal outward to the grid wall (the reflection).

  The antenna ray is the continuation of the figure's neck edge: a 45-degree
  diagonal leaving the top of the neck and travelling up-and-outward until it
  exits the grid (a side wall or the top edge). It therefore always spans the
  full available width/height, independent of how the grid extent was decoupled
  from the figure size.
  """
  height, width = len(g), len(g[0])
  # The neck top sits on row `height - 2`; the ray occupies the rows above it.
  for r in range(height - 3, -1, -1):
    c = (r - (height - 2 - shoulder)) if side == "left" \
        else ((height - 2 - shoulder + size - 1) - r)
    if 0 <= c < width:
      g[r][c] = antenna
  return g


def generate(neck=None, shoulder=None, shirt=None, antenna=None, b=0,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    neck: the width of the neck
    shoulder: the width of the shoulder
    shirt: the color of the shirt
    antenna: the color of the antenna
    b: the integer used for all background cells
    height: the number of rows in the grid (>= figure height); None squares it
    width: the number of columns in the grid (>= figure width); None squares it
  """
  if neck is None:
    neck = 2 * common.randint(0, 1) + 1
    shoulder = common.randint(1, 3)
    colors = common.random_colors(2)
    shirt, antenna = colors[0], colors[1]

  size = neck + 2 * shoulder
  # The figure spans exactly `size` columns (neck + 2 shoulders) and
  # `shoulder + 2` rows. Decouple the grid extent from the figure: height is
  # the row count (>= figure height), width the column count (>= figure width).
  # The figure is anchored to the bottom-left; remaining cells stay background.
  if height is None:
    height = size
  if width is None:
    width = size
  height = max(height, size)
  width = max(width, size)
  grid = _draw_figure(common.grid(width, height, b),
                      neck, shoulder, size, shirt, antenna)
  output = _draw_figure(common.grid(width, height, b),
                        neck, shoulder, size, shirt, antenna)
  output = _draw_reflection_ray(output, shoulder, size, antenna, "left")
  output = _draw_reflection_ray(output, shoulder, size, antenna, "right")
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(neck=1, shoulder=1, shirt=2, antenna=4),
      generate(neck=1, shoulder=2, shirt=8, antenna=3),
      generate(neck=3, shoulder=1, shirt=6, antenna=1),
      generate(neck=3, shoulder=2, shirt=2, antenna=4),
  ]
  test = [
      generate(neck=3, shoulder=3, shirt=8, antenna=2),
  ]
  return {"train": train, "test": test}
