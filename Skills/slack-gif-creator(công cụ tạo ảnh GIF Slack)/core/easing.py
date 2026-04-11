#!/usr/bin/env python3
"""
Easing Functions - Timing functions for smooth animations.

Provides a comprehensive set of easing (timing) functions for natural motion,
suitable for UI animations, game development, and data visualization.

All core easing functions take a normalized time `t` in [0, 1] and return an
eased value also in [0, 1], unless otherwise specified.

Additional utilities:
- `interpolate()`: interpolate between two values with any easing.
- `apply_squash_stretch()`: simulate squash/stretch effect.
- `calculate_arc_motion()`: parabolic arc path.

Example:
    >>> import easing
    >>> t = 0.5
    >>> easing.ease_out_quad(t)  # quadratic ease-out
    0.75
    >>> easing.interpolate(0, 100, t, "bounce_out")
    100.0
"""

import math
from typing import Callable, Dict, Tuple, Union

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))


def _ensure_t(t: float) -> float:
    """Ensure t is in [0,1] and return clamped value."""
    return clamp(t, 0.0, 1.0)


# ------------------------------------------------------------------------------
# Basic easing functions
# ------------------------------------------------------------------------------

def linear(t: float) -> float:
    """Linear interpolation (no easing)."""
    return _ensure_t(t)


def ease_in_quad(t: float) -> float:
    """Quadratic ease-in: slow start, accelerating.

    Args:
        t: Normalized time (0..1)

    Returns:
        Eased value (0..1)
    """
    t = _ensure_t(t)
    return t * t


def ease_out_quad(t: float) -> float:
    """Quadratic ease-out: fast start, decelerating."""
    t = _ensure_t(t)
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease-in-out: slow start and end, fastest at middle."""
    t = _ensure_t(t)
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_in_cubic(t: float) -> float:
    """Cubic ease-in (slow start)."""
    t = _ensure_t(t)
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out (fast start)."""
    t = _ensure_t(t)
    return (t - 1) ** 3 + 1


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out."""
    t = _ensure_t(t)
    if t < 0.5:
        return 4 * t * t * t
    return (t - 1) * (2 * t - 2) ** 2 + 1


# ------------------------------------------------------------------------------
# Bounce easing
# ------------------------------------------------------------------------------

def ease_in_bounce(t: float) -> float:
    """Bounce ease-in: bouncy start (mirrored from ease_out_bounce)."""
    t = _ensure_t(t)
    return 1 - ease_out_bounce(1 - t)


def ease_out_bounce(t: float) -> float:
    """Bounce ease-out: bouncy end (simulates a bouncing ball)."""
    t = _ensure_t(t)
    # Magic constants from Robert Penner's easing equations
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t_adj = t - 1.5 / 2.75
        return 7.5625 * t_adj * t_adj + 0.75
    elif t < 2.5 / 2.75:
        t_adj = t - 2.25 / 2.75
        return 7.5625 * t_adj * t_adj + 0.9375
    else:
        t_adj = t - 2.625 / 2.75
        return 7.5625 * t_adj * t_adj + 0.984375


def ease_in_out_bounce(t: float) -> float:
    """Bounce ease-in-out: bounce at both ends."""
    t = _ensure_t(t)
    if t < 0.5:
        return ease_in_bounce(t * 2) * 0.5
    return ease_out_bounce(t * 2 - 1) * 0.5 + 0.5


# ------------------------------------------------------------------------------
# Elastic easing (spring effect)
# ------------------------------------------------------------------------------

def ease_in_elastic(t: float) -> float:
    """Elastic ease-in: springy start."""
    t = _ensure_t(t)
    if t == 0 or t == 1:
        return t
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)


def ease_out_elastic(t: float) -> float:
    """Elastic ease-out: springy end."""
    t = _ensure_t(t)
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1


def ease_in_out_elastic(t: float) -> float:
    """Elastic ease-in-out: spring at both ends."""
    t = _ensure_t(t)
    if t == 0 or t == 1:
        return t
    t2 = t * 2 - 1
    if t2 < 0:
        return -0.5 * math.pow(2, 10 * t2) * math.sin((t2 - 0.1) * 5 * math.pi)
    return math.pow(2, -10 * t2) * math.sin((t2 - 0.1) * 5 * math.pi) * 0.5 + 1


# ------------------------------------------------------------------------------
# Back easing (slight overshoot)
# ------------------------------------------------------------------------------

# Overshoot constants
_BACK_C1 = 1.70158
_BACK_C2 = _BACK_C1 * 1.525
_BACK_C3 = _BACK_C1 + 1


def ease_back_in(t: float) -> float:
    """Back ease-in: moves backward slightly before forward motion."""
    t = _ensure_t(t)
    return _BACK_C3 * t * t * t - _BACK_C1 * t * t


def ease_back_out(t: float) -> float:
    """Back ease-out: overshoots target then settles back."""
    t = _ensure_t(t)
    return 1 + _BACK_C3 * (t - 1) ** 3 + _BACK_C1 * (t - 1) ** 2


def ease_back_in_out(t: float) -> float:
    """Back ease-in-out: overshoot at both ends."""
    t = _ensure_t(t)
    if t < 0.5:
        return ((2 * t) ** 2 * ((_BACK_C2 + 1) * 2 * t - _BACK_C2)) / 2
    return ((2 * t - 2) ** 2 * ((_BACK_C2 + 1) * (t * 2 - 2) + _BACK_C2) + 2) / 2


# ------------------------------------------------------------------------------
# Utility functions for animation
# ------------------------------------------------------------------------------

# Mapping from string names to easing functions
EASING_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    "linear": linear,
    "ease_in": ease_in_quad,
    "ease_out": ease_out_quad,
    "ease_in_out": ease_in_out_quad,
    "quad_in": ease_in_quad,
    "quad_out": ease_out_quad,
    "quad_in_out": ease_in_out_quad,
    "cubic_in": ease_in_cubic,
    "cubic_out": ease_out_cubic,
    "cubic_in_out": ease_in_out_cubic,
    "bounce_in": ease_in_bounce,
    "bounce_out": ease_out_bounce,
    "bounce": ease_in_out_bounce,
    "elastic_in": ease_in_elastic,
    "elastic_out": ease_out_elastic,
    "elastic": ease_in_out_elastic,
    "back_in": ease_back_in,
    "back_out": ease_back_out,
    "back_in_out": ease_back_in_out,
    "anticipate": ease_back_in,   # alias
    "overshoot": ease_back_out,   # alias
}


def get_easing(name: str = "linear") -> Callable[[float], float]:
    """Get an easing function by name.

    Args:
        name: Easing name (see EASING_FUNCTIONS keys).

    Returns:
        Easing function (t -> eased t). Defaults to linear if name not found.
    """
    return EASING_FUNCTIONS.get(name, linear)


def interpolate(start: float, end: float, t: float, easing: str = "linear") -> float:
    """Interpolate between two values with an easing curve.

    Args:
        start: Start value.
        end: End value.
        t: Normalized progress (0..1).
        easing: Name of the easing function.

    Returns:
        Interpolated value.
    """
    t_clamped = _ensure_t(t)
    ease_func = get_easing(easing)
    eased_t = ease_func(t_clamped)
    return start + (end - start) * eased_t


def apply_squash_stretch(
    base_scale: Tuple[float, float],
    intensity: float,
    direction: str = "vertical"
) -> Tuple[float, float]:
    """Apply squash-and-stretch effect to a scale tuple.

    Squash reduces size in one axis, stretches in the perpendicular axis
    to preserve perceived volume.

    Args:
        base_scale: (width_scale, height_scale) normal scales (usually 1,1).
        intensity: Effect strength (0.0 to 1.0).
        direction: "vertical", "horizontal", or "both".

    Returns:
        New (width_scale, height_scale) after squash/stretch.
    """
    intensity = clamp(intensity, 0.0, 1.0)
    w, h = base_scale

    if direction == "vertical":
        h *= 1 - intensity * 0.5
        w *= 1 + intensity * 0.5
    elif direction == "horizontal":
        w *= 1 - intensity * 0.5
        h *= 1 + intensity * 0.5
    else:  # both
        w *= 1 - intensity * 0.3
        h *= 1 - intensity * 0.3

    return (w, h)


def calculate_arc_motion(
    start: Tuple[float, float],
    end: Tuple[float, float],
    height: float,
    t: float
) -> Tuple[float, float]:
    """Calculate position along a parabolic arc.

    Useful for jumping, throwing, or bouncing motion.

    Args:
        start: (x, y) starting point.
        end: (x, y) ending point.
        height: Maximum arc height above the direct line (positive = upward).
        t: Normalized progress (0..1).

    Returns:
        (x, y) point on the arc.
    """
    t_clamped = _ensure_t(t)
    x1, y1 = start
    x2, y2 = end

    # Linear x
    x = x1 + (x2 - x1) * t_clamped

    # Parabolic y: y = linear + arc offset
    arc_offset = 4 * height * t_clamped * (1 - t_clamped)
    y = y1 + (y2 - y1) * t_clamped - arc_offset

    return (x, y)


# ------------------------------------------------------------------------------
# Demo / Example usage
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Quick demonstration
    print("Easing functions demo (t = 0.5):")
    t = 0.5
    for name in ["linear", "quad_out", "cubic_in_out", "bounce_out", "elastic_out", "back_out"]:
        val = get_easing(name)(t)
        print(f"  {name:15s} -> {val:.4f}")

    print("\nInterpolation demo: from 0 to 100 with bounce_out")
    for i in range(0, 11):
        t_val = i / 10.0
        result = interpolate(0, 100, t_val, "bounce_out")
        print(f"  t={t_val:.1f} -> {result:.1f}")

    print("\nSquash/stretch example:")
    original = (1.0, 1.0)
    squashed = apply_squash_stretch(original, intensity=0.6, direction="vertical")
    print(f"  Original: {original} -> Vertical squash/stretch: {squashed}")

    print("\nArc motion: from (0,0) to (100,0) with height 30 at t=0.5")
    arc_point = calculate_arc_motion((0, 0), (100, 0), 30, 0.5)
    print(f"  Point at t=0.5: {arc_point}")