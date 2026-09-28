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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    pixels = common.diagonally_connected_sprite()
    colors = []
    for r in range(3):
      for c in range(3):
        colors.append(5 if (r, c) in pixels else 0)

  grid = common.grid(3, 3)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = color

  output = common.grid(15, 15)

  def draw(brow, bcol):
    for i, color in enumerate(colors):
      output[brow + i // 3][bcol + i % 3] = color

  def magnify_center():
    """Blows the input up 3x into the middle 9x9 (each cell a solid block)."""
    for i, color in enumerate(colors):
      for r in range(3):
        for c in range(3):
          output[3 + 3 * (i // 3) + r][3 + 3 * (i % 3) + c] = color

  def project_top():
    """Stamps the sprite above every lit cell on the input's top edge."""
    for i, color in enumerate(colors):
      if color and i // 3 == 0: draw(0, 3 + 3 * (i % 3))

  def project_bottom():
    """Stamps the sprite below every lit cell on the input's bottom edge."""
    for i, color in enumerate(colors):
      if color and i // 3 == 2: draw(12, 3 + 3 * (i % 3))

  def project_left():
    """Stamps the sprite left of every lit cell on the input's left edge."""
    for i, color in enumerate(colors):
      if color and i % 3 == 0: draw(3 + 3 * (i // 3), 0)

  def project_right():
    """Stamps the sprite right of every lit cell on the input's right edge."""
    for i, color in enumerate(colors):
      if color and i % 3 == 2: draw(3 + 3 * (i // 3), 12)

  magnify_center()
  project_top()
  project_bottom()
  project_left()
  project_right()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 5, 0, 5, 5, 0, 0, 0, 5]),
      generate(colors=[0, 5, 0, 5, 5, 5, 0, 5, 0]),
      generate(colors=[5, 0, 0, 0, 5, 0, 0, 0, 5]),
  ]
  test = [
      generate(colors=[0, 5, 0, 0, 5, 0, 5, 0, 5]),
  ]
  return {"train": train, "test": test}
