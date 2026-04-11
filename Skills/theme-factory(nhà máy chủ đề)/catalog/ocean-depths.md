# 🌊 Ocean Depths Theme

> A professional and calming maritime theme inspired by the serene depths of the ocean – **trustworthy, composed, and quietly powerful**.

## 🎨 Color Palette

| Color Name | Hex Code  | Inspired by          | Suggested Usage                                             |
| ---------- | --------- | -------------------- | ----------------------------------------------------------- |
| Deep Navy  | `#1a2332` | Midnight ocean floor | Primary background, footer, dark contrast areas             |
| Teal       | `#2d8b8b` | Tropical lagoon      | Accent color for buttons, links, highlights, charts         |
| Seafoam    | `#a8dadc` | Gentle wave foam     | Secondary accent for cards, borders, lighter highlights     |
| Cream      | `#f1faee` | Sandy shore foam     | Text on dark backgrounds, clean backgrounds, negative space |

> 💡 Pro tip: Use `Cream` for body text on `Deep Navy` background. Use `Teal` for CTAs and `Seafoam` for subtle separators.

## 🔤 Typography

| Type          | Font             | Character                                |
| ------------- | ---------------- | ---------------------------------------- |
| **Headers**   | DejaVu Sans Bold | Bold, clear, modern – commands attention |
| **Body Text** | DejaVu Sans      | Lightweight, crisp, highly readable      |

> DejaVu Sans is an open-source sans-serif font with excellent multi-language support. Using a single font family ensures consistency and a clean, professional look.

## ✅ Best Used For

Ocean Depths builds trust and conveys stability, making it ideal for:

- 🏢 **Corporate presentations** – projects reliability and authority
- 📈 **Financial reports, annual reviews** – calm colors reduce anxiety around numbers
- 🧑‍💼 **Professional consulting decks** – builds client confidence
- 🔒 **Trust-building content** (security, privacy, legal) – navy blue evokes security
- 🌍 **Sustainability & ESG reports** – maritime theme ties naturally to ocean/environmental topics

## 📂 How to Use in Theme Factory Skill

1. Place this file in the `themes/` directory as `ocean-depths.md`.
2. When the user selects "Ocean Depths" from the theme showcase:
   - Main background: `#1a2332` (Deep Navy)
   - Body text color: `#f1faee` (Cream)
   - Primary accent (buttons, links): `#2d8b8b` (Teal)
   - Secondary accent (borders, highlights): `#a8dadc` (Seafoam)
   - Font: DejaVu Sans for everything, Bold for headers
3. Check contrast: Cream on Deep Navy meets WCAG AAA standards; Teal on Deep Navy also works well.

## 🖼️ Quick CSS Example

```css
body {
  background-color: #1a2332; /* Deep Navy */
  color: #f1faee; /* Cream */
  font-family: "DejaVu Sans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "DejaVu Sans Bold", sans-serif;
  color: #f1faee;
  border-bottom: 2px solid #2d8b8b; /* Teal */
}
.button {
  background-color: #2d8b8b; /* Teal */
  color: #f1faee;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
}
.card {
  background-color: #2a3a4a; /* slightly lighter than Deep Navy */
  border-left: 4px solid #a8dadc; /* Seafoam */
  padding: 1rem;
}
```
