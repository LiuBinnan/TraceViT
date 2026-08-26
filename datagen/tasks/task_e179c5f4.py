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


def generate(width=None, height=10, line_count=None, xpose=False):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    line_count: the number of mirrored zigzag starts to complete
    xpose: whether to transpose the final grids
  """
  if width is None:
    width = common.randint(2, 10)
  if line_count is None:
    line_count = 1
  line_count = max(1, min(4, line_count))
  if height <= width:
    height = width + 1

  if xpose:
    grid, output = common.grid(height, width), common.grid(height, width,
                                                          common.cyan())
  else:
    grid, output = common.grid(width, height), common.grid(width, height,
                                                          common.cyan())
  path = []
  c, c_dir = 0, 1
  for r in range(height - 1, -1, -1):
    path.append((r, c))
    c += c_dir
    if c == 0 or c == width - 1:
      c_dir = -c_dir
  paths = [path]
  if line_count > 1:
    paths.append([(r, width - 1 - c) for r, c in path])
  if line_count > 2:
    paths.append([(height - 1 - r, c) for r, c in path])
  if line_count > 3:
    paths.append([(height - 1 - r, width - 1 - c) for r, c in path])
  for line in paths:
    r, c = line[0]
    if xpose:
      grid[c][r] = output[c][r] = common.blue()
    else:
      grid[r][c] = output[r][c] = common.blue()
  for line in paths:
    for r, c in line[:len(line) // 2]:
      if xpose:
        output[c][r] = common.blue()
      else:
        output[r][c] = common.blue()
  for line in paths:
    for r, c in line[len(line) // 2:]:
      if xpose:
        output[c][r] = common.blue()
      else:
        output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2),
      generate(width=3),
      generate(width=4),
  ]
  test = [
      generate(width=5),
  ]
  return {"train": train, "test": test}
