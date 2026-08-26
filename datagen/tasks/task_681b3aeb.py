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


def generate(rows=None, cols=None, idxs=None, colors=None, size=10, minisize=3,
             height=None, width=None, out_height=None, out_width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where halves should be placed
    cols: a list of horizontal coordinates where halves should be placed
    idxs: a list of indices into the colors pair
    colors: a pair of digits representing the colors of the halves
    size: the width and height of the input grid
    minisize: the width and height of the output grid
    height: the height of the input grid
    width: the width of the input grid
    out_height: the height of the output grid
    out_width: the width of the output grid
  """
  if rows is None:
    if out_height is None: out_height = minisize
    if out_width is None: out_width = out_height
    out_height = min(8, max(2, out_height))
    out_width = out_height
    if height is None: height = common.randint(3 * out_height, 30)
    if width is None: width = common.randint(3 * out_width, 30)
    height = min(30, max(height, 3 * out_height))
    width = min(30, max(width, 3 * out_width))
    while True:
      rows = [common.randint(0, height - out_height) for _ in range(2)]
      cols = [common.randint(0, width - out_width) for _ in range(2)]
      if (abs(rows[0] - rows[1]) >= out_height and
          abs(cols[0] - cols[1]) >= out_width): break
    while True:
      pixels = common.all_pixels(out_width, out_height)
      if out_height == 2:
        one = {(0, common.randint(0, 1)), (1, common.randint(0, 1))}
        if len(one) == 1: continue
        two = set(pixels) - one
      else:
        starts = common.sample(pixels, 2)
        one, two = {starts[0]}, {starts[1]}
        remaining = [pixel for pixel in pixels if pixel not in starts]
        while remaining:
          one_cands = [pixel for pixel in remaining
                       if any(abs(pixel[0] - r) + abs(pixel[1] - c) == 1
                              for r, c in one)]
          two_cands = [pixel for pixel in remaining
                       if any(abs(pixel[0] - r) + abs(pixel[1] - c) == 1
                              for r, c in two)]
          choices = []
          if one_cands: choices.append(0)
          if two_cands: choices.append(1)
          idx = common.choice(choices)
          pixel = common.choice(one_cands if idx == 0 else two_cands)
          if idx == 0:
            one.add(pixel)
          else:
            two.add(pixel)
          remaining.remove(pixel)
      idxs = []
      for r in range(out_height):
        for c in range(out_width):
          idxs.append(0 if (r, c) in one else 1)
      # Make sure the two halves are both self-connnected.
      one = [(i // out_width, i % out_width)
             for i, color in enumerate(idxs) if color == 0]
      two = [(i // out_width, i % out_width)
             for i, color in enumerate(idxs) if color == 1]
      if not common.diagonally_connected(one): continue
      if not common.diagonally_connected(two): continue
      one_rows, one_cols = [r for r, _ in one], [c for _, c in one]
      two_rows, two_cols = [r for r, _ in two], [c for _, c in two]
      if len(one) == ((max(one_rows) - min(one_rows) + 1) *
                      (max(one_cols) - min(one_cols) + 1)): continue
      if len(two) == ((max(two_rows) - min(two_rows) + 1) *
                      (max(two_cols) - min(two_cols) + 1)): continue
      # Make sure the solution can't be "split" evenly (causes ambiguity).
      unsplittable = False
      for r in range(out_height):
        if len(set([idxs[r * out_width + c] for c in range(out_width)])) > 1:
          unsplittable = True
      if not unsplittable: continue
      unsplittable = False
      for c in range(out_width):
        if len(set([idxs[r * out_width + c] for r in range(out_height)])) > 1:
          unsplittable = True
      if not unsplittable: continue
      break
    colors = common.random_colors(2)
  else:
    if out_height is None: out_height = minisize
    if out_width is None: out_width = minisize
    if height is None: height = size
    if width is None: width = size

  grid, output = common.grid(width, height), common.grid(out_width, out_height)
  for r in range(out_height):
    for c in range(out_width):
      idx = idxs[r * out_width + c]
      grid[rows[idx] + r][cols[idx] + c] = colors[idx]

  def reveal_color(idx):
    for r in range(out_height):
      for c in range(out_width):
        if idxs[r * out_width + c] == idx:
          output[r][c] = colors[idx]

  reveal_color(0)
  reveal_color(1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 7], cols=[1, 7], idxs=[0, 0, 1, 0, 1, 1, 0, 1, 1],
               colors=[3, 7]),
      generate(rows=[-1, 2], cols=[8, 3], idxs=[1, 1, 1, 0, 1, 1, 0, 0, 1],
               colors=[4, 6]),
      generate(rows=[3, 8], cols=[3, 1], idxs=[1, 1, 1, 1, 0, 1, 0, 0, 0],
               colors=[3, 1]),
  ]
  test = [
      generate(rows=[2, 6], cols=[2, 7], idxs=[1, 1, 0, 1, 0, 0, 1, 1, 1],
               colors=[2, 8]),
  ]
  return {"train": train, "test": test}
