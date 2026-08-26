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


def generate(width=None, height=3, num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    num_colors: the number of distractor colors to scatter
    density: the number of distractor cells to scatter
  """
  randomized = width is None
  if width is None:
    width = common.randint(5, 25)
  if num_colors is None:
    num_colors = common.randint(1, 7) if randomized else 0
  num_colors = max(0, min(num_colors, 7))

  grid, output = common.grids(width, height)
  mode = -1
  lower_fills, upper_fills = [], []
  background_cells = []
  for c in range(width):
    r = c % (2 * height - 2)
    r = r if r < height else 2 * height - r - 2
    output[r][c] = grid[r][c] = common.red()
    for rr in range(height):
      if rr != r:
        background_cells.append((rr, c))
    mode = mode if r not in [0, height - 1] else (mode + 1) % 6
    if mode in [0, 5]:
      lower_fills.append((c, r + 1, height))
    if mode in [2, 3]:
      upper_fills.append((c, 0, r))

  if density is None:
    density = common.randint(0, len(background_cells)) if randomized else 0
  density = max(0, min(density, len(background_cells)))
  noise_colors = common.random_colors(
      num_colors, exclude=[common.red(), common.yellow()])

  def scatter_noise():
    if not noise_colors or density == 0:
      return
    for idx, (r, c) in enumerate(common.sample(background_cells, density)):
      color = noise_colors[idx] if idx < num_colors else common.choice(noise_colors)
      output[r][c] = grid[r][c] = color

  scatter_noise()

  def fill_lower():
    for c, start, end in lower_fills:
      for i in range(start, end):
        output[i][c] = common.yellow()

  def fill_upper():
    for c, start, end in upper_fills:
      for i in range(start, end):
        output[i][c] = common.yellow()

  fill_lower()
  fill_upper()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10),
      generate(width=15),
      generate(width=18),
  ]
  test = [
      generate(width=25),
  ]
  return {"train": train, "test": test}
