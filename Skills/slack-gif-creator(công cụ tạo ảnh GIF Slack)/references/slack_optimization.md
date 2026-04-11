# Slack Optimization & Constraints — Elite 2026

Slack has strict technical limits for GIFs. In 2026, failing to optimize means your content won't load or will look blurry for team members.

---

## 📐 1. Technical Specifications
An Elite engineer designs within constraints.

| Context | Dimension | Target FPS | Optimization | Max Size |
| :--- | :--- | :--- | :--- | :--- |
| **Slack Emoji** | 128 x 128 px | 10–15 | 32–64 Colors | < 128 KB |
| **Slack Message**| 480 x 480 px | 20–30 | 128 Colors | < 2 MB |

## 🎨 2. Color Quantization
GIFs are limited to 256 colors.
- **Palette Management**: Use the smallest palette possible to keep file size low.
- `builder.save(num_colors=48)`: For simple emojis, 48 colors is often indistinguishable from 256 but significantly smaller.
- **Transparency**: For emojis, ensure you use a transparent background or match it to Slack's UI themes.

## 🔄 3. Seamless Loop Synchronization
A high-quality GIF must loop without a "jump" or flicker.
- **State Matching**: The state at `t = 1.0` must exactly match the state at `t = 0.0`.
- **Logic Check**: `t = frame_index / total_frames`. Since `frame_index` goes from `0` to `total_frames - 1`, the final state is just slightly before the initial state, creating a smooth transition.

## 🧹 4. Performance Profiling
Before finalizing:
- **Validation**: Use `validators.validate_gif` to check if your file meets the targeted context (Emoji vs Message).
- **Cleanup**: Remove unnecessary frames if the animation is static for parts of the duration.

---

## ⚡ Elite Insight
> "Avoid using complex gradients. GIFs handle solid blocks of color and dithering better than smooth gradients. If you must use a gradient, keep the step count low to avoid 'banding'."
