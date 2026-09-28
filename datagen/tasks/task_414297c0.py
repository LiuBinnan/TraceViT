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


def _sample_params():
  """Samples puzzle parameters with the original random-call order."""
  num_boxes = common.randint(3, 5)
  bgcolor = common.random_color(exclude=[2])
  hues = common.random_colors(num_boxes, exclude=[2, bgcolor])
  # First, make sure we can get nonoverlapping input / output positions.
  for _ in range(64):
    inwidth, inheight = common.randint(15, 30), common.randint(15, 30)
    outwidth = common.randint(inwidth // 3, 2 * inwidth // 3)
    outheight = common.randint(inheight // 3, 2 * inheight // 3)
    brow = common.randint(1, inheight - outheight - 1)
    bcol = common.randint(1, inwidth - outwidth - 1)
    irows = [common.randint(1, inheight - 4) for _ in range(num_boxes)]
    icols = [common.randint(1, inwidth - 4) for _ in range(num_boxes)]
    orows = [common.randint(0, outheight - 3) for _ in range(num_boxes)]
    ocols = [common.randint(0, outwidth - 3) for _ in range(num_boxes)]
    rows, cols = [brow] + irows, [bcol] + icols
    wides, talls = [outwidth] + [3] * num_boxes, [outheight] + [3] * num_boxes
    if common.overlaps(rows, cols, wides, talls, 1): continue
    if common.overlaps(orows, ocols, [3] * num_boxes, [3] * num_boxes):
      continue
    if common.some_abutted(orows, ocols, [3] * num_boxes, [3] * num_boxes):
      continue
    break
  else:
    # If rejection sampling hits its cap, resample dimensions and greedily take
    # shuffled valid slots. This retains the original dimensional bands and
    # irregular placements while bounding the dense-packing search.
    for _ in range(64):
      inwidth, inheight = common.randint(15, 30), common.randint(15, 30)
      outwidth = common.randint(inwidth // 3, 2 * inwidth // 3)
      outheight = common.randint(inheight // 3, 2 * inheight // 3)
      brow = common.randint(1, inheight - outheight - 1)
      bcol = common.randint(1, inwidth - outwidth - 1)
      input_slots = common.shuffle([
          (row, col)
          for row in range(1, inheight - 3)
          for col in range(1, inwidth - 3)
      ])
      irows, icols = [], []
      for irow, icol in input_slots:
        next_rows = [brow] + irows + [irow]
        next_cols = [bcol] + icols + [icol]
        if common.overlaps(next_rows, next_cols,
                           [outwidth] + [3] * (len(irows) + 1),
                           [outheight] + [3] * (len(irows) + 1), 1):
          continue
        irows.append(irow)
        icols.append(icol)
        if len(irows) == num_boxes: break
      if len(irows) < num_boxes: continue
      output_slots = common.shuffle([
          (row, col)
          for row in range(outheight - 2)
          for col in range(outwidth - 2)
      ])
      orows, ocols = [], []
      for orow, ocol in output_slots:
        next_orows, next_ocols = orows + [orow], ocols + [ocol]
        if common.overlaps(next_orows, next_ocols,
                           [3] * len(next_orows), [3] * len(next_orows)):
          continue
        if common.some_abutted(next_orows, next_ocols,
                               [3] * len(next_orows), [3] * len(next_orows)):
          continue
        orows.append(orow)
        ocols.append(ocol)
        if len(orows) == num_boxes: break
      if len(orows) == num_boxes: break
    else:
      # A separated lattice is the guaranteed terminal fallback.
      inwidth = inheight = 30
      outwidth = outheight = 15
      brow = bcol = 1
      input_slots = common.shuffle([
          (row, col)
          for row in range(1, inheight - 3, 5)
          for col in range(18, inwidth - 3, 5)
      ])
      output_slots = common.shuffle([
          (row, col)
          for row in range(0, outheight - 2, 4)
          for col in range(0, outwidth - 2, 4)
      ])
      irows = [row for row, _ in input_slots[:num_boxes]]
      icols = [col for _, col in input_slots[:num_boxes]]
      orows = [row for row, _ in output_slots[:num_boxes]]
      ocols = [col for _, col in output_slots[:num_boxes]]
  # Second, shift rows/cols to be center-oriented, and (sometimes) drop a box.
  irows, icols = [irow + 1 for irow in irows], [icol + 1 for icol in icols]
  orows, ocols = [orow + 1 for orow in orows], [ocol + 1 for ocol in ocols]
  if common.randint(0, 2) == 0: orows[0] = ocols[0] = -1
  # Third, figure out the contents of the sprites.
  colors = []
  for hue in hues:
    pixels = common.diagonally_connected_sprite()
    values = []
    for r in range(3):
      for c in range(3):
        values.append(2 if (r, c) in pixels else 0)
    values[4] = hue
    colors.extend(values)
  colors = "".join(str(c) for c in colors)
  return (inwidth, inheight, outwidth, outheight, brow, bcol, bgcolor, irows,
          icols, orows, ocols, colors)


def generate(inwidth=None, inheight=None, outwidth=None, outheight=None,
             brow=None, bcol=None, bgcolor=None, irows=None, icols=None,
             orows=None, ocols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    inwidth: The width of the input grid.
    inheight: The height of the input grid.
    outwidth: The width of the output grid.
    outheight: The height of the output grid.
    brow: The row of the main box.
    bcol: The column of the main box.
    bgcolor: The color of the output grid.
    irows: The rows of the input sprites.
    icols: The columns of the input sprites.
    orows: The rows of the output sprites.
    ocols: The columns of the output sprites.
    colors: The colors of all the sprites.
  """

  if inwidth is None:
    (inwidth, inheight, outwidth, outheight, brow, bcol, bgcolor, irows, icols,
     orows, ocols, colors) = _sample_params()

  grid = common.grid(inwidth, inheight)
  output = common.grid(outwidth, outheight, bgcolor)
  sprites = []
  for i in range(len(irows)):
    sprite = []
    for r in range(3):
      sprite.append([int(colors[i * 9 + r * 3 + c]) for c in range(3)])
    sprites.append(sprite)

  def place_sprite(index):
    if index >= len(sprites) or orows[index] == -1:
      return
    sprite, orow, ocol = sprites[index], orows[index], ocols[index]
    for r in range(3):
      for c in range(3):
        if sprite[r][c]:
          output[orow + r - 1][ocol + c - 1] = sprite[r][c]

  common.rect(grid, outwidth, outheight, brow, bcol, bgcolor)
  for sprite, irow, icol, orow, ocol in zip(sprites, irows, icols, orows, ocols):
    for r in range(3):
      for c in range(3):
        grid[irow + r - 1][icol + c - 1] = sprite[r][c]
    if orow != -1:
      grid[brow + orow][bcol + ocol] = sprite[1][1]
  place_sprite(0)
  place_sprite(1)
  place_sprite(2)
  place_sprite(3)
  place_sprite(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(inwidth=20, inheight=16, outwidth=6, outheight=9, brow=6, bcol=1,
               bgcolor=8, irows=[3, 5, 10], icols=[11, 17, 12],
               orows=[2, -1, 7], ocols=[1, -1, 3],
               colors="020212200202032202202042222"),
      generate(inwidth=22, inheight=18, outwidth=11, outheight=12, brow=5,
               bcol=10, bgcolor=1, irows=[2, 3, 6, 10], icols=[7, 2, 5, 2],
               orows=[2, 9, 5, 9], ocols=[8, 7, 4, 2],
               colors="200232002020272020020242022222282202"),
      generate(inwidth=18, inheight=16, outwidth=12, outheight=6, brow=1,
               bcol=1, bgcolor=3, irows=[9, 11, 12], icols=[15, 10, 4],
               orows=[1, 3, 4], ocols=[6, 2, 9],
               colors="222040222000212020220280002"),
  ]
  test = [
      generate(inwidth=24, inheight=26, outwidth=15, outheight=9, brow=11,
               bcol=1, bgcolor=4, irows=[2, 3, 7, 13, 23],
               icols=[3, 12, 5, 20, 7], orows=[2, 5, 2, 7, 7],
               ocols=[12, 9, 3, 13, 1],
               colors="000272220220260002020212020220082022022232220"),
  ]
  return {"train": train, "test": test}
