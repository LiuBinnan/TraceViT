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

# The recolor rule's legal input colors: the eight non-fixed points of the
# colormap. Black (0) and orange (7) map to themselves and are left out of the
# sampled field, matching the original task's domain. Sampling WHICH and HOW
# MANY of these appear -- and scattering them per cell -- is the structural
# variation; the color map itself is the (untouchable) rule.
_POOL = (1, 2, 3, 4, 5, 6, 8, 9)

# The colormap's substitutions as disjoint (a, b) pairs (a <-> b). Revealing one
# pair at a time is the solving process and yields one step per substitution.
_GROUPS = ((3, 4), (8, 9), (2, 6), (1, 5))


def _reveal(output, source, colormap, group):
  """Returns a copy of `output` with every `source` cell whose color is in
  `group` recolored through `colormap`, leaving all other cells untouched.

  One such call is a single solving step: it applies one color substitution.
  """
  result = [row[:] for row in output]
  for r in range(len(source)):
    for c in range(len(source[r])):
      if source[r][c] in group:
        result[r][c] = colormap[source[r][c]]
  return result


def generate(colors=None, colormap=(0, 5, 6, 4, 3, 1, 2, 7, 9, 8),
             height=None, width=None, num_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: an explicit per-column color list reproducing the original column
      layout; when omitted the input is a per-cell random field over the rule's
      legal colors.
    colormap: the fixed substitution map (the rule); color c -> colormap[c].
    height: number of rows in the grids.
    width: number of columns in the grids.
    num_colors: how many distinct legal colors appear in the sampled field.
  """
  if colors is None:
    if height is None:
      height = common.randint(4, 30)
    if width is None:
      width = common.randint(4, 30)
    if num_colors is None:
      num_colors = common.randint(1, len(_POOL))
    num_colors = min(num_colors, len(_POOL))
    palette = common.sample(list(_POOL), num_colors)
    grid = [[common.choice(palette) for _ in range(width)]
            for _ in range(height)]
  else:
    if width is None:
      width = len(colors)
    if height is None:
      height = len(colors)
    grid = [[colors[c] for c in range(width)] for _ in range(height)]

  output = [row[:] for row in grid]
  output = _reveal(output, grid, colormap, _GROUPS[0])
  output = _reveal(output, grid, colormap, _GROUPS[1])
  output = _reveal(output, grid, colormap, _GROUPS[2])
  output = _reveal(output, grid, colormap, _GROUPS[3])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 1, 2]),
      generate(colors=[2, 3, 8]),
      generate(colors=[5, 8, 6]),
      generate(colors=[9, 4, 2]),
  ]
  test = [
      generate(colors=[8, 1, 3]),
  ]
  return {"train": train, "test": test}
