# 🌿 Botanical Garden Theme

> Một theme tươi mát, hữu cơ lấy cảm hứng từ khu vườn – mang lại sự **sống động**, **gần gũi với thiên nhiên** và **ấm áp** cho các bài thuyết trình, tài liệu hoặc trang web.

## 🎨 Bảng màu

| Tên màu    | Mã HEX    | Ứng dụng gợi ý                                                       |
| ---------- | --------- | -------------------------------------------------------------------- |
| Fern Green | `#4a7c59` | Màu chính, tiêu đề, khung nổi bật (tượng trưng cho cây cỏ)           |
| Marigold   | `#f9a620` | Màu nhấn mạnh (nút CTA, icon, trích dẫn) – tươi sáng như hoa cúc     |
| Terracotta | `#b7472a` | Màu nền ấm cho phần chân trang, sidebar hoặc điểm nhấn đất           |
| Cream      | `#f5f3ed` | Nền chính mềm mại, trung tính – giảm độ chói, tăng cảm giác tự nhiên |

> 💡 Mẹo phối hợp: Dùng `Cream` làm nền toàn bộ, `Fern Green` cho tiêu đề lớn, `Marigold` cho các yếu tố tương tác, `Terracotta` cho đường viền hoặc phân cách.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ         | Đặc điểm                                             |
| --------------------- | ----------------- | ---------------------------------------------------- |
| **Tiêu đề (Headers)** | DejaVu Serif Bold | Chữ có chân – cổ điển, thân thiện, gợi nhớ vườn tược |
| **Nội dung (Body)**   | DejaVu Sans       | Chữ không chân – hiện đại, dễ đọc trên màn hình      |

> Kết hợp Serif cho tiêu đề và Sans cho nội dung tạo sự cân bằng giữa truyền thống và hiện đại, rất hợp với các thương hiệu về thực phẩm hoặc thiên nhiên.

## ✅ Khi nào nên dùng theme này

Botanical Garden tỏa sáng trong các bối cảnh:

- 🌱 **Trung tâm vườn, cây cảnh** – gợi cảm giác xanh, sạch, thư giãn.
- 🍅 **Thực phẩm, nông sản sạch** – phù hợp với phong cách farm-to-table, hữu cơ.
- 🧴 **Thương hiệu mỹ phẩm tự nhiên** – truyền tải sự an lành, thuần khiết.
- 📰 **Blog về làm vườn, nấu ăn** – tạo cảm giác ấm cúng, mộc mạc.
- 🌾 **Sự kiện ngoài trời, sinh thái** – đồng bộ với thiên nhiên.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `botanical-garden.md`.
2. Khi người dùng chọn "Botanical Garden" từ theme showcase:
   - Áp dụng màu nền chính: `#f5f3ed` (Cream)
   - Màu tiêu đề & đường kẻ: `#4a7c59` (Fern Green)
   - Màu nhấn nút, liên kết: `#f9a620` (Marigold)
   - Màu viền, phân cách: `#b7472a` (Terracotta)
   - Font: DejaVu Serif Bold cho heading, DejaVu Sans cho body
3. Kiểm tra độ tương phản (ví dụ: chữ `#1e3b2b` trên nền Cream đảm bảo đọc được).

## 🖼️ Ví dụ nhanh (mô phỏng CSS)

```css
body {
  background-color: #f5f3ed; /* Cream */
  color: #2d3e2b; /* màu xanh đậm tự chọn cho chữ */
  font-family: "DejaVu Sans", sans-serif;
}
h1,
h2,
h3,
h4 {
  font-family: "DejaVu Serif Bold", serif;
  color: #4a7c59; /* Fern Green */
}
.button {
  background-color: #f9a620; /* Marigold */
  color: #2d3e2b;
  border: none;
}
.footer {
  border-top: 3px solid #b7472a; /* Terracotta */
}
```
