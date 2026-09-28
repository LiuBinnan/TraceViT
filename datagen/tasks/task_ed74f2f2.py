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


def generate(color=None, shape=None, psize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    color: A color to use.
    shape: A shape to use.
    psize: The height and width of the shape.
  """

  if color is None:
    if psize is None:
      psize = common.randint(3, 6)
    color = common.randint(1, 3)
    tries = common.randint(1, 2 * psize)
    pixels = None
    for _ in range(50):
      rows, cols = common.conway_sprite(psize, psize, tries)
      candidate = sorted(list(zip(rows, cols)))
      if common.diagonally_connected(candidate):
        pixels = candidate
        break
    if pixels is None:
      # The shared rejection sampler becomes vanishingly unlikely to finish on
      # larger panels. Fall back to bounded removals from a full, valid sprite.
      pixels = [(r, c) for r in range(psize) for c in range(psize)]
      for _ in range(tries):
        for pixel in common.sample(pixels, len(pixels)):
          candidate = [p for p in pixels if p != pixel]
          if len({r for r, _ in candidate}) != psize: continue
          if len({c for _, c in candidate}) != psize: continue
          if not common.diagonally_connected(candidate): continue
          pixels = candidate
          break
        else:
          break
    shape = []
    for r in range(psize):
      for c in range(psize):
        shape.append(1 if (r, c) in pixels else 0)
  elif psize is None:
    psize = 3

  # Input: a gray shape on the right, and a gray "key" beside the bar whose
  # marker layout names the color the shape should become. Build it first.
  grid, output = (common.grid(6 + psize, max(5, psize + 2)),
                  common.grid(psize, psize))
  grid[1][2] = grid[2][2] = grid[3][2] = 5
  if color == 1: grid[1][1] = grid[1][3] = 5
  if color == 2: grid[1][1] = grid[3][3] = 5
  if color == 3: grid[3][1] = grid[1][3] = 5
  for i, hue in enumerate(shape):
    grid[1 + i // psize][5 + i % psize] = 5 * hue

  # Stage 1: lift the gray shape out onto the answer canvas.
  def extract_shape():
    for i, hue in enumerate(shape):
      output[i // psize][i % psize] = common.gray() * hue

  # Stage 2: repaint it with the color named by the key.
  def recolor_shape():
    for i, hue in enumerate(shape):
      output[i // psize][i % psize] = color * hue

  extract_shape()
  recolor_shape()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(color=1, shape=[1, 0, 1, 1, 1, 1, 1, 1, 0]),
      generate(color=3, shape=[1, 0, 1, 1, 0, 1, 1, 1, 0]),
      generate(color=1, shape=[1, 0, 1, 0, 1, 1, 1, 0, 1]),
      generate(color=2, shape=[1, 1, 0, 0, 1, 1, 0, 1, 0]),
      generate(color=2, shape=[1, 1, 1, 1, 0, 1, 1, 0, 1]),
      generate(color=2, shape=[1, 0, 0, 0, 1, 1, 1, 0, 0]),
  ]
  test = [
      generate(color=3, shape=[1, 1, 0, 1, 1, 1, 1, 0, 1]),
  ]
  return {"train": train, "test": test}
