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


def generate(width=None, height=None, gcol=None, offset=None, bcols=None,
             lengths=None, colors=None, extra=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    gcol: The column of the gray dot.
    offset: The row offset of the first stripe.
    bcols: The column of each stripe.
    lengths: The length of each stripe.
    colors: The color of each stripe.
    extra: An extra parameter used in some broken / ambiguous examples.
  """

  if width is None:
    width, offset = common.randint(3, 16), common.randint(1, 2)
    height = max(4, width - (0 if width < 10 else common.randint(0, 3)))
    gcol = common.randint(2, width - 1)
    bcols, lengths, colors = [], [], []
    for _ in range(offset, height, 2):
      lengths.append(common.randint(2, min(gcol, 5)))
      bcols.append(common.randint(0, gcol - lengths[-1]))
      colors.append(common.randint(1, 9))

  # The solving story: the grey dot marks a target column; each horizontal
  # stripe measures its own length and stamps a length-coded pixel in that
  # column (2->blue, 3->yellow, 4->maroon, 5->magenta). We build the input,
  # then reveal one stripe's code per frame.
  grid = common.grid(width, height)
  grid[0][gcol] = common.gray()
  for i, (bcol, length, color) in enumerate(zip(bcols, lengths, colors)):
    row = offset + 2 * i
    for j in range(length):
      grid[row][bcol + j] = color
  output = common.deepcopy(grid)

  def reveal_marker(i):
    """Stamps stripe i's length-code in the grey dot's column."""
    if i >= len(lengths): return
    row = offset + 2 * i
    length = lengths[i]
    if length == 2: output[row][gcol] = common.blue()
    if length == 3: output[row][gcol] = common.yellow()
    if length == 4: output[row][gcol] = 9 - (extra if extra else 0)
    if length == 5: output[row][gcol] = 6 + (extra if extra else 0)

  reveal_marker(0)
  reveal_marker(1)
  reveal_marker(2)
  reveal_marker(3)
  reveal_marker(4)
  reveal_marker(5)
  for i in range(6, len(lengths)):
    reveal_marker(i)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=4, gcol=2, offset=2, bcols=[0], lengths=[2],
               colors=[1]),
      generate(width=10, height=10, gcol=7, offset=2, bcols=[1, 1, 1, 1],
               lengths=[3, 2, 4, 5], colors=[2, 3, 1, 9]),
      generate(width=11, height=8, gcol=9, offset=1, bcols=[2, 0, 1, 1],
               lengths=[2, 2, 5, 2], colors=[4, 2, 7, 8], extra=3),
      generate(width=6, height=6, gcol=5, offset=1, bcols=[0, 0, 0],
               lengths=[2, 3, 4], colors=[2, 2, 2]),
  ]
  test = [
      generate(width=12, height=10, gcol=4, offset=2, bcols=[0, 0, 1, 0],
               lengths=[2, 3, 2, 4], colors=[2, 2, 5, 9]),
  ]
  return {"train": train, "test": test}
