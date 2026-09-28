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


def generate(colors=None, bsize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    bsize: The side length of each block.
  """

  if bsize is None:
    bsize = common.choice([3, 4, 5]) if colors is None else 3

  if colors is None:
    colors = ""
    counts = common.shuffle(common.sample(range(bsize * bsize + 1), 9))
    for count in counts:
      pixels = common.sample(
          [(r, c) for r in range(bsize) for c in range(bsize)], count)
      for r in range(bsize):
        for c in range(bsize):
          colors += "1" if (r, c) in pixels else "2"

  side = (bsize + 1) * 3 - 1
  grid, output = common.grids(side, side)
  blue_to_groups = {}
  for gr in range(3):
    for gc in range(3):
      blues = 0
      for r in range(bsize):
        for c in range(bsize):
          color = int(colors[gr * (3 * bsize * bsize)
                             + gc * (bsize * bsize) + r * bsize + c])
          grid[(bsize + 1) * gr + r][(bsize + 1) * gc + c] = color
          if color == 1: blues += 1
      blue_to_groups[blues] = 3 * gr + gc

  # The blocks are ranked by how many blue pixels they hold; the output lays
  # them out in that order, filling the bottom row left-to-right, then upward.
  order = sorted(blue_to_groups.keys())

  def place_block(i):
    """Drops the block with the i-th fewest blues into its ranked cell."""
    if i >= len(order): return
    group = blue_to_groups[order[i]]
    for r in range(bsize):
      for c in range(bsize):
        color = int(colors[group * (bsize * bsize) + r * bsize + c])
        output[(bsize + 1) * (2 - i // 3) + r][
            (bsize + 1) * (i % 3) + c] = color

  place_block(0)
  place_block(1)
  place_block(2)
  place_block(3)
  place_block(4)
  place_block(5)
  place_block(6)
  place_block(7)
  place_block(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="112212122212212122211111112121211122111111121222212222122221222121211121111111111"),
      generate(colors="221122222222222122121112212221122212212121221222222222211121121111111121111211112"),
      generate(colors="222221222222222222221122212211121212111111111111211121211121211121121222211111111"),
  ]
  test = [
      generate(colors="222122212212122212221121212112121121111111111111112111211111112211121122222222222"),
  ]
  return {"train": train, "test": test}
