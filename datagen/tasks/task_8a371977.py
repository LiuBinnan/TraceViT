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


def generate(length=None, num_boxes=None, thick=None, border=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: the length of the box.
    num_boxes: the number of boxes.
    thick: the thickness of the lines.
    trim: how much to inflate the border.
  """

  if length is None:
    while True:
      length = common.randint(1, 5)
      num_boxes = common.randint(3, 11)
      thick = common.randint(1, 2)
      border = common.randint(2 - thick, 1)
      size = (length + thick) * num_boxes + border
      if size <= 30: break

  size = (length + thick) * num_boxes + border
  grid = common.grid(size, size, 1)
  for r in range(num_boxes):
    for c in range(num_boxes):
      row, col = r * (length + thick) + 1, c * (length + thick) + 1
      common.rect(grid, length, length, row, col, 0)
  output = common.deepcopy(grid)

  def color_ring_boxes():
    """Paints the boxes on the lattice's outer ring red."""
    for r in range(num_boxes):
      for c in range(num_boxes):
        if r in [0, num_boxes - 1] or c in [0, num_boxes - 1]:
          row, col = r * (length + thick) + 1, c * (length + thick) + 1
          common.rect(output, length, length, row, col, common.red())

  def color_inner_boxes():
    """Paints the boxes inside the ring green."""
    for r in range(1, num_boxes - 1):
      for c in range(1, num_boxes - 1):
        row, col = r * (length + thick) + 1, c * (length + thick) + 1
        common.rect(output, length, length, row, col, common.green())

  color_ring_boxes()
  color_inner_boxes()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=1, num_boxes=11, thick=1, border=1),
      generate(length=4, num_boxes=3, thick=2, border=1),
      generate(length=3, num_boxes=6, thick=1, border=1),
  ]
  test = [
      generate(length=4, num_boxes=5, thick=2, border=0),
  ]
  return {"train": train, "test": test}
