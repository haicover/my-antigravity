# 🎨 Mastery Chapter 2: UI/UX Fidelity & Aesthetic Engineering

> "Hiện vật web không chỉ để chạy, nó phải là một tác phẩm nghệ thuật kỹ thuật số."

## 🧩 1. Shadcn/ui Integration

Phần lõi của `web-artifacts-builder` là thư viện Shadcn/ui.
- **Copy-Paste Architecture:** Chúng ta không cài qua npm thông thường mà copy code component vào dự án. Điều này giúp chúng ta có thể tùy chỉnh (Custom) từng dòng code để phù hợp với môi trường Artifact.
- **Components sẵn có:** Button, Card, Dialog, Tabs, Input, v.v. đã được bundle sẵn trong `shadcn-components.tar.gz`.

## 🌈 2. Tailwind CSS Beyond the Basics

Để Artifact trông cao cấp (Premium), hãy tránh các giá trị mặc định:
- **Custom Color Palette:** Định nghĩa các biến CSS trong `index.css` (e.g., `--primary: 222.2 47.4% 11.2%`).
- **Dark Mode Support:** Luôn xây dựng giao diện hỗ trợ `dark` selector.
- **Glassmorphism:** Sử dụng `backdrop-blur-md` kết hợp với opacity thấp để tạo cảm giác hiện đại.

---

## ✨ 3. Micro-animations với Framer Motion

Chuyển động làm cho Artifact cảm thấy "sống":
- **Enter/Exit Animations:** Dùng cho Modal hoặc Toast.
- **Layout Transitions:** Dùng cho thay đổi danh sách hoặc chuyển View.
- **Hover effects:** Tăng cường tính tương tác (feedback) cho người dùng.

---

## 📐 4. Layout Engineering

Tránh lỗi "AI Slop" trong thiết kế:
- **Grids vs Flex:** Dùng `grid-cols-12` để kiểm soát bố cục đa cột chuyên nghiệp.
- **Whitespace:** Đừng sợ khoảng trắng. Hãy dùng `p-8`, `gap-10` để tạo sự thoáng đãng.
- **Typography:** Ưu tiên dùng `font-sans` với hệ thống font chữ hiện đại (Inter, Geist).

---
🔗 **Resources:**
- [Mastery Chapter 3: Build Engineering](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/build_engineering.md)
