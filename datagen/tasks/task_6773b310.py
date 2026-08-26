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


def generate(rows=None, cols=None, minirows=None, minicols=None, minisize=3,
             height=None, width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    minisize: the width and height of the mini grids
    height: number of mini-grid rows (output height); defaults to minisize
    width: number of mini-grid columns (output width); defaults to minisize
  """
  if height is None: height = minisize
  if width is None: width = minisize
  if rows is None:
    while True:
      rows, cols, minirows, minicols, some_two = [], [], [], [], False
      for r in range(height):
        for c in range(width):
          count = common.randint(1, 2)
          if count == 2: some_two = True
          pixels = common.sample(common.all_pixels(minisize, minisize), count)
          rows.extend([r] * count)
          cols.extend([c] * count)
          minirows.extend([p[0] for p in pixels])
          minicols.extend([p[1] for p in pixels])
      if some_two: break

  grid = [[common.cyan() if r % (minisize + 1) == minisize or
           c % (minisize + 1) == minisize else common.black()
           for c in range(width * (minisize + 1) - 1)]
          for r in range(height * (minisize + 1) - 1)]
  output = common.grid(width, height)
  m = {}
  for r, c, mr, mc in zip(rows, cols, minirows, minicols):
    grid[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = common.pink()
    m[(r, c)] = 1 if (r, c) not in m else m[(r, c)] + 1
  crowded = [(r, c) for (r, c), num_pixels in sorted(m.items()) if num_pixels >= 2]

  def filter_crowded():
    nonlocal output
    output = [list(row) for row in grid]
    for r, c, mr, mc in zip(rows, cols, minirows, minicols):
      if (r, c) in crowded:
        continue
      output[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = common.black()

  def make_output():
    nonlocal output
    output = common.grid(width, height)
    for r, c in crowded:
      output[r][c] = common.blue()

  filter_crowded()
  make_output()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 1, 2],
               minirows=[1, 2, 1, 1, 2, 0, 2, 0, 2, 0, 2, 1],
               minicols=[0, 2, 1, 2, 1, 1, 1, 2, 0, 2, 0, 1]),
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 2, 0, 1, 2, 2, 0, 0, 1, 2],
               minirows=[0, 1, 1, 0, 2, 1, 2, 1, 2, 2, 2],
               minicols=[0, 2, 2, 0, 2, 1, 0, 0, 1, 1, 2]),
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 1, 2, 0, 1, 2, 2],
               minirows=[2, 0, 2, 0, 1, 2, 1, 2, 1, 2, 0, 1],
               minicols=[1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 0, 2]),
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 2],
               minirows=[1, 2, 0, 1, 1, 0, 1, 2, 1, 2, 1],
               minicols=[2, 1, 2, 0, 0, 1, 2, 1, 2, 1, 0]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 2, 2, 0, 1, 1, 2, 2, 0, 0, 1, 2],
               minirows=[1, 1, 0, 0, 1, 1, 2, 0, 2, 0, 1, 2, 1],
               minicols=[1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 0, 1, 1]),
  ]
  return {"train": train, "test": test}
