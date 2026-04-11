# 🌲 Forest Canopy Theme

> Một theme tự nhiên, vững chãi với tông màu đất lấy cảm hứng từ những cánh rừng già – **mát mắt, bền vững và đầy sức sống**.

## 🎨 Bảng màu

| Tên màu      | Mã HEX    | Cảm hứng từ          | Ứng dụng gợi ý                                       |
| ------------ | --------- | -------------------- | ---------------------------------------------------- |
| Forest Green | `#2d4a2b` | Tán rừng sâu thẳm    | Màu chính cho tiêu đề lớn, khung nổi bật, chân trang |
| Sage         | `#7d8471` | Lá xô thơm phủ sương | Màu nhấn cho nút bấm, đường viền, biểu đồ            |
| Olive        | `#a4ac86` | Quả ô liu chín       | Nền phụ, highlight văn bản, vùng đệm                 |
| Ivory        | `#faf9f6` | Ngà voi mềm mại      | Nền chính sạch sẽ, vùng đọc, nền slide               |

> 💡 Mẹo phối hợp: Dùng `Ivory` làm nền toàn bộ, `Forest Green` cho các tiêu đề quan trọng, `Sage` cho các thành phần tương tác, `Olive` làm màu phân cách hoặc biểu đồ nhẹ nhàng.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ      | Đặc điểm                                                       |
| --------------------- | -------------- | -------------------------------------------------------------- |
| **Tiêu đề (Headers)** | FreeSerif Bold | Chữ có chân – cổ điển, ổn định, gợi cảm giác thư thái của rừng |
| **Nội dung (Body)**   | FreeSans       | Chữ không chân – hiện đại, tối giản, dễ đọc trên mọi thiết bị  |

> Sự kết hợp giữa Serif cho tiêu đề và Sans cho nội dung tạo chiều sâu, vừa ấm cúng vừa chuyên nghiệp – rất hợp với các thương hiệu thiên nhiên và bền vững.

## ✅ Khi nào nên dùng theme này

Forest Canopy tỏa sáng trong các bối cảnh:

- 🌍 **Thuyết trình về môi trường, khí hậu** – màu xanh đất truyền tải sự cam kết và trách nhiệm.
- 📊 **Báo cáo phát triển bền vững (ESG)** – tạo cảm giác minh bạch, thân thiện với trái đất.
- 🏕️ **Thương hiệu ngoài trời, du lịch sinh thái** – gợi nhắc rừng, núi, thiên nhiên hoang dã.
- 🧘 **Nội dung chăm sóc sức khỏe, thiền, yoga** – màu sắc dịu mắt, giảm căng thẳng.
- 🥑 **Sản phẩm hữu cơ, thực phẩm sạch** – tạo niềm tin về nguồn gốc tự nhiên.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `forest-canopy.md`.
2. Khi người dùng chọn "Forest Canopy" từ theme showcase:
   - Màu nền chính: `#faf9f6` (Ivory)
   - Màu tiêu đề chính: `#2d4a2b` (Forest Green)
   - Màu nền phụ hoặc card: `#a4ac86` (Olive)
   - Màu nút, đường kẻ, icon: `#7d8471` (Sage)
   - Font: FreeSerif Bold cho heading, FreeSans cho body
3. Kiểm tra độ tương phản: chữ `#2d4a2b` trên nền `#faf9f6` rất rõ; chữ trắng trên nền `#2d4a2b` cũng tốt.

## 🖼️ Ví dụ nhanh (CSS)

```css
body {
  background-color: #faf9f6; /* Ivory */
  color: #2c3e2b; /* màu xanh đen tự chọn cho chữ chính */
  font-family: "FreeSans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "FreeSerif Bold", serif;
  color: #2d4a2b; /* Forest Green */
}
.card {
  background-color: #a4ac86; /* Olive */
  padding: 1rem;
  border-radius: 16px;
  color: #1e2a1d;
}
.button {
  background-color: #7d8471; /* Sage */
  color: #faf9f6;
  border: none;
  border-radius: 8px;
}
.highlight {
  background-color: #e0e5d6; /* pha loãng của Olive */
}
```
