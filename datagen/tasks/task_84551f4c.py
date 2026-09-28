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


def generate(width=None, height=None, cols=None, lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    colors: The colors of the lines.
  """

  if width is None:
    width = common.randint(5, 30)
    while True:
      col, cols, lengths, colors = 0, [], [], []
      while True:
        length = common.randint(2, 4)
        if col + length > width: break
        cols.append(col)
        lengths.append(length)
        colors.append(common.randint(1, 2) if not colors or colors[-1] != 1 else 2)
        col += length + common.randint(0, 1)
      if len(set(colors)) == 2: break
    height = max(lengths) + common.randint(0, 5)

  grid = common.grid(width, height)
  for col, length, color in zip(cols, lengths, colors):
    for r in range(length):
      grid[height - r - 1][col] = color
  output = common.grid(width, height)

  last, knocks = None, []
  for col, length, color in zip(cols, lengths, colors):
    knock = (color == 1) or (last is not None and last == col)
    knocks.append(knock)
    last = (col + length) if knock else col

  def topple_initiators():
    """Color-1 bars are pushed over and fall rightward onto the floor."""
    for i in range(len(cols)):
      if not knocks[i] or colors[i] != 1: continue
      for r in range(lengths[i]):
        output[height - 1][cols[i] + r] = colors[i]

  def propagate_chain():
    """Bars struck by a fallen neighbor topple too (the domino chain)."""
    for i in range(len(cols)):
      if not knocks[i] or colors[i] == 1: continue
      for r in range(lengths[i]):
        output[height - 1][cols[i] + r] = colors[i]

  def keep_standing():
    """Bars that nothing knocked over remain upright."""
    for i in range(len(cols)):
      if knocks[i]: continue
      for r in range(lengths[i]):
        output[height - r - 1][cols[i]] = colors[i]

  topple_initiators()
  propagate_chain()
  keep_standing()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=3, cols=[0, 3, 6, 10, 13],
               lengths=[3, 3, 3, 3, 3], colors=[1, 2, 2, 2, 2]),
      generate(width=16, height=3, cols=[0, 4, 8, 11], lengths=[3, 3, 3, 3],
               colors=[1, 2, 1, 2]),
      generate(width=7, height=3, cols=[0, 3], lengths=[3, 3], colors=[1, 2]),
  ]
  test = [
      generate(width=30, height=9, cols=[0, 3, 7, 11, 14, 17, 20, 24, 27],
               lengths=[2, 4, 3, 3, 3, 3, 4, 3, 3],
               colors=[1, 2, 2, 1, 2, 2, 2, 2, 1]),
      generate(width=30, height=3, cols=[0, 3, 7, 11, 14, 17, 20, 24, 27],
               lengths=[3, 3, 3, 3, 3, 3, 3, 3, 3],
               colors=[1, 2, 2, 1, 2, 2, 2, 2, 1])
  ]
  return {"train": train, "test": test}
