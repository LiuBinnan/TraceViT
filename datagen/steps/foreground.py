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

"""Post-hoc foreground recolor: apply one consistent random color bijection to
input + output + every step (background fixed). The mimetic generators bake in
the original ARC colors; this diversifies the foreground colors of already-
generated, color-blind examples without re-running the generator -- so it works
on tasks the generator-level recolor (colors_pool) cannot touch. Color-sensitive
tasks must be excluded by the caller (see add_foregrounds._should_recolor).

Complements steps.background.recolor_background: that one relabels only a black
(0) background to an unused color, while this one fixes the background (the
most-common color of the input, matching steps.background._most_common) and
permutes every foreground color among the remaining 0..9 \\ {bg}."""

from collections import Counter


def background_color(grid):
    """The most-common color in `grid` (treated as the fixed background)."""
    counts = Counter(c for row in grid for c in row)
    return counts.most_common(1)[0][0] if counts else 0


def _appearing(frames):
    seen = set()
    for grid in frames:
        for row in grid:
            seen.update(row)
    return seen


def recolor_foreground(input_grid, output_grid, steps, rng, freeze=()):
    """Return (new_input, new_output, new_steps, applied) with one consistent
    random injection applied to every frame's non-background colors.

    `applied` is the {src: dst} actually changed (identity entries omitted).
    Background (most-common color of `input_grid`) is excluded from both domain
    and codomain, so it stays put and no foreground color collides with it.
    Each color in `freeze` is likewise excluded from both domain and codomain
    (neither recolored nor a target), for semantically load-bearing colors (gray
    axis, yellow legend, ...) that must stay put while other colors recolor."""
    bg = background_color(input_grid)
    frames = [input_grid, output_grid] + list(steps)
    frozen = set(freeze)
    frozen.add(bg)                                         # bg always frozen
    domain = sorted(c for c in _appearing(frames) if c not in frozen)
    available = [c for c in range(10) if c not in frozen]  # targets, never frozen
    targets = rng.sample(available, len(domain))           # distinct -> injection
    mapping = dict(zip(domain, targets))

    def remap(grid):
        return [[mapping.get(c, c) for c in row] for row in grid]

    new_input = remap(input_grid)
    new_output = remap(output_grid)
    new_steps = [remap(s) for s in steps]
    applied = {s: d for s, d in mapping.items() if s != d}
    return new_input, new_output, new_steps, applied
