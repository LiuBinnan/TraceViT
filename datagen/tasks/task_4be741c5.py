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


def generate(width=None, height=None, colors=None, lengths=None, xpose=None,
             num_colors=None, transpose=None, disturbances=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: the colors of the input grid
    lengths: the lengths of each line (all color 0, then all color 1, etc.)
    xpose: whether to transpose the input grid
  """
  if width is None:
    width = common.randint(6, 30)
  if height is None:
    height = common.randint(4, 30)
  if colors is None:
    if num_colors is None:
      num_colors = common.randint(2, max(2, min(10, width // 3)))
    colors = common.sample(list(range(10)), num_colors)
  if xpose is None:
    xpose = common.randint(0, 1) if transpose is None else transpose
  if lengths is None:
    # "Thicks" refer to columns of solid colors; "gaps" are columns with mixes.
    if width < len(colors):
      width = len(colors)
    boundaries = sorted(common.sample(list(range(1, width)), len(colors) - 1))
    raw_lengths = [b - a for a, b in zip([0] + boundaries, boundaries + [width])]
    thicks = [
        common.randint(1, length) if idx < len(colors) - 1 else length
        for idx, length in enumerate(raw_lengths)
    ]
    gaps = [raw_lengths[idx] - thicks[idx] for idx in range(len(colors) - 1)]
    # First, figure out how colors shift within each "gap" column.
    cols = []
    for gap in gaps:
      c = common.randint(0, gap)
      for _ in range(height):
        cols.append(c)
        c = min(max(c + common.randint(-2, 2), 0), gap)
    # Second, use those columns to determine column lengths.
    lengths = []
    for idx in range(len(colors)):
      for r in range(height):
        length = thicks[idx]
        if idx > 0:  # Add length contributed by the gap to the left.
          length += gaps[idx - 1] - cols[(idx - 1) * height + r]
        if idx < len(gaps):  # Add length contributed by the gap to the right.
          length += cols[idx * height + r]
        lengths.append(length)
    if disturbances is None:
      disturbances = common.randint(0, 3 * height * len(colors))
    for _ in range(disturbances):
      row = common.randint(0, height - 1)
      idx = common.randint(0, len(colors) - 2)
      left, right = idx * height + row, (idx + 1) * height + row
      delta = common.randint(-2, 2)
      if delta > 0 and lengths[right] > delta:
        lengths[left] += delta
        lengths[right] -= delta
      elif delta < 0 and lengths[left] > -delta:
        lengths[left] += delta
        lengths[right] -= delta

  grid = common.grid(width, height, 0)
  for r in range(height):
    col = 0
    for idx, color in enumerate(colors):
      for _ in range(lengths[idx * height + r]):
        grid[r][col] = color
        col += 1
  if xpose:
    grid = common.transpose(grid)
  band_output = common.grid(len(colors), 1, 0)
  for idx, color in enumerate(colors[:(len(colors) + 1) // 2]):
    band_output[0][idx] = color
  output = common.transpose(band_output) if xpose else [row[:] for row in band_output]
  for idx, color in enumerate(colors[(len(colors) + 1) // 2:],
                              start=(len(colors) + 1) // 2):
    band_output[0][idx] = color
  output = common.transpose(band_output) if xpose else [row[:] for row in band_output]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=14, colors=[4, 2, 8],
               lengths=[7, 8, 8, 7, 6, 6, 7, 7, 5, 5, 4, 4, 5, 6,
                        7, 4, 4, 5, 7, 6, 5, 6, 9, 9, 9, 8, 7, 7,
                        2, 4, 4, 4, 3, 4, 4, 3, 2, 2, 3, 4, 4, 3],
               xpose=0),
      generate(width=9, height=7, colors=[2, 8, 5],
               lengths=[4, 3, 3, 3, 4, 4, 3,
                        3, 5, 4, 3, 2, 3, 4,
                        2, 1, 2, 3, 3, 2, 2],
               xpose=1),
      generate(width=11, height=9, colors=[6, 4, 2, 3],
               lengths=[3, 2, 1, 1, 3, 2, 3, 2, 2,
                        4, 4, 5, 6, 4, 5, 3, 4, 5,
                        2, 2, 3, 2, 2, 2, 3, 2, 1,
                        2, 3, 2, 2, 2, 2, 2, 3, 3],
               xpose=1),
  ]
  test = [
      generate(width=14, height=14, colors=[3, 2, 1, 8],
               lengths=[4, 3, 5, 5, 4, 5, 3, 4, 4, 3, 3, 4, 5, 6,
                        5, 5, 2, 2, 5, 4, 5, 4, 4, 6, 6, 4, 3, 3,
                        3, 3, 3, 4, 3, 4, 4, 3, 4, 3, 2, 4, 4, 3,
                        2, 3, 4, 3, 2, 1, 2, 3, 2, 2, 3, 2, 2, 2],
               xpose=0),
  ]
  return {"train": train, "test": test}
