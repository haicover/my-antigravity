# 🧱 Mastery Chapter 2: Block Development & Gutenberg (React)

> "WordPress của năm 2026 là một ứng dụng React khổng lồ."

## 🧩 1. Custom Block Development

Bỏ qua các Page Builder nặng nề, hãy xây dựng các blocks tùy chỉnh siêu nhẹ bằng React.

### 1.1 Block Anatomy
Mỗi block gồm 3 phần chính:
- **`block.json`**: Định nghĩa Metadata (tên, icon, attributes).
- **`edit.js`**: Giao diện hiển thị trong Backend (React).
- **`save.js`**: Logic render HTML ra Frontend (hoặc động).

### 1.2 Attributes & Data Flow
Quản lý dữ liệu trong block thông qua Attributes. Hãy sử dụng `InnerBlocks` để cho phép lồng ghép các thành phần khác nhau bên trong block của bạn.

---

## 🎨 2. Full Site Editing (FSE) & `theme.json`

FSE cho phép xây dựng toàn bộ website mà không cần viết quá nhiều code PHP logic.
- **`theme.json`**: Trái tim của Block Theme. Nơi bạn định nghĩa Global Styles, Colors, Typography và Layout constraints.
- **Template Parts**: Xây dựng Header, Footer dưới dạng blocks để người dùng có thể kéo thả chỉnh sửa.

---

## ✨ 3. Interactivity API

Đây là cuộc cách mạng của WP dành cho các tương tác Frontend mượt mà:
- **What it is:** Bộ công cụ giúp thêm các hiệu ứng live (like, giỏ hàng, search) mà không cần reload trang và cực kỳ nhẹ (không cần jQuery).
- **Concept:** Sử dụng `directives` (tương tự Vue/Alpine) ngay trong HTML của block.

---

## 🛠️ 4. Tools for Block Developers

1.  **`@wordpress/scripts`**: Bộ công cụ build chuẩn từ WP Core.
2.  **Gutenberg Plugin**: Luôn cài bản mới nhất để thử nghiệm các tính năng sắp ra mắt.
3.  **Block Lab / ACF Blocks**: Giải pháp nhanh cho các dự án yêu cầu thời gian triển khai ngắn.

---
🔗 **Resources:**
- [Mastery Chapter 3: Headless WP](file:///e:/Google%20Antigravity/Skills/WordPress%28L%E1%BA%ADp%20tr%C3%ACnh%20WordPress%20chuy%C3%AAn%20nghi%E1%BB%87p%29/references/headless_wp_graphql.md)
