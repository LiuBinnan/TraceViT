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


_TRANSFORMS = (
    lambda r, c: (r, c),
    lambda r, c: (r, -c),
    lambda r, c: (-r, c),
    lambda r, c: (-r, -c),
    lambda r, c: (c, r),
    lambda r, c: (c, -r),
    lambda r, c: (-c, r),
    lambda r, c: (-c, -r),
)


def _with_neighbors(cells, width, height):
  """Returns cells plus their 8-neighborhood, clipped to the grid."""
  blocked = set()
  for row, col in cells:
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        r, c = row + dr, col + dc
        if 0 <= r < height and 0 <= c < width:
          blocked.add((r, c))
  return blocked


def _rotated_cell(row, col, wide, tall, rot):
  if rot == 1: return wide - col - 1, row
  if rot == 2: return col, tall - row - 1
  if rot == 3: return tall - row - 1, col
  if rot == 4: return col, row
  return row, col


def _normalize_colored(cells):
  min_row = min(row for _, row, _ in cells)
  min_col = min(col for _, _, col in cells)
  return tuple(sorted((color, row - min_row, col - min_col)
                      for color, row, col in cells))


def _transform_points(points, transform_idx):
  transform = _TRANSFORMS[transform_idx]
  transformed = [transform(row, col) for row, col in points]
  min_row = min(row for row, _ in transformed)
  min_col = min(col for _, col in transformed)
  return [(row - min_row, col - min_col) for row, col in transformed]


def _transform_colored(marker_items, transform_idx):
  transform = _TRANSFORMS[transform_idx]
  transformed = [(color,) + transform(row, col)
                 for color, row, col in marker_items]
  return _normalize_colored(transformed)


def _marker_signatures(marker_items):
  signatures = set()
  for transform_idx in range(len(_TRANSFORMS)):
    signatures.add(_transform_colored(marker_items, transform_idx))
  return signatures


def _source_views(pixels, marker_items):
  views = []
  for transform_idx in range(len(_TRANSFORMS)):
    transform = _TRANSFORMS[transform_idx]
    raw_markers = [(color,) + transform(row, col)
                   for color, row, col in marker_items]
    marker_row = min(row for _, row, _ in raw_markers)
    marker_col = min(col for _, _, col in raw_markers)
    signature = tuple(sorted((color, row - marker_row, col - marker_col)
                             for color, row, col in raw_markers))
    raw_points = [transform(row, col) for row, col in pixels]
    full_points = tuple((row - marker_row, col - marker_col)
                        for row, col in raw_points)
    views.append((signature, full_points))
  return views


def _has_extra_marker_occurrence(marker_cells, source_views,
                                 intended_markers, width, height):
  for source_idx, views in enumerate(source_views):
    for signature, full_points in views:
      max_row = max(row for _, row, _ in signature)
      max_col = max(col for _, _, col in signature)
      for brow in range(height - max_row):
        for bcol in range(width - max_col):
          occurrence = frozenset((color, brow + row, bcol + col)
                                 for color, row, col in signature)
          if occurrence.issubset(marker_cells):
            full_cells = frozenset((brow + row, bcol + col)
                                   for row, col in full_points
                                   if 0 <= brow + row < height and
                                   0 <= bcol + col < width)
            if (source_idx, occurrence, full_cells) not in intended_markers:
              return True
  return False


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             colors=None, brows=None, bcols=None, rotates=None,
             num_sprites=None, num_clones=None, sprite_size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates where the sprites should be placed
    bcols: a list of horizontal coordinates where the sprites should be placed
    rotates: a list of rotations for the sprites
  """
  if width is None:
    # Choose locations for source sprites and clone targets until at least one
    # source and one clone are feasible.
    while True:
      width, height = common.randint(10, 30), common.randint(10, 30)
      source_goal = num_sprites
      if source_goal is None:
        source_goal = common.randint(1, max(1, min(width, height) // 5))
      clone_goal = num_clones
      if clone_goal is None:
        clone_goal = common.randint(1, max(1, (width * height) // 30))
      color_list = common.random_colors(4)
      rows, cols, idxs, colors = [], [], [], []
      brows, bcols, rotates, clone_idxs = [], [], [], []
      clone_maps = []
      placed, blocked, sprite_shapes = set(), set(), []
      marker_cells, intended_markers, source_views = set(), set(), []
      used_marker_signatures = set()
      source_trials = 0
      while len(sprite_shapes) < source_goal and source_trials < 5 * source_goal:
        source_trials += 1
        box_wide, box_tall = common.randint(3, 7), common.randint(3, 7)
        size = sprite_size
        if size is None:
          size = common.randint(5, 20)
        size = min(size, box_wide * box_tall)
        pixels = common.continuous_creature(size, box_wide, box_tall)
        wide = max(c for _, c in pixels) + 1
        tall = max(r for r, _ in pixels) + 1
        while True:  # Pick positions that aren't all in a line.
          pos = common.sample(range(len(pixels)), 3)
          if len(set(pixels[idx][0] for idx in pos)) == 1: continue
          if len(set(pixels[idx][1] for idx in pos)) == 1: continue
          break
        marker_items = [(color_list[j],) + pixels[pos[j]] for j in range(3)]
        marker_signatures = _marker_signatures(marker_items)
        if used_marker_signatures & marker_signatures:
          continue
        for _ in range(50):
          brow = common.randint(0, height - tall)
          bcol = common.randint(0, width - wide)
          cells = {(brow + r, bcol + c) for r, c in pixels}
          if cells & blocked:
            continue
          sprite_idx = len(sprite_shapes)
          sprite_shapes.append((pixels, wide, tall, marker_items))
          source_views.append(_source_views(pixels, marker_items))
          brows.append(brow)
          bcols.append(bcol)
          sprite_colors = [color_list[3]] * len(pixels)
          sprite_colors[pos[0]] = color_list[0]
          sprite_colors[pos[1]] = color_list[1]
          sprite_colors[pos[2]] = color_list[2]
          rows.extend(p[0] for p in pixels)
          cols.extend(p[1] for p in pixels)
          idxs.extend([sprite_idx] * len(pixels))
          colors.extend(sprite_colors)
          used_marker_signatures |= marker_signatures
          placed |= cells
          blocked |= _with_neighbors(cells, width, height)
          break
      if not sprite_shapes:
        continue
      clone_trials = 0
      while len(clone_idxs) < clone_goal and clone_trials < 10 * clone_goal:
        clone_trials += 1
        sprite_idx = common.randint(0, len(sprite_shapes) - 1)
        pixels, wide, tall, marker_items = sprite_shapes[sprite_idx]
        transform_idx = common.randint(0, len(_TRANSFORMS) - 1)
        rotated = _transform_points(pixels, transform_idx)
        max_row = max(r for r, _ in rotated)
        max_col = max(c for _, c in rotated)
        brow = common.randint(0, height - max_row - 1)
        bcol = common.randint(0, width - max_col - 1)
        cells = {(brow + r, bcol + c) for r, c in rotated}
        if cells & blocked:
          continue
        clone_map = dict(zip(pixels, rotated))
        candidate_markers = frozenset(
            (color, brow + clone_map[(r, c)][0], bcol + clone_map[(r, c)][1])
            for color, r, c in marker_items)
        new_marker_cells = marker_cells | set(candidate_markers)
        candidate_full = frozenset(cells)
        new_intended = intended_markers | {
            (sprite_idx, candidate_markers, candidate_full)}
        if _has_extra_marker_occurrence(new_marker_cells, source_views,
                                        new_intended, width, height):
          continue
        clone_idxs.append(sprite_idx)
        brows.append(brow)
        bcols.append(bcol)
        rotates.append(transform_idx)
        clone_maps.append(clone_map)
        marker_cells = new_marker_cells
        intended_markers = new_intended
        placed |= cells
        blocked |= _with_neighbors(cells, width, height)
      if clone_idxs:
        break

  num_sprites, mode = max(idxs) + 1, max(set(colors), key=colors.count)
  if "clone_idxs" not in locals():
    clone_idxs = list(range(len(brows) - num_sprites))
  grid, output = common.grids(width, height)

  def draw_sprite(sprite_idx):
    for row, col, i, color in zip(rows, cols, idxs, colors):
      if i != sprite_idx:
        continue
      r, c = row, col
      brow, bcol = brows[i], bcols[i]
      grid[brow + r][bcol + c] = color
      wide = max([c for c, idx in zip(cols, idxs) if idx == i]) + 1
      tall = max([r for r, idx in zip(rows, idxs) if idx == i]) + 1
      for clone_pos, clone_idx in enumerate(clone_idxs):
        if clone_idx != i:
          continue
        if "clone_maps" in locals():
          rr, cc = clone_maps[clone_pos][(r, c)]
        else:
          rr, cc = _rotated_cell(r, c, wide, tall, rotates[clone_pos])
        brow, bcol = brows[num_sprites + clone_pos], bcols[num_sprites + clone_pos]
        output[brow + rr][bcol + cc] = color
        if color == mode: continue  # For the clone, we hide the common color.
        grid[brow + rr][bcol + cc] = color

  for sprite_idx in range(1):
    draw_sprite(sprite_idx)
  for sprite_idx in range(1, num_sprites):
    draw_sprite(sprite_idx)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=14,
               rows=[0, 1, 1, 1, 2, 2, 2, 0, 1, 1, 2, 2, 2, 3, 3, 4],
               cols=[1, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 2, 0, 2, 0],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               colors=[8, 3, 8, 1, 8, 4, 8, 3, 8, 8, 8, 8, 4, 8, 8, 1],
               brows=[1, 6, 9, 2], bcols=[2, 7, 1, 13], rotates=[1, 1]),
      generate(width=15, height=14,
               rows=[0, 1, 1, 1, 2, 3, 4, 5, 5, 5],
               cols=[1, 0, 1, 2, 1, 1, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               colors=[2, 4, 3, 3, 3, 3, 3, 3, 1, 3],
               brows=[3, 10], bcols=[3, 9], rotates=[2]),
      generate(width=14, height=16,
               rows=[0, 1, 1, 2, 2, 2, 2, 2, 2, 3],
               cols=[4, 0, 4, 0, 1, 2, 3, 4, 5, 4],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               colors=[4, 8, 8, 1, 8, 8, 8, 2, 8, 8],
               brows=[2, 10], bcols=[5, 1], rotates=[3]),
  ]
  test = [
      generate(width=19, height=24,
               rows=[0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 0, 0, 1, 1, 2, 2, 2],
               cols=[2, 1, 2, 3, 4, 5, 2, 5, 0, 1, 2, 3, 0, 1, 1, 3, 1, 2, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
               colors=[5, 5, 1, 5, 5, 4, 5, 5, 2, 5, 5, 5, 5, 2, 5, 5, 4, 5, 1],
               brows=[3, 9, 16, 12], bcols=[5, 10, 9, 2], rotates=[1, 4]),
  ]
  return {"train": train, "test": test}
