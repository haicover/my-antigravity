# 🌇 Sunset Boulevard Theme

> A warm, vibrant, and energetic theme inspired by golden hour sunsets – **bold, creative, and irresistibly inviting**.

## 🎨 Color Palette

| Color Name   | Hex Code  | Inspired by     | Suggested Usage                                     |
| ------------ | --------- | --------------- | --------------------------------------------------- |
| Burnt Orange | `#e76f51` | Glowing embers  | Primary accent – buttons, CTAs, key highlights      |
| Coral        | `#f4a261` | Soft coral reef | Secondary accent – icons, subheadings, hover states |
| Warm Sand    | `#e9c46a` | Sunlit beach    | Backgrounds, highlight boxes, light fills           |
| Deep Purple  | `#264653` | Twilight sky    | Dark text, footers, contrast backgrounds            |

> 💡 Pro tip: Use `Warm Sand` as a light background, `Deep Purple` for body text, `Burnt Orange` for all interactive elements, and `Coral` for supporting details.

## 🔤 Typography

| Type          | Font              | Character                                   |
| ------------- | ----------------- | ------------------------------------------- |
| **Headers**   | DejaVu Serif Bold | Serif – classic, warm, confident            |
| **Body Text** | DejaVu Sans       | Sans-serif – modern, clean, highly readable |

> Pairing a serif header with a sans-serif body creates a dynamic yet balanced contrast – perfect for creative and marketing content.

## ✅ Best Used For

Sunset Boulevard adds energy and emotion, making it ideal for:

- 🎨 **Creative pitches & agency decks** – stands out, memorable
- 📣 **Marketing presentations, product launches** – grabs attention, drives excitement
- 🌿 **Lifestyle brands, wellness, travel** – evokes warmth, adventure, positivity
- 🎉 **Event promotions (concerts, festivals)** – vibrant, festive, high-energy
- 💡 **Inspirational content, motivational talks** – uplifting color psychology

## 📂 How to Use in Theme Factory Skill

1. Place this file in the `themes/` directory as `sunset-boulevard.md`.
2. When the user selects "Sunset Boulevard" from the theme showcase:
   - Main background: `#e9c46a` (Warm Sand) – light and airy
   - Body text: `#264653` (Deep Purple) – strong contrast
   - Primary accent (buttons, links): `#e76f51` (Burnt Orange)
   - Secondary accent (icons, borders): `#f4a261` (Coral)
   - Font: DejaVu Sans for body, DejaVu Serif Bold for headers
3. Check contrast: Deep Purple on Warm Sand meets WCAG AA; white text on Burnt Orange also readable.

## 🖼️ Quick CSS Example

```css
body {
  background-color: #e9c46a; /* Warm Sand */
  color: #264653; /* Deep Purple */
  font-family: "DejaVu Sans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "DejaVu Serif Bold", serif;
  color: #264653;
}
.button {
  background-color: #e76f51; /* Burnt Orange */
  color: white;
  border: none;
  border-radius: 40px;
  padding: 10px 24px;
  transition: 0.3s;
}
.button:hover {
  background-color: #f4a261; /* Coral */
}
.highlight {
  background-color: #f4a261;
  padding: 2px 8px;
  border-radius: 12px;
  color: #264653;
}
```
