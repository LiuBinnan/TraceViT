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


def generate(same=None, diff=None, idx=None, color=None, size=5,
             sprite_h=None, sprite_w=None):
  """Returns input and output grids according to the given parameters.

  Args:
    same: a list of pixel indices for the "same" sprites
    diff: a list of pixel indices for the "different" sprite
    idx: the cell where the different sprite should live
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    sprite_h: the height of each sprite cell (decouples the row extent)
    sprite_w: the width of each sprite cell (decouples the col extent)
  """
  # Default sprite size is 2x2, matching the original square layout. The grid is
  # always a 2x2 arrangement of sprite cells separated by a 1-cell background gap,
  # so the original size=5 corresponds to sprite_h=sprite_w=2.
  if sprite_h is None:
    sprite_h = (size - 1) // 2
  if sprite_w is None:
    sprite_w = (size - 1) // 2
  num_pixels = sprite_h * sprite_w

  if same is None:
    while True:
      # CRITICAL GUARD: the pixel-index pool and the per-sprite "on" count are
      # derived from the (widened) sprite size; keep them in step with the loop
      # below (which now handles all num_pixels indices, not a fixed unrolled 4).
      lo = max(1, num_pixels // 3)
      hi = max(lo, (num_pixels * 2) // 3) if num_pixels > 1 else 1
      same = common.sample(range(num_pixels), common.randint(lo, hi))
      diff = common.sample(range(num_pixels), common.randint(lo, hi))
      if set(same) != set(diff): break
    idx = common.randint(0, 3)
    color = common.random_color()

  gw, gh = 2 * sprite_w + 1, 2 * sprite_h + 1
  grid = common.grid(gw, gh)
  output = common.grid(sprite_w, sprite_h)
  for i, r, c in zip(range(4), [0, 0, 1, 1], [0, 1, 0, 1]):
    the_list = diff if i == idx else same
    base_r, base_c = r * (sprite_h + 1), c * (sprite_w + 1)
    for k in the_list:
      grid[base_r + k // sprite_w][base_c + k % sprite_w] = color
  for k in diff:
    output[k // sprite_w][k % sprite_w] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(same=[1, 2, 3], diff=[0, 1, 2], idx=3, color=2),
      generate(same=[0, 3], diff=[0, 2, 3], idx=2, color=1),
      generate(same=[0, 1, 2], diff=[1, 2], idx=1, color=8),
  ]
  test = [
      generate(same=[0, 1, 3], diff=[0, 3], idx=1, color=5),
  ]
  return {"train": train, "test": test}
