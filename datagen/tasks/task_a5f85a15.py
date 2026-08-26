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


def generate(size=None, height=None, width=None, diags=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: square fallback (keeps validate() byte-identical)
    height: number of rows (independent of width)
    width: number of columns (independent of height)
    diags: a list of diagonals where we use the color
    color: a digit representing a color to be used
  """
  if size is None:
    if height is None: height = common.randint(3, 30)
    if width is None: width = common.randint(3, 30)
    num_diags = common.randint(1, min(5, max(height, width) // 3))  # cap to the 5 recolor_diag handlers
    top_diags = list(range(0, -width + 1, -2))  # Odd tops are ambiguous.
    bottom_diags = list(range(1, height - 1))
    diags = common.sample(top_diags + bottom_diags, num_diags)
    color = common.random_color(exclude=[common.yellow()])
  else:
    height = width = size

  grid = common.grid(width, height)   # common.grid(width, height): 1st arg=cols, 2nd=rows
  for r in range(height):
    for c in range(width):
      grid[r][c] = color if r - c in diags else common.black()
  output = [row[:] for row in grid]

  def recolor_diag(diag_idx):
    if diag_idx >= len(diags):
      return
    diag = diags[diag_idx]
    for r in range(height):
      for c in range(width):
        if r - c == diag:
          output[r][c] = common.yellow() if c % 2 else color

  recolor_diag(0)
  recolor_diag(1)
  recolor_diag(2)
  recolor_diag(3)
  recolor_diag(4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, diags=[0], color=2),
      generate(size=8, diags=[-2, 4], color=9),
      generate(size=6, diags=[-2, 3], color=3),
  ]
  test = [
      generate(size=12, diags=[-4, 1, 8], color=6),
  ]
  return {"train": train, "test": test}
