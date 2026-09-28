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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    def get_color(row, col):
      seen, queue = [], [(row, col)]
      while queue:
        r, c = queue.pop()
        if (r, c) in seen: continue
        seen.append((r, c))
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
          nr, nc = r + dr, c + dc
          if 0 <= nr < height and 0 <= nc < width:
            if colors[nr * width + nc] == 2 and (nr, nc) not in seen:
              queue.append((nr, nc))
      return 6 if len(seen) >= 4 else 2
    for i, color in enumerate(colors):
      if not color: continue
      grid[i // width][i % width] = color
      output[i // width][i % width] = get_color(i // width, i % width)
    if len(set(common.flatten(output))) != 3: return None, None
    return grid, output

  def make_shape(width, height):
    while True:
      num_pixels = common.randint(1, 8)
      shape = []
      queue = [(common.randint(0, height - 1), common.randint(0, width - 1))]
      while queue and len(shape) < num_pixels:
        queue = common.shuffle(queue)
        r, c = queue.pop()
        if (r, c) in shape: continue
        shape.append((r, c))
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in shape or (nc, nr) in queue: continue
            if 0 <= nr < height and 0 <= nc < width: queue.append((nr, nc))
      if len(shape) < 4 or common.connected(shape): break
    return shape

  if colors is None:
    width, height = common.randint(6, 24), common.randint(6, 24)
    # Area-scaled ceiling: larger canvases hold more no-touch shapes (grids stay
    # <=24x24 <=30 by construction). The divisor keeps shape density comfortable
    # (roughly the original 8-on-144 packing) so the no-touch rejection loop
    # settles fast. Floor at the original minimum of 4 for small grids.
    num_shapes_hi = min(12, (width * height) // 24)
    if num_shapes_hi < 4: num_shapes_hi = 4
    num_shapes = common.randint(4, num_shapes_hi)
    attempts = 0
    while True:
      # Cap the no-touch rejection tail: if a layout will not settle, thin the
      # shape count (never below 4) and keep trying, so wide bands cannot hang.
      attempts += 1
      if attempts > 30:
        attempts = 0
        if num_shapes > 4: num_shapes -= 1
      shapes = [make_shape(width, height) for _ in range(num_shapes)]
      colors = common.grid(width, height, -1)
      good = True
      # Draw the IDs of the shapes (they can't overlap).
      for i, shape in enumerate(shapes):
        for r, c in shape:
          if colors[r][c] != -1: good = False
          colors[r][c] = i
      # Check that no shape touches any other.
      for row in range(height):
        for col in range(width):
          if colors[row][col] == -1: continue
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              color = common.get_pixel(colors, row + dr, col + dc)
              if color not in [-1, colors[row][col]]: good = False
      if not good: continue
      colors = [2 if c != -1 else 0 for c in common.flatten(colors)]
      grid, _ = draw()
      if grid: break

  # Solve it forward. Every isolated blob is classified by size: a blob of 4 or
  # more cells becomes color 6, a smaller blob stays color 2. Reveal the answer
  # one blob at a time, painting each in the color its size class earns.
  grid, full_output = draw()
  output = common.grid(width, height)

  blobs = []
  visited = set()
  for r in range(height):
    for c in range(width):
      if grid[r][c] == 0 or (r, c) in visited: continue
      cells, stack = [], [(r, c)]
      while stack:
        a, b = stack.pop()
        if (a, b) in visited: continue
        visited.add((a, b))
        cells.append((a, b))
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            na, nb = a + dr, b + dc
            if 0 <= na < height and 0 <= nb < width and grid[na][nb] != 0 and (na, nb) not in visited:
              stack.append((na, nb))
      blobs.append(cells)

  def reveal_blob(k):
    """Paints the k-th blob in the color its size class earns (6 big, 2 small)."""
    nonlocal output
    if k >= len(blobs): return
    for r, c in blobs[k]:
      output[r][c] = full_output[r][c]

  reveal_blob(0)
  reveal_blob(1)
  reveal_blob(2)
  reveal_blob(3)
  reveal_blob(4)
  reveal_blob(5)
  reveal_blob(6)
  reveal_blob(7)
  # Catch-all: the widened num_shapes band can exceed the 8 unrolled reveals, so
  # paint any remaining blobs here to keep the final frame the complete answer.
  for k in range(8, len(blobs)): reveal_blob(k)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6,
               colors=[2, 2, 0, 0, 0, 2,
                       2, 2, 0, 0, 0, 2,
                       0, 0, 0, 2, 0, 0,
                       0, 2, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 2,
                       0, 2, 2, 2, 0, 0]),
      generate(width=12, height=10,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                       0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                       0, 2, 0, 0, 2, 2, 0, 0, 0, 2, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2,
                       0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0]),
      generate(width=9, height=10,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 2, 2, 0,
                       0, 0, 0, 0, 0, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0]),
      generate(width=8, height=10,
               colors=[0, 0, 0, 0, 0, 0, 0, 0,
                       2, 2, 0, 0, 0, 2, 2, 0,
                       0, 2, 2, 0, 0, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 2, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 2, 2, 0, 0, 0, 0,
                       2, 0, 2, 2, 0, 0, 2, 2,
                       2, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=8, height=6,
               colors=[0, 0, 0, 0, 2, 2, 2, 0,
                       2, 2, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 0, 2, 2, 0,
                       0, 2, 0, 0, 0, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 2, 2, 0, 0, 0, 2]),
  ]
  return {"train": train, "test": test}
