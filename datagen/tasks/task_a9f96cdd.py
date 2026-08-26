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


def generate(row=None, col=None, width=5, height=3, count=None,
             bg_color=None, marker_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the center should be placed
    col: a horizontal coordinate where the center should be placed
    width: the width of the grid
    height: the height of the grid
    count: the requested number of marker centers to place
    bg_color: the background color
    marker_color: the color of the input centers
  """
  centers = []
  if row is not None and col is not None:
    centers.append((row, col))
  if count is None:
    count = 1 if centers else common.randint(1, max(1, width * height // 10))
  legal_colors = [0, 1, 2, 4, 5, 9]
  if bg_color is None:
    bg_color = common.black() if centers else common.choice(legal_colors)
  if marker_color is None:
    marker_color = (
        common.red() if centers else common.choice(
            [color for color in legal_colors if color != bg_color]))

  grid, output = common.grids(width, height, bg_color)
  open_centers = common.all_pixels(width, height)
  for r, c in centers:
    open_centers = [
        (rr, cc) for rr, cc in open_centers
        if abs(rr - r) > 2 or abs(cc - c) > 2
    ]
  while len(centers) < count and open_centers:
    idx = common.randint(0, len(open_centers) - 1)
    r, c = open_centers[idx]
    centers.append((r, c))
    open_centers = [
        (rr, cc) for rr, cc in open_centers
        if abs(rr - r) > 2 or abs(cc - c) > 2
    ]

  for row, col in centers:
    common.draw(grid, row, col, marker_color)
    common.draw(output, row - 1, col - 1, common.green())
    common.draw(output, row - 1, col + 1, common.pink())
    common.draw(output, row + 1, col - 1, common.cyan())
    common.draw(output, row + 1, col + 1, common.orange())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, col=1),
      generate(row=2, col=4),
      generate(row=0, col=2),
      generate(row=1, col=3),
  ]
  test = [
      generate(row=1, col=4),
  ]
  return {"train": train, "test": test}
