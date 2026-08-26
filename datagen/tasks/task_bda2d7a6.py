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


def generate(half=None, colors=None, hheight=None, hwidth=None, nrings=None,
             ncolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    half: half of the width or height of the (square) grid
    colors: a list of colors to choose from
    hheight: half of the grid height (overrides the square half for rows)
    hwidth: half of the grid width (overrides the square half for cols)
    nrings: number of concentric rings (equals min(hheight, hwidth))
    ncolors: number of distinct colors cycled across the rings
  """
  if colors is None:
    # Structural long-tail widening (rule-preserving). The concentric-ring
    # recolor is a MODULAR rotation of the color cycle; it stays faithful to the
    # object-based reference rule ONLY when nrings % ncolors is 0 or 1 (the
    # reference's inner==outer merge branch supplies the "+1" wrap), so we draw
    # (nrings, ncolors) strictly inside that safe set. The recolor_ring handlers
    # below are unrolled exactly MAX_RINGS (=10) times, so nrings -- which equals
    # min(hheight, hwidth) -- MUST stay <= MAX_RINGS.
    MAX_RINGS = 10
    if nrings is None:
      nrings = common.randint(2, MAX_RINGS)
    nrings = min(nrings, MAX_RINGS)  # guard: never exceed the handler count
    if ncolors is None:
      safe = [k for k in range(2, nrings + 1) if nrings % k in (0, 1)]
      ncolors = common.sample(safe, 1)[0]
    colors = common.sample(range(0, 10), ncolors)  # Includes black!
    half = nrings
    # The short side fixes the ring count; the long side grows independently so
    # the output dimensions and foreground density fan out across examples.
    long_half = common.randint(nrings, 14)
    if common.randint(0, 1):
      hheight = nrings
      hwidth = long_half
    else:
      hwidth = nrings
      hheight = long_half

  # Fallbacks preserve byte-for-byte square behavior when half is supplied.
  if hheight is None:
    hheight = half
  if hwidth is None:
    hwidth = half

  gh = 2 * hheight
  gw = 2 * hwidth
  grid, output = common.grids(gw, gh)
  for r in range(hheight):
    for c in range(hwidth):
      color_idx = min(r, c) % len(colors)
      grid[r][c] = colors[color_idx]
      grid[r][gw - 1 - c] = colors[color_idx]
      grid[gh - 1 - r][c] = colors[color_idx]
      grid[gh - 1 - r][gw - 1 - c] = colors[color_idx]

  def recolor_ring(ring_idx):
    if ring_idx >= min(hheight, hwidth):
      return
    color = colors[(ring_idx + len(colors) - 1) % len(colors)]
    for r in range(hheight):
      for c in range(hwidth):
        if min(r, c) != ring_idx:
          continue
        output[r][c] = color
        output[r][gw - 1 - c] = color
        output[gh - 1 - r][c] = color
        output[gh - 1 - r][gw - 1 - c] = color

  recolor_ring(0)
  recolor_ring(1)
  recolor_ring(2)
  recolor_ring(3)
  recolor_ring(4)
  recolor_ring(5)
  recolor_ring(6)
  recolor_ring(7)
  recolor_ring(8)
  recolor_ring(9)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(half=3, colors=[3, 2, 0]),
      generate(half=3, colors=[0, 7, 6]),
      generate(half=4, colors=[8, 0, 5]),
  ]
  test = [
      generate(half=3, colors=[9, 0, 1]),
      generate(half=4, colors=[3, 7, 6]),
  ]
  return {"train": train, "test": test}
