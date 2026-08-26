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


def generate(width=None, idxs=None, height=3, colors=(1, 7, 8),
             num_colors=None, density=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    idxs: the indices of the colors to use
    height: the height of the grid
    colors: the integers used for the colors
    num_colors: how many distinct non-orange colors fill the non-orange cells
    density: fraction of cells that are orange (the color the rule rewrites)
  """
  if idxs is None:
    if width is None:
      width = common.randint(4, 30)
    cells = width * height
    # Fillers for the non-orange cells: any legal color except orange (7, the
    # color the rule rewrites) and gray (5, its result) -- keeps the 7->5 map
    # unambiguous and honors the foreground_freeze override. How many appear
    # varies, mirroring re_arc's numc band.
    palette = [common.black(), common.blue(), common.red(), common.green(),
               common.yellow(), common.pink(), common.cyan(), common.maroon()]
    if num_colors is None:
      num_colors = common.randint(1, len(palette))
    others = common.sample(palette, num_colors)
    colors = [common.orange()] + others
    # Orange cells (rewritten to gray) drive the foreground density; re_arc
    # bands this 0..cells//2.
    if density is None:
      num_orange = common.randint(0, cells // 2)
    else:
      num_orange = max(0, min(cells, int(round(density * cells))))
    orange_cells = set(common.sample(list(range(cells)), num_orange))
    idxs = [0 if p in orange_cells else common.randint(1, num_colors)
            for p in range(cells)]

  grid, output = [], []
  for r in range(height):
    row = [colors[idx] for idx in idxs[r * width : (r + 1) * width]]
    grid.append(row[:])
    new_row = []
    for color in row:
      new_row.append(color if color != common.orange() else common.gray())
    output.append(new_row)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, idxs=[0, 2, 2, 1, 1, 2,
                              0, 0, 1, 1, 0, 2,
                              1, 0, 0, 1, 1, 2]),
      generate(width=4, idxs=[1, 1, 1, 0,
                              0, 2, 0, 1,
                              1, 0, 0, 1]),
      generate(width=5, idxs=[0, 2, 0, 1, 0,
                              1, 2, 2, 0, 0,
                              1, 0, 2, 2, 1]),
  ]
  test = [
      generate(width=5, idxs=[0, 1, 1, 0, 1,
                              2, 0, 1, 1, 1,
                              2, 1, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
