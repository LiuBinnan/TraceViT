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


def generate(width=None, height=None, bgcolor=None, orders=None, pattern=None,
             num_shapes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the shapes.
    height: The height of the shapes.
    bgcolor: The background color.
    orders: The order of the shapes in the output.
    pattern: The pattern of the shapes.
    num_shapes: The number of key-and-hole bands.
  """

  if pattern is None:
    if width is None:
      width = common.randint(3, 5)
    if height is None:
      height = common.randint(2, 4)
    if num_shapes is None:
      num_shapes = common.randint(3, 5)
    if 2 * width + 4 > 30:
      raise ValueError("key-and-hole input is wider than 30 columns")
    if (height + 1) * num_shapes + 1 > 30:
      raise ValueError("key-and-hole input is taller than 30 rows")
    shapes = []
    attempts = 0
    while len(shapes) < num_shapes and attempts < 256:
      attempts += 1
      shape = []
      for r in range(height):
        for c in range(width):
          if common.randint(0, 1): shape.append((r, c))
      if not shape: continue  # Degenerate: common.connected([]) would crash.
      if not common.connected(shape) or shape in shapes: continue
      if len(set([r for r, _ in shape])) != height: continue
      shapes.append(shape)
    if len(shapes) < num_shapes:
      # Bound the rejection tail with distinct, connected, full-height shapes.
      fallback_shapes = [
          [(r, 0) for r in range(height)],
          [(r, width - 1) for r in range(height)],
          [(r, 0) for r in range(height)] + [(0, c) for c in range(1, width)],
          [(r, 0) for r in range(height)] +
          [(height - 1, c) for c in range(1, width)],
          [(r, 0) for r in range(height)] +
          [(0, c) for c in range(1, width)] +
          [(height - 1, c) for c in range(1, width)],
      ]
      for shape in fallback_shapes:
        if shape not in shapes:
          shapes.append(shape)
        if len(shapes) == num_shapes:
          break
    bgcolor = common.random_color()
    colors = common.random_colors(num_shapes, exclude=[bgcolor])
    pattern = []
    for i, shape in enumerate(shapes):
      for r in range(height):
        for c in range(width):
          pattern.append(0 if (r, c) not in shape else colors[i])
    orders = common.shuffle(list(range(num_shapes)))

  # The sheet (left) is a solid slab of bgcolor with a hole punched through it
  # in each band; the key (right) shows every shape in its own color.
  grid = common.grid(2 * width + 4, (height + 1) * len(orders) + 1)
  common.rect(grid, width + 2, (height + 1) * len(orders) + 1, 0, 0, bgcolor)
  for i, order in enumerate(orders):
    for r in range(height):
      for c in range(width):
        in_color = pattern[i * height * width + r * width + c]
        grid[i * (height + 1) + r + 1][width + 3 + c] = in_color
        out_color = pattern[order * height * width + r * width + c]
        if out_color:
          grid[i * (height + 1) + r + 1][c + 1] = 0
  output = [row[:width + 2] for row in grid]

  def hole(band):
    """Returns the outline of the hole punched into the sheet's band."""
    return [(r, c) for r in range(height) for c in range(width)
            if not grid[band * (height + 1) + r + 1][c + 1]]

  def key(band):
    """Returns the outline and the color of the key shape in the band."""
    cells = [(r, c) for r in range(height) for c in range(width)
             if grid[band * (height + 1) + r + 1][width + 3 + c]]
    r, c = cells[0]
    return cells, grid[band * (height + 1) + r + 1][width + 3 + c]

  def plug_hole(band):
    """Plugs the band's hole with the key shape that has the same outline."""
    if band >= len(orders): return
    cells = hole(band)
    for other in range(len(orders)):
      shape, color = key(other)
      if shape != cells: continue
      for r, c in cells:
        output[band * (height + 1) + r + 1][c + 1] = color

  plug_hole(0)
  plug_hole(1)
  plug_hole(2)
  plug_hole(3)
  for band in range(4, len(orders)):
    plug_hole(band)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, bgcolor=5, orders=[2, 1, 0],
               pattern=[3, 0, 0, 3, 3, 0, 0, 3, 3, 3, 3, 3,
                        2, 2, 2, 0, 2, 2, 0, 0, 2, 0, 0, 0,
                        0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]),
      generate(width=4, height=2, bgcolor=1, orders=[1, 2, 0],
               pattern=[0, 2, 2, 0, 0, 2, 2, 0,
                        0, 3, 3, 0, 3, 3, 3, 3,
                        6, 6, 6, 6, 0, 6, 6, 0]),
  ]
  test = [
      generate(width=3, height=3, bgcolor=8, orders=[2, 0, 1, 3],
               pattern=[2, 2, 2, 0, 0, 2, 0, 0, 2,
                        4, 0, 4, 4, 0, 4, 4, 4, 4,
                        3, 3, 3, 0, 3, 0, 3, 3, 3,
                        0, 7, 7, 7, 7, 7, 7, 7, 0]),
  ]
  return {"train": train, "test": test}
