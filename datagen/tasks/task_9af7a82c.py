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


def _grow_counts(num_colors, area):
  """num_colors distinct cell-counts (each 1..30) that sum to area.

  Mirrors re_arc: start at 1..num_colors and repeatedly bump an eligible count,
  keeping every count distinct and <= 30 (so every color has a unique frequency,
  which the histogram rule requires).
  """
  counts = list(range(1, num_colors + 1))
  eligible = {num_colors - 1}
  while sum(counts) < area:
    ranked = sorted(eligible, reverse=True)
    idx = ranked[common.randint(0, len(ranked) - 1)]
    counts[idx] += 1
    if idx > 0:
      eligible.add(idx - 1)
    if idx < num_colors - 1 and counts[idx] == counts[idx + 1] - 1:
      eligible.discard(idx)
    if counts[idx] == 30:
      eligible.discard(idx)
  return counts


def generate(width=None, height=None, colors=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    colors: a list of digits representing the colors to be used
    num_colors: how many distinct colors (histogram bars) the input contains
  """
  if width is None:
    if num_colors is None:
      num_colors = common.randint(2, 9)
    num_colors = max(2, min(9, num_colors))
    least = num_colors * (num_colors + 1) // 2
    most = sum(range(30, 30 - num_colors, -1))
    options = sorted(
        [(h, w) for h in range(1, 31) for w in range(1, 31)
         if least <= h * w <= most],
        key=lambda hw: hw[0] * hw[1])
    height, width = options[common.randint(0, len(options) - 1)]
    counts = _grow_counts(num_colors, width * height)
    color_list = common.random_colors(num_colors)
    cells = common.sample(list(range(width * height)), width * height)
    colors, idx = [0] * (width * height), 0
    for i in range(num_colors):
      for _ in range(counts[i]):
        colors[cells[idx]] = color_list[i]
        idx += 1

  counts_to_colors = {colors.count(x): x for x in colors}
  counts = sorted(counts_to_colors.keys(), reverse=True)
  grid, output = common.grid(width, height), common.grid(len(counts), counts[0])
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]

  def reveal_count(count_idx):
    if count_idx >= len(counts):
      return
    count = counts[count_idx]
    for r in range(count):
      output[r][count_idx] = counts_to_colors[count]

  reveal_count(0)
  reveal_count(1)
  reveal_count(2)
  reveal_count(3)
  reveal_count(4)
  reveal_count(5)
  reveal_count(6)
  reveal_count(7)
  reveal_count(8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, colors=[2, 2, 1, 2, 3, 1, 1, 1, 1]),
      generate(width=4, height=3, colors=[3, 1, 1, 4, 2, 2, 2, 4, 4, 4, 4, 4]),
      generate(width=3, height=4, colors=[8, 8, 2, 3, 8, 8, 3, 3, 4, 3, 3, 4]),
      generate(width=3, height=4, colors=[1, 1, 1, 2, 2, 1, 2, 8, 1, 2, 8, 1]),
  ]
  test = [
      generate(width=4, height=4,
               colors=[8, 8, 2, 2, 1, 8, 8, 2, 1, 3, 3, 4, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
