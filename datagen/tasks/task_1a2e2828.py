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


def generate(width=None, height=None, values=None, thicks=None, cdirs=None,
             colors=None, num_h=None, num_v=None, max_thick=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if values is None:
    custom_layout = any(x is not None for x in (num_h, num_v, max_thick))
    if width is None:
      base = common.randint(5, 12)
      width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
    else:
      base = min(width, height)
    default_num_h, default_num_v = base // 4, base // 4
    if base > 8 and common.randint(0, 1): default_num_h += 1
    if base > 8 and common.randint(0, 1): default_num_v += 1
    if num_h is None and num_v is None:
      # Preserve the original seed-only behavior, which used num_v for both.
      num_h, num_v = default_num_v, default_num_v
    else:
      if num_h is None: num_h = default_num_h
      if num_v is None: num_v = default_num_v
    thick_limit = 3 if max_thick is None else max_thick
    if custom_layout:
      h_fit = max(1, (height - num_h - 1) // num_h)
      v_fit = max(1, (width - num_v - 1) // num_v)
    else:
      h_fit, v_fit = height - 2, width - 2
    while True:
      h_thicks = [common.randint(1, min(thick_limit, height - 2, h_fit))
                  for _ in range(num_h)]
      v_thicks = [common.randint(1, min(thick_limit, width - 2, v_fit))
                  for _ in range(num_v)]
      h_vals = [common.randint(1, height - thick - 1) for thick in h_thicks]
      v_vals = [common.randint(1, width - thick - 1) for thick in v_thicks]
      if common.overlaps_1d(h_vals, h_thicks, 1): continue
      if common.overlaps_1d(v_vals, v_thicks, 1): continue
      values, thicks, cdirs = [], [], []
      while h_thicks or v_thicks:
        if common.randint(0, 1):
          if not h_thicks: continue
          thicks, values = thicks + [h_thicks.pop()], values + [h_vals.pop()]
          cdirs.append(0)
        else:
          if not v_thicks: continue
          thicks, values = thicks + [v_thicks.pop()], values + [v_vals.pop()]
          cdirs.append(1)
      if cdirs[-1] != cdirs[-2]: break
    colors = common.random_colors(len(values))

  grid = common.grid(width, height)
  for value, thick, cdir, color in zip(values, thicks, cdirs, colors):
    if cdir:
      common.rect(grid, thick, height, 0, value, color)
    else:
      common.rect(grid, width, thick, value, 0, color)
  output = common.deepcopy(grid)

  def isolate_unbroken_bar():
    """Erases every bar that was overpainted at a crossing."""
    for row in range(height):
      for col in range(width):
        if output[row][col] != colors[-1]:
          output[row][col] = common.black()

  isolate_unbroken_bar()

  def reveal_bar_color():
    """Reduces the surviving bar to its one-cell color answer."""
    nonlocal output
    output = common.grid(1, 1, colors[-1])

  reveal_bar_color()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=11, values=[1, 4, 6, 8, 3],
               thicks=[1, 2, 2, 1, 2], cdirs=[0, 1, 0, 1, 0],
               colors=[2, 3, 4, 5, 1]),
      generate(width=11, height=9, values=[2, 3, 5, 8], thicks=[1, 2, 2, 1],
               cdirs=[0, 1, 0, 1], colors=[3, 4, 6, 8]),
      generate(width=11, height=11, values=[1, 1, 7, 6, 4],
               thicks=[3, 2, 2, 2, 1], cdirs=[0, 1, 1, 0, 1],
               colors=[1, 2, 8, 4, 6]),
      generate(width=3, height=3, values=[1, 1], thicks=[1, 1], cdirs=[1, 0],
               colors=[1, 3]),
      generate(width=12, height=8, values=[2, 1, 7, 5], thicks=[2, 2, 1, 1],
               cdirs=[0, 1, 1, 0], colors=[3, 2, 8, 6]),
  ]
  test = [
      generate(width=13, height=11, values=[2, 3, 6, 9], thicks=[2, 2, 1, 1],
               cdirs=[0, 1, 0, 1], colors=[1, 3, 6, 7]),
  ]
  return {"train": train, "test": test}
