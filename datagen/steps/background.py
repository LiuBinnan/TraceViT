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

"""Post-hoc background-color augmentation.

Relabels a black (0) background to a random *unused* color B, as a single
bijection (the swap 0<->B) applied consistently to input, output and every
step. Because B is absent from every frame, only the background changes -- the
foreground objects and the input->output transformation are untouched -- so the
relabel is semantically safe for any task and B can never collide with a
foreground color. Mirrors re_arc's varied backgrounds while keeping ARC
fidelity.
"""

import collections


def _most_common(grid):
    counter = collections.Counter()
    for row in grid:
        counter.update(row)
    return counter.most_common(1)[0][0] if counter else 0


def _used_colors(frames):
    used = set()
    for grid in frames:
        for row in grid:
            used.update(row)
    return used


def _swap(grid, a, b):
    """Return `grid` with colors a and b swapped (a<->b, others unchanged)."""
    return [[b if value == a else (a if value == b else value)
             for value in row] for row in grid]


def recolor_background(input_grid, output_grid, steps, rng, any_background=False):
    """Relabel the background to a random unused color.

    Returns (input, output, steps, background) where `background` is the chosen
    color B (the original background when the example is left unchanged).

    By default acts only when 0 is the most-common color of `input_grid` (a
    black-background example) -- the canonical, always-safe case. With
    `any_background=True` (opt-in, per a task's `"background_recolor": "any"`
    override) it instead relabels whatever the most-common color IS, e.g. an
    orange canvas; use this only for tasks whose most-common color is a genuine
    background (not load-bearing). B is drawn uniformly from {src} U (colors
    absent from all frames), so most examples get a new background while ~1/(k+1)
    keep the original (matching re_arc, which keeps ~14% black). The swap
    src<->B is a bijection and B is unused, so the relabel only changes the
    background -- foreground and the transformation are preserved, with no color
    collision. When all of 1..9 are present (no unused color) B is src
    (unchanged)."""
    steps = list(steps)
    src = _most_common(input_grid)
    if not any_background and src != 0:
        return input_grid, output_grid, steps, 0
    used = _used_colors([input_grid, output_grid] + steps)
    choices = [src] + [c for c in range(1, 10) if c not in used and c != src]
    background = rng.choice(choices)
    if background == src:
        return input_grid, output_grid, steps, src
    return (_swap(input_grid, src, background),
            _swap(output_grid, src, background),
            [_swap(step, src, background) for step in steps],
            background)
