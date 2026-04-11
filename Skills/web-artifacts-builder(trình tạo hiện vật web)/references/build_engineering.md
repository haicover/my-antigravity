# ⚙️ Mastery Chapter 3: Build Engineering & Automation

> "Phép thuật thực sự nằm ở cách chúng ta biến hàng nghìn file code thành một file HTML duy nhất."

## 🚀 1. The `init-artifact.sh` Workflow

Script khởi tạo project làm nhiệm vụ:
- **Project Scaffolding:** Tạo cấu trúc Vite + React + TS.
- **Dependency Injection:** Cài đặt Tailwind CSS, Framer Motion, Lucide React, Radix UI.
- **Component Deployment:** Giải nén `shadcn-components.tar.gz` vào thư mục `@/components/ui`.

## 📦 2. The `bundle-artifact.sh` Process

Đây là nơi "nén" toàn bộ ứng dụng:
- **Bundler Selection:** Sử dụng **Parcel** hoặc **Vite-plugin-singlefile**.
- **Asset Inlining:**
  - Chuyển đổi toàn bộ CSS thành thẻ `<style>` trong HTML.
  - Chuyển đổi toàn bộ JS thành thẻ `<script>` trong HTML.
  - Mã hóa hình ảnh nhỏ thành chuỗi **Base64**.
- **Minification:** Xóa bỏ khoảng trắng và giảm dung lượng mã để Artifact load nhanh hơn.

---

## 🏗️ 3. Managing Artifact Size

Kích thước lý tưởng cho một Artifact là dưới **2MB**.
- **Tree-shaking:** Chỉ bundle những component thực sự được sử dụng.
- **External CDN for Heavy Assets:** Nếu có video hoặc ảnh cực lớn, hãy host chúng bên ngoài và link tới URL thay vì inline.
- **SVG vs PNG:** Ưu tiên sử dụng Lucide React (SVG) thay vì file ảnh raster.

---

## 🛠️ 4. Local Development vs. Production

1.  **Dev Mode:** Sử dụng `npm run dev` để có HMR (Hot Module Replacement) - code đến đâu thấy kết quả đến đó.
2.  **Prod Mode:** Chạy `bash scripts/bundle-artifact.sh`. Kiểm tra file `bundle.html` cuối cùng trong browser để đảm bảo mọi thứ hiển thị đúng.

---
🔗 **Resources:**
- [Mastery Chapter 4: Quality & Delivery](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/quality_assurance_delivery.md)
