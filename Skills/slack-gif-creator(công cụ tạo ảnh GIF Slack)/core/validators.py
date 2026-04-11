#!/usr/bin/env python3
"""
Validators - Check if GIFs meet Slack's requirements.

This module provides functions to validate GIF files against Slack's
recommendations for emoji and message attachments.

Slack limits:
- Emoji GIF: recommended 128x128, max ~1MB, < 50 frames
- Message GIF: aspect ratio ≤ 2:1, min dimension 320-640, max ~5MB
"""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image, UnidentifiedImageError

# Configure module logger
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Slack Recommendations (constants)
# ------------------------------------------------------------------------------

class SlackLimits:
    """Slack file size and dimension recommendations."""

    # Emoji limits
    EMOJI_SIZE_RECOMMENDED = 128
    EMOJI_SIZE_MIN = 64
    EMOJI_SIZE_MAX = 128
    EMOJI_MAX_FRAMES = 50
    EMOJI_MAX_SIZE_MB = 1.0
    EMOJI_MAX_SIZE_KB = 1024.0

    # Message GIF limits
    MSG_ASPECT_RATIO_MAX = 2.0
    MSG_MIN_DIMENSION_MIN = 320
    MSG_MIN_DIMENSION_MAX = 640
    MSG_MAX_SIZE_MB = 5.0
    MSG_MAX_SIZE_KB = 5120.0

    # General
    MAX_COLORS = 256  # GIF format limit


# ------------------------------------------------------------------------------
# Result Dataclass
# ------------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Structured result of GIF validation."""

    file: str
    passes: bool
    width: int
    height: int
    size_bytes: int
    size_kb: float
    size_mb: float
    frame_count: int
    duration_seconds: Optional[float]
    fps: Optional[float]
    is_emoji: bool
    optimal: Optional[bool] = None
    suggestions: list[str] = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


# ------------------------------------------------------------------------------
# Core Validation Functions
# ------------------------------------------------------------------------------

def _get_gif_info(gif_path: Path) -> Tuple[int, int, int, float, float]:
    """
    Extract GIF metadata.

    Returns:
        (width, height, frame_count, total_duration_sec, fps)
    Raises:
        FileNotFoundError, UnidentifiedImageError, OSError
    """
    with Image.open(gif_path) as img:
        if img.format != "GIF":
            raise ValueError(f"File is not a GIF: {gif_path}")

        width, height = img.size
        frame_count = 0
        total_duration_ms = 0

        try:
            while True:
                img.seek(frame_count)
                duration = img.info.get("duration", 0)
                # Some GIFs have 0 duration; fallback to 100ms (10 fps)
                total_duration_ms += duration if duration > 0 else 100
                frame_count += 1
        except EOFError:
            pass

        total_duration_sec = total_duration_ms / 1000.0
        fps = frame_count / total_duration_sec if total_duration_sec > 0 else 0

        return width, height, frame_count, total_duration_sec, fps


def validate_gif(
    gif_path: Union[str, Path],
    is_emoji: bool = True,
    verbose: bool = True,
) -> Tuple[bool, Union[dict, ValidationResult]]:
    """
    Validate GIF against Slack requirements.

    Args:
        gif_path: Path to GIF file.
        is_emoji: If True, validate as emoji (128x128, small size).
                  If False, validate as message GIF (aspect ratio ≤2:1).
        verbose: If True, print summary to console and use logging.

    Returns:
        Tuple of (passes, result) where result is either a dict (for backward
        compatibility) or a ValidationResult object. Use `return_dict=False`
        to get the dataclass.

    Examples:
        >>> passes, info = validate_gif("my.gif", is_emoji=True)
        >>> if passes:
        ...     print("Ready for Slack!")
        ... else:
        ...     print("Suggestions:", info.get("suggestions", []))
    """
    gif_path = Path(gif_path)

    # Validate file existence
    if not gif_path.exists():
        error_msg = f"File not found: {gif_path}"
        if verbose:
            logger.error(error_msg)
        return False, {"error": error_msg, "file": str(gif_path)}

    # Get file size
    size_bytes = gif_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    # Extract GIF metadata
    try:
        width, height, frame_count, duration_sec, fps = _get_gif_info(gif_path)
    except (UnidentifiedImageError, ValueError, OSError) as e:
        error_msg = f"Failed to read GIF: {e}"
        if verbose:
            logger.error(error_msg)
        return False, {"error": error_msg, "file": str(gif_path)}

    # Validate based on type
    optimal = None
    passes = True
    suggestions = []

    if is_emoji:
        # Emoji: should be square and within 64-128
        if width != height:
            passes = False
            suggestions.append(f"Emoji must be square (width={width}, height={height})")
        elif width < SlackLimits.EMOJI_SIZE_MIN or width > SlackLimits.EMOJI_SIZE_MAX:
            passes = False
            suggestions.append(
                f"Emoji size should be {SlackLimits.EMOJI_SIZE_RECOMMENDED}x{SlackLimits.EMOJI_SIZE_RECOMMENDED} "
                f"(got {width}x{height})"
            )
        else:
            optimal = (width == SlackLimits.EMOJI_SIZE_RECOMMENDED)

        # Check file size
        if size_mb > SlackLimits.EMOJI_MAX_SIZE_MB:
            passes = False
            suggestions.append(
                f"Emoji file size exceeds {SlackLimits.EMOJI_MAX_SIZE_MB:.1f}MB "
                f"(current: {size_mb:.2f}MB). Reduce colors or frames."
            )
        elif size_mb > SlackLimits.EMOJI_MAX_SIZE_MB * 0.8:
            suggestions.append(f"File size is close to limit ({size_mb:.2f}MB). Consider optimizing.")

        # Check frame count
        if frame_count > SlackLimits.EMOJI_MAX_FRAMES:
            passes = False
            suggestions.append(
                f"Emoji has {frame_count} frames (max recommended {SlackLimits.EMOJI_MAX_FRAMES}). "
                "Reduce frame count by lowering FPS or duration."
            )

    else:
        # Message GIF: aspect ratio ≤2:1, min dimension 320-640
        min_dim = min(width, height)
        max_dim = max(width, height)
        aspect_ratio = max_dim / min_dim if min_dim > 0 else float("inf")

        if aspect_ratio > SlackLimits.MSG_ASPECT_RATIO_MAX:
            passes = False
            suggestions.append(
                f"Aspect ratio {aspect_ratio:.2f}:1 exceeds {SlackLimits.MSG_ASPECT_RATIO_MAX}:1. "
                "Crop or resize to a wider shape."
            )

        if not (SlackLimits.MSG_MIN_DIMENSION_MIN <= min_dim <= SlackLimits.MSG_MIN_DIMENSION_MAX):
            passes = False
            suggestions.append(
                f"Smallest dimension should be between {SlackLimits.MSG_MIN_DIMENSION_MIN} and "
                f"{SlackLimits.MSG_MIN_DIMENSION_MAX} pixels (got {min_dim})."
            )

        # Check file size
        if size_mb > SlackLimits.MSG_MAX_SIZE_MB:
            passes = False
            suggestions.append(
                f"File size exceeds {SlackLimits.MSG_MAX_SIZE_MB:.1f}MB (current: {size_mb:.2f}MB). "
                "Reduce colors, frames, or dimensions."
            )
        elif size_mb > SlackLimits.MSG_MAX_SIZE_MB * 0.8:
            suggestions.append(f"File size is near limit ({size_mb:.2f}MB). Consider optimization.")

    # Build result
    result = ValidationResult(
        file=str(gif_path),
        passes=passes,
        width=width,
        height=height,
        size_bytes=size_bytes,
        size_kb=size_kb,
        size_mb=size_mb,
        frame_count=frame_count,
        duration_seconds=duration_sec,
        fps=fps,
        is_emoji=is_emoji,
        optimal=optimal,
        suggestions=suggestions,
    )

    # Print / log if verbose
    if verbose:
        print(f"\n📷 Validating {gif_path.name}:")
        print(f"  Dimensions: {width}x{height}" + (f" (optimal)" if optimal else ""))
        print(f"  Size: {size_kb:.1f} KB ({size_mb:.2f} MB)")
        if fps:
            print(f"  Frames: {frame_count} @ {fps:.1f} fps ({duration_sec:.1f}s)")
        else:
            print(f"  Frames: {frame_count}")

        if passes:
            print("  ✅ Passes Slack requirements")
        else:
            print("  ❌ Does NOT pass Slack requirements")
            if suggestions:
                print("  Suggestions:")
                for s in suggestions[:3]:  # show top 3
                    print(f"    - {s}")

        if not passes and suggestions:
            logger.warning(f"GIF validation failed for {gif_path.name}: {suggestions[0]}")

    # Return as dict for backward compatibility (original API)
    # But we also include the full result as 'result' key for new users
    return passes, {
        **result.to_dict(),
        "error": None,
        "result": result,  # embedded dataclass for advanced use
    }


def is_slack_ready(
    gif_path: Union[str, Path],
    is_emoji: bool = True,
    verbose: bool = True,
) -> bool:
    """
    Quick check if GIF is ready for Slack.

    Args:
        gif_path: Path to GIF file.
        is_emoji: True for emoji GIF, False for message GIF.
        verbose: Print feedback.

    Returns:
        True if dimensions and size are acceptable.
    """
    passes, _ = validate_gif(gif_path, is_emoji, verbose)
    return passes


# ------------------------------------------------------------------------------
# Batch Validation
# ------------------------------------------------------------------------------

def validate_multiple(
    gif_paths: list[Union[str, Path]],
    is_emoji: bool = True,
    verbose: bool = True,
) -> dict[str, ValidationResult]:
    """
    Validate multiple GIFs at once.

    Returns:
        Dictionary mapping file path to ValidationResult.
    """
    results = {}
    for path in gif_paths:
        _, res_dict = validate_gif(path, is_emoji, verbose)
        # Extract the dataclass from the dict
        result = res_dict.get("result")
        if result:
            results[str(path)] = result
        else:
            # Fallback: create a minimal result from dict
            results[str(path)] = ValidationResult(**{k: v for k, v in res_dict.items() if k != "result"})
    return results


# ------------------------------------------------------------------------------
# Demo
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Configure logging for demo
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Example: create a dummy GIF file for testing (requires imageio)
    import tempfile

    try:
        import imageio.v3 as iio
        import numpy as np

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
            dummy_path = tmp.name

        # Create a simple 5-frame GIF
        frames = []
        for i in range(5):
            img = np.zeros((128, 128, 3), dtype=np.uint8)
            img[:, :, 0] = i * 50  # varying red
            frames.append(img)
        iio.imwrite(dummy_path, frames, duration=100)

        # Validate as emoji
        is_ready, info = validate_gif(dummy_path, is_emoji=True, verbose=True)
        print(f"\nReady for Slack emoji: {is_ready}")

        # Clean up
        Path(dummy_path).unlink()
    except ImportError:
        print("Demo requires imageio. Install with: pip install imageio")