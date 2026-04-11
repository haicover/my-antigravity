#!/usr/bin/env python3
"""
Frame Composer - Utilities for composing visual elements into frames.

Provides functions for creating blank frames, drawing shapes, text, gradients,
and compositing elements together for animation or image generation.

Dependencies:
    - Pillow (PIL) >= 9.0.0
    - numpy >= 1.20.0

Example:
    >>> from frame_composer import create_blank_frame, draw_circle, draw_text
    >>> frame = create_blank_frame(400, 300, color=(255,255,255))
    >>> frame = draw_circle(frame, (200,150), 50, fill_color=(255,0,0))
    >>> frame.save("output.png")
"""

import math
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
Point = Tuple[int, int]
Rect = Tuple[int, int, int, int]  # (x1, y1, x2, y2)

# Common colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_TRANSPARENT = (0, 0, 0, 0)

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def _clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))


def _clamp_point(x: int, y: int, width: int, height: int) -> Tuple[int, int]:
    """Clamp coordinates to image boundaries."""
    return (_clamp(x, 0, width - 1), _clamp(y, 0, height - 1))


# ------------------------------------------------------------------------------
# Core frame creation
# ------------------------------------------------------------------------------

def create_blank_frame(
    width: int,
    height: int,
    color: Color = COLOR_WHITE,
    mode: str = "RGB"
) -> Image.Image:
    """
    Create a blank frame with a solid color background.

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.
        color: RGB or RGBA tuple (e.g., (255,0,0) or (255,0,0,128)).
        mode: Image mode ("RGB", "RGBA", "L", etc.). Default "RGB".

    Returns:
        PIL Image object.
    """
    if mode == "RGBA" and len(color) == 3:
        color = (*color, 255)  # add alpha
    return Image.new(mode, (width, height), color)


# ------------------------------------------------------------------------------
# Shape drawing (in-place modifications)
# ------------------------------------------------------------------------------

def draw_rectangle(
    frame: Image.Image,
    bbox: Rect,
    fill_color: Optional[Color] = None,
    outline_color: Optional[Color] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a rectangle on the frame.

    Args:
        frame: PIL Image to draw on (modified in-place).
        bbox: (x1, y1, x2, y2) top-left and bottom-right coordinates.
        fill_color: RGB/RGBA fill color (None for transparent fill).
        outline_color: RGB/RGBA outline color (None for no outline).
        outline_width: Width of outline in pixels.

    Returns:
        The modified frame (same object).
    """
    draw = ImageDraw.Draw(frame)
    draw.rectangle(bbox, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_circle(
    frame: Image.Image,
    center: Point,
    radius: int,
    fill_color: Optional[Color] = None,
    outline_color: Optional[Color] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a circle on the frame.

    Args:
        frame: PIL Image to draw on.
        center: (x, y) center point.
        radius: Circle radius in pixels.
        fill_color: Fill color (None for transparent).
        outline_color: Outline color (None for no outline).
        outline_width: Outline width.

    Returns:
        Modified frame.
    """
    draw = ImageDraw.Draw(frame)
    x, y = center
    bbox = (x - radius, y - radius, x + radius, y + radius)
    draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_line(
    frame: Image.Image,
    start: Point,
    end: Point,
    color: Color,
    width: int = 1,
) -> Image.Image:
    """
    Draw a straight line.

    Args:
        frame: PIL Image to draw on.
        start: (x, y) start point.
        end: (x, y) end point.
        color: RGB/RGBA color.
        width: Line width in pixels.

    Returns:
        Modified frame.
    """
    draw = ImageDraw.Draw(frame)
    draw.line([start, end], fill=color, width=width)
    return frame


def draw_polygon(
    frame: Image.Image,
    points: List[Point],
    fill_color: Optional[Color] = None,
    outline_color: Optional[Color] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a polygon from a list of points.

    Args:
        frame: PIL Image to draw on.
        points: List of (x, y) vertices.
        fill_color: Fill color (None for transparent).
        outline_color: Outline color (None for no outline).
        outline_width: Outline width.

    Returns:
        Modified frame.
    """
    draw = ImageDraw.Draw(frame)
    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_star(
    frame: Image.Image,
    center: Point,
    size: int,
    fill_color: Color,
    outline_color: Optional[Color] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a 5-pointed star.

    Args:
        frame: PIL Image to draw on.
        center: (x, y) center point.
        size: Outer radius (distance from center to outer points).
        fill_color: Fill color.
        outline_color: Outline color (None for no outline).
        outline_width: Outline width.

    Returns:
        Modified frame.
    """
    x, y = center
    points = []
    for i in range(10):
        # Angle: 36 degrees per point, start at top (-90°)
        angle = (i * 36 - 90) * math.pi / 180
        radius = size if i % 2 == 0 else size * 0.4  # outer / inner
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))
    return draw_polygon(frame, points, fill_color, outline_color, outline_width)


# ------------------------------------------------------------------------------
# Text drawing
# ------------------------------------------------------------------------------

# Simple font cache
_FONT_CACHE = {}


def _get_font(font_path: Optional[str] = None, size: int = 16) -> ImageFont.ImageFont:
    """Get a PIL font with caching."""
    key = (font_path, size)
    if key not in _FONT_CACHE:
        try:
            if font_path:
                _FONT_CACHE[key] = ImageFont.truetype(font_path, size)
            else:
                _FONT_CACHE[key] = ImageFont.load_default()
        except (IOError, OSError):
            # Fallback to default font
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]


def draw_text(
    frame: Image.Image,
    text: str,
    position: Point,
    color: Color = COLOR_BLACK,
    font_path: Optional[str] = None,
    font_size: int = 16,
    centered: bool = False,
) -> Image.Image:
    """
    Draw text on the frame.

    Args:
        frame: PIL Image to draw on.
        text: String to draw (supports Unicode/emoji if font supports).
        position: (x, y) top-left corner (or center if centered=True).
        color: RGB/RGBA text color.
        font_path: Path to .ttf/.otf font file. If None, uses default.
        font_size: Font size in points.
        centered: If True, position is treated as the center of the text.

    Returns:
        Modified frame.
    """
    draw = ImageDraw.Draw(frame)
    font = _get_font(font_path, font_size)

    if centered:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        position = (x, y)

    draw.text(position, text, fill=color, font=font)
    return frame


# ------------------------------------------------------------------------------
# Gradients and special effects
# ------------------------------------------------------------------------------

def create_gradient_background(
    width: int,
    height: int,
    top_color: Color,
    bottom_color: Color,
    mode: str = "RGB",
) -> Image.Image:
    """
    Create a vertical gradient background using NumPy (fast).

    Args:
        width: Image width.
        height: Image height.
        top_color: RGB/RGBA color at top.
        bottom_color: RGB/RGBA color at bottom.
        mode: Image mode ("RGB" or "RGBA").

    Returns:
        PIL Image with vertical gradient.
    """
    # Ensure both colors have same number of channels
    top_len = len(top_color)
    bottom_len = len(bottom_color)
    if top_len != bottom_len:
        raise ValueError("top_color and bottom_color must have same number of channels")

    channels = top_len
    if mode == "RGB" and channels == 4:
        # Ignore alpha if mode RGB
        top_color = top_color[:3]
        bottom_color = bottom_color[:3]
        channels = 3

    # Create gradient array
    gradient = np.zeros((height, width, channels), dtype=np.uint8)
    for c in range(channels):
        top_val = top_color[c]
        bottom_val = bottom_color[c]
        # Linear interpolation for each row
        gradient[:, :, c] = np.linspace(top_val, bottom_val, height, dtype=np.uint8)[:, np.newaxis]

    return Image.fromarray(gradient, mode=mode)


def apply_squash_stretch(
    frame: Image.Image,
    intensity: float,
    direction: str = "vertical",
    preserve_volume: bool = True,
) -> Image.Image:
    """
    Apply squash-and-stretch effect by resizing the frame.

    Args:
        frame: PIL Image to transform.
        intensity: Strength of effect (0.0 to 1.0).
        direction: "vertical" (squash height, stretch width) or "horizontal".
        preserve_volume: If True, keep area roughly constant.

    Returns:
        Resized image (new object).
    """
    intensity = max(0.0, min(1.0, intensity))
    w, h = frame.size

    if direction == "vertical":
        new_h = int(h * (1 - intensity * 0.5))
        new_w = int(w * (1 + intensity * 0.5)) if preserve_volume else w
    elif direction == "horizontal":
        new_w = int(w * (1 - intensity * 0.5))
        new_h = int(h * (1 + intensity * 0.5)) if preserve_volume else h
    else:
        raise ValueError("direction must be 'vertical' or 'horizontal'")

    return frame.resize((new_w, new_h), Image.Resampling.LANCZOS)


# ------------------------------------------------------------------------------
# Composite multiple frames (layering)
# ------------------------------------------------------------------------------

def overlay_frame(
    background: Image.Image,
    foreground: Image.Image,
    position: Point = (0, 0),
    alpha: float = 1.0,
) -> Image.Image:
    """
    Overlay a foreground image onto a background.

    Args:
        background: Base image (will be modified).
        foreground: Image to overlay.
        position: (x, y) top-left corner for foreground placement.
        alpha: Global alpha factor (0.0 transparent to 1.0 opaque).

    Returns:
        New image with overlay (background unchanged).
    """
    # Convert to RGBA if needed for blending
    if background.mode != "RGBA":
        bg = background.convert("RGBA")
    else:
        bg = background.copy()

    fg = foreground.convert("RGBA")
    if alpha < 1.0:
        fg = Image.blend(Image.new("RGBA", fg.size, (0, 0, 0, 0)), fg, alpha)

    bg.paste(fg, position, fg)
    return bg


# ------------------------------------------------------------------------------
# Demo
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Create a gradient background
    bg = create_gradient_background(400, 300, (135, 206, 235), (25, 25, 112))
    bg.save("demo_gradient.png")

    # Draw a star and circle
    bg = draw_star(bg, (200, 150), 60, fill_color=(255, 215, 0), outline_color=(255, 140, 0), outline_width=2)
    bg = draw_circle(bg, (200, 150), 70, outline_color=COLOR_WHITE, outline_width=3)

    # Draw text
    bg = draw_text(bg, "★ Star Power ★", (200, 260), color=COLOR_WHITE, font_size=24, centered=True)

    # Save result
    bg.save("demo_frame_composer.png")
    print("Demo images saved: demo_gradient.png and demo_frame_composer.png")