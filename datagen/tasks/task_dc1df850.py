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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             max_shape=None, density=None, red_count=None, background=None,
             num_colors=None):
  """Returns input and output grids according to the given parameters.

  The scene is a field of colored pixels on a non-blue/non-red background.
  Red pixels "glow": their background neighbours turn blue while the red cell
  and any existing non-background pixels are copied through unchanged.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    max_shape: legacy parameter, ignored by the widened random sampler.
    density: number of occupied cells. ``None`` randomizes sparse foreground
      outside the red glow footprints.
    red_count: number of red cells, capped at four separated glow centers.
    background: background color; random samples exclude blue and red.
    num_colors: number of legal non-red foreground colors to sample.
  """
  coords_given = (isinstance(rows, (list, tuple)) and
                  isinstance(cols, (list, tuple)) and
                  isinstance(colors, (list, tuple)))
  if not coords_given:
    if width is None:
      width = common.randint(4, 30)
    if height is None:
      height = common.randint(4, 30)
    if background is None:
      background = common.choice([0, 3, 4, 5, 6, 7, 8, 9])

    if red_count is None:
      red_count = common.randint(1, 4)
    red_count = min(max(1, red_count), min(4, width * height))
    legal_colors = [color for color in [0, 3, 4, 5, 6, 7, 8, 9]
                    if color != background]
    if num_colors is None:
      num_colors = common.randint(1, len(legal_colors))
    num_colors = min(max(1, num_colors), len(legal_colors))
    palette = common.sample(legal_colors, num_colors)

    glow_offsets = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1]]
    def glow_cells(pixel):
      r, c = pixel
      cells = []
      for dr, dc in glow_offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
          cells.append((nr, nc))
      return set(cells)

    def choose_reds(candidates, chosen, reserved):
      if len(chosen) == red_count:
        return chosen
      if len(candidates) < red_count - len(chosen):
        return None
      for idx, pixel in enumerate(candidates):
        footprint = glow_cells(pixel)
        if reserved.isdisjoint(footprint):
          result = choose_reds(candidates[idx + 1:], chosen + [pixel],
                               reserved | footprint)
          if result is not None:
            return result
      return None

    candidates = common.shuffle(common.all_pixels(width, height))
    red_pixels = choose_reds(candidates, [], set())
    while red_pixels is None and red_count > 1:
      red_count -= 1
      red_pixels = choose_reds(candidates, [], set())
    red_pixels = set(red_pixels)
    reserved = set()
    for pixel in red_pixels:
      reserved |= glow_cells(pixel)

    noise_slots = [pixel for pixel in common.all_pixels(width, height)
                   if pixel not in reserved]
    max_noise = min(len(noise_slots), max(1, min(12, (width * height) // 20)))
    noise_count = common.randint(0, max_noise) if density is None else density - red_count
    noise_count = min(max(0, noise_count), max_noise)
    noise_pixels = common.sample(noise_slots, noise_count)
    pixels = common.shuffle(list(red_pixels) + noise_pixels)
    rows, cols, colors = [], [], []
    for r, c in pixels:
      rows.append(r)
      cols.append(c)
      if (r, c) in red_pixels:
        colors.append(common.red())
      else:
        colors.append(common.choice(palette))
  elif background is None:
    background = 0

  grid = common.grid(width, height, background)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  output = common.deepcopy(grid)

  reds = [(r, c) for r, c, color in zip(rows, cols, colors)
          if color == common.red()]
  def glow_red(idx):
    if idx >= len(reds):
      return
    r, c = reds[idx]
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        if common.get_pixel(output, r + dr, c + dc) == background:
          common.draw(output, r + dr, c + dc, common.blue())
    output[r][c] = common.red()

  glow_red(0)
  glow_red(1)
  glow_red(2)
  glow_red(3)
  glow_red(4)
  glow_red(5)
  glow_red(6)
  glow_red(7)
  glow_red(8)
  glow_red(9)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=5, rows=[0, 1, 3], cols=[0, 3, 1],
               colors=[2, 2, 6]),
      generate(width=8, height=8, rows=[0, 2, 4, 6], cols=[7, 3, 6, 2],
               colors=[2, 3, 8, 2]),
      generate(width=5, height=4, rows=[1], cols=[1], colors=[2]),
  ]
  test = [
      generate(width=10, height=10, rows=[0, 1, 3, 5, 7, 9],
               cols=[8, 2, 7, 1, 5, 9], colors=[7, 2, 2, 7, 2, 5]),
  ]
  return {"train": train, "test": test}
