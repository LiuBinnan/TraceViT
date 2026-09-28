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


def generate(wides=None, talls=None, bgcolor=None, fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    bgcolor: The color of the background.
    fgcolor: The color of the foreground.
  """

  if wides is None:
    while True:
      num_boxes = common.randint(4, 6)
      talls = [common.randint(1, 6) for _ in range(num_boxes)]
      wides = [common.randint(1, min(5, 9 // tall)) for tall in talls]
      top_width = sum(max(wide, tall)
                      for wide, tall in zip(wides, talls)) + num_boxes - 1
      bottom_width = sum(min(wide, tall)
                         for wide, tall in zip(wides, talls)) + num_boxes - 1
      if top_width <= 28 and bottom_width <= 28:
        break
    colors = common.random_colors(2)
    bgcolor, fgcolor = colors[0], colors[1]

  longests = [max(wide, tall) for wide, tall in zip(wides, talls)]
  in_width, in_height = sum(wides) + len(wides) - 1, max(talls)
  out_width, out_height = sum(longests) + len(longests) - 1, 10
  # Build the input grid: the original upright boxes in a row.
  grid = common.grid(in_width, in_height, bgcolor)
  col = 0
  for wide, tall in zip(wides, talls):
    common.rect(grid, wide, tall, 0, col, fgcolor)
    col += wide + 1

  # Derive the output forward. Top copies are packed by their laid-flat width
  # (the longest side); bottom copies by their stood-up width (the shortest).
  output = common.grid(out_width, out_height, bgcolor)
  top_cols, bottom_cols = [], []
  top_col = bottom_col = 0
  for wide, tall in zip(wides, talls):
    top_cols.append(top_col)
    bottom_cols.append(bottom_col)
    top_col += max(wide, tall) + 1
    bottom_col += min(wide, tall) + 1

  def place_box(i):
    """Lays box i flat along the top and stands it up along the bottom."""
    if i >= len(wides): return
    longest, shortest = max(wides[i], talls[i]), min(wides[i], talls[i])
    common.rect(output, longest, shortest, 0, top_cols[i], fgcolor)
    common.rect(output, shortest, longest, out_height - longest, bottom_cols[i],
                fgcolor)

  # One frame per box (bound: num_boxes = randint(4, 6)).
  place_box(0)
  place_box(1)
  place_box(2)
  place_box(3)
  place_box(4)
  place_box(5)
  for i in range(6, len(wides)):
    place_box(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[2, 1, 1, 2, 1, 1], talls=[1, 2, 1, 3, 1, 4],
               bgcolor=1, fgcolor=8),
      generate(wides=[3, 1, 2, 1, 3, 1], talls=[1, 3, 2, 4, 2, 5],
               bgcolor=3, fgcolor=7),
      generate(wides=[1, 2, 4, 1], talls=[6, 2, 1, 1],
               bgcolor=6, fgcolor=7),
  ]
  test = [
      generate(wides=[1, 1, 1, 3, 2, 1], talls=[1, 1, 1, 3, 1, 2],
               bgcolor=9, fgcolor=2),
  ]
  return {"train": train, "test": test}
