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


def generate(rows=None, cols=None, idxs=None, colors=None, midrows=None,
             midcols=None, size=11, minisize=3, height=None, width=None,
             out_height=None, out_width=None, markrow=None, markcol=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of colors for the pixels
    midrows: a list of vertical coordinates for the middle points
    midcols: a list of horizontal coordinates for the middle points
    size: the width and height of the input grid
    minisize: the width and height of the output grid
  """
  if rows is None:
    if out_height is None: out_height = common.randint(2, 4)
    if out_width is None: out_width = common.randint(2, 4)
    if markrow is None: markrow = min(1, out_height - 1)
    if markcol is None: markcol = min(1, out_width - 1)
    pixels = []
    for r in range(out_height):
      for c in range(out_width):
        if r == markrow and c == markcol: continue
        pixels.append((r, c))
    if num_colors is None:
      num_colors = common.randint(1, min(len(pixels), 8))
    num_colors = min(num_colors, len(pixels), 8)

    def component_count(assignments, target_idx):
      unseen = {pixel for pixel, idx in assignments.items() if idx == target_idx}
      count = 0
      while unseen:
        count += 1
        queue = [unseen.pop()]
        while queue:
          r, c = queue.pop()
          for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if (nr, nc) in unseen:
              unseen.remove((nr, nc))
              queue.append((nr, nc))
      return count

    for _ in range(100):
      trial_idxs = list(range(num_colors))
      while len(trial_idxs) < len(pixels):
        trial_idxs.append(common.randint(0, num_colors - 1))
      trial_idxs = common.shuffle(trial_idxs)
      assignments = dict(zip(pixels, trial_idxs))
      max_components = max(component_count(assignments, idx)
                           for idx in range(num_colors))
      if max_components < num_colors or (num_colors == 1 and max_components == 1):
        idxs = trial_idxs
        break
    else:
      assignments = {}
      seeds = common.shuffle(pixels)[:num_colors]
      for idx, pixel in enumerate(seeds):
        assignments[pixel] = idx
      remaining = [pixel for pixel in pixels if pixel not in assignments]
      while remaining:
        choices = []
        for pixel in remaining:
          r, c = pixel
          for neighbor in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if neighbor in assignments:
              choices.append((pixel, assignments[neighbor]))
        pixel, idx = common.choice(choices)
        assignments[pixel] = idx
        remaining.remove(pixel)
      idxs = [assignments[pixel] for pixel in pixels]
    pixels = common.shuffle(pixels)
    rows, cols = zip(*pixels)
    idxs = [assignments[pixel] for pixel in pixels]
    colors = common.random_colors(num_colors, exclude=[common.gray()])

    def placements(grid_height, grid_width, spacing):
      spots = []
      for top in range(grid_height - out_height + 1):
        for left in range(grid_width - out_width + 1):
          spots.append((top, left))
      spots = common.shuffle(spots)
      placed = []
      for top, left in spots:
        ok = True
        for old_top, old_left in placed:
          rows_clear = (top + out_height + spacing <= old_top or
                        old_top + out_height + spacing <= top)
          cols_clear = (left + out_width + spacing <= old_left or
                        old_left + out_width + spacing <= left)
          if not (rows_clear or cols_clear):
            ok = False
            break
        if not ok:
          continue
        placed.append((top, left))
        if len(placed) == num_colors:
          break
      return placed

    min_size = min(out_height, out_width) * 2
    fixed_height, fixed_width = height is not None, width is not None
    safe_spacing = max(out_height, out_width)
    for _ in range(100):
      trial_height = height if fixed_height else common.randint(min_size, 30)
      trial_width = width if fixed_width else common.randint(min_size, 30)
      placed = placements(trial_height, trial_width, safe_spacing)
      if len(placed) == num_colors:
        height, width = trial_height, trial_width
        break
    else:
      if not fixed_height: height = 30
      if not fixed_width: width = 30
      placed = placements(height, width, safe_spacing)
    midrows = [top + markrow for top, _ in placed]
    midcols = [left + markcol for _, left in placed]

  if out_height is None: out_height = minisize
  if out_width is None: out_width = minisize
  if markrow is None: markrow = 1
  if markcol is None: markcol = 1
  if height is None: height = size
  if width is None: width = size
  if num_colors is None: num_colors = len(colors)

  grid, output = common.grid(width, height), common.grid(out_width, out_height)
  for r, c, color in zip(midrows, midcols, colors):
    grid[r][c] = 0 if color == 0 else common.gray()
  output[markrow][markcol] = common.gray()
  def place_color(target_idx):
    for r, c, idx in zip(rows, cols, idxs):
      if idx != target_idx:
        continue
      grid[r + midrows[idx] - markrow][c + midcols[idx] - markcol] = colors[idx]
      output[r][c] = colors[idx]

  for target_idx in range(num_colors):
    place_color(target_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 0, 1, 2, 1, 3, 3, 2], colors=[6, 7, 0, 4],
               midrows=[2, 8, 8, 2], midcols=[7, 5, 1, 3]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 1, 2, 2, 3, 3, 3], colors=[6, 2, 7, 3],
               midrows=[3, 9, 3, 7], midcols=[2, 2, 5, 7]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 1, 1, 2, 3, 3, 2], colors=[0, 1, 2, 9],
               midrows=[1, 3, 4, 8], midcols=[9, 1, 5, 7]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 2, 1, 0, 1, 3, 3], colors=[4, 9, 8, 2],
               midrows=[4, 2, 7, 9], midcols=[1, 8, 6, 3]),
  ]
  return {"train": train, "test": test}
