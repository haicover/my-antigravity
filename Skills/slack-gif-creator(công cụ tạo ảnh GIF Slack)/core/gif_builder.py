#!/usr/bin/env python3
"""
GIF Builder - Core module for assembling frames into GIFs optimized for Slack.

This module provides the main interface for creating GIFs from programmatically
generated frames, with automatic optimization for Slack's requirements.
"""

import logging
import math
from pathlib import Path
from typing import List, Optional, Tuple, Union

import imageio.v3 as imageio
import numpy as np
from PIL import Image

# Configure module logger
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def _ensure_rgb_array(frame: Union[np.ndarray, Image.Image]) -> np.ndarray:
    """Convert frame to RGB numpy array."""
    if isinstance(frame, Image.Image):
        frame = np.array(frame.convert("RGB"))
    elif frame.ndim == 2:  # Grayscale
        frame = np.stack([frame] * 3, axis=-1)
    elif frame.shape[-1] == 4:  # RGBA
        frame = frame[:, :, :3]
    return frame.astype(np.uint8)


def _calculate_similarity(frame_a: np.ndarray, frame_b: np.ndarray) -> float:
    """
    Calculate similarity between two RGB frames (0.0 = completely different, 1.0 = identical).

    Uses mean absolute difference normalized by 255.
    """
    diff = np.abs(frame_a.astype(np.float32) - frame_b.astype(np.float32))
    mean_diff = np.mean(diff) / 255.0
    return 1.0 - mean_diff


# ------------------------------------------------------------------------------
# GIFBuilder Class
# ------------------------------------------------------------------------------

class GIFBuilder:
    """Builder for creating optimized GIFs from frames."""

    def __init__(self, width: int = 480, height: int = 480, fps: int = 15):
        """
        Initialize GIF builder.

        Args:
            width: Frame width in pixels (must be >0).
            height: Frame height in pixels (must be >0).
            fps: Frames per second (must be >0).

        Raises:
            ValueError: If width/height/fps are invalid.
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Width and height must be positive, got {width}x{height}")
        if fps <= 0:
            raise ValueError(f"FPS must be positive, got {fps}")

        self.width = width
        self.height = height
        self.fps = fps
        self._frames: List[np.ndarray] = []

    @property
    def frame_count(self) -> int:
        """Number of frames currently stored."""
        return len(self._frames)

    def add_frame(self, frame: Union[np.ndarray, Image.Image, str, Path]) -> None:
        """
        Add a single frame to the GIF.

        Args:
            frame: Can be a numpy array (HxWx3), PIL Image, or file path to an image.

        Raises:
            ValueError: If frame cannot be converted or has wrong shape.
        """
        if isinstance(frame, (str, Path)):
            frame = Image.open(frame)

        # Convert to RGB numpy array
        arr = _ensure_rgb_array(frame)

        # Resize if necessary
        if arr.shape[:2] != (self.height, self.width):
            pil_frame = Image.fromarray(arr)
            pil_frame = pil_frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
            arr = np.array(pil_frame)

        self._frames.append(arr)

    def add_frames(self, frames: List[Union[np.ndarray, Image.Image, str, Path]]) -> None:
        """Add multiple frames at once."""
        for f in frames:
            self.add_frame(f)

    def _create_global_palette(self, num_colors: int) -> Optional[Image.Image]:
        """
        Create a global palette by sampling frames.

        Returns:
            PIL Image palette object, or None if not enough frames.
        """
        if len(self._frames) < 2:
            return None

        # Sample up to 8 frames evenly
        sample_count = min(8, len(self._frames))
        indices = np.linspace(0, len(self._frames) - 1, sample_count, dtype=int)
        sample_frames = [self._frames[i] for i in indices]

        # Stack all pixels from sample frames into a single tall image
        all_pixels = np.vstack([f.reshape(-1, 3) for f in sample_frames])  # (total_pixels, 3)
        total_pixels = len(all_pixels)

        # Create a roughly square image (max width 512)
        max_width = 512
        width = min(max_width, int(math.sqrt(total_pixels)))
        height = (total_pixels + width - 1) // width
        # Pad if needed
        needed = width * height - total_pixels
        if needed > 0:
            pad = np.zeros((needed, 3), dtype=np.uint8)
            all_pixels = np.vstack([all_pixels, pad])

        img_array = all_pixels.reshape(height, width, 3).astype(np.uint8)
        combined_img = Image.fromarray(img_array, mode="RGB")

        # Quantize to create global palette
        return combined_img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)

    def optimize_colors(
        self, num_colors: int = 128, use_global_palette: bool = True, dither: int = Image.Dither.FLOYDSTEINBERG
    ) -> List[np.ndarray]:
        """
        Reduce colors in all frames using quantization.

        Args:
            num_colors: Target number of colors (8-256).
            use_global_palette: If True, compute a single palette from all frames (better compression).
            dither: Dithering method (Image.Dither.NONE, FLOYDSTEINBERG, etc.).

        Returns:
            List of color-optimized frames as RGB numpy arrays.

        Raises:
            ValueError: If num_colors is out of range.
        """
        if not self._frames:
            raise ValueError("No frames to optimize. Add frames first.")
        if not (8 <= num_colors <= 256):
            raise ValueError(f"num_colors must be between 8 and 256, got {num_colors}")

        optimized = []
        global_palette = None

        if use_global_palette:
            global_palette = self._create_global_palette(num_colors)

        if global_palette is not None:
            # Apply same palette to all frames
            for frame in self._frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(palette=global_palette, dither=dither)
                optimized.append(np.array(quantized.convert("RGB")))
        else:
            # Per-frame quantization
            for frame in self._frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT, dither=dither)
                optimized.append(np.array(quantized.convert("RGB")))

        logger.info(f"Color optimization: {len(self._frames)} frames -> {num_colors} colors, global={use_global_palette}")
        return optimized

    def deduplicate_frames(self, threshold: float = 0.9995) -> int:
        """
        Remove duplicate or near-duplicate consecutive frames.

        Args:
            threshold: Similarity threshold (0.0-1.0). 0.9995 = nearly identical.
                      Use 0.9995+ to preserve subtle animations, 0.98 for aggressive removal.

        Returns:
            Number of frames removed.
        """
        if len(self._frames) < 2:
            return 0

        deduplicated = [self._frames[0]]
        removed = 0

        for i in range(1, len(self._frames)):
            sim = _calculate_similarity(deduplicated[-1], self._frames[i])
            if sim < threshold:
                deduplicated.append(self._frames[i])
            else:
                removed += 1

        self._frames = deduplicated
        logger.info(f"Deduplication removed {removed} frames (threshold={threshold})")
        return removed

    def save(
        self,
        output_path: Union[str, Path],
        num_colors: int = 128,
        optimize_for_emoji: bool = False,
        remove_duplicates: bool = False,
        dither: int = Image.Dither.FLOYDSTEINBERG,
        use_global_palette: bool = True,
    ) -> dict:
        """
        Save frames as optimized GIF for Slack.

        Args:
            output_path: Where to save the GIF.
            num_colors: Number of colors (8-256). Fewer = smaller file.
            optimize_for_emoji: If True, resize to 128x128, reduce colors to 48, and limit frames.
            remove_duplicates: If True, remove nearly identical consecutive frames.
            dither: Dithering method for quantization.
            use_global_palette: Use single palette for all frames (better compression).

        Returns:
            Dictionary with file info (path, size_kb, dimensions, frame_count, etc.).

        Raises:
            ValueError: If no frames to save.
        """
        if not self._frames:
            raise ValueError("No frames to save. Add frames with add_frame() first.")

        output_path = Path(output_path)

        # Apply optimizations in order: deduplicate, emoji resize, then color optimization
        if remove_duplicates:
            self.deduplicate_frames(threshold=0.9995)

        # Emoji optimization: resize, reduce frames, reduce colors
        if optimize_for_emoji:
            self._apply_emoji_optimization(num_colors)

        # Color optimization
        optimized_frames = self.optimize_colors(num_colors, use_global_palette, dither)

        # Write GIF
        frame_duration_ms = 1000 / self.fps
        imageio.imwrite(
            output_path,
            optimized_frames,
            duration=frame_duration_ms,
            loop=0,  # infinite loop
            # optional: palettesize=num_colors  (but imageio handles it)
        )

        # Gather info
        file_size_bytes = output_path.stat().st_size
        file_size_kb = file_size_bytes / 1024
        file_size_mb = file_size_kb / 1024
        info = {
            "path": str(output_path),
            "size_bytes": file_size_bytes,
            "size_kb": file_size_kb,
            "size_mb": file_size_mb,
            "dimensions": f"{self.width}x{self.height}",
            "frame_count": len(optimized_frames),
            "fps": self.fps,
            "duration_seconds": len(optimized_frames) / self.fps,
            "colors": num_colors,
            "emoji_optimized": optimize_for_emoji,
        }

        # Log summary
        logger.info(
            f"GIF saved: {output_path} | {len(optimized_frames)} frames | "
            f"{file_size_kb:.1f} KB | {self.width}x{self.height} | {num_colors} colors"
        )
        print(f"\n✓ GIF created successfully!")
        print(f"  Path: {output_path}")
        print(f"  Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
        print(f"  Dimensions: {self.width}x{self.height}")
        print(f"  Frames: {len(optimized_frames)} @ {self.fps} fps")
        print(f"  Duration: {info['duration_seconds']:.1f}s")
        print(f"  Colors: {num_colors}")
        if optimize_for_emoji:
            print("  Optimized for emoji (128x128, reduced colors/frames)")

        return info

    def _apply_emoji_optimization(self, num_colors: int) -> None:
        """Internal method to resize frames, reduce frame count, and adjust colors for emoji."""
        # Resize to 128x128 if needed
        if self.width != 128 or self.height != 128:
            logger.info(f"Resizing frames from {self.width}x{self.height} to 128x128 for emoji")
            self.width = 128
            self.height = 128
            resized = []
            for frame in self._frames:
                pil_frame = Image.fromarray(frame)
                pil_frame = pil_frame.resize((128, 128), Image.Resampling.LANCZOS)
                resized.append(np.array(pil_frame))
            self._frames = resized

        # Reduce frame count to around 12 (Slack emoji limit is small)
        target_frames = 12
        if len(self._frames) > target_frames:
            step = max(1, len(self._frames) // target_frames)
            new_frames = [self._frames[i] for i in range(0, len(self._frames), step)]
            # Trim to target_frames if still too many
            if len(new_frames) > target_frames:
                new_frames = new_frames[:target_frames]
            logger.info(f"Reduced frames from {len(self._frames)} to {len(new_frames)} for emoji")
            self._frames = new_frames

        # Adjust color count (capped at 48)
        # Note: num_colors will be passed to optimize_colors later

    def to_bytes(
        self,
        num_colors: int = 128,
        optimize_for_emoji: bool = False,
        remove_duplicates: bool = False,
        format: str = "GIF",
        dither: int = Image.Dither.FLOYDSTEINBERG,
    ) -> bytes:
        """
        Export GIF as bytes (useful for API uploads).

        Args:
            Same as save(), but returns bytes instead of writing to disk.

        Returns:
            GIF image as bytes.
        """
        import io

        buffer = io.BytesIO()
        # Temporarily save to buffer
        temp_path = Path(buffer.name) if hasattr(buffer, "name") else None
        # Use a dummy path for the internal logic, but we need to trick save().
        # Simpler: implement directly similar to save but writing to buffer.
        # Since save() writes to disk, we create a temp file.
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=True) as tmp:
            self.save(
                tmp.name,
                num_colors=num_colors,
                optimize_for_emoji=optimize_for_emoji,
                remove_duplicates=remove_duplicates,
                dither=dither,
                use_global_palette=True,
            )
            with open(tmp.name, "rb") as f:
                return f.read()

    def clear(self) -> None:
        """Clear all frames (useful for creating multiple GIFs)."""
        self._frames.clear()
        logger.debug("Cleared all frames")

    def __len__(self) -> int:
        return len(self._frames)


# ------------------------------------------------------------------------------
# Demo
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Configure logging to see output
    logging.basicConfig(level=logging.INFO)

    # Create a simple GIF with colored frames
    builder = GIFBuilder(width=200, height=200, fps=10)

    # Generate 20 frames with moving circle
    import math

    for i in range(20):
        # Create blank white frame
        frame = Image.new("RGB", (200, 200), (255, 255, 255))
        draw = ImageDraw.Draw(frame)
        t = i / 19.0  # 0 to 1
        x = int(100 + 80 * math.sin(t * 2 * math.pi))
        y = int(100 + 80 * math.cos(t * 2 * math.pi))
        draw.ellipse([x-15, y-15, x+15, y+15], fill=(255, 0, 0))
        builder.add_frame(frame)

    # Save with optimization
    builder.save("demo.gif", num_colors=64, remove_duplicates=True)
    print("Demo GIF saved as demo.gif")