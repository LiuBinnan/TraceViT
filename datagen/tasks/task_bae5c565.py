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


def generate(colors=None, boost=None):
  """Returns input and output grids according to the given parameters.

  Args:
   colors: the colors of the pixels.
   boost: how much to boost the middle pillar.
  """

  if colors is None:
    size = 2 * common.randint(4, 14) + 1
    colors = common.choices([0, 1, 2, 3, 4, 6, 7, 8, 9], size)
    colors[size // 2] = 5
    boost = common.randint(0, 3)

  # Input: a row of colors on top, plus the central 8-pillar (the marker column
  # grown downward). The output turns those top colors into a symmetric pyramid:
  # each column c falls into a pillar whose top sits at row |c - mid| below the
  # center's, so pillars shorten with distance from the middle.
  size = len(colors)
  grid, output = common.grids(size, size, 5)
  mid = size // 2
  for c, color in enumerate(colors):
    grid[0][c] = color
  for r in range(max(mid - boost, size - mid - 1 - boost), size):
    grid[r][mid] = 8

  def reveal_level(k):
    """Grows the pyramid's distance-`k` pillars (both sides, one step shorter)."""
    if k > size // 2: return
    for c in {mid - k, mid + k}:
      for r in range(max(c - boost, size - c - 1 - boost), size):
        output[r][c] = 8 if c * 2 + 1 == size else colors[c]

  reveal_level(0)
  reveal_level(1)
  reveal_level(2)
  reveal_level(3)
  reveal_level(4)
  reveal_level(5)
  reveal_level(6)
  for k in range(7, size // 2 + 1): reveal_level(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 7, 1, 9, 1, 5, 8, 6, 0, 3, 2, 2], boost=1),
      generate(colors=[0, 1, 6, 9, 5, 9, 6, 1, 0], boost=1),
  ]
  test = [
      generate(colors=[4, 6, 7, 2, 9, 5, 3, 3, 4, 3, 3], boost=0),
  ]
  return {"train": train, "test": test}
