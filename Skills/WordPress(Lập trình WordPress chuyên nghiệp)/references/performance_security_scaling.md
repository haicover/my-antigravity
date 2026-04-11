# 🛡️ Mastery Chapter 4: Performance, Security & Enterprise Scaling

> "WordPress chỉ chậm khi bạn không biết cách tối ưu."

## ⚡ 1. The Performance Pyramid

Để WP chạy như "bay", bạn cần tối ưu từ hạ tầng đến code.

### 1.1 Object Caching with Redis
Giảm tải cho Database bằng cách lưu trữ các kết quả truy vấn SQL vào bộ nhớ RAM.
- **Why:** Phản hồi nhanh gấp 10-20 lần cho các website nhiều dữ liệu.

### 1.2 SQL Optimization
- Tránh sử dụng `-meta_query` hoặc `tax_query` quá phức tạp nếu không có index.
- Sử dụng **Query Monitor** plugin để tìm ra các query chậm (slow queries).

### 1.3 Core Web Vitals
- Tối ưu hóa hình ảnh (WebP, AVIF).
- Trì hoãn JS không cần thiết (Defer/Async).
- Sử dụng CDN (Cloudflare/BunnyCDN).

---

## 🔐 2. Security Hardening (Elite Level)

### 2.1 File & Directory Security
- Chặn truy cập trực tiếp vào các file nhạy cảm (`.htaccess` hoặc Nginx config).
- Disallow file edit trong `wp-config.php`.

### 2.2 Data Sanitization & Escaping
Rule số 1: **"Trust no one"**.
- Dùng `sanitize_text_field()`, `absint()` trước khi lưu vào DB.
- Dùng `esc_html()`, `esc_attr()`, `esc_url()` khi render ra Frontend.

---

## 🏗️ 3. Enterprise Scaling

Khi website có triệu view, WP cần một kiến trúc khác:
- **WP Multisite:** Quản lý hàng trăm subdomain/domain trên một database duy nhất.
- **Load Balancing:** Chạy WP trên nhiều servers đồng thời.
- **Microservices for WP:** Tách biệt các tác vụ nặng (xử lý ảnh, email) sang các service riêng biệt qua API.

---

## 🧪 4. Quality Guardrails

Trước khi deploy, luôn đảm bảo:
- **PHPStan:** Phân tích code tĩnh để tìm lỗi logic.
- **PHP_CodeSniffer:** Đảm bảo code tuân thủ WordPress Coding Standards.
- **Unit Testing (PHPUnit):** Kiểm tra các hàm logic quan trọng của plugin/theme.

---
🔗 **Resources:**
- [Elite 2026 Roadmap](file:///e:/Google%20Antigravity/Skills/WordPress%28L%E1%BA%ADp%20tr%C3%ACnh%20WordPress%20chuy%C3%AAn%20nghi%E1%BB%87p%29/references/roadmap-2026.md)
