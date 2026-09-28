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


def generate(brows=None, bcols=None, colors=None, gsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    gsize: The side length of the square grid.
  """

  if brows is None:
    if gsize is None:
      gsize = common.randint(7, 14)
    max_boxes = min(3, max(2, gsize * gsize // 49))
    boxes = common.randint(1, max_boxes)
    colors = common.choices([0, 1, 2, 3, 4, 5, 6, 8, 9], boxes * 8)
    while True:
      brows = [common.randint(0, gsize - 3) for _ in range(boxes)]
      bcols = [common.randint(0, gsize - 3) for _ in range(boxes)]
      if common.overlaps(brows, bcols, [3] * boxes, [3] * boxes): continue
      if common.some_abutted(brows, bcols, [3] * boxes, [3] * boxes): continue
      break

  grid, output = common.grids(7 if gsize is None else gsize,
                              7 if gsize is None else gsize, 7)
  for i, (brow, bcol) in enumerate(zip(brows, bcols)):
    for color, (dr, dc) in zip(colors[i * 8:i * 8 + 8],
                               [(0, 0), (0, 1), (0, 2), (1, 0),
                                (1, 2), (2, 0), (2, 1), (2, 2)]):
      grid[brow + dr][bcol + dc] = color

  corner_moves = [((0, 0), (2, 0)), ((0, 2), (0, 0)),
                  ((2, 0), (2, 2)), ((2, 2), (0, 2))]
  for brow, bcol in zip(brows, bcols):
    for (sr, sc), (dr, dc) in corner_moves:
      output[brow + dr][bcol + dc] = grid[brow + sr][bcol + sc]

  edge_moves = [((0, 1), (1, 2)), ((1, 2), (2, 1)),
                ((2, 1), (1, 0)), ((1, 0), (0, 1))]
  for brow, bcol in zip(brows, bcols):
    for (sr, sc), (dr, dc) in edge_moves:
      output[brow + dr][bcol + dc] = grid[brow + sr][bcol + sc]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[0, 4], bcols=[0, 3], colors=[9, 6, 5, 8, 1, 0, 8, 9, 1, 8, 4, 4, 6, 6, 2, 4]),
      generate(brows=[2], bcols=[2], colors=[5, 2, 8, 1, 9, 4, 3, 0]),
      generate(brows=[1, 4], bcols=[3, 0], colors=[6, 5, 5, 5, 6, 1, 5, 1, 8, 8, 8, 9, 9, 0, 0, 0]),
  ]
  test = [
      generate(brows=[1, 2], bcols=[0, 4], colors=[2, 6, 5, 1, 9, 4, 0, 9, 0, 1, 9, 6, 1, 5, 9, 2]),
  ]
  return {"train": train, "test": test}
