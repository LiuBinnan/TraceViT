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


def _symmetric_block(size, palette):
  """Builds a size x size block symmetric about the main diagonal."""
  block = [[common.black()] * size for _ in range(size)]
  for r in range(size):
    for c in range(r, size):
      color = palette[common.randint(0, len(palette) - 1)]
      block[r][c] = color
      block[c][r] = color
  return block


def _break_symmetry(block, size, num_asym, palette):
  """Perturbs num_asym off-diagonal cells so the block loses its symmetry."""
  pairs = [(r, c) for r in range(size) for c in range(r + 1, size)]
  num_asym = min(max(num_asym, 1), len(pairs))
  for r, c in common.sample(pairs, num_asym):
    choices = [color for color in palette if color != block[r][c]]
    block[c][r] = choices[common.randint(0, len(choices) - 1)]


def _one_asymmetric(colors, num_blocks, size, idx):
  """True iff block idx is the only one asymmetric about the main diagonal."""
  for k in range(num_blocks):
    asymmetric = False
    for r in range(size):
      for c in range(size):
        if colors[(k * size + r) * size + c] != colors[(k * size + c) * size + r]:
          asymmetric = True
    if asymmetric != (k == idx):
      return False
  return True


def generate(idx=None, colors=None, block_size=None, num_blocks=None,
             num_colors=None, num_asym=None):
  """Returns input and output grids according to the given parameters.

  Args:
    idx: which of the grids is the asymmetric one
    colors: the colors with which to fill the grid
    block_size: side length of each square block
    num_blocks: how many stacked blocks make up the input strip
    num_colors: how many distinct colors make up the grid's palette
    num_asym: how many off-diagonal cells break the answer block's symmetry
  """
  if idx is None:
    d = block_size if block_size is not None else common.randint(2, 7)
    ng = num_blocks if num_blocks is not None else common.randint(2, 30 // d)
    nc = num_colors if num_colors is not None else common.randint(2, 9)
    nd = num_asym if num_asym is not None else common.randint(
        1, max(1, d * (d - 1) // 2))
    idx = common.randint(0, ng - 1)
    while True:
      palette = common.random_colors(min(nc, 9))
      colors = [common.black()] * (ng * d * d)
      for k in range(ng):
        block = _symmetric_block(d, palette)
        if k == idx:
          _break_symmetry(block, d, nd, palette)
        for br in range(d):
          for bc in range(d):
            colors[(k * d + br) * d + bc] = block[br][bc]
      if _one_asymmetric(colors, ng, d, idx):
        break
  else:
    d, ng = 3, 3

  grid = common.grid(d, ng * d)
  for r in range(ng * d):
    for c in range(d):
      grid[r][c] = colors[r * d + c]
  output = common.deepcopy(grid)

  def reflect_blocks():
    for i in range(ng):
      for r in range(d):
        for c in range(r):
          output[i * d + r][c], output[i * d + c][r] = (
              output[i * d + c][r], output[i * d + r][c])

  def keep_asymmetric_block():
    for i in range(ng):
      changed = output[i * d:i * d + d] != grid[i * d:i * d + d]
      for r in range(d):
        for c in range(d):
          output[i * d + r][c] = grid[i * d + r][c] if changed else common.black()

  def crop_block():
    nonlocal output
    for i in range(ng):
      if output[i * d][0] != common.black():
        output = common.deepcopy(grid[i * d:i * d + d])
        return

  reflect_blocks()
  keep_asymmetric_block()
  crop_block()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idx=2,
               colors=[8, 9, 8, 9, 8, 8, 8, 8, 8, 2, 2, 1, 2, 2, 1, 1, 1, 2, 4,
                       4, 4, 4, 4, 3, 3, 3, 3]),
      generate(idx=1,
               colors=[1, 5, 5, 5, 1, 1, 5, 1, 1, 3, 3, 3, 3, 6, 3, 3, 6, 6, 7,
                       7, 7, 7, 2, 2, 7, 2, 2]),
      generate(idx=2,
               colors=[2, 2, 2, 2, 2, 3, 2, 3, 3, 5, 7, 7, 7, 5, 5, 7, 5, 5, 8,
                       8, 1, 1, 8, 1, 1, 8, 1]),
      generate(idx=0,
               colors=[8, 8, 4, 4, 4, 4, 4, 4, 8, 1, 1, 3, 1, 3, 3, 3, 3, 1, 6,
                       2, 2, 2, 2, 2, 2, 2, 6]),
  ]
  test = [
      generate(idx=0,
               colors=[5, 4, 4, 4, 5, 4, 4, 5, 4, 3, 3, 2, 3, 3, 2, 2, 2, 3, 1,
                       1, 1, 1, 8, 8, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
