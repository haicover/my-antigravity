# Animation Physics & Dynamics — Elite 2026

In 2026, creating high-quality GIFs requires an understanding of motion physics. Professional animations are smooth, natural, and mathematically sound.

---

## 📐 1. The Mathematics of Motion
To move objects across the screen, we use trigonometry and time-based functions.
- **Trigonometry (Sin/Cos)**: Perfect for oscillating motions.
    - `dx = math.sin(t * 2 * math.pi) * amplitude` (Shake/Wave)
    - `scale = 1.0 + 0.2 * math.sin(t * 2 * math.pi)` (Pulse/Breathe)
- **Time Normalization**: Always normalize your loop progress `t` between `0.0` and `1.0`. `t = frame_index / total_frames`.

## 🔄 2. Easing Functions
Linear motion is boring. Elite animations use **Easing** to simulate weight and inertia.
- **Ease-In/Out**: Smooth starts and deceleration.
- **Bounce**: Simulate a hard surface impact (using `core.easing.bounce_out`).
- **Elastic**: Add a "rubbery" feel to scaling or rotation (using `core.easing.elastic_out`).

## 📽️ 3. Frame Interpolation
Interpolation is the process of calculating values between a start state and an end state.
- Use `core.easing.interpolate(start, end, t, easing='ease_out')` to calculate positions, colors, or sizes.
- **Color Interpolation**: Smoothly transitioning between colors in a gradient.

## 🏃 4. Multi-Step Choreography
Complex animations are composed of multiple stages:
1. **Entry**: Object enters from off-screen with `ease_out`.
2. **Action**: Object performs a `shake` or `pulse`.
3. **Exit**: Object fades or explodes.

---

## ⚡ Elite Insight
> "The secret to smooth animation is the **FPS/Frame count** balance. For Slack emojis, 15 FPS is the sweet spot. If your animation feels 'staccato', check your interpolation logic for non-linear easing."
