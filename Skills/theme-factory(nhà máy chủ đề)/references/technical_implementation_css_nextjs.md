# 💻 Mastery Chapter 4: Technical Implementation (CSS & Next.js)

> Chuyển đổi các ý tưởng thiết kế thành mã nguồn thực tế sử dụng các công nghệ hiện đại nhất 2026.

## 🛠️ 1. CSS Variables: The Foundation

Cách tiếp cận linh hoạt nhất để triển khai **Theme Factory** là sử dụng CSS Variables.

```css
:root {
  /* Ocean Depths Theme Default */
  --primary: #0077be;
  --secondary: #00a8cc;
  --background: #f0f8ff;
  --text: #003366;
}

[data-theme='arctic-frost'] {
  --primary: #4a6fa5;
  --secondary: #d4e4f7;
  --background: #fafafa;
  --text: #1e2a3a;
}
```

---

## 🌊 2. Tailwind CSS Integration

Để sử dụng các theme này một cách hiệu quả trong Tailwind, hãy cấu hình `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--primary)',
        secondary: 'var(--secondary)',
        background: 'var(--background)',
        text: 'var(--text)',
      },
    },
  },
}
```

---

## ⚛️ 3. Dynamic Theming in Next.js

Sử dụng thư viện `next-themes` để quản lý việc chuyển đổi giữa 10 theme một cách mượt mà.

### 3.1 Setup Provider
```tsx
import { ThemeProvider } from 'next-themes'

export default function RootLayout({ children }) {
  return (
    <ThemeProvider attribute="data-theme" defaultTheme="ocean-depths">
      {children}
    </ThemeProvider>
  )
}
```

### 3.2 Theme Switcher Component
```tsx
import { useTheme } from 'next-themes'

const ThemeSwitcher = () => {
  const { theme, setTheme } = useTheme()

  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
      <option value="ocean-depths">Ocean Depths</option>
      <option value="arctic-frost">Arctic Frost</option>
      {/* ... other themes from catalog */}
    </select>
  )
}
```

---

## ✨ 4. Animated Transitions (Framer Motion)

Một theme "Elite" cần những hiệu ứng chuyển cảnh mượt mà.

```tsx
import { motion, AnimatePresence } from 'framer-motion'

const PageWrapper = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0 }}
    transition={{ duration: 0.5, ease: "easeOut" }}
  >
    {children}
  </motion.div>
)
```

---
🔗 **Resources:**
- [Next-Themes Documentation](https://github.com/pacocoursey/next-themes)
- [Tailwind CSS Customization](https://tailwindcss.com/docs/customizing-colors)
- [Framer Motion Guide](https://www.framer.com/motion/)
