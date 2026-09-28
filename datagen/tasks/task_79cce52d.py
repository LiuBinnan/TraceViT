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


def generate(hoff=None, voff=None, colors=None, msize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    hoff: The horizontal offset.
    voff: The vertical offset.
    colors: A list of colors to use.
    msize: The height and width of the mosaic.
  """

  if colors is None:
    if msize is None:
      msize = common.randint(5, 8)
    voff = common.randint(0, msize - 1)
    hoff = common.randint(0, msize - 1)
    colors = [0] * (msize * msize)
    while True:
      length = common.randint(2, min(5, msize - 1))
      off = common.randint(0, msize - length)
      pos = common.randint(0, msize - 1)
      cdir = common.randint(0, 1)
      color = common.choice([1, 3, 4, 5, 8, 9])
      for i in range(off, off + length):
        if cdir: colors[pos * msize + i] = color
        else: colors[i * msize + pos] = color
      if 0 in colors: continue
      if len(set(colors)) != 6: continue
      counts = [colors.count(c) for c in set(colors)]
      if min(counts) < 4: continue
      break
    colors = "".join(str(c) for c in colors)
  elif msize is None:
    msize = 6

  grid = common.grid(msize + 1, msize + 1, 6)
  grid[0][0] = 7
  grid[0][hoff + 1] = grid[voff + 1][0] = 2

  output = common.grid(msize, msize)
  for i, color in enumerate(colors):
    row, col = i // msize, i % msize
    grid[1 + row][1 + col] = int(color)
    output[row][col] = int(color)

  for _ in range(voff):
    output = output[-1:] + output[:-1]
  for _ in range(hoff):
    output = [row[-1:] + row[:-1] for row in output]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(hoff=0, voff=0, colors="888444988844933354939355999355111115"),
      generate(hoff=2, voff=2, colors="559988555981844981844991883331833311"),
      generate(hoff=3, voff=1, colors="355555335999334949114449114849118888"),
  ]
  test = [
      generate(hoff=1, voff=5, colors="553399555398133398114488114448114448"),
  ]
  return {"train": train, "test": test}
