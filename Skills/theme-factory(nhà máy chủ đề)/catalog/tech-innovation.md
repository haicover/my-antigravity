# ⚡ Tech Innovation Theme

> A bold, modern, high‑contrast theme that screams **innovation, speed, and cutting‑edge technology**. Perfect for when you want to look like the future.

## 🎨 Color Palette

| Color Name    | Hex Code  | Vibe                                | Suggested Usage                                  |
| ------------- | --------- | ----------------------------------- | ------------------------------------------------ |
| Electric Blue | `#0066ff` | Vibrant, energetic, trustworthy     | Primary accent – buttons, links, key data points |
| Neon Cyan     | `#00ffff` | Futuristic, glowing, alert          | Highlights, hover effects, call‑out boxes        |
| Dark Gray     | `#1e1e1e` | Deep, professional, non‑distracting | Main background – creates depth                  |
| White         | `#ffffff` | Clean, crisp, readable              | Body text, icons, contrast elements              |

> 💡 Pro tip: Use `Dark Gray` as your main background, `White` for body text, `Electric Blue` for CTAs, and `Neon Cyan` sparingly for maximum impact (like a laser beam).

## 🔤 Typography

| Type          | Font             | Character                                          |
| ------------- | ---------------- | -------------------------------------------------- |
| **Headers**   | DejaVu Sans Bold | Bold, clean, highly legible on dark backgrounds    |
| **Body Text** | DejaVu Sans      | Lightweight, modern, perfect for technical content |

> DejaVu Sans is an open‑source sans‑serif with excellent readability. Using a single font family keeps the focus on your content – not on fancy typography.

## ✅ Best Used For

Tech Innovation screams “future” and works best in these scenarios:

- 🚀 **Tech startups & pitch decks** – signals confidence and disruption
- 📱 **Software launches, product demos** – high energy, captures attention
- 🤖 **AI/ML presentations** – cyan/blue feels algorithmic and precise
- 💡 **Innovation showcases, R&D** – makes your ideas look groundbreaking
- 🔄 **Digital transformation content** – modern, agile, forward‑looking

## 📂 How to Use in Theme Factory Skill

1. Place this file in the `themes/` directory as `tech-innovation.md`.
2. When the user selects "Tech Innovation" from the theme showcase:
   - Main background: `#1e1e1e` (Dark Gray)
   - Body text: `#ffffff` (White)
   - Primary accent (buttons, links): `#0066ff` (Electric Blue)
   - Secondary accent / highlights: `#00ffff` (Neon Cyan) – use sparingly
   - Font: DejaVu Sans for everything, Bold for headers
3. Critical contrast check: White on Dark Gray = excellent (AAA). Electric Blue on Dark Gray = good for buttons. Never use Neon Cyan as background for body text – it's only for small accents.

## 🖼️ Quick CSS Example

```css
body {
  background-color: #1e1e1e; /* Dark Gray */
  color: #ffffff; /* White */
  font-family: "DejaVu Sans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "DejaVu Sans Bold", sans-serif;
  color: #ffffff;
}
.button {
  background-color: #0066ff; /* Electric Blue */
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  transition: 0.2s;
}
.button:hover {
  background-color: #0052cc; /* slightly darker blue */
  box-shadow: 0 0 8px #0066ff;
}
.highlight {
  color: #00ffff; /* Neon Cyan */
  font-weight: bold;
  text-shadow: 0 0 2px #00ffff;
}
.code-block {
  background-color: #2d2d2d;
  border-left: 4px solid #0066ff;
  padding: 1rem;
}
```
