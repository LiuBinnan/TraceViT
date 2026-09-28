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


def generate(width=None, frames=None, offset=None, flip=None, colors=None,
             pattern=None, extra=None, height=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the pattern.
    frames: The number of frames to generate.
    offset: The offset of the pattern.
    flip: Whether to flip the pattern.
    colors: The colors to use for the pattern.
    pattern: The pattern to generate.
    extra: Whether to add an extra row (for an ambiguous case).
    height: The height of the boxes and grids.
  """

  if width is None:
    width = common.randint(4, 5)
    height = common.randint(12, 26) if height is None else height
    frames = common.randint(3, 5 if width == 4 else 4)
    offset = common.randint(1, (height - 5) // frames)
    flip = common.randint(0, 1)
    bgcolor = common.random_color()
    mgcolor = common.random_color(exclude=[bgcolor])
    fgcolor = common.random_color(exclude=[mgcolor])
    colors = [bgcolor, mgcolor, fgcolor]
    pattern = [1] * (width - 2)
    if width == 4:
      a = common.randint(0, 1)
      pattern.extend([a, a])
    if width == 5:
      a, b = common.randint(0, 1), common.randint(0, 1)
      pattern.extend([a, b, a])
  else:
    height = 16 if height is None else height

  # Input: `frames` side-by-side boxes; each box holds the same dot-pattern,
  # descended by `offset` rows relative to the previous one (an animation).
  grid = common.grid((width + 1) * frames + 1, height, colors[0])
  for f in range(frames):
    common.rect(grid, width, height - 2, 1, f * (width + 1) + 1, colors[1])
    for row in range(2):
      for col in range(width - 2):
        if not pattern[row * (width - 2) + col]: continue
        grid[2 + f * offset + row][f * (width + 1) + 2 + col] = colors[2]

  # Output: the NEXT frame of the animation. Solve it by continuing the descent
  # inside a single box, one frame per step, until the pattern lands one
  # `offset` past the last input frame (`frames * offset`, plus the `extra`
  # nudge used for the ambiguous case).
  extra = extra if extra else 0
  output = common.grid(width + 2, height, colors[0])

  def place_pattern(k):
    """Slides the descending pattern to its frame-`k` position in the box."""
    if k > frames: return
    common.rect(output, width, height - 2, 1, 1, colors[1])
    base = 2 + k * offset + (extra if k == frames else 0)
    for row in range(2):
      for col in range(width - 2):
        if not pattern[row * (width - 2) + col]: continue
        output[base + row][2 + col] = colors[2]

  place_pattern(0)
  place_pattern(1)
  place_pattern(2)
  place_pattern(3)
  place_pattern(4)
  for k in range(5, frames + 1):
    place_pattern(k)
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, frames=4, offset=1, flip=0, colors=[1, 2, 3],
               pattern=[1, 1, 0, 0]),
      generate(width=4, frames=3, offset=3, flip=0, colors=[8, 2, 8],
               pattern=[1, 1, 1, 1], extra=1),
      generate(width=5, frames=3, offset=3, flip=1, colors=[3, 1, 2],
               pattern=[1, 1, 1, 1, 0, 1]),
  ]
  test = [
      generate(width=5, frames=4, offset=2, flip=0, colors=[4, 3, 8],
               pattern=[1, 1, 1, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
