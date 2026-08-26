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


def generate(width=None, height=None, prow=None, pcol=None, lengths=None,
             brow=None, bcol=None, flip=None, xpose=None, starts=None,
             num_lengths=None, max_length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    prow: the horizontal coordinate of the cyan pixel
    pcol: the vertical coordinate of the cyan pixel
    lengths: a list of lengths of the cyan strips
    brow: the vertical coordinate of the box
    bcol: the horizontal coordinate of the box
    flip: whether to flip the grids horizontally
    xpose: whether to transpose the grids
    starts: a list of horizontal starts for the cyan strips
    num_lengths: the number of cyan strips
    max_length: the width of the cyan strips' bounding box
  """
  if lengths is None:
    width = common.randint(4, 30) if width is None else max(4, min(width, 30))
    height = common.randint(4, 30) if height is None else max(4, min(height, 30))
    num_lengths = (
        common.randint(2, min(9, height)) if num_lengths is None else
        max(2, min(num_lengths, 9, height)))
    max_length = (
        common.randint(2, width) if max_length is None else
        max(2, min(max_length, width)))
    while True:
      if common.randint(0, 1):
        lengths = [1] * num_lengths
        starts = [common.randint(0, max_length - 1)]
        for _ in range(1, num_lengths):
          if starts[-1] == 0:
            step = 1
          elif starts[-1] == max_length - 1:
            step = -1
          else:
            step = -1 if common.randint(0, 1) else 1
          starts.append(starts[-1] + step)
      else:
        length_cap = max(1, min(max_length, 4,
                                max(1, (width * height - 1) // num_lengths)))
        lengths = [common.randint(1, length_cap) for _ in range(num_lengths)]
        starts = [common.randint(0, max_length - lengths[0])]
        for idx in range(1, num_lengths):
          prev_start = starts[-1]
          prev_end = prev_start + lengths[idx - 1] - 1
          start_min = max(0, prev_start - lengths[idx])
          start_max = min(max_length - lengths[idx], prev_end + 1)
          starts.append(common.randint(start_min, start_max))
      prow = common.randint(0, num_lengths - 2)
      pcol = common.randint(starts[prow], starts[prow] + lengths[prow] - 1)
      brow = common.randint(0, height - num_lengths)
      bcol = common.randint(0, width - max_length)
      left = min(min(starts), pcol)
      right = max(max(starts[idx] + lengths[idx] - 1
                      for idx in range(num_lengths)), pcol)
      pixels = {(idx, c) for idx, length in enumerate(lengths)
                for c in range(starts[idx], starts[idx] + length)}
      pixels.add((prow, pcol))
      if 2 * len(pixels) >= width * height:
        continue
      extension = False
      for idx, length in enumerate(lengths):
        start = starts[idx]
        for c in range(left, right + 1):
          if not (start <= c < start + length) and (idx != prow or c != pcol):
            extension = True
      if extension:
        break
    flip = common.randint(0, 1) if flip is None else flip
    xpose = common.randint(0, 1) if xpose is None else xpose

  out_width, starts = (height if xpose else width), (
      starts if starts is not None else [0] * len(lengths))
  out_height = width if xpose else height
  grid, output = common.grids(out_width, out_height)

  def coords(r, c):
    c = width - c - 1 if flip else c
    return (c, r) if xpose else (r, c)

  def set_cell(bitmap, r, c, color):
    r, c = coords(r, c)
    bitmap[r][c] = color

  def set_both(r, c, color):
    set_cell(grid, r, c, color)
    set_cell(output, r, c, color)

  for r, length in enumerate(lengths):
    start = starts[r]
    for c in range(start, start + length):
      set_both(brow + r, bcol + c, common.cyan())
  set_both(brow + prow, bcol + pcol, common.cyan())
  active_rows, left, right = [], min(min(starts), pcol), max(
      max(starts[idx] + lengths[idx] - 1 for idx in range(len(lengths))), pcol)
  for idx, length in enumerate(lengths):
    start = starts[idx]
    for c in range(left, right + 1):
      if not (start <= c < start + length) and (idx != prow or c != pcol):
        active_rows.append(idx)
        break

  def extend_row(idx):
    if idx >= len(active_rows):
      return
    idx = active_rows[idx]
    start = starts[idx]
    for c in range(left, right + 1):
      if not (start <= c < start + lengths[idx]) and (idx != prow or c != pcol):
        set_cell(output, brow + idx, bcol + c, common.red())

  extend_row(0)
  extend_row(1)
  extend_row(2)
  extend_row(3)
  extend_row(4)
  extend_row(5)
  extend_row(6)
  extend_row(7)
  extend_row(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=14, prow=0, pcol=0,
               lengths=[3, 1, 4, 2, 3, 1, 3, 3, 2], brow=2, bcol=1, flip=0,
               xpose=0),
      generate(width=7, height=8, prow=4, pcol=3,
               lengths=[3, 1, 4, 2, 1, 4], brow=1, bcol=1, flip=0, xpose=1),
      generate(width=8, height=9, prow=1, pcol=2,
               lengths=[5, 1, 4, 3, 2, 3], brow=1, bcol=2, flip=1, xpose=0),
  ]
  test = [
      generate(width=9, height=11, prow=4, pcol=4,
               lengths=[6, 3, 4, 2, 1, 5, 2], brow=2, bcol=1, flip=1, xpose=1),
  ]
  return {"train": train, "test": test}
