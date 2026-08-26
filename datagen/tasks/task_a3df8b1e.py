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


def generate(width=None, height=10, num_lines=None, transform=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    num_lines: number of mirrored zigzag paths to complete
    transform: orientation transform to apply before adding mirrored paths
  """
  randomized = width is None
  if width is None:
    width = common.randint(2, 10)
  if randomized and height == 10:
    height = common.randint(width + 1, 30)
  if num_lines is None:
    num_lines = common.randint(1, 4) if randomized else 1
  if transform is None:
    transform = common.randint(0, 7) if randomized else 0
  num_lines = min(4, max(1, num_lines))
  transform, width, height = (
      transform % 8,
      height - 1 if height <= width and width >= 30 else width,
      width + 1 if height <= width and width < 30 else height,
  )

  path = []
  c, c_dir = 0, 1
  for r in range(height - 1, -1, -1):
    path.append((r, c))
    c += c_dir
    if c == 0 or c == width - 1:
      c_dir = -c_dir

  def orient_path(src_path, src_width, src_height, mode):
    if mode == 0:
      return src_path, src_width, src_height
    if mode == 1:
      return [(src_height - 1 - r, c) for r, c in src_path], src_width, src_height
    if mode == 2:
      return [(r, src_width - 1 - c) for r, c in src_path], src_width, src_height
    if mode == 3:
      return [(src_height - 1 - r, src_width - 1 - c)
              for r, c in src_path], src_width, src_height
    if mode == 4:
      return [(c, src_height - 1 - r) for r, c in src_path], src_height, src_width
    if mode == 5:
      return [(src_width - 1 - c, r) for r, c in src_path], src_height, src_width
    if mode == 6:
      return [(c, r) for r, c in src_path], src_height, src_width
    return [(src_width - 1 - c, src_height - 1 - r)
            for r, c in src_path], src_height, src_width

  path, width, height = orient_path(path, width, height, transform)
  paths = [path]
  if num_lines > 1:
    paths.append([(height - 1 - r, c) for r, c in path])
  if num_lines > 2:
    paths.append([(r, width - 1 - c) for r, c in path])
  if num_lines > 3:
    paths.append([(height - 1 - r, width - 1 - c) for r, c in path])

  grid = common.grid(width, height)
  output = common.grid(width, height)
  for line_path in paths:
    r, c = line_path[0]
    grid[r][c] = output[r][c] = common.blue()

  def draw_path_part(part_idx):
    for line_path in paths:
      split = (len(line_path) + 1) // 2
      start = 0 if part_idx == 0 else split
      stop = split if part_idx == 0 else len(line_path)
      for r, c in line_path[start:stop]:
        output[r][c] = common.blue()

  draw_path_part(0)
  draw_path_part(1)
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
