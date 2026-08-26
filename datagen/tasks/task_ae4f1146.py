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


def generate(rows=None, cols=None, idxs=None, minirows=None, minicols=None,
             size=9, minisize=3, height=None, width=None, miniheight=None,
             miniwidth=None, num=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the mini-lists
    minirows: a list of vertical coordinates where boxes should be placed
    minicols: a list of horizontal coordinates where boxes should be placed
    size: the width and height of the (square) grid
    minisize: the width and height of the (square) boxes
    height: the number of rows of the grid (defaults to size)
    width: the number of columns of the grid (defaults to size)
    miniheight: the number of rows of each box (defaults to minisize)
    miniwidth: the number of columns of each box (defaults to minisize)
    num: the number of boxes to place (defaults to an area-scaled random count)
  """
  if miniheight is None: miniheight = minisize
  if miniwidth is None: miniwidth = minisize
  if rows is None:
    # Widen the arena beyond the tight 3x-minibox default and the object count
    # beyond a fixed 4, so the object-count and density axes reach re_arc's
    # band. Mirrors re_arc generate_ae4f1146: an independent height/width up to
    # 30 (each box at most a third of the grid) and an area-scaled box count.
    # This changes neither the puzzle rule (boxes carry distinct blue-mark
    # counts; the answer is the box with the most marks) nor validate(), which
    # passes explicit rows/... and so skips this whole block.  The lower grid
    # bound keeps the original max(size, 3 * mini) floor and only expands up.
    if height is None:
      height = common.randint(max(size, 3 * miniheight),
                              max(size, 3 * miniheight, 30))
    if width is None:
      width = common.randint(max(size, 3 * miniwidth),
                             max(size, 3 * miniwidth, 30))
    if num is None:
      # Cap at miniheight * miniwidth: the boxes carry DISTINCT mark counts
      # sampled without replacement from range(miniheight * miniwidth), so a
      # unique maximum (the rule's answer) always exists.
      num = common.randint(1, min(
          miniheight * miniwidth,
          max(1, (height * width) // (2 * miniheight * miniwidth))))
  if height is None: height = max(size, 3 * miniheight)
  if width is None: width = max(size, 3 * miniwidth)
  if num is None: num = 4
  if rows is None:
    # Place num non-overlapping boxes.  If the arena is too crowded to place
    # them by random rejection, drop one box and retry (re_arc likewise emits
    # fewer objects when they will not fit) so the loop can never hang.
    tries = 0
    while True:
      minirows = [common.randint(0, height - miniheight) for _ in range(num)]
      minicols = [common.randint(0, width - miniwidth) for _ in range(num)]
      # We can touch corners, but touching edges is probably not good.
      overlaps = False
      for j in range(num):
        for i in range(j):
          rowdiff = abs(minirows[j] - minirows[i])
          coldiff = abs(minicols[j] - minicols[i])
          if rowdiff > miniheight or coldiff > miniwidth: continue
          if rowdiff == miniheight and coldiff == miniwidth: continue
          overlaps = True
      if not overlaps: break
      tries += 1
      if tries >= 500 and num > 1:
        num -= 1
        tries = 0
    lengths = common.sample(range(miniheight * miniwidth), num)
    lengths.sort()
    rows, cols, idxs = [], [], []
    for idx, length in enumerate(lengths):
      pixels = common.sample(common.all_pixels(miniwidth, miniheight), length)
      rows.extend([r for r, _ in pixels])
      cols.extend([c for _, c in pixels])
      idxs.extend([idx] * len(pixels))

  grid = common.grid(width, height, common.black())
  output = common.grid(miniwidth, miniheight, common.cyan())
  for row, col in zip(minirows, minicols):
    for r in range(miniheight):
      for c in range(miniwidth):
        grid[row + r][col + c] = common.cyan()
  for r, c, idx in zip(rows, cols, idxs):
    grid[minirows[idx] + r][minicols[idx] + c] = common.blue()
    if idx + 1 < len(minirows): continue
    output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 0, 2, 0, 1, 1, 0, 1, 1, 2, 2],
               cols=[0, 2, 1, 1, 0, 1, 1, 0, 2, 0, 2],
               idxs=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3],
               minirows=[0, 4, 1, 5], minicols=[0, 1, 4, 6]),
      generate(rows=[2, 0, 1, 0, 1, 2, 0, 1, 1, 2],
               cols=[0, 2, 1, 1, 0, 2, 1, 0, 1, 2],
               idxs=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3], minirows=[6, 0, 1, 4],
               minicols=[6, 1, 5, 2]),
      generate(rows=[2, 0, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 1, 0, 2],
               idxs=[1, 2, 2, 2, 3, 3, 3, 3, 3], minirows=[1, 0, 5, 4],
               minicols=[0, 4, 0, 6]),
      generate(rows=[1, 2, 0, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 1, 1, 2],
               cols=[2, 0, 1, 0, 2, 0, 1, 2, 0, 1, 1, 2, 0, 1, 2, 1],
               idxs=[0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
               minirows=[4, 5, 0, 1], minicols=[0, 4, 2, 6]),
  ]
  test = [
      generate(rows=[2, 0, 1, 2, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 2, 1, 0, 1, 1, 2, 0, 1],
               idxs=[0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
               minirows=[0, 3, 0, 6], minicols=[0, 3, 6, 6]),
  ]
  return {"train": train, "test": test}
