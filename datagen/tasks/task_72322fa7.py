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
             idxs=None, megarows=None, megacols=None, megaidxs=None,
             megashows=None, sprite_types=None, count=None,
             shape_count=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    idxs: a list of indices into the array of sprite types
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where sprites should be placed
    megaidxs: a list of indices into the array of sprite types
    megashows: a list of values in the set {0, 1, 2} to indicate what to show
  """
  if (width is None or height is None or rows is None or cols is None or
      colors is None or idxs is None or megarows is None or megacols is None or
      megaidxs is None or megashows is None):
    while True:
      if width is None: width = common.randint(10, 30)
      if height is None: height = common.randint(10, 30)
      # First, choose the sprite types
      max_slots = max(1, ((height + 1) // 4) * ((width + 1) // 4))
      if sprite_types is None:
        sprite_types = common.randint(1, 4)
      sprite_types = max(1, min(sprite_types, 4, max_slots))
      color_list = common.shuffle(range(1, 10))
      rows, cols, colors, idxs = [], [], [], []
      sprite_shapes = [
          [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
          [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
          [(1, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1)],
          [(0, 0), (1, 0), (1, 1), (1, 2)],
          [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
          [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
          [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)],
          [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
          [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
          [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
           (2, 0), (2, 2)],
          [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
           (2, 0), (2, 1), (2, 2)],
      ]
      if shape_count is None:
        shape_count = common.randint(4, len(sprite_shapes))
      shape_count = max(1, min(shape_count, len(sprite_shapes)))
      for idx in range(sprite_types):
        color0, color1 = color_list[2 * idx], color_list[2 * idx + 1]
        sprite_shape = sprite_shapes[common.randint(0, shape_count - 1)]
        for row, col in sprite_shape:
          rows.append(row)
          cols.append(col)
          colors.append(color1 if row == 1 and col == 1 else color0)
          idxs.append(idx)
      # Second, choose some non-overlapping locations.
      megarows, megacols, megaidxs, megashows = [], [], [], []
      sprite_cells = [idxs.count(idx) for idx in range(sprite_types)]
      avg_cells = max(1, sum(sprite_cells) // len(sprite_cells))
      if count is None:
        max_count = min(48, max_slots,
                        max(sprite_types + 1, (height * width) //
                            (avg_cells * 2)))
        min_count = sprite_types + 1 if max_count > sprite_types else sprite_types
        count = common.randint(min_count, max_count)
      count = max(sprite_types, min(count, max_slots, 48))
      slots = [(idx, 0) for idx in range(sprite_types)]
      extra_slots = []
      for _ in range(count - sprite_types):
        extra_slots.append((common.randint(0, sprite_types - 1),
                            common.randint(1, 2)))
      slots.extend(common.shuffle(extra_slots))

      def can_place(row, col, idx):
        for old_row, old_col, old_idx in zip(megarows, megacols, megaidxs):
          spacing = 5 if old_idx == idx else 4
          if old_row + spacing <= row: continue
          if row + spacing <= old_row: continue
          if old_col + spacing <= col: continue
          if col + spacing <= old_col: continue
          return False
        return True

      for idx, show in slots:
        cands = []
        for row in range(height - 2):
          for col in range(width - 2):
            if can_place(row, col, idx):
              cands.append((row, col))
        if not cands:
          continue
        row, col = cands[common.randint(0, len(cands) - 1)]
        megarows.append(row)
        megacols.append(col)
        megaidxs.append(idx)
        megashows.append(show)
      if megarows: break

  grid, output = common.grids(width, height)
  for mr, mc, mi, ms in zip(megarows, megacols, megaidxs, megashows):
    for row, col, color, idx in zip(rows, cols, colors, idxs):
      if idx != mi: continue
      grid[mr + row][mc + col] = color
      if ms == 0: continue
      if ms == 1 and row == 1 and col == 1: continue
      if ms == 2 and (row != 1 or col != 1): continue
      grid[mr + row][mc + col] = common.black()

  def reveal_sprite(sprite_idx):
    if sprite_idx >= len(megarows):
      return
    mr, mc, mi = megarows[sprite_idx], megacols[sprite_idx], megaidxs[sprite_idx]
    for row, col, color, idx in zip(rows, cols, colors, idxs):
      if idx == mi:
        output[mr + row][mc + col] = color

  reveal_sprite(0)
  reveal_sprite(1)
  reveal_sprite(2)
  reveal_sprite(3)
  reveal_sprite(4)
  reveal_sprite(5)
  reveal_sprite(6)
  reveal_sprite(7)
  reveal_sprite(8)
  reveal_sprite(9)
  reveal_sprite(10)
  reveal_sprite(11)
  reveal_sprite(12)
  reveal_sprite(13)
  reveal_sprite(14)
  reveal_sprite(15)
  reveal_sprite(16)
  reveal_sprite(17)
  reveal_sprite(18)
  reveal_sprite(19)
  reveal_sprite(20)
  reveal_sprite(21)
  reveal_sprite(22)
  reveal_sprite(23)
  reveal_sprite(24)
  reveal_sprite(25)
  reveal_sprite(26)
  reveal_sprite(27)
  reveal_sprite(28)
  reveal_sprite(29)
  reveal_sprite(30)
  reveal_sprite(31)
  reveal_sprite(32)
  reveal_sprite(33)
  reveal_sprite(34)
  reveal_sprite(35)
  reveal_sprite(36)
  reveal_sprite(37)
  reveal_sprite(38)
  reveal_sprite(39)
  reveal_sprite(40)
  reveal_sprite(41)
  reveal_sprite(42)
  reveal_sprite(43)
  reveal_sprite(44)
  reveal_sprite(45)
  reveal_sprite(46)
  reveal_sprite(47)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=13, rows=[0, 0, 1, 2, 2, 0, 1, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 1, 0, 1, 2, 1],
               colors=[1, 1, 3, 1, 1, 8, 8, 6, 8, 8],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[0, 3, 4, 9, 9, 9], megacols=[12, 5, 18, 1, 8, 15],
               megaidxs=[0, 1, 1, 0, 1, 1], megashows=[1, 0, 1, 0, 1, 2]),
      generate(width=12, height=13, rows=[1, 1, 1], cols=[0, 1, 2],
               colors=[4, 8, 4], idxs=[0, 0, 0], megarows=[2, 3, 8, 9],
               megacols=[1, 9, 0, 6], megaidxs=[0, 0, 0, 0],
               megashows=[0, 1, 2, 1]),
      generate(width=19, height=14, rows=[1, 1, 1, 0, 1, 2],
               cols=[0, 1, 2, 1, 1, 1],
               colors=[8, 2, 8, 1, 3, 1],
               idxs=[0, 0, 0, 1, 1, 1],
               megarows=[0, 2, 4, 10, 11], megacols=[15, 8, 2, 4, 11],
               megaidxs=[0, 0, 1, 0, 1], megashows=[0, 2, 0, 1, 1]),
  ]
  test = [
      generate(width=19, height=19, rows=[1, 1, 1, 0, 1, 2, 0, 1, 1, 1, 2],
               cols=[0, 1, 2, 1, 1, 1, 1, 0, 1, 2, 1],
               colors=[3, 7, 3, 1, 8, 1, 2, 2, 4, 2, 2],
               idxs=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2],
               megarows=[0, 1, 2, 5, 7, 9, 9, 14, 15, 15],
               megacols=[12, 7, 2, 5, 15, 0, 8, 10, 4, 16],
               megaidxs=[0, 1, 2, 0, 2, 1, 0, 2, 2, 1],
               megashows=[0, 1, 1, 2, 0, 1, 1, 2, 1, 0]),
  ]
  return {"train": train, "test": test}
