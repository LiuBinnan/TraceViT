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


def generate(width=None, height=None, rows=None, cols=None, offset=None,
             redline=None, flip=None, xpose=None, obj_height=None,
             obj_width=None, cell_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the offset of the green creature
    redline: the horizontal coordinate of the redline
    flip: whether to flip the input grid horizontally
    xpose: whether to transpose the input grid
    obj_height: the sampled height of the green creature's bounding box
    obj_width: the sampled width of the green creature's bounding box
    cell_count: the number of cells in the green creature
  """
  if (width is None or height is None or rows is None or cols is None or
      offset is None or redline is None or flip is None or xpose is None):
    if width is None:
      width = common.randint(6, 30)
    if height is None:
      height = common.randint(4, 30)
    max_obj_width = max(1, (width - 3) // 2)
    if obj_width is None:
      obj_width = common.randint(1, max_obj_width)
    else:
      obj_width = min(max(1, obj_width), max_obj_width)
    if obj_height is None:
      obj_height = common.randint(1, height)
    else:
      obj_height = min(max(1, obj_height), height)
    obj_area = obj_width * obj_height
    if cell_count is None:
      delta = common.randint(0, obj_area // 2)
      cell_count = common.choice((delta + 1, obj_area - delta))
    cell_count = min(max(1, cell_count), obj_area)
    if rows is None or cols is None:
      pixels = [(common.randint(0, obj_height - 1),
                 common.randint(0, obj_width - 1))]
      while len(pixels) < cell_count:
        seen = set(pixels)
        frontier = []
        for pixel_r, pixel_c in pixels:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if dr == 0 and dc == 0:
                continue
              r, c = pixel_r + dr, pixel_c + dc
              if r < 0 or r >= obj_height or c < 0 or c >= obj_width:
                continue
              if (r, c) in seen or (r, c) in frontier:
                continue
              frontier.append((r, c))
        pixels.append(common.choice(frontier))
      min_row = min(r for r, _ in pixels)
      min_col = min(c for _, c in pixels)
      pixels = [(r - min_row, c - min_col) for r, c in pixels]
      rows, cols = zip(*pixels)
    max_col = max(cols)
    if redline is None:
      redline = common.randint(max_col + 2, width - 1)
    else:
      redline = min(max(max_col + 2, redline), width - 1)
    if offset is None:
      offset = common.randint(0, redline - max_col - 1)
    else:
      offset = min(max(0, offset), redline - max_col - 1)
    if flip is None:
      flip = common.randint(0, 1)
    if xpose is None:
      xpose = common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c + offset] = common.green()
    output[r][c + redline - max(cols) - 1] = common.green()
  for r in range(height):
    output[r][redline] = grid[r][redline] = common.red()
    output[r][redline - max(cols) - 2] = common.cyan()
  if flip: grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=4, rows=[0, 1, 1, 1, 2, 2, 3, 3, 3],
               cols=[1, 1, 2, 3, 0, 1, 1, 2, 3], offset=0, redline=10, flip=0,
               xpose=0),
      generate(width=17, height=5, rows=[4, 3, 3, 2, 1, 1, 1, 0, 0, 0],
               cols=[2, 2, 3, 3, 0, 2, 3, 0, 1, 2], offset=1, redline=15,
               flip=0, xpose=1),
      generate(width=17, height=5, rows=[0, 0, 0, 1, 1, 2, 3, 3, 3],
               cols=[0, 1, 2, 0, 2, 2, 0, 1, 2], offset=3, redline=13, flip=1,
               xpose=1),
  ]
  test = [
      generate(width=18, height=4, rows=[0, 0, 1, 1, 2, 2, 2, 3],
               cols=[0, 1, 0, 2, 0, 1, 2, 2], offset=4, redline=13, flip=1,
               xpose=0),
  ]
  return {"train": train, "test": test}
