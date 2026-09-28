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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, thicks=None, colors=None, hdiffs=None, vdiffs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the output grid.
    height: The height of the output grid.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The rows of the rectangles.
    bcols: The columns of the rectangles.
    thicks: The thicknesses of the stripes.
    colors: The colors of the stripes.
    hdiffs: Whether to contract the horizontal dimensions.
    vdiffs: Whether to contract the vertical dimensions.
  """

  def layers_for(wide, tall, brow, bcol):
    layers = []
    w, t, r, c = wide, tall, brow, bcol
    for thick, color in zip(thicks, colors):
      if w <= 0 or t <= 0: return None
      layers.append((w, t, r, c, color))
      if hdiffs[0]: w, c = w - thick, c + thick
      if hdiffs[1]: w = w - thick
      if vdiffs[0]: t, r = t - thick, r + thick
      if vdiffs[1]: t = t - thick
    return layers

  if width is None:
    width, height = common.randint(25, 30), common.randint(25, 30)
    num_boxes = common.randint(2, min(4, width * height // 180))
    box_max = 10 if num_boxes == 4 else 16
    while True:
      thicks = [common.randint(1, 3) for _ in range(common.randint(3, 4))]
      if sum(thicks) > 8: continue
      hdiffs = [common.randint(0, 1) for _ in range(2)]
      vdiffs = [common.randint(0, 1) for _ in range(2)]
      if sum(hdiffs) + sum(vdiffs) < 2: continue
      if sum(hdiffs) < 2 and sum(vdiffs) < 2: continue
      wides = [common.randint(7, box_max) for _ in range(num_boxes)]
      talls = [common.randint(7, box_max) for _ in range(num_boxes)]
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      colors = common.random_colors(len(thicks))
      if all(layers_for(wide, tall, brow, bcol) is not None
             for wide, tall, brow, bcol in zip(wides, talls, brows, bcols)):
        break

  grid, output = common.grids(width, height)
  box_layers = [layers_for(wide, tall, brow, bcol)
                for wide, tall, brow, bcol in zip(wides, talls, brows, bcols)]

  def paint_box(index):
    if index >= len(box_layers):
      return
    for w, t, r, c, color in box_layers[index]:
      common.rect(output, w, t, r, c, color)

  for i, layers in enumerate(box_layers):
    for j, (w, t, r, c, color) in enumerate(layers):
      if i == 0 or j == 0:
        common.rect(grid, w, t, r, c, color)
  paint_box(0)
  paint_box(1)
  paint_box(2)
  for i in range(3, len(box_layers)):
    paint_box(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=30, wides=[11, 9, 16], talls=[10, 9, 10],
               brows=[2, 8, 19], bcols=[3, 19, 5], thicks=[3, 1, 2],
               colors=[2, 6, 8], hdiffs=[0, 1], vdiffs=[1, 1]),
      generate(width=30, height=27, wides=[16, 15], talls=[11, 9],
               brows=[2, 15], bcols=[3, 14], thicks=[2, 2, 2, 2],
               colors=[3, 4, 1, 8], hdiffs=[1, 1], vdiffs=[1, 0]),
      generate(width=30, height=30, wides=[11, 10, 16], talls=[9, 7, 11],
               brows=[3, 5, 17], bcols=[4, 19, 3], thicks=[2, 1, 2],
               colors=[8, 4, 2], hdiffs=[1, 1], vdiffs=[1, 1]),
  ]
  test = [
      generate(width=30, height=30, wides=[13, 11, 14], talls=[10, 15, 12],
               brows=[1, 3, 14], bcols=[2, 18, 2], thicks=[2, 2, 1, 2],
               colors=[1, 2, 8, 4], hdiffs=[1, 1], vdiffs=[0, 0]),
  ]
  return {"train": train, "test": test}
