"""Helpers for applying ARC-GEN generator variations."""

import common


def normalize_kwargs(generator_kwargs):
    """Return a shallow copy of generator kwargs, validating the public shape."""
    if generator_kwargs is None:
        return {}
    if not isinstance(generator_kwargs, dict):
        raise TypeError("generator_kwargs must be a dict or None")
    return dict(generator_kwargs)


def normalize_colors(colors):
    """Return a copy of a color override, or None when no override is present."""
    if colors is None:
        return None
    colors = list(colors)
    if len(colors) != 10:
        raise ValueError("colors must contain exactly 10 entries")
    for color in colors:
        if not isinstance(color, int) or color < 0 or color > 9:
            raise ValueError("colors entries must be integers from 0 to 9")
    return colors


def push_colors(colors):
    """Apply a color override and return the previous color state."""
    colors = normalize_colors(colors)
    if colors is None:
        return None
    previous = list(common.internal_colors)
    common.set_colors(colors)
    return previous


def pop_colors(previous):
    """Restore a color state returned by push_colors()."""
    if previous is not None:
        common.set_colors(previous)
