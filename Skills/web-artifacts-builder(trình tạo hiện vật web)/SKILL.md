# 🧩 Web Artifacts Builder (Trình tạo Hiện vật Web)

> **Elite 2026 Standard**: "Crafting High-Fidelity Atomic Interactive Experiences."
> Chuyên dụng cho việc xây dựng các ứng dụng React phức tạp, đa thành phần, được đóng gói thành một file HTML duy nhất để chạy trong Claude Artifacts hoặc nhúng vào bất kỳ hệ thống nào.

## 🕹️ Command Center

- 🗺️ **Lộ trình phát triển**: [Elite 5-Phase Roadmap](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/roadmap-2026.md)
- 🧠 **Tư duy cốt lõi**: [Atomic Design, Single-File Architecture, State-Driven UI]
- 🛠️ **Công cụ mũi nhọn**: Vite, Parcel, Shadcn/ui, Tailwind CSS, Framer Motion.

---

## 📚 Mastery Chapters (Hệ thống kiến thức)

Hệ thống 4 chương chuyên sâu đưa bạn trở thành bậc thầy chế tác "Hiện vật tương tác".

### 🏛️ Chapter 1: [Architectural Patterns for Artifacts](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/architectural_patterns.md)
Cách cấu trúc dự án React trong giới hạn một file HTML. Quản lý State với Zustand và kỹ thuật giả lập Routing.

### 🎨 Chapter 2: [UI/UX Fidelity & Aesthetic Engineering](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/ui_ux_fidelity.md)
Tích hợp Shadcn/ui cao cấp, làm chủ Tailwind CSS và tạo chuyển động mượt mà với Framer Motion.

### ⚙️ Chapter 3: [Build Engineering & Automation](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/build_engineering.md)
Làm chủ scripts `init` và `bundle`. Kỹ thuật inline assets (Base64) và tối ưu hóa kích thước file Artifact.

### 🧪 Chapter 4: [Quality Assurance & Artifact Delivery](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/quality_assurance_delivery.md)
Testing, bảo mật và các phương thức phân phối hiện vật đến Claude hoặc Self-hosting.

---

## ⚡ Quick Start (Hành động ngay)

### 1. Khởi tạo Project
```bash
# Thay 'my-artifact' bằng tên dự án của bạn
bash scripts/init-artifact.sh my-artifact
cd my-artifact
```

### 2. Phát triển (Live Preview)
```bash
npm run dev
```
Code tại `src/App.tsx`. Sử dụng `@/` để import components từ shadcn.

### 3. Đóng gói (Bàn giao)
```bash
bash ../scripts/bundle-artifact.sh
```
Kết quả sẽ là file `bundle.html` sẵn sàng để paste vào Claude.

---
> [!IMPORTANT]
> **Elite Rule:** Luôn giữ file bundle dưới **2MB** để đảm bảo khả năng render và tương tác mượt mà nhất trên mọi thiết bị.

---
*Cập nhật lần cuối: 2026 - Bởi Đội ngũ Antigravity (Elite Engineering Division)*
