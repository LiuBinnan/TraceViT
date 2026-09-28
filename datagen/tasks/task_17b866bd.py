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
    colors: The colors of the pixels.
  """

  if width is None or height is None or colors is None:
    if width is None:
      width = common.randint(2, 5)
    if height is None:
      height = common.randint(2, 4)
    if colors is None:
      while True:
        colors = common.choices([0, 1, 4, 8], k=width * height)
        if len(set(colors)) >= 3: break

  grid = common.grid(width * 5 + 1, height * 5 + 1)
  def put_grid(coords, color):
    for coord in coords:
      r, c = coord
      grid[r][c] = color
  for i, color in enumerate(colors):
    row, col = i // width, i % width
    grid[row * 5][col * 5] = color
  for i in range(height):
    for j in range(width):
      put_grid([(i * 5 + 1, j * 5 + 1),
                (i * 5 + 1, j * 5 + 4),
                (i * 5 + 4, j * 5 + 1),
                (i * 5 + 4, j * 5 + 4)], common.cyan())
      for k in range(4):
        put_grid([(i * 5, j * 5 + 1 + k),
                  (i * 5 + 1 + k, j * 5),
                  (i * 5 + 5, j * 5 + 1 + k),
                  (i * 5 + 1 + k, j * 5 + 5)], common.cyan())
  output = common.grid(width * 5 + 1, height * 5 + 1)

  def draw_lattice():
    for i in range(height):
      for j in range(width):
        for r, c in [(i * 5 + 1, j * 5 + 1),
                     (i * 5 + 1, j * 5 + 4),
                     (i * 5 + 4, j * 5 + 1),
                     (i * 5 + 4, j * 5 + 4)]:
          output[r][c] = common.cyan()
        for k in range(4):
          for r, c in [(i * 5, j * 5 + 1 + k),
                       (i * 5 + 1 + k, j * 5),
                       (i * 5 + 5, j * 5 + 1 + k),
                       (i * 5 + 1 + k, j * 5 + 5)]:
            output[r][c] = common.cyan()

  def expand_marker_row(row):
    if row >= height: return
    for col in range(width):
      color = colors[row * width + col]
      for r in range(4):
        for c in range(4):
          if r in [0, 3] and c in [0, 3]: continue
          output[5 * row + 1 + r][5 * col + 1 + c] = color

  draw_lattice()
  expand_marker_row(0)
  expand_marker_row(1)
  expand_marker_row(2)
  expand_marker_row(3)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, colors=[0, 0, 0, 0, 0, 0, 8, 0, 4, 0, 0, 0]),
      generate(width=3, height=3, colors=[7, 0, 0, 0, 0, 1, 0, 4, 0]),
  ]
  test = [
      generate(width=3, height=4, colors=[8, 8, 8, 8, 1, 8, 8, 8, 8, 0, 0, 0]),
      generate(width=3, height=3, colors=[1, 1, 1, 1, 0, 4, 4, 4, 4]),
  ]
  return {"train": train, "test": test}
