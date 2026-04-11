# ⚪ Modern Minimalist Theme

> Một theme sạch sẽ, đương đại với bảng màu xám tinh tế – **tối giản nhưng không hề đơn điệu**, phù hợp với hầu hết mọi loại nội dung nhờ sự linh hoạt tối đa.

## 🎨 Bảng màu

| Tên màu    | Mã HEX    | Cảm hứng từ       | Ứng dụng gợi ý                                      |
| ---------- | --------- | ----------------- | --------------------------------------------------- |
| Charcoal   | `#36454f` | Than đá sâu lắng  | Màu chính cho tiêu đề lớn, chân trang, vùng đậm     |
| Slate Gray | `#708090` | Đá phiến tự nhiên | Màu nhấn cho nút bấm, đường viền, biểu đồ           |
| Light Gray | `#d3d3d3` | Mây nhẹ           | Nền phụ, đường kẻ phân cách, vùng đệm               |
| White      | `#ffffff` | Tinh khôi         | Nền chính, văn bản (trên nền tối), tạo khoảng trống |

> 💡 Mẹo phối hợp: Dùng `White` làm nền chính, `Charcoal` cho chữ và tiêu đề, `Slate Gray` cho các yếu tố cần chú ý, `Light Gray` để phân tách các khối nội dung.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ        | Đặc điểm                                       |
| --------------------- | ---------------- | ---------------------------------------------- |
| **Tiêu đề (Headers)** | DejaVu Sans Bold | Đậm, rõ ràng, hiện đại – tạo điểm nhấn mạnh mẽ |
| **Nội dung (Body)**   | DejaVu Sans      | Nhẹ nhàng, dễ đọc, giữ được sự tối giản        |

> DejaVu Sans là họ font sans-serif mã nguồn mở, hỗ trợ nhiều ngôn ngữ. Sự nhất quán giữa header và body giúp giao diện gọn gàng, chuyên nghiệp.

## ✅ Khi nào nên dùng theme này

Modern Minimalist phù hợp với hầu hết mọi bối cảnh, nhưng đặc biệt hiệu quả trong:

- 💻 **Thuyết trình công nghệ, phần mềm** – tạo cảm giác sạch sẽ, tập trung vào nội dung.
- 🏛️ **Portfolio kiến trúc, thiết kế** – để hình ảnh và bố cục tự nói lên tất cả.
- 📊 **Trực quan hoá dữ liệu** – màu xám trung tính không làm sai lệch cảm nhận, dữ liệu nổi bật.
- 📑 **Đề xuất kinh doanh hiện đại** – truyền tải sự chuyên nghiệp, đáng tin cậy.
- 🖼️ **Showcase nghệ thuật, nhiếp ảnh** – màu trắng đen làm nền hoàn hảo cho tác phẩm.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `modern-minimalist.md`.
2. Khi người dùng chọn "Modern Minimalist" từ theme showcase:
   - Màu nền chính: `#ffffff` (White)
   - Màu chữ chính: `#36454f` (Charcoal)
   - Màu nút, liên kết, icon: `#708090` (Slate Gray)
   - Màu đường kẻ, khung, vùng đệm: `#d3d3d3` (Light Gray)
   - Font: DejaVu Sans cho mọi thứ, header dùng Bold
3. Kiểm tra độ tương phản: chữ `#36454f` trên nền `#ffffff` đạt chuẩn WCAG AAA; chữ trắng trên nền `#36454f` cũng rất rõ.

## 🖼️ Ví dụ nhanh (CSS)

```css
body {
  background-color: #ffffff; /* White */
  color: #36454f; /* Charcoal */
  font-family: "DejaVu Sans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "DejaVu Sans Bold", sans-serif;
  color: #36454f;
}
.button {
  background-color: #708090; /* Slate Gray */
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
}
.divider {
  border-top: 1px solid #d3d3d3; /* Light Gray */
}
.card {
  background-color: #f5f5f5; /* nhạt hơn Light Gray một chút */
  border: 1px solid #d3d3d3;
  padding: 1rem;
}
```
