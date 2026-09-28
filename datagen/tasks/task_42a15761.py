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


def generate(size=None, vals=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    vals: The values of the columns.
  """

  if size is None:
    size = common.randint(3, 7)
    in_order = {}
    for count in range(1, size + 1):
      idxs = common.sample(range(size), k=count)
      in_order[count] = [1 if i in idxs else 0 for i in range(size)]
    vals = []
    orders = common.shuffle(list(range(1, size + 1)))
    while orders == sorted(orders):
      orders = common.shuffle(orders)
    for order in orders:
      vals.extend(in_order[order])

  grid, output = common.grids(4 * size - 1, 2 * size + 1, 2)
  for i in range(size - 1):
    for r in range(2 * size + 1):
      output[r][4 * i + 3] = grid[r][4 * i + 3] = 0
  for i, val in enumerate(vals):
    grid[2 * (i % size) + 1][4 * (i // size) + 1] = 0 if val else 2
  columns_by_count = {}
  for i in range(size):
    column = vals[size * i:size * (i + 1)]
    columns_by_count[sum(column)] = column

  def place_count(count):
    if count > size:
      return
    for r, val in enumerate(columns_by_count[count]):
      output[2 * r + 1][4 * (count - 1) + 1] = 0 if val else 2

  place_count(1)
  place_count(2)
  place_count(3)
  place_count(4)
  place_count(5)
  for c in range(6, size + 1):
    place_count(c)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, vals=[0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0]),
      generate(size=3, vals=[1, 1, 0, 0, 0, 1, 1, 1, 1]),
      generate(size=4, vals=[0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1]),
  ]
  test = [
      generate(size=5,
               vals=[0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
