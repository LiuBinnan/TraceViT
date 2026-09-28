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


def generate(size=None, tcolor=None, bcolor=None, fcolor=None, lrow=None,
             mrow=None, flip=None, xpose=None, thues=None, bhues=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if size is None:
    spacing = common.randint(0, 1)
    size = common.randint(8, 20)
    mrow = common.randint(1, size // 2)
    lrow = common.randint(mrow + 1, size - 3)
    colors = common.shuffle(list(range(10)))
    tcolor = colors.pop()
    bcolor = tcolor if common.randint(0, 2) else colors.pop()
    fcolor = colors.pop()
    num_colors = common.randint(3, 5)
    while len(colors) > num_colors:
      colors.pop()
    while True:
      col, thues, bhues, sames = 1, [], [], []
      while True:
        thues.append(common.choice(colors))
        bhues.append(thues[-1] if common.randint(0, 1) else common.choice(colors))
        sames.append(thues[-1] == bhues[-1])
        col += 1
        if col + 1 >= size: break
        if spacing:
          thues.append(-1)
          bhues.append(-1)
          col += 1
        if col + 1 >= size: break
        if common.randint(0, 9) == 0:
          thues.append(-1)
          bhues.append(-1)
          col += 1
        if col + 1 >= size: break
      if True in sames and False in sames: break
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  # Input: two colour zones split by a divider frame, with a top token on row
  # `mrow` and a fixed bottom token just under the divider in each live column.
  grid = common.grid(size, size)
  common.rect(grid, size, lrow, 0, 0, tcolor)
  common.rect(grid, size, size - lrow, lrow, 0, bcolor)
  common.hollow_rect(grid, size, size, lrow, 0, fcolor)
  for i, (thue, bhue) in enumerate(zip(thues, bhues)):
    if thue == -1 or bhue == -1: continue
    grid[lrow + 1][i + 1] = bhue
    grid[mrow][i + 1] = thue

  # Solve the puzzle forward on a fresh board: each column's top token moves to
  # the divider if it matches its bottom token, or up to the top edge if not.
  output = common.grid(size, size)

  def build_field():
    """Redraws the two colour zones and the dividing frame (fixed board)."""
    common.rect(output, size, lrow, 0, 0, tcolor)
    common.rect(output, size, size - lrow, lrow, 0, bcolor)
    common.hollow_rect(output, size, size, lrow, 0, fcolor)

  def carry_bottom():
    """Keeps each column's bottom token as the anchor its top token compares to."""
    for i, (thue, bhue) in enumerate(zip(thues, bhues)):
      if thue == -1 or bhue == -1: continue
      output[lrow + 1][i + 1] = bhue

  def sink_matches():
    """Matched columns: the top token descends to touch the divider."""
    for i, (thue, bhue) in enumerate(zip(thues, bhues)):
      if thue == -1 or bhue == -1 or thue != bhue: continue
      output[lrow - 1][i + 1] = thue

  def raise_mismatches():
    """Mismatched columns: the top token rises to the top edge."""
    for i, (thue, bhue) in enumerate(zip(thues, bhues)):
      if thue == -1 or bhue == -1 or thue == bhue: continue
      output[0][i + 1] = thue

  build_field()
  carry_bottom()
  sink_matches()
  raise_mismatches()

  if flip: grid, output = common.flip(grid), common.flip(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, tcolor=9, bcolor=9, fcolor=0, lrow=7, mrow=3,
               flip=False, xpose=False,
               thues=[5, -1, 3, -1, 5, -1, 2, -1, 3, -1, 2, -1, 5],
               bhues=[5, -1, 5, -1, 3, -1, 5, -1, 3, -1, 5, -1, 2]),
      generate(size=16, tcolor=7, bcolor=7, fcolor=4, lrow=13, mrow=7,
               flip=True, xpose=True,
               thues=[8, -1, 2, -1, 8, -1, 1, -1, 8, -1, 5, -1, -1, 1],
               bhues=[1, -1, 1, -1, 3, -1, 1, -1, 8, -1, 1, -1, -1, 8]),
  ]
  test = [
      generate(size=8, tcolor=3, bcolor=8, fcolor=4, lrow=3, mrow=2,
               flip=True, xpose=True,
               thues=[0, 5, -1, 2, 0, 5],
               bhues=[5, 5, -1, 2, 2, 0]),
  ]
  return {"train": train, "test": test}
