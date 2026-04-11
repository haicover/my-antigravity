# 🚀 Mastery Chapter 3: Headless WP & Decoupled Architecture

> "Dùng WordPress cho dữ liệu, dùng Next.js cho trải nghiệm."

## 📡 1. WP GraphQL vs. REST API

Trong kiến trúc Headless, việc truy xuất dữ liệu là sống còn.
- **WP GraphQL (Recommended):** Cho phép bạn lấy chính xác những gì bạn cần trong một yêu cầu duy nhất. Hiệu quả hơn REST API rất nhiều khi xử lý dữ liệu Post, Meta, và Menu.
- **REST API:** Vẫn hữu ích cho các tác vụ đơn giản hoặc tích hợp cũ.

## ⚛️ 2. Connecting with Next.js

Đây là combo mạnh nhất năm 2026:
- **SSG (Static Site Generation):** Build website WP thành các file HTML tĩnh, cho tốc độ load cực nhanh và bảo mật tuyệt đối.
- **ISR (Incremental Static Regeneration):** Tự động cập nhật trang ngay khi bạn nhấn "Update" trong WordPress dashboard mà không cần rebuild lại toàn bộ site.

---

## 🔐 3. Authentication & Security

Làm thế nào để ứng dụng Frontend lưu trữ dữ liệu vào WP an toàn?
- **JWT (JSON Web Tokens):** Chuẩn phổ biến nhất để xác thực user giữa App và WP Backend.
- **App Passwords:** Giải pháp nhanh cho các server-to-server integrations.

---

## 🏗️ 4. Headless Hosting Strategy

- **Backend:** Host WordPress trên các server tối ưu PHP (e.g., Kinsta, WP Engine, hoặc DigitalOcean với RunCloud).
- **Frontend:** Deploy Next.js lên Vercel hoặc Netlify để tận dụng Edge Network toàn cầu.

---
🔗 **Resources:**
- [Mastery Chapter 4: Performance & Scaling](file:///e:/Google%20Antigravity/Skills/WordPress%28L%E1%BA%ADp%20tr%C3%ACnh%20WordPress%20chuy%C3%AAn%20nghi%E1%BB%87p%29/references/performance_security_scaling.md)
