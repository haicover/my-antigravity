# 🌸 Desert Rose Theme

> Một theme nhẹ nhàng, tinh tế với tông màu phấn trầm ấm áp – lấy cảm hứng từ hoa hồng sa mạc và cát vàng hoàng hôn. **Sang trọng, lãng mạn, đầy chất thơ.**

## 🎨 Bảng màu

| Tên màu       | Mã HEX    | Ấn tượng                       | Ứng dụng gợi ý                                            |
| ------------- | --------- | ------------------------------ | --------------------------------------------------------- |
| Dusty Rose    | `#d4a5a5` | Hồng phấn nhẹ, nữ tính, êm dịu | Màu nền chính, khung ảnh, tiêu đề phụ                     |
| Clay          | `#b87d6d` | Nâu đỏ đất, ấm áp, tự nhiên    | Màu nhấn cho nút bấm, đường viền, biểu tượng              |
| Sand          | `#e8d5c4` | Kem cát, trung tính, dễ chịu   | Nền toàn trang, vùng đọc chính                            |
| Deep Burgundy | `#5d2e46` | Đỏ đô đậm, bí ẩn, quý phái     | Chữ tiêu đề lớn, chân trang, tạo điểm nhấn tương phản cao |

> 💡 Mẹo phối hợp: Dùng `Sand` làm nền chính, `Dusty Rose` cho các khối nội dung, `Clay` cho nút kêu gọi hành động, `Deep Burgundy` cho văn bản quan trọng hoặc tiêu đề cấp cao nhất.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ     | Ghi chú                |
| --------------------- | ------------- | ---------------------- |
| **Tiêu đề (Headers)** | FreeSans Bold | Đậm, rõ ràng, hiện đại |
| **Nội dung (Body)**   | FreeSans      | Nhẹ hơn, dễ đọc lướt   |

> FreeSans là họ font sans-serif mã nguồn mở, tương thích tốt trên mọi hệ điều hành. Việc dùng chung một họ giúp giao diện nhất quán, chỉ khác độ đậm để phân cấp.

## ✅ Khi nào nên dùng theme này

Desert Rose đặc biệt hiệu quả trong các bối cảnh cần sự tinh tế, lãng mạn và sang trọng:

- 👗 **Thời trang & Làm đẹp** – tone hồng đất tôn lên sự nữ tính, đẳng cấp.
- 💍 **Tổ chức đám cưới, sự kiện** – màu sắc ấm áp, lãng mạn, dễ phối với hoa tươi.
- 🛋️ **Thiết kế nội thất** – gợi cảm giác ấm cúng, gần gũi nhưng vẫn hiện đại.
- 🛍️ **Cửa hàng thời trang nhỏ (boutique)** – tạo thương hiệu riêng biệt, dễ thương nhưng không hề trẻ con.
- 🎨 **Portfolio nghệ thuật** – tone màu trầm giúp tác phẩm nổi bật hơn.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `desert-rose.md`.
2. Khi người dùng chọn "Desert Rose" từ theme showcase:
   - Màu nền chính: `#e8d5c4` (Sand)
   - Màu tiêu đề chính: `#5d2e46` (Deep Burgundy)
   - Màu nền phụ, highlight: `#d4a5a5` (Dusty Rose)
   - Màu nút, đường kẻ: `#b87d6d` (Clay)
   - Font: FreeSans cho mọi thứ, riêng header dùng phiên bản Bold
3. Kiểm tra độ tương phản: ví dụ chữ `#5d2e46` trên nền `#e8d5c4` đạt chuẩn; chữ trắng trên nền `#5d2e46` cũng tốt.

## 🖼️ Ví dụ nhanh (CSS)

```css
body {
  background-color: #e8d5c4; /* Sand */
  color: #3e2a2f; /* màu tối tự chọn cho chữ */
  font-family: "FreeSans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "FreeSans", sans-serif;
  font-weight: bold;
  color: #5d2e46; /* Deep Burgundy */
}
.card {
  background-color: #d4a5a5; /* Dusty Rose */
  padding: 1rem;
  border-radius: 12px;
}
.button {
  background-color: #b87d6d; /* Clay */
  color: white;
  border: none;
}
```
