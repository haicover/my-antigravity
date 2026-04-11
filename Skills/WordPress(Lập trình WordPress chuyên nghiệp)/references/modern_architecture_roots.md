# 🏗️ Mastery Chapter 1: Modern WP Architecture & Roots Ecosystem

> "WordPress chuyên nghiệp không bắt đầu bằng Zip file, mà bắt đầu bằng `composer create-project`."

## 🌳 1. The Roots Ecosystem

Roots là tiêu chuẩn vàng cho phát triển WordPress chuyên nghiệp năm 2026.

### 1.1 Bedrock: Modern WordPress Stack
Bedrock thay đổi cấu trúc thư mục của WP để an toàn và chuyên nghiệp hơn:
- **Dependency Management:** Dùng Composer để quản lý plugins, themes, và core WP.
- **Environment Variables:** Quản lý cấu hình nhạy cảm qua file `.env`.
- **Better Folder Structure:** Tách biệt mã nguồn (`web/wp/`) và nội dung tải lên (`web/app/`).

### 1.2 Sage: Advanced Starter Theme
Sage mang những công nghệ frontend tốt nhất vào WP themes:
- **Blade Templating:** Dùng cú pháp Laravel Blade thay vì PHP thuần.
- **Tailwind CSS:** Tích hợp sẵn framework CSS hàng đầu.
- **Vite/Bud:** Build process siêu nhanh.

---

## 🛠️ 2. Professional Development Workflow

### 2.1 Composer for WP
Đừng bao giờ cài plugin qua dashboard nữa.
- **Usage:** `composer require wpackagist-plugin/contact-form-7`
- **Benefit:** Dễ dàng quản lý version và đồng bộ giữa các môi trường (Dev/Staging/Prod).

### 2.2 WP-CLI: The Power of Terminal
Mọi thứ bạn làm trên dashboard, WP-CLI làm nhanh hơn:
- `wp plugin install --activate`
- `wp search-replace 'domain.local' 'domain.com'`
- `wp user create`

---

## 🐳 3. Local Development with Docker

Sử dụng môi trường ảo hóa giúp dự án chạy ổn định trên mọi máy:
- **Trellis:** Giải pháp full-stack (Local -> Production) của Roots.
- **Lando / DDEV:** Các công cụ Docker nhẹ cho WP development.

---
🔗 **Resources:**
- [Mastery Chapter 2: Block Development](file:///e:/Google%20Antigravity/Skills/WordPress%28L%E1%BA%ADp%20tr%C3%ACnh%20WordPress%20chuy%C3%AAn%20nghi%E1%BB%87p%29/references/block_development_gutenberg.md)
