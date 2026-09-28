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


def generate(width=None, height=None, wide=None, tall=None, lrow=None,
             lcol=None, brow=None, bcol=None, left=None, right=None,
             colors=None, pattern=None, canvas_width=None,
             canvas_height=None, half_width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the grids.
    height: Height of the grids.
    wide: Width of the block.
    tall: Height of the block.
    lrow: Row of the legend.
    lcol: Column of the legend.
    brow: Row of the block.
    bcol: Column of the block.
    left: Left boundary of the block.
    right: Right boundary of the block.
    colors: Colors of the block.
    pattern: Pattern of the block.
    canvas_width: Sampled width when an explicit recipe is not supplied.
    canvas_height: Sampled height when an explicit recipe is not supplied.
    half_width: Sampled half-width of the mirrored sprite.
  """

  def draw():
    if left >= right: return None, None  # No colors shown
    if left == 0 and right == len(colors): return None, None  # Everything shown
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      for j, bit in enumerate(pattern):
        if bit == "0": continue
        row, col = brow + i * tall + j // wide, bcol + j % wide
        output[row][col] = int(bit) * color
        if left <= i < right:
          grid[row][col] = int(bit) * color
    # Check lengend area is empty.
    for r in range(-1, 4):
      for c in range(-1, len(colors) + 1):
        if grid[lrow + r][lcol + c]: return None, None
    # Draw legend.
    for r in range(3):
      for c in range(len(colors)):
        if grid[lrow + r][lcol + c]: return None, None
        grid[lrow + r][lcol + c] = colors[c]
    return grid, output

  if width is None:
    for attempt in range(100):
      width = (common.randint(12, 20)
               if canvas_width is None else canvas_width)
      height = (common.randint(14, 26)
                if canvas_height is None else canvas_height)
      num_colors = common.randint(3, min(5, height // 3))
      colors = common.random_colors(num_colors)
      half = common.randint(2, 4) if half_width is None else half_width
      wide, tall = half * 2, common.randint(3, height // len(colors))
      lrow = 1 if common.randint(0, 1) else height - 4
      lcol = common.randint(1, width - len(colors) - 1)
      brow = common.randint(0, height - tall * len(colors))
      bcol = common.randint(0, width - wide)
      left = common.randint(0, len(colors) - 1)
      right = common.randint(1, len(colors))
      if attempt == 99:
        lrow = 1
        left, right = len(colors) - 1, len(colors)
      grid = common.grid(wide, tall)
      pixels = common.diagonally_connected_sprite(
          wide // 2, tall, wide // 2 + tall)
      for (row, col) in pixels:
        grid[row][col] = grid[row][wide - 1 - col] = 1
      pattern = "".join(map(str, common.flatten(grid)))
      grid, _ = draw()
      if grid: break

  # Input: a color legend listing colors[0..n-1] in order, plus a partial
  # vertical stack of the shape (only copies left..right-1 are drawn). The
  # legend is the key; rebuild the FULL stack from it (draw() is unchanged).
  grid, _ = draw()
  output = common.grid(width, height)

  def reveal_copy(i):
    """Stamps the i-th stacked shape copy in its legend color colors[i]."""
    if i >= len(colors): return
    color = colors[i]
    for j, bit in enumerate(pattern):
      if bit == "0": continue
      row, col = brow + i * tall + j // wide, bcol + j % wide
      output[row][col] = color

  # Complete the stack top-to-bottom: one copy per legend color.
  reveal_copy(0)
  reveal_copy(1)
  reveal_copy(2)
  reveal_copy(3)
  reveal_copy(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=18, wide=6, tall=3, lrow=1, lcol=7, brow=5,
               bcol=2, left=1, right=3, colors=[7, 2, 1, 3],
               pattern="010010111111001100"),
      generate(width=13, height=17, wide=8, tall=5, lrow=1, lcol=2, brow=2,
               bcol=1, left=1, right=3, colors=[4, 1, 6],
               pattern="0011110000100100111001110110011001111110"),
  ]
  test = [
      generate(width=15, height=18, wide=6, tall=3, lrow=14, lcol=8, brow=0,
               bcol=3, left=2, right=3, colors=[2, 3, 1, 8, 7],
               pattern="001100010010111111"),
  ]
  return {"train": train, "test": test}
