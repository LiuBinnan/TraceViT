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


def generate(size=None, flip=None, flop=None, xpose=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
    xpose: Whether to transpose the grid.
    colors: The colors of the grid.
  """

  def draw():
    grid, output = common.grids(size, size, 7)
    for i, color in enumerate(colors):
      if color: output[i // size][i % size] = grid[i // size][i % size] = 8
    output[1][0] = output[1][1] = grid[1][0] = grid[1][1] = 3
    row, col, rdir, cdir, bounces = 1, 2, 0, 1, 0
    while True:
      if bounces > 10: return None, None, None  # avoid an infinite loop
      if row < 0 or col < 0 or row >= size or col >= size: break
      output[row][col] = 3
      if common.get_pixel(output, row + rdir, col + cdir) == 8:
        bounces += 1
        alt_row = row if abs(rdir) else (row - 1)
        alt_col = col if abs(cdir) else (col - 1)
        increase = common.get_pixel(output, alt_row, alt_col) == 8
        alt_row = row if abs(rdir) else (row + 1)
        alt_col = col if abs(cdir) else (col + 1)
        decrease = common.get_pixel(output, alt_row, alt_col) == 8
        if increase == decrease: return None, None, None
        if decrease: rdir, cdir = 0 if abs(rdir) else -1, 0 if abs(cdir) else -1
        if increase: rdir, cdir = 0 if abs(rdir) else 1, 0 if abs(cdir) else 1
      row, col = row + rdir, col + cdir
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output, bounces

  if size is None:
    flip, flop = common.randint(0, 1), common.randint(0, 1)
    xpose = common.randint(0, 1)
    expected_bounces = common.randint(3, 6)
    attempts = 0
    while True:
      size = common.randint(5, 14)
      colors = [0 if common.randint(0, 4) else 1 for _ in range(size * size)]
      colors[size] = colors[size + 1] = colors[size + 2] = 0
      grid, _, bounces = draw()
      if grid is not None and bounces == expected_bounces: break
      attempts += 1
      if attempts < 300: continue

      # Construct a southeast staircase with exactly the requested number of
      # turns.  Each turn has a reflector ahead and another opposite the new
      # direction; the protected path prevents distractors from changing it.
      if expected_bounces >= 5 and size < 6:
        size = common.randint(6, 14)
      path, reflectors = set(), set()
      row, col, direction = 1, 2, 0  # east=0, south=1
      horizontal = (expected_bounces + 1) // 2
      vertical = expected_bounces // 2
      for _ in range(expected_bounces):
        if direction == 0:
          horizontal -= 1
          end = common.randint(col, size - horizontal - 2)
          path.update((row, c) for c in range(col, end + 1))
          col = end
          reflectors.update([(row, col + 1), (row - 1, col)])
          row, direction = row + 1, 1
        else:
          vertical -= 1
          end = common.randint(row, size - vertical - 2)
          path.update((r, col) for r in range(row, end + 1))
          row = end
          reflectors.update([(row + 1, col), (row, col - 1)])
          col, direction = col + 1, 0
      if direction == 0:
        path.update((row, c) for c in range(col, size))
      else:
        path.update((r, col) for r in range(row, size))

      source = {(1, 0), (1, 1), (1, 2)}
      colors = []
      for row in range(size):
        for col in range(size):
          pixel = (row, col)
          color = pixel in reflectors
          if pixel not in path and pixel not in source:
            color = color or common.randint(0, 4) == 0
          colors.append(1 if color else 0)
      colors[size] = colors[size + 1] = colors[size + 2] = 0
      grid, _, bounces = draw()
      if grid is not None and bounces == expected_bounces: break
      raise ValueError("constructive bounce fallback failed")

  grid, _, _ = draw()
  output = common.deepcopy(grid)

  def trace_segments():
    """Traces the beam into one segment per reflector encounter."""
    reflectors = common.grid(size, size)
    for i, color in enumerate(colors):
      if color:
        reflectors[i // size][i % size] = common.gray()
    segments, segment = [], []
    row, col, rdir, cdir = 1, 2, 0, 1
    while 0 <= row < size and 0 <= col < size:
      segment.append((row, col))
      if common.get_pixel(reflectors, row + rdir, col + cdir) == common.gray():
        segments.append(segment)
        segment = []
        alt_row = row if abs(rdir) else (row - 1)
        alt_col = col if abs(cdir) else (col - 1)
        increase = common.get_pixel(reflectors, alt_row, alt_col) == common.gray()
        alt_row = row if abs(rdir) else (row + 1)
        alt_col = col if abs(cdir) else (col + 1)
        decrease = common.get_pixel(reflectors, alt_row, alt_col) == common.gray()
        if decrease:
          rdir, cdir = 0 if abs(rdir) else -1, 0 if abs(cdir) else -1
        if increase:
          rdir, cdir = 0 if abs(rdir) else 1, 0 if abs(cdir) else 1
      row, col = row + rdir, col + cdir
    segments.append(segment)
    return segments

  segments = trace_segments()

  def draw_segment(i):
    """Draws one beam segment in the input grid's orientation."""
    if i >= len(segments):
      return
    for row, col in segments[i]:
      if flip:
        row = size - row - 1
      if flop:
        col = size - col - 1
      if xpose:
        row, col = col, row
      output[row][col] = common.green()

  draw_segment(0)
  draw_segment(1)
  draw_segment(2)
  draw_segment(3)
  draw_segment(4)
  draw_segment(5)
  draw_segment(6)
  draw_segment(7)
  draw_segment(8)
  draw_segment(9)
  draw_segment(10)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, flip=True, flop=False, xpose=False,
               colors=[0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 1, 0,
                       0, 0, 0, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 0, 0, 0, 1,
                       1, 0, 0, 1, 0, 1, 0]),
      generate(size=5, flip=False, flop=True, xpose=True,
               colors=[0, 0, 0, 1, 0,
                       0, 0, 0, 0, 1,
                       0, 0, 0, 0, 0,
                       1, 0, 0, 0, 1,
                       0, 1, 0, 1, 0]),
  ]
  test = [
      generate(size=8, flip=False, flop=True, xpose=False,
               colors=[0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 0,
                       0, 1, 0, 1, 0, 0, 0, 0,
                       1, 0, 0, 0, 1, 0, 1, 0,
                       0, 0, 0, 0, 1, 0, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
