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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(size, size)
    origins = []
    for i, color in enumerate(colors):
      r, c = i // size, i % size
      output[r][c] = grid[r][c] = color
      if color not in [0, 5]: origins.append((r, c))
    for origin in origins:
      queue, changed = [origin], False
      while queue:
        row, col = queue.pop()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          r, c = row + dr, col + dc
          color = common.get_pixel(output, r, c)
          if color in [-1, 5, output[row][col]]: continue
          if color != 0: return None, None  # Another color overlaps with us.
          output[r][c] = output[row][col]
          queue.append((r, c))
          changed = True
      if not changed: return None, None  # No change.
    return grid, output

  if size is None:
    for _attempt in range(500):
      size = common.randint(7, 16)
      colors = common.choices([0, 5], size * size)
      values = common.random_colors(common.choice([2, 3, 3, 3]), exclude=[5])
      for value in values:
        row, col = common.randint(0, size - 1), common.randint(0, size - 1)
        colors[row * size + col] = value
      if sum(color not in [0, 5] for color in colors) != len(values):
        continue
      grid, _ = draw()
      if grid: break
    else:
      raise RuntimeError("Unable to sample non-overlapping flood regions")

  # Input: black/gray background with the colored seed pixels. Seeds are
  # collected in reading order; each will flood its own black region.
  grid, output = common.grids(size, size)
  origins = []
  for i, color in enumerate(colors):
    r, c = i // size, i % size
    output[r][c] = grid[r][c] = color
    if color not in [common.black(), common.gray()]:
      origins.append((r, c))

  def flood_from(idx):
    """Floods seed idx's color across its connected black region (gray walls)."""
    if idx >= len(origins):
      return
    queue = [origins[idx]]
    while queue:
      row, col = queue.pop()
      for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + dr, col + dc
        color = common.get_pixel(output, r, c)
        if color in [-1, common.gray(), output[row][col]]:
          continue
        if color != common.black():
          continue
        output[r][c] = output[row][col]
        queue.append((r, c))

  flood_from(0)
  flood_from(1)
  flood_from(2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, colors=[5, 1, 0, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 0, 3, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 5, 0, 0, 7, 0, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 0, 5, 5, 0]),
      generate(size=9, colors=[5, 0, 6, 0, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 5, 5, 8, 0, 0, 5, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0]),
      generate(size=7, colors=[0, 0, 5, 0, 0, 5, 0, 5, 5, 4, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0, 5, 0, 0, 5, 0, 5, 0, 8, 5, 3, 0, 5, 5, 5, 0, 0]),
  ]
  test = [
      generate(size=9, colors=[0, 0, 0, 5, 0, 3, 0, 5, 0, 5, 5, 5, 0, 0, 0, 5, 5, 0, 0, 8, 5, 5, 0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 5, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 6, 0, 0, 5]),
  ]
  return {"train": train, "test": test}
