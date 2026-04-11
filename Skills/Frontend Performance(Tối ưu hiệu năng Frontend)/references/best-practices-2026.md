# Danh sách Best Practices Tối ưu Frontend (2026)

Làm chủ hiệu năng frontend với các kỹ thuật tiên tiến nhất.

## 🚀 1. Tối ưu hóa Hình ảnh & Media
- [ ] **AVIF by Default**: Chuyển đổi toàn bộ ảnh sang định dạng AVIF (hoặc WebP cho legacy browser).
- [ ] **Responsive Images**: Sử dụng `srcset` và `sizes` để trình duyệt chọn ảnh phù hợp nhất với màn hình.
- [ ] **Lazy Loading**: Áp dụng `loading="lazy"` cho tất cả các ảnh dưới nếp gấp (below the fold).
- [ ] **Priority Hints**: Sử dụng `fetchpriority="high"` cho ảnh LCP để nó được tải sớm nhất.

## 🏗️ 2. Tối ưu hóa Rendering (Next.js/React Focus)
- [ ] **Server Components (RSC)**: Di chuyển càng nhiều logic lên server càng tốt để giảm bundle size client.
- [ ] **Partial Hydration**: Chỉ hydrate những component cần tính tương tác (Selective Hydration).
- [ ] **Streaming & Suspense**: Hiển thị khung trang (Skeleton) và stream nội dung ngay khi sẵn sàng.
- [ ] **Optimistic UI**: Cập nhật giao diện ngay lập tức khi người dùng tương tác, trước khi server phản hồi.

## 📦 3. Bundle & JavaScript
- [ ] **Dynamic Imports**: Sử dụng `next/dynamic` hoặc `React.lazy` để split code theo route và component.
- [ ] **Package Audit**: Thường xuyên kiểm tra bundle size bằng `Bundle Analyzer`. Loại bỏ các thư viện quá nặng (ví dụ: dùng `date-fns` thay cho `moment`).
- [ ] **Web Workers**: Di chuyển logic xử lý dữ liệu phức tạp sang worker thread.
- [ ] **Module Preloading**: Sử dụng `<link rel="modulepreload">` cho các module quan trọng.

## 🎨 4. CSS & Font
- [ ] **Critical CSS**: Inline các style cần thiết cho màn hình đầu tiên để tránh render-blocking.
- [ ] **Zero-Runtime CSS**: Ưu tiên Tailwind CSS hoặc CSS Modules để không tốn chi phí xử lý style lúc runtime.
- [ ] **Font Optimization**: Sử dụng `next/font` (cho Next.js) hoặc `font-display: swap` để tránh Flash of Invisible Text (FOIT).
- [ ] **Preconnect**: Thêm `<link rel="preconnect">` cho các domain chứa font (như Google Fonts).

## 📈 5. Core Web Vitals (2026 Standards)
- [ ] **LCP (Largest Contentful Paint)**: Mục tiêu < 2.0s.
- [ ] **CLS (Cumulative Layout Shift)**: Mục tiêu < 0.1 (Tránh giật trang).
- [ ] **INP (Interaction to Next Paint)**: Mục tiêu < 200ms (Cực kỳ quan trọng cho SEO 2026).
- [ ] **Security (CSP)**: Thiết lập Content Security Policy chặt chẽ để tránh script lạ làm chậm trang.

---
*Tối ưu frontend là một hành trình liên tục. Hãy sử dụng Lighthouse và PageSpeed Insights để đo lường thường xuyên.*
